#!/usr/bin/env python3
"""
geekbench_wrapper.py -- Run Geekbench on Android and parse results
Requires: Geekbench 6 APK installed on device
Usage: python3 geekbench_wrapper.py [--output results.json]
"""
import subprocess, re, json, argparse, time

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def get_geekbench_apk():
    """Check if Geekbench is installed"""
    out = adb("pm list packages | grep geekbench")
    return "geekbench" in out.lower()

def launch_geekbench():
    """Launch Geekbench and wait for results"""
    print("📊 Launching Geekbench on device...")
    adb("am start -n com.primatelabs.geekbench6/com.primatelabs.geekbench6.MainActivity")
    
    # Wait for test to complete (typically 3-5 minutes)
    print("⏳ Running benchmark... this takes 3-5 minutes")
    
    # Poll for completion
    max_wait = 600  # 10 minutes
    start = time.time()
    while time.time() - start < max_wait:
        running = adb("pidof com.primatelabs.geekbench6 2>/dev/null")
        if not running:
            break
        time.sleep(10)
        print(".", end="", flush=True)
    
    print("\nTest complete!")

def get_results():
    """Extract Geekbench results from device storage"""
    print("📥 Retrieving results...")
    
    # Results are typically saved in app's private storage
    # We can also check the app's displayed results via dumpsys
    out = adb("dumpsys activity top | grep -A 50 geekbench")
    
    results = {
        "single_core": None,
        "multi_core": None,
        "device": adb("getprop ro.product.model"),
        "android": adb("getprop ro.build.version.release"),
    }
    
    # Try to parse from logcat or dumpsys (varies by Geekbench version)
    single_m = re.search(r"Single[- ]Core:?\s+(\d+)", out, re.IGNORECASE)
    multi_m = re.search(r"Multi[- ]Core:?\s+(\d+)", out, re.IGNORECASE)
    
    if single_m:
        results["single_core"] = int(single_m.group(1))
    if multi_m:
        results["multi_core"] = int(multi_m.group(1))
    
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Save results to JSON file")
    args = parser.parse_args()

    if not get_geekbench_apk():
        print("❌ Geekbench 6 not installed. Get it from:")
        print("   Google Play Store: com.primatelabs.geekbench6")
        return

    launch_geekbench()
    results = get_results()
    
    print("\n📈 RESULTS:")
    print(f"  Device:      {results['device']} (Android {results['android']})")
    print(f"  Single-core: {results['single_core'] or 'N/A'}")
    print(f"  Multi-core:  {results['multi_core'] or 'N/A'}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Saved to {args.output}")

if __name__ == "__main__":
    main()
