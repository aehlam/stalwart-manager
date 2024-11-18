# Installation Guide

## Quick Installation

```bash
pip install stalwart-manager
```

## Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stalwart-manager.git
cd stalwart-manager
```

2. Install in development mode:
```bash
pip install -e .
```

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Cloudflare account with API access
- Linux operating system (Ubuntu/Debian recommended)

## System Requirements

- Minimum 2GB RAM
- 20GB available disk space
- Network access to ports:
  - 25 (SMTP)
  - 465 (SMTP SSL)
  - 587 (SMTP Submission)
  - 143 (IMAP)
  - 993 (IMAP SSL)
  - 8080 (Management API)

## Installation Steps

1. **Install System Dependencies**

```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    docker.io \
    docker-compose
```

2. **Install Stalwart Manager**

```bash
pip install stalwart-manager
```

3. **Start the Service**

```bash
stalwart-manager
```

4. Access the web interface at `http://localhost:8000`

## Configuration

1. **Required Information**

- Domain name
- Cloudflare API token
- Cloudflare Zone ID
- Admin email address

2. **Environment Variables**

You can configure the following environment variables:

```bash
STALWART_HOST=0.0.0.0  # Interface to bind to
STALWART_PORT=8000     # Web interface port
STALWART_DEBUG=false   # Enable debug mode
```

## Troubleshooting

1. **Port Conflicts**

If you see "address already in use" errors:
```bash
sudo netstat -tulpn | grep -E ":(25|465|587|143|993|8080)"
```

2. **Docker Issues**

Verify Docker is running:
```bash
sudo systemctl status docker
```

3. **Permission Issues**

Ensure proper permissions:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Security Notes

1. Always use strong passwords
2. Keep system and packages updated
3. Use firewall rules to restrict access
4. Store API tokens securely
5. Enable TLS for all services

## Updating

To update to the latest version:

```bash
pip install --upgrade stalwart-manager
```

## Uninstallation

To remove Stalwart Manager:

```bash
pip uninstall stalwart-manager
```

To completely remove all data:

```bash
docker-compose down -v
rm -rf ~/.stalwart-manager
```
