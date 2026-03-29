# Raspberry Pi 5 — Kernel Module Compilation & WiFi Monitor Mode

## Overview

The `lab-02` Raspberry Pi 5 was configured as a dedicated 802.11 packet capture sensor by compiling a custom kernel module for a TP-Link WN722N v2 adapter. The goal was to enable monitor mode and packet injection capabilities for authorized wireless security research.

## The Problem

The WN722N v2 uses a **Realtek RTL8188EU** chipset — not the Atheros chipset found in the v1 revision. The stock Ubuntu driver supports only managed (client) mode, which disables monitor mode and packet injection entirely.

The v2 revision is commonly sold under the same product name as the v1, making hardware identification a prerequisite before any driver work.

## Phase 1 — Hardware Identification

Confirmed the adapter revision using `lsusb` and cross-referenced the USB vendor/product ID against known chipset databases. The v2 (Realtek) requires a completely different driver path than the v1 (Atheros), so this step was critical before proceeding.

## Phase 2 — Kernel Module Compilation

Cloned the Aircrack-ng community driver for the RTL8188EU chipset and attempted compilation.

**Initial failure:** The default Makefile uses `CONFIG_PLATFORM_ARM_RPI=y`, which targets 32-bit ARM. The Raspberry Pi 5 runs a 64-bit kernel, causing the build to fail.

**Fix:** Explicitly targeted the correct architecture:

```bash
make ARCH=arm64
```

The module (`8188eu.ko`) compiled successfully and was inserted into the running kernel:

```bash
sudo insmod 8188eu.ko
```

## Phase 3 — Interface Configuration

Ubuntu assigned the adapter a predictable interface name based on its MAC address (`wlx3c52a1e25e99`) rather than a generic `wlan1`. Transitioned the interface from managed to monitor mode:

```bash
sudo ip link set wlx3c52a1e25e99 down
sudo iwconfig wlx3c52a1e25e99 mode monitor
sudo ip link set wlx3c52a1e25e99 up
```

Verified with `iwconfig` — mode confirmed as `Monitor`.

## Phase 4 — Toolchain Compilation from Source

The `aircrack-ng` suite was unavailable in the Ubuntu 24.04 ARM64 repository — marked FTBFS (Fails To Build From Source) by the Ubuntu maintainers for this architecture.

Built the full toolchain from the official Aircrack-ng v1.7 source, resolving all cryptographic library dependencies manually, and registered shared libraries with `ldconfig`.

## Result

A Raspberry Pi 5 running a custom-compiled kernel module and a from-source wireless analysis toolchain, capable of passive 2.4GHz packet capture and WPA2 handshake collection for authorized network auditing.

## Key Takeaways

- Hardware revision identification is a prerequisite — the same product name can ship with entirely different chipsets requiring different driver paths.
- Cross-architecture compilation failures are often caused by incorrect platform flags in the Makefile, not actual incompatibilities.
- When a package is marked FTBFS for a target architecture, building from source with manually resolved dependencies is a reliable fallback.
