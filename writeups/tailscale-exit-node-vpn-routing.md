# Tailscale Exit Node & VPN Routing (lab-02)

## Overview

`lab-02` (Raspberry Pi 5) is configured as a **Tailscale Exit Node**, routing all outbound traffic from connected devices through the home network's public IP via an encrypted WireGuard tunnel. This allows any device on the Tailscale mesh — regardless of physical location — to appear as if it is on the home network.

## The Problem

`lab-02` also runs a commercial VPN client (NordVPN) for certain use cases. Running both simultaneously creates a routing conflict: the VPN intercepts outbound traffic before it reaches the Tailscale tunnel, breaking Exit Node functionality for connected devices.

Manually toggling between the two was error-prone and introduced risk of routing loops leaving the host without a valid default route.

## Solution

Automated the full reconfiguration sequence in a bash script: [`setup_vpn_routing.sh`](../scripts/setup_vpn_routing.sh)

The script handles the following in order:

1. Brings down the commercial VPN interface cleanly
2. Configures the OpenVPN daemon with policy-based routing rules to prevent tunnel conflicts
3. Re-advertises the Tailscale Exit Node to the mesh
4. Verifies tunnel continuity via a heartbeat check before exiting

## Key Technical Details

**Policy-based routing** is the core mechanism. Rather than relying on a single default route (which causes the conflict), traffic is routed based on source address — Tailscale tunnel traffic follows one routing table, VPN traffic follows another. This isolates the two tunnels at the kernel routing level.

**Exit Node advertisement** must be explicitly re-triggered after any network reconfiguration, as Tailscale withdraws the advertisement when it detects interface changes:

```bash
tailscale up --advertise-exit-node --reset
```

## Result

Seamless switching between VPN and Exit Node modes without manual intervention or risk of routing loops. Connected devices (Windows PC, iPhone) can route all traffic through the home network from any location, with sub-second failover between modes.

## Key Takeaways

- Running two tunnel-based solutions simultaneously requires policy-based routing rather than a single default route — otherwise one tunnel will always shadow the other.
- Tailscale Exit Node advertisements are stateful and must be re-triggered after interface changes.
- Automating network reconfigurations that involve multiple interdependent services significantly reduces the risk of leaving the host in a broken routing state.
