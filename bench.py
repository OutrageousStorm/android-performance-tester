#!/usr/bin/env python3
"""
bench.py -- Benchmark Android device performance
Measures: CPU speed, RAM available, storage I/O, battery drain rate
Usage: python3 bench.py [--duration 30]
"""
import subprocess, time, json, argparse
from datetime import datetime

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def get_cpu_freq():
    """Get current CPU frequency in MHz"""
    try:
        freq_khz = int(adb("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"))
        return freq_khz / 1000
    except:
        return 0

def get_ram():
    """Get RAM usage in MB"""
    out = adb("free -m | tail -1")
    try:
        parts = out.split()
        total, used = int(parts[1]), int(parts[2])
        return {"total": total, "used": used, "free": total - used, "percent": (used / total) * 100}
    except:
        return {"total": 0, "used": 0, "free": 0, "percent": 0}

def get_battery():
    """Get battery level and temperature"""
    temp = adb("dumpsys battery | grep temperature | awk '{print $NF}'").strip()
    level = adb("dumpsys battery | grep level | awk '{print $NF}'").strip()
    return {"level": int(level) if level.isdigit() else 0, "temp_c": int(temp) // 10 if temp.isdigit() else 0}

def get_storage():
    """Get storage I/O speed (simple read test)"""
    # Time a 10MB read from /dev/zero
    start = time.time()
    adb("dd if=/dev/zero bs=1M count=10 of=/sdcard/bench_test 2>/dev/null")
    elapsed = time.time() - start
    adb("rm /sdcard/bench_test 2>/dev/null")
    mb_per_sec = 10 / max(elapsed, 0.01)
    return {"mb_per_sec": mb_per_sec, "time_sec": elapsed}

def benchmark(duration=30):
    print(f"\n📊 Android Performance Benchmark ({duration}s)")
    print("=" * 50)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "duration_sec": duration,
        "samples": []
    }
    
    end_time = time.time() + duration
    sample_num = 0
    
    while time.time() < end_time:
        sample_num += 1
        cpu_freq = get_cpu_freq()
        ram = get_ram()
        batt = get_battery()
        
        sample = {
            "num": sample_num,
            "cpu_mhz": cpu_freq,
            "ram_mb": ram["used"],
            "battery_pct": batt["level"],
            "temp_c": batt["temp_c"]
        }
        results["samples"].append(sample)
        
        elapsed = int(time.time() - (end_time - duration))
        print(f"  [{elapsed:2d}s] CPU: {cpu_freq:>5.0f}MHz  RAM: {ram['used']:>5}MB/{ram['total']}MB  Batt: {batt['level']}%  Temp: {batt['temp_c']}°C")
        
        time.sleep(2)
    
    # Summary
    cpus = [s["cpu_mhz"] for s in results["samples"]]
    rams = [s["ram_mb"] for s in results["samples"]]
    
    print("")
    print("Summary:")
    print(f"  CPU avg: {sum(cpus)/len(cpus):.0f} MHz  (min: {min(cpus):.0f}, max: {max(cpus):.0f})")
    print(f"  RAM avg: {sum(rams)/len(rams):.0f} MB")
    print(f"  Storage: ", end="")
    try:
        storage = get_storage()
        print(f"{storage['mb_per_sec']:.1f} MB/s")
    except:
        print("N/A")
    
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Saved to: benchmark_results.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=30, help="Benchmark duration in seconds")
    args = parser.parse_args()
    benchmark(args.duration)
