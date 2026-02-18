# OpenRoam Ansible Automation

Ansible playbooks for deploying and managing OpenRoam clusters.

## Prerequisites

```bash
pip install ansible
```

## Inventory

Edit `inventory/cluster.yml` with your node IPs:

```yaml
all:
  children:
    openroam:
      children:
        nav_nodes:
          hosts:
            openroam-nav:
              ansible_host: 192.168.4.10
        net_nodes:
          hosts:
            openroam-net:
              ansible_host: 192.168.4.11
        nas_nodes:
          hosts:
            openroam-nas:
              ansible_host: 192.168.4.12
        ai_nodes:
          hosts:
            openroam-ai:
              ansible_host: 192.168.4.13
```

## Playbooks

### Initial Setup

```bash
# Configure all nodes from fresh install
ansible-playbook -i inventory/cluster.yml playbooks/setup-cluster.yml
```

### Deploy Dashboard

```bash
ansible-playbook -i inventory/cluster.yml playbooks/deploy-dashboard.yml
```

### Deploy Services

```bash
ansible-playbook -i inventory/cluster.yml playbooks/deploy-services.yml
```

### Update All Nodes

```bash
ansible-playbook -i inventory/cluster.yml playbooks/update-all.yml
```

### Backup

```bash
ansible-playbook -i inventory/cluster.yml playbooks/backup.yml
```

## Roles

| Role | Description |
|------|-------------|
| common | Base packages, users, SSH |
| docker | Docker CE installation |
| k3s-server | k3s control plane |
| k3s-agent | k3s worker node |
| mosquitto | MQTT broker |
| influxdb | Time-series database |
| dashboard | OpenRoam web UI |
| media-server | Plex/Jellyfin |
| ai-inference | Hailo/TFLite setup |

## Variables

Edit `group_vars/all.yml`:

```yaml
# Network
cluster_domain: openroam.local
cluster_network: 192.168.4.0/24

# Versions
dashboard_version: "0.1.0"
core_version: "0.1.0"

# Features
enable_plex: true
enable_jellyfin: true
enable_frigate: true
```

## Ad-hoc Commands

```bash
# Ping all nodes
ansible openroam -i inventory/cluster.yml -m ping

# Restart service on all nodes
ansible openroam -i inventory/cluster.yml -m systemd \
  -a "name=openroam-core state=restarted"

# Run command on specific node
ansible nav_nodes -i inventory/cluster.yml -m shell \
  -a "systemctl status mosquitto"
```

## Troubleshooting

### SSH Connection Issues

```bash
# Test SSH access
ssh openroam@192.168.4.10

# Use verbose mode
ansible-playbook -vvv -i inventory/cluster.yml playbooks/setup.yml
```

### Playbook Failures

```bash
# Start from specific task
ansible-playbook -i inventory/cluster.yml playbooks/setup.yml \
  --start-at-task="Install Docker"

# Run specific tags
ansible-playbook -i inventory/cluster.yml playbooks/setup.yml \
  --tags="docker,k3s"
```
