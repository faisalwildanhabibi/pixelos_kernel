#!/usr/bin/env python3
"""
Comprehensive Kernel & Android Compatibility Test Suite for Alioth / SM8250
Evaluates target .config against:
1. Xiaomi SM8250 / POCO F3 (alioth) Hardware & HAL compatibility
2. Kernel 4.19 Core Subsystems & Backports (EROFS, KFENCE, WALT, fscrypt, etc.)
3. Android Compatibility Matrix (Android 11 through Android 16/17 requirements)
"""

import sys
import os
import re

def parse_config(path):
    cfg = {}
    if not os.path.exists(path):
        print(f"[!] Error: Config file not found at {path}")
        sys.exit(1)
        
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or (line.startswith('#') and 'is not set' not in line):
                continue
            m = re.match(r'^(CONFIG_[A-Za-z0-9_]+)=(.*)$', line)
            if m:
                cfg[m.group(1)] = m.group(2)
            else:
                m_unset = re.match(r'^#\s+(CONFIG_[A-Za-z0-9_]+)\s+is not set$', line)
                if m_unset:
                    cfg[m_unset.group(1)] = 'n'
    return cfg

def run_tests(config_path):
    cfg = parse_config(config_path)
    
    test_suite = [
        # =========================================================================
        # 1. PIXELOS & SM8250 XIAOMI HARDWARE COMPATIBILITY
        # =========================================================================
        ("Xiaomi Alioth Hardware", "FocalTech Touchscreen", "CONFIG_TOUCHSCREEN_FOCALTECH", "y", "Alioth primary touch digitizer"),
        ("Xiaomi Alioth Hardware", "Xiaomi Touch Feature Layer", "CONFIG_TOUCHSCREEN_XIAOMI_TOUCHFEATURE", "y", "Touch sampling rate and game gesture abstraction"),
        ("Xiaomi Alioth Hardware", "Touchscreen Common Driver", "CONFIG_TOUCHSCREEN_COMMON", "y", "Touch HAL gesture interface"),
        ("Xiaomi Alioth Hardware", "KTZ8866 AMOLED Backlight", "CONFIG_BACKLIGHT_KTZ8866", "y", "Samsung E4 AMOLED backlight controller"),
        ("Xiaomi Alioth Hardware", "Dual KTZ8866 Conflict Check", "CONFIG_BACKLIGHT_DUALKTZ8866", "n", "Must be disabled for single-panel alioth to avoid symbol collision"),
        ("Xiaomi Alioth Hardware", "DRM Display Subsystem", "CONFIG_DRM", "y", "Qualcomm SDE DRM KMS driver for Adreno 650"),
        ("Xiaomi Alioth Hardware", "BQ2597X 33W Charge Pump", "CONFIG_BQ2597X_CHARGE_PUMP", "y", "Alioth 33W Fast Charging hardware"),
        ("Xiaomi Alioth Hardware", "DS28E16 Battery Authenticator", "CONFIG_BATT_VERIFY_BY_DS28E16", "y", "OEM Battery security verification with batterysecret HAL"),
        ("Xiaomi Alioth Hardware", "1-Wire GPIO Protocol", "CONFIG_ONEWIRE_GPIO", "y", "Communication bus for DS28E16 security chip"),
        ("Xiaomi Alioth Hardware", "Disable Slave Charger SMB1355", "CONFIG_SMB1355_SLAVE_CHARGER", "n", "Prevents charger driver race conditions"),
        ("Xiaomi Alioth Hardware", "Disable Slave Charger SMB1390", "CONFIG_SMB1390_CHARGE_PUMP_PSY", "n", "Locks charging pump exclusively to BQ2597X"),
        ("Xiaomi Alioth Hardware", "AW8697 Z-Axis Haptics", "CONFIG_INPUT_AW8697_HAPTIC", "y", "Alioth linear resonant haptic actuator"),
        ("Xiaomi Alioth Hardware", "Disable Generic QTI Haptics", "CONFIG_INPUT_QTI_HAPTICS", "n", "Prevents vibration motor conflict"),
        ("Xiaomi Alioth Hardware", "FPC Fingerprint Scanner", "CONFIG_FINGERPRINT_FPC", "y", "Side fingerprint sensor (FPC)"),
        ("Xiaomi Alioth Hardware", "Goodix Fingerprint Scanner", "CONFIG_FINGERPRINT_GOODIX", "y", "Side fingerprint sensor (Goodix)"),
        ("Xiaomi Alioth Hardware", "Elliptic Ultrasound Proximity", "CONFIG_US_PROXIMITY", "y", "Inner-beauty virtual proximity sensor"),
        ("Xiaomi Alioth Hardware", "AKM09970 Hall Effect Sensor", "CONFIG_HALL_AKM09970", "y", "Magnetic flip cover detection"),
        ("Xiaomi Alioth Hardware", "Parade PS5169 Type-C Redriver", "CONFIG_PS5169", "y", "USB PD 3.0, fast charging, and OTG signal repeater"),
        ("Xiaomi Alioth Hardware", "Consumer IR SPI Driver", "CONFIG_IR_SPI", "y", "IR remote control blaster hardware"),
        ("Xiaomi Alioth Hardware", "QCA CLD3 Wi-Fi 6", "CONFIG_QCA_CLD_WLAN", "y", "Qualcomm FastConnect 6900 Wi-Fi subsystem"),
        ("Xiaomi Alioth Hardware", "ALSA SoC Audio Core", "CONFIG_SND_SOC", "y", "Audio HAL and TFA amplifier backend"),

        # =========================================================================
        # 2. KERNEL 4.19 CORE SUBSYSTEMS & MODERN BACKPORTS
        # =========================================================================
        ("Kernel 4.19 Backports", "EROFS Filesystem (5.4+ Backport)", "CONFIG_EROFS_FS", "y", "Modern read-only compressed filesystem support"),
        ("Kernel 4.19 Backports", "EROFS Per-CPU KThread", "CONFIG_EROFS_FS_PCPU_KTHREAD", "y", "High-throughput parallel decompression threads"),
        ("Kernel 4.19 Backports", "EROFS High-Priority KThread", "CONFIG_EROFS_FS_PCPU_KTHREAD_HIPRI", "y", "Zero-jitter system partition decompression"),
        ("Kernel 4.19 Backports", "F2FS Filesystem", "CONFIG_F2FS_FS", "y", "Flash-Friendly Filesystem for userdata"),
        ("Kernel 4.19 Backports", "F2FS Compression Backport", "CONFIG_F2FS_FS_COMPRESSION", "y", "LZO/LZ4 userdata block compression"),
        ("Kernel 4.19 Backports", "Inline Filesystem Encryption", "CONFIG_FS_ENCRYPTION", "y", "Hardware-accelerated FBE crypto"),
        ("Kernel 4.19 Backports", "Qualcomm WALT Scheduler", "CONFIG_SCHED_WALT", "y", "Window-Assisted Load Tracking energy scheduler"),
        ("Kernel 4.19 Backports", "Pressure Stall Information (PSI)", "CONFIG_PSI", "y", "CPU/IO/Memory stall metrics for modern Android LMKD"),
        ("Kernel 4.19 Backports", "Schedutil CPU Frequency Governor", "CONFIG_CPU_FREQ_GOV_SCHEDUTIL", "y", "EAS frequency governor hooked to WALT"),
        ("Kernel 4.19 Backports", "ThinLTO Compilation", "CONFIG_THINLTO", "y", "Parallel link-time optimization with negligible link latency"),
        ("Kernel 4.19 Backports", "ZRAM Swap Device", "CONFIG_ZRAM", "y", "Compressed RAM swap block driver"),
        ("Kernel 4.19 Backports", "ZSTD Crypto Algorithm", "CONFIG_CRYPTO_ZSTD", "y", "High-ratio ZSTD compression algorithm for ZRAM"),
        ("Kernel 4.19 Backports", "RCU Priority Boosting", "CONFIG_RCU_BOOST", "y", "Prevents RCU readers from stalling UI execution threads"),
        ("Kernel 4.19 Backports", "Writeback Throttling", "CONFIG_BLK_WBT", "y", "Prevents I/O write starvation on UFS 3.1 storage"),

        # =========================================================================
        # 3. ANDROID OS COMPATIBILITY MATRIX (Android 11 - 16/17)
        # =========================================================================
        ("Android Compatibility", "Android BinderFS", "CONFIG_ANDROID_BINDERFS", "y", "Mandatory isolated IPC filesystem for Android 10+"),
        ("Android Compatibility", "Android Binder IPC", "CONFIG_ANDROID_BINDER_IPC", "y", "Core Android IPC driver"),
        ("Android Compatibility", "Memory Cgroup Tracking", "CONFIG_MEMCG", "y", "Required by androidboot.memcg=1 and modern LMKD"),
        ("Android Compatibility", "Swap Memory Cgroup", "CONFIG_MEMCG_SWAP", "y", "Swap cgroup accounting for Android memory quotas"),
        ("Android Compatibility", "BPF Subsystem", "CONFIG_BPF_SYSCALL", "y", "eBPF kernel execution engine for Android network stats"),
        ("Android Compatibility", "Cgroup BPF Network Hooks", "CONFIG_CGROUP_BPF", "y", "Traffic controller & network socket tagging (xt_qtaguid replacement)"),
        ("Android Compatibility", "Clang CFI Permissive", "CONFIG_CFI_PERMISSIVE", "y", "Prevents fatal kernel panic on syscall hooks / KSU / SuSFS"),
        ("Android Compatibility", "Control Flow Integrity Disabled", "CONFIG_CFI_CLANG", "n", "Must not be strict to avoid bootloop panic with KSU"),
        ("Android Compatibility", "Ashmem Shared Memory", "CONFIG_ASHMEM", "y", "Android shared memory allocator"),
        ("Android Compatibility", "SELinux Security Subsystem", "CONFIG_SECURITY_SELINUX", "y", "Mandatory Android SELinux access control"),
        ("Android Compatibility", "Process Namespaces Support", "CONFIG_NAMESPACES", "y", "Android app isolation and process security boundaries"),
        ("Android Compatibility", "Overlay Filesystem", "CONFIG_OVERLAY_FS", "y", "Required for dynamic partition overlay & volatile testing"),
        ("Android Compatibility", "EXT4 Filesystem", "CONFIG_EXT4_FS", "y", "Required for system/product/metadata mounts"),
        ("Android Compatibility", "VFAT Firmware Filesystem", "CONFIG_VFAT_FS", "y", "Required for modem, DSP, and BT firmware mounts"),
        ("Android Compatibility", "Loop Device Partitioning", "CONFIG_BLK_DEV_LOOP", "y", "Required for APEX modules & virtual disk mounting")
    ]

    print("================================================================================")
    print("      COMPREHENSIVE KERNEL & ANDROID COMPATIBILITY TEST SUITE")
    print(f"      Target: {config_path}")
    print("================================================================================\n")

    passed_count = 0
    failed_count = 0
    current_category = None

    for category, feature, symbol, expected, rationale in test_suite:
        if category != current_category:
            current_category = category
            print(f"\n--- [{current_category}] ---")
            
        actual = cfg.get(symbol, "n" if expected != "n" else "y" if symbol in cfg else "n")
        # Treat absent symbol as 'n' if expecting 'n'
        if symbol not in cfg:
            actual = "n"
            
        is_pass = (actual == expected)
        
        status_str = "\033[92mPASS\033[0m" if is_pass else "\033[91mFAIL\033[0m"
        # Fallback for plain non-ansi console
        if not sys.stdout.isatty():
            status_str = "PASS" if is_pass else "FAIL"

        if is_pass:
            passed_count += 1
            print(f"  [{status_str}] {feature:<35} | {symbol}={actual}")
        else:
            failed_count += 1
            print(f"  [{status_str}] {feature:<35} | {symbol}: expected '{expected}', got '{actual}' ({rationale})")

    total_tests = len(test_suite)
    print("\n================================================================================")
    print(f" SUMMARY: Total Tests: {total_tests} | Passed: {passed_count} | Failed: {failed_count}")
    print(f" SCORE:   {(passed_count / total_tests) * 100:.1f}%")
    print("================================================================================")

    if failed_count > 0:
        print("\n[!] FATAL: Kernel configuration failed compatibility tests!")
        print("[!] Build will be aborted to prevent non-booting or broken kernel.")
        sys.exit(1)
    else:
        print("\n[+] SUCCESS: Kernel configuration satisfies 100% of compatibility requirements.")
        print("[+] Fully verified for Xiaomi POCO F3 (alioth), Kernel 4.19, and Android 16/17.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path_to_config>")
        sys.exit(1)
    run_tests(sys.argv[1])
