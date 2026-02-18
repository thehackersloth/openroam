# OpenRoam Quick Start Guide

Get your OpenRoam system up and running in under an hour.

## What You'll Need

### Hardware
- 2x Raspberry Pi 5 8GB (Nav Node, AI Node)
- 2x Raspberry Pi 4 4GB or 8GB (Net Node, NAS Node)
- 4x microSD cards (32GB+ each)
- 1x NVMe SSD (for NAS node, 500GB-2TB)
- 4x USB-C power supplies (5V 3A)
- Ethernet switch (optional, for initial setup)
- HAT modules as needed

### Software
- Raspberry Pi Imager
- SSH client (Terminal on Mac/Linux, PuTTY on Windows)

## Step 1: Flash SD Cards (15 minutes)

### Download Images

Download the pre-built images from the releases page:
- `openroam-nav-node.img.gz`
- `openroam-net-node.img.gz`
- `openroam-nas-node.img.gz`
- `openroam-ai-node.img.gz`

### Flash with Raspberry Pi Imager

1. Open Raspberry Pi Imager
2. Click "Choose OS" → "Use Custom" → Select image
3. Click "Choose Storage" → Select SD card
4. Click gear icon for advanced settings:
   - Set hostname (e.g., `openroam-nav`)
   - Enable SSH with password authentication
   - Set username: `openroam`
   - Set password: (your choice)
   - Configure WiFi (for initial setup)
5. Click "Write"

Repeat for each node.

## Step 2: First Boot (10 minutes)

### Connect and Power On

1. Insert SD cards into each Pi
2. Connect to your network (Ethernet or WiFi)
3. Power on all nodes

### Find Your Nodes

Wait 2-3 minutes for boot, then:

```bash
# On Mac/Linux
ping openroam-nav.local

# Or scan your network
nmap -sn 192.168.1.0/24
```

### SSH into Nav Node

```bash
ssh openroam@openroam-nav.local
```

## Step 3: Initial Configuration (10 minutes)

### Run Setup Wizard

```bash
sudo openroam-setup
```

The wizard will:
1. Update system packages
2. Configure network settings
3. Set timezone
4. Initialize MQTT broker
5. Set up k3s cluster
6. Deploy dashboard

### Join Other Nodes

On the Nav node:
```bash
# Get join token
sudo openroam-cluster token
```

On each other node:
```bash
ssh openroam@openroam-nas.local
sudo openroam-cluster join <token>
```

## Step 4: Access Dashboard (5 minutes)

### Open in Browser

Navigate to: `http://openroam-nav.local`

Default credentials:
- Username: `admin`
- Password: `openroam`

**Change password immediately!**

### Verify Systems

The dashboard should show:
- All 4 nodes online
- MQTT connected
- Mock data flowing (no hardware yet)

## Step 5: Connect Hardware (varies)

### Install HATs

1. Power off the node
2. Align HAT with GPIO header
3. Press down firmly
4. Secure with standoffs

### Configure HATs

Edit `/etc/openroam/hardware.yaml`:

```yaml
hats:
  - type: nav-hat
    i2c_address: 0x42
  - type: power-hat
    i2c_address: 0x40
```

Restart services:
```bash
sudo systemctl restart openroam-core
```

## Step 6: Install in Vehicle

See full installation guide for:
- Mounting cluster box
- Running wiring
- Connecting sensors
- Antenna placement

## Verification Checklist

- [ ] All nodes visible in dashboard
- [ ] GPS showing location (if Nav HAT installed)
- [ ] Battery voltage reading (if Power HAT installed)
- [ ] Tank levels showing (if Tank HAT installed)
- [ ] WiFi network "OpenRoam" visible
- [ ] Can access dashboard from phone

## Troubleshooting

### Node Won't Boot
- Check power supply (5V 3A minimum)
- Verify SD card is properly seated
- Try re-flashing the SD card

### Can't Find Node on Network
- Check WiFi credentials in advanced settings
- Try connecting via Ethernet
- Check router DHCP leases

### Dashboard Won't Load
```bash
# Check services
ssh openroam@openroam-nav.local
sudo systemctl status openroam-dashboard
journalctl -u openroam-dashboard -f
```

### No Sensor Data
```bash
# Check HAT detection
i2cdetect -y 1

# Check MQTT messages
mosquitto_sub -h localhost -t "openroam/#" -v
```

## Next Steps

1. **Configure your vehicle** - Set tank capacities, battery specs
2. **Add integrations** - Victron, Starlink, etc.
3. **Customize dashboard** - Rearrange widgets, add pages
4. **Set up remote access** - Configure Tailscale VPN

## Getting Help

- GitHub Discussions: General questions
- GitHub Issues: Bug reports
- Documentation: `/docs` folder

Welcome to the OpenRoam community!
