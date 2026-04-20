package com.outrageousstorm.perftest

import android.app.Activity
import android.os.Bundle
import android.widget.TextView
import java.io.RandomAccessFile
import kotlin.system.measureTimeMillis

class PerformanceTest : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val text = TextView(this).apply {
            textSize = 12f
            setPadding(16, 16, 16, 16)
        }
        
        val sb = StringBuilder("📊 Performance Test\n\n")
        
        // CPU
        val cpuTime = measureTimeMillis {
            var sum = 0L
            for (i in 0..10000000) sum += i
        }
        sb.append("CPU (sum): $${cpuTime}ms\n")
        
        // Memory
        val runtime = Runtime.getRuntime()
        val memBefore = runtime.totalMemory() - runtime.freeMemory()
        val list = (0..1000).map { ByteArray(10240) }
        val memAfter = runtime.totalMemory() - runtime.freeMemory()
        sb.append("Memory: $${(memAfter - memBefore) / 1024}KB\n")
        
        // Device
        sb.append("\nCores: $${Runtime.getRuntime().availableProcessors()}\n")
        sb.append("RAM: $${runtime.maxMemory() / 1024 / 1024}MB\n")
        
        text.text = sb.toString()
        setContentView(text)
    }
}
