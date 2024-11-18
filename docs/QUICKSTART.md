# Quick Start Guide

To install Stalwart Manager on a fresh server, run this command as root:

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/stalwart-manager/main/bootstrap.sh | bash
```

This will:
1. Install all required dependencies
2. Set up Docker and Python environment
3. Configure the mail server
4. Set up the web interface
5. Configure all necessary ports
6. Create systemd service

## System Requirements

- Fresh Ubuntu/Debian server
- Minimum 2GB RAM
- 20GB available disk space
- Root access
- Open ports:
  * 25 (SMTP)
  * 465 (SMTP SSL)
  * 587 (SMTP Submission)
  * 143 (IMAP)
  * 993 (IMAP SSL)
  * 8080 (Management API)
  * 8000 (Web Interface)

## Post-Installation

After installation:

1. Access the web interface:
```
http://YOUR-SERVER-IP:8000
```

2. Configure your domain:
   - Add DNS records
   - Set up SSL certificates
   - Configure email accounts

3. Monitor the service:
```bash
# Check service status
systemctl status stalwart-manager

# View logs
journalctl -u stalwart-manager

# Use CLI tool
stalwart-manager-cli
```

## Troubleshooting

If you encounter issues:

1. Check system requirements
2. Verify all ports are open
3. Check service logs
4. Ensure Docker is running
5. Verify network connectivity

For detailed installation options and configuration, see [INSTALL.md](INSTALL.md)
