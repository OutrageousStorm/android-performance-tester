package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

func adb(cmd string) string {
	out, _ := exec.Command("bash", "-c", "adb shell "+cmd).Output()
	return string(out)
}

func main() {
	duration := flag.Int("duration", 60, "Test duration seconds")
	interval := flag.Int("interval", 5, "Measurement interval")
	flag.Parse()

	fmt.Println("\n⚡ Android Performance Tester")
	fmt.Println("=============================\n")

	start := time.Now()
	deadline := start.Add(time.Duration(*duration) * time.Second)

	for time.Now().Before(deadline) {
		fmt.Printf("[%s] Sampling...", time.Now().Format("15:04:05"))
		
		// CPU
		cpu := adb("cat /proc/stat | head -1")
		fmt.Printf(" CPU: %s", cpu[:30])

		// Memory
		mem := adb("dumpsys meminfo | grep TOTAL")
		fmt.Printf(" MEM: %s", strings.TrimSpace(mem)[:30])

		// Battery
		bat := adb("dumpsys battery | grep level")
		fmt.Printf(" BAT: %s", strings.TrimSpace(bat))

		time.Sleep(time.Duration(*interval) * time.Second)
	}

	fmt.Println("\n✅ Complete")
}
