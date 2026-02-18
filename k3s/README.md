# OpenRoam Kubernetes (k3s) Configuration

Kubernetes manifests for deploying OpenRoam services across the 4-node cluster.

## Cluster Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     k3s Cluster                             │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Nav Node   │  │  NAS Node   │  │  AI Node    │         │
│  │  (server)   │  │  (agent)    │  │  (agent)    │         │
│  │             │  │             │  │             │         │
│  │ - Dashboard │  │ - Plex      │  │ - Frigate   │         │
│  │ - MQTT      │  │ - Jellyfin  │  │ - Camera    │         │
│  │ - InfluxDB  │  │ - Syncthing │  │   Streams   │         │
│  │ - Grafana   │  │ - Nextcloud │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  ┌─────────────┐                                           │
│  │  Net Node   │  (Usually runs outside k3s for            │
│  │  (agent)    │   network stability)                      │
│  └─────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

## Deployment

### Install k3s on Nav Node (Server)

```bash
curl -sfL https://get.k3s.io | sh -s - server \
  --write-kubeconfig-mode 644 \
  --disable traefik \
  --disable servicelb
```

### Get Join Token

```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```

### Join Agent Nodes

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://openroam-nav:6443 \
  K3S_TOKEN=<token> sh -s - agent
```

## Applying Manifests

```bash
# Apply all base resources
kubectl apply -f base/

# Apply node-specific resources
kubectl apply -f nav-node/
kubectl apply -f nas-node/
kubectl apply -f ai-node/
```

## Services

### Core Services (Nav Node)

| Service | Port | Description |
|---------|------|-------------|
| Dashboard | 80 | Web interface |
| MQTT | 1883, 9001 | Message broker |
| InfluxDB | 8086 | Time-series DB |
| Grafana | 3000 | Metrics dashboard |
| API | 8080 | REST API |

### Media Services (NAS Node)

| Service | Port | Description |
|---------|------|-------------|
| Plex | 32400 | Media server |
| Jellyfin | 8096 | Media server (FOSS) |
| Syncthing | 8384 | File sync |
| Nextcloud | 443 | File cloud |

### AI Services (AI Node)

| Service | Port | Description |
|---------|------|-------------|
| Frigate | 5000 | NVR |
| RTSP | 8554 | Camera streams |

## Storage

### Persistent Volumes

```yaml
# Local path provisioner for each node
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
```

### NAS Node NVMe Storage

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nas-nvme
spec:
  capacity:
    storage: 2Ti
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/nvme
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - openroam-nas
```

## Monitoring

### Prometheus (Optional)

```bash
kubectl apply -f monitoring/prometheus.yaml
```

### Node Exporter

Each node runs node_exporter for system metrics.

## Updating

### Rolling Update

```bash
# Update dashboard
kubectl set image deployment/dashboard \
  dashboard=openroam/dashboard:v0.2.0

# Watch rollout
kubectl rollout status deployment/dashboard
```

### Full Cluster Update

```bash
# Apply updated manifests
kubectl apply -f .

# Restart all deployments
kubectl rollout restart deployment --all
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -A
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Node Issues

```bash
kubectl get nodes
kubectl describe node <node-name>
```

### Network Issues

```bash
kubectl get svc -A
kubectl get endpoints
```

## Offline Operation

The cluster is designed to operate fully offline:

- All images pre-pulled during setup
- Local container registry on Nav node
- No external dependencies required

### Pre-pull Images

```bash
./scripts/pull-images.sh
```

### Local Registry

```bash
# Push to local registry
docker tag openroam/dashboard:latest \
  openroam-nav:5000/openroam/dashboard:latest
docker push openroam-nav:5000/openroam/dashboard:latest
```
