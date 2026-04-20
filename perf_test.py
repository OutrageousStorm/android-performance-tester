#!/usr/bin/env python3
"""
perf_test.py -- Test Android device performance — CPU, RAM, storage, render time
Usage: python3 perf_test.py [--csv results.csv]
"""
import subprocess, time, csv

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

print("\n⚡ Android Performance Test\n")

# 1. CPU frequency
print("Testing CPU...")
freq = adb("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
max_freq = adb("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
print(f"  Current: {int(freq)//1000} MHz, Max: {int(max_freq)//1000} MHz")

# 2. RAM
print("\nTesting Memory...")
meminfo = adb("cat /proc/meminfo | grep MemTotal")
print(f"  {meminfo}")

# 3. Storage I/O (dd test)
print("\nTesting Storage I/O...")
start = time.time()
adb("dd if=/dev/zero of=/data/test_10mb.bin bs=1M count=10")
elapsed = time.time() - start
mb_per_sec = 10 / elapsed
print(f"  Write: {mb_per_sec:.1f} MB/s")
adb("rm /data/test_10mb.bin")

# 4. Render time (measure frame time)
print("\nTesting Frame Render...")
result = adb("dumpsys gfxinfo | grep 'Frame time'")
print(f"  {result[:80]}")

print("\n✅ Tests complete")
