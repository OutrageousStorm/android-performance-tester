#!/bin/bash
# Android performance benchmark suite
# Usage: ./bench.sh [all|cpu|mem|io|thermal]

TESTS="${1:-all}"

function cpu_bench() {
    echo "CPU Benchmark — calculating SHA-256 checksums..."
    adb shell time dd if=/dev/zero bs=1M count=100 | sha256sum
}

function mem_bench() {
    echo "Memory Benchmark..."
    TOTAL=$(adb shell cat /proc/meminfo | grep MemTotal | awk '{print $2}')
    FREE=$(adb shell cat /proc/meminfo | grep MemFree | awk '{print $2}')
    echo "  Total: $((TOTAL/1024)) MB"
    echo "  Free: $((FREE/1024)) MB"
}

function io_bench() {
    echo "I/O Benchmark — write test..."
    adb shell "time dd if=/dev/zero of=/data/test.bin bs=1M count=50; rm /data/test.bin"
}

function thermal_bench() {
    echo "Thermal Monitoring..."
    for i in {1..10}; do
        TEMP=$(adb shell cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null | awk '{print $1/1000}')
        echo "  [$i] ${TEMP}°C"
        sleep 1
    done
}

echo "🚀 Android Performance Benchmark"
echo "=============================="

[[ "$TESTS" == "all" || "$TESTS" == "cpu" ]] && cpu_bench
[[ "$TESTS" == "all" || "$TESTS" == "mem" ]] && mem_bench
[[ "$TESTS" == "all" || "$TESTS" == "io" ]] && io_bench
[[ "$TESTS" == "all" || "$TESTS" == "thermal" ]] && thermal_bench

echo "Done."
