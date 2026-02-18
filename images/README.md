# OpenRoam Raspberry Pi Images

Pre-configured OS images for each node in the OpenRoam cluster.

## Node Roles

| Node | Hardware | Image | Primary Role |
|------|----------|-------|--------------|
| **Nav Node** | RPi 5 8GB | nav-node | Dashboard, MQTT, primary control |
| **Net Node** | RPi 4 4GB | net-node | WiFi AP, cellular, VPN |
| **NAS Node** | RPi 4 8GB | nas-node | Media server, storage |
| **AI Node** | RPi 5 8GB | ai-node | Camera processing, AI inference |

## Building Images

Images are built using pi-gen or custom scripts based on Raspberry Pi OS Lite.

### Prerequisites

```bash
# On Linux (Debian/Ubuntu)
sudo apt install qemu-user-static debootstrap

# Clone pi-gen
git clone https://github.com/RPi-Distro/pi-gen.git
```

### Build All Images

```bash
./build-images.sh
```

### Build Single Image

```bash
./build-images.sh nav-node
```

## Flashing Images

```bash
# Using dd
sudo dd if=nav-node.img of=/dev/sdX bs=4M status=progress

# Using Raspberry Pi Imager
# Select "Use custom" and choose the .img file
```

## First Boot Configuration

### Network

Edit `boot/openroam.conf` on the SD card before first boot:

```ini
[network]
wifi_ssid=YourNetwork
wifi_password=YourPassword
hostname=openroam-nav

[mqtt]
broker=openroam-nav.local
port=1883
```

### SSH

SSH is enabled by default. Default credentials:
- Username: `openroam`
- Password: `changeme`

**Change password on first login!**

## Image Contents

### Common (All Nodes)

- Raspberry Pi OS Lite (64-bit)
- Python 3.11+
- openroam-core package
- Mosquitto MQTT client
- Tailscale VPN client
- Docker CE
- k3s agent

### Nav Node Specific

- Mosquitto MQTT broker
- InfluxDB
- Grafana
- openroam-dashboard
- k3s server (control plane)
- Chromium (kiosk mode for display)

### Net Node Specific

- hostapd (WiFi AP)
- dnsmasq (DHCP/DNS)
- OpenWRT packages
- Pi-hole
- Tailscale exit node

### NAS Node Specific

- Plex Media Server
- Jellyfin
- Syncthing
- Nextcloud
- Samba
- NFS server

### AI Node Specific

- Hailo SDK
- Frigate NVR
- TensorFlow Lite
- OpenCV
- gstreamer

## Customization

### Adding HAT Support

1. Edit `config/nav-node/config.txt`:
```ini
dtparam=i2c_arm=on
dtparam=spi=on
dtoverlay=uart5
```

2. Enable services in `config/nav-node/services.conf`:
```ini
openroam-nav-hat=enabled
openroam-power-hat=enabled
```

### Network Configuration

Edit `config/*/network.conf`:

```ini
# Static IP (optional)
static_ip=192.168.4.10
gateway=192.168.4.1
dns=192.168.4.1

# VLAN support
vlan_id=100
```

## Updating Images

### Online Update

```bash
# On each node
sudo openroam-update
```

### Offline Update

1. Download update package
2. Copy to USB drive
3. Insert USB on node
4. Run: `sudo openroam-update --offline /media/usb/update.tar.gz`

## Troubleshooting

### Node Won't Boot

1. Check SD card seating
2. Verify power supply (5V 3A minimum)
3. Check activity LED patterns
4. Connect HDMI to see boot messages

### Network Issues

```bash
# Check network status
networkctl status

# Check WiFi
iwconfig wlan0

# Restart networking
sudo systemctl restart networking
```

### Service Issues

```bash
# Check service status
sudo systemctl status openroam-core

# View logs
journalctl -u openroam-core -f
```

## Security

### Hardening

After first boot:

1. Change default password
2. Set up SSH keys
3. Disable password authentication
4. Configure firewall
5. Enable automatic updates

```bash
# Run security setup
sudo openroam-secure
```

### Certificates

Generate HTTPS certificates:

```bash
sudo openroam-certs generate
```

## Support

See main project README for support channels.
