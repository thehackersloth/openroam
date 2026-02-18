# OpenRoam Software

Software components for the OpenRoam mobile living computing platform.

## Components

### openroam-dashboard

SvelteKit web application providing the user interface for monitoring and controlling all vehicle systems.

**Features:**
- Real-time system monitoring
- Touch-friendly mobile interface
- Dark mode optimized for night use
- Offline capability (PWA)
- MQTT integration

**Tech Stack:**
- SvelteKit 2.0
- TypeScript
- Tailwind CSS
- Chart.js
- Leaflet maps
- MQTT.js

**Quick Start:**
```bash
cd openroam-dashboard
npm install
npm run dev
```

**Build for Production:**
```bash
npm run build
```

### openroam-core

Python library for backend services, hardware interfacing, and data processing.

**Features:**
- HAT hardware drivers
- MQTT broker integration
- RoamK data model
- InfluxDB time-series storage
- REST API server

**Tech Stack:**
- Python 3.11+
- FastAPI
- Paho MQTT
- InfluxDB client
- smbus2 (I2C)
- pyserial

**Quick Start:**
```bash
cd openroam-core
pip install -e .
```

**Run Services:**
```bash
openroam-server
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser                          │
│                 (Dashboard SPA)                         │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/WebSocket
┌─────────────────────▼───────────────────────────────────┐
│                   Nav Node                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Dashboard  │  │  MQTT       │  │  InfluxDB   │     │
│  │  (Svelte)   │  │  Broker     │  │             │     │
│  └─────────────┘  └──────┬──────┘  └─────────────┘     │
│                          │                              │
│  ┌───────────────────────▼─────────────────────────┐   │
│  │              openroam-core                       │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐         │   │
│  │  │ HAT     │  │ RoamK   │  │ API     │         │   │
│  │  │ Drivers │  │ Store   │  │ Server  │         │   │
│  │  └────┬────┘  └─────────┘  └─────────┘         │   │
│  │       │                                         │   │
│  │  ┌────▼────────────────────────────────────┐   │   │
│  │  │        Hardware Abstraction Layer        │   │   │
│  │  └────┬─────────┬─────────┬─────────┬──────┘   │   │
│  └───────┼─────────┼─────────┼─────────┼──────────┘   │
│          │         │         │         │              │
│     ┌────▼───┐ ┌───▼───┐ ┌───▼───┐ ┌───▼───┐         │
│     │Nav HAT │ │Power  │ │Tank   │ │Climate│         │
│     │        │ │HAT    │ │HAT    │ │HAT    │         │
│     └────────┘ └───────┘ └───────┘ └───────┘         │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### RoamK Data Model

All vehicle data flows through the RoamK data store (similar to Signal K for marine vessels):

```
Hardware → HAT Driver → MQTT → RoamK Store → Dashboard
                ↓
           InfluxDB (history)
```

### MQTT Topics

All topics use the `openroam/` prefix:

```
openroam/power/battery/house/voltage
openroam/power/battery/house/current
openroam/power/battery/house/soc
openroam/tanks/fresh/level
openroam/climate/interior/temperature
openroam/nav/gps/latitude
openroam/nav/gps/longitude
...
```

## Development

### Prerequisites

- Node.js 18+
- Python 3.11+
- MQTT broker (Mosquitto)
- InfluxDB 2.x (optional)

### Local Development

1. Start MQTT broker:
```bash
mosquitto -c /etc/mosquitto/mosquitto.conf
```

2. Start dashboard:
```bash
cd openroam-dashboard
npm run dev
```

3. Start core services:
```bash
cd openroam-core
python -m openroam_core.server
```

### Testing with Mock Data

For development without hardware:
```bash
python -m openroam_core.mock_data
```

This publishes simulated sensor data to MQTT.

## Deployment

### Single Node (Development)

```bash
docker-compose up -d
```

### 4-Node Cluster (Production)

Use Ansible playbooks in `../tools/ansible/`:

```bash
ansible-playbook -i inventory/cluster.yml playbooks/deploy-dashboard.yml
ansible-playbook -i inventory/cluster.yml playbooks/deploy-services.yml
```

## Configuration

### Dashboard

Edit `openroam-dashboard/src/lib/config.ts`:

```typescript
export const config = {
  mqttHost: 'openroam.local',
  mqttPort: 9001,
  apiUrl: 'http://openroam.local:8080'
};
```

### Core Services

Edit `/etc/openroam/config.yaml`:

```yaml
mqtt:
  host: localhost
  port: 1883

influxdb:
  url: http://localhost:8086
  token: your-token
  org: openroam
  bucket: telemetry

hardware:
  i2c_bus: 1
  hats:
    - nav-hat
    - power-hat
    - tank-hat
```

## License

MIT License
