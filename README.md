# Stalwart Mail Server Manager

A web-based management interface for automated deployment and configuration of Stalwart Mail Server infrastructure.

## Features

- One-click Stalwart Mail Server deployment
- Automatic Cloudflare DNS configuration
- Docker-based deployment
- Web interface for server configuration
- TLS/SSL support
- SMTP, IMAP, and API endpoint configuration

## Prerequisites

- Ubuntu/Debian Linux
- Python 3.8+
- Docker and Docker Compose
- Cloudflare account with API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stalwart-manager.git
cd stalwart-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Access the web interface at `http://localhost:8000`

## Configuration

### Required Information

1. **Server Configuration**
   - Hostname (e.g., "mail")
   - Domain (e.g., "example.com")
   - Admin email address

2. **Cloudflare Configuration**
   - API Token with DNS edit permissions
   - Zone ID for your domain

### Mail Server Ports

The following ports will be configured:

- SMTP: 25 (incoming mail)
- SMTP Submission: 587 (outgoing mail)
- SMTP Submission SSL: 465
- IMAP: 143
- IMAP SSL: 993
- Management API: 8080

## Security Considerations

- Store Cloudflare API tokens securely
- Use strong passwords for mail accounts
- Keep the system and Docker images updated
- Configure firewall rules appropriately
- Enable TLS for all services

## Directory Structure

```
stalwart-manager/
├── app/
│   ├── static/
│   └── templates/
│       └── index.html
├── config/
├── data/
├── logs/
├── main.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
