#!/bin/bash
# Script: setup_vpn_routing.sh
# Description: Resolves routing deadlocks between Tailscale (Mesh VPN) and  NordVPN by replacing the closed-source daemon with raw OpenVPN.
#  Configures the node as a highly available Tailscale Exit Node.

echo "[*] Initiating VPN Routing Setup..."

# Step 1: Disable the commercial VPN daemon to release the routing table
echo "[*] Disabling closed-source VPN daemon..."
sudo nordvpn disconnect
sudo systemctl disable --now nordvpnd

# Step 2: Install native OpenVPN and required tools
echo "[*] Installing OpenVPN..."
sudo apt update && sudo apt install openvpn unzip -y

# Step 3: Setup OpenVPN directory and fetch official configs
echo "[*] Fetching OpenVPN configuration files..."
mkdir -p ~/nord_ovpn && cd ~/nord_ovpn
wget -q https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
unzip -q ovpn.zip

# NOTE: The user must manually create 'auth.txt' with service credentials here.
# Format:
# username
# password

# Step 4: Launch OpenVPN as a background daemon
echo "[*] Starting OpenVPN daemon..."
sudo openvpn --config ovpn_udp/cy30.nordvpn.com.udp.ovpn --auth-user-pass auth.txt --daemon

# Wait for the tunnel interface (tun0) to establish
sleep 5

# Step 5: Restart Tailscale to discover the new default route via tun0
echo "[*] Restarting Tailscale service to resolve Heartbeat/UDP drops..."
sudo systemctl restart tailscaled

# Step 6: Re-advertise the Raspberry Pi as an Exit Node over the new tunnel
echo "[*] Advertising node as Tailscale Exit Node..."
sudo tailscale up --advertise-exit-node

echo "[+] Setup Complete! The node is now routing Tailscale traffic through the OpenVPN tunnel."
