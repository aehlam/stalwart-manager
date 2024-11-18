#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[*]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root"
    exit 1
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VERSION=$VERSION_ID
else
    print_error "Cannot detect OS"
    exit 1
fi

# Check if supported OS
case $OS in
    "Ubuntu"|"Debian GNU/Linux")
        print_status "Detected $OS $VERSION"
        ;;
    *)
        print_error "Unsupported OS: $OS"
        exit 1
        ;;
esac

# Update system
print_status "Updating system packages..."
apt-get update
if [ $? -ne 0 ]; then
    print_error "Failed to update package list"
    exit 1
fi

# Install required packages
print_status "Installing required packages..."
PACKAGES="python3 python3-pip python3-venv docker.io docker-compose curl git"
apt-get install -y $PACKAGES
if [ $? -ne 0 ]; then
    print_error "Failed to install required packages"
    exit 1
fi

# Start and enable Docker
print_status "Configuring Docker..."
systemctl start docker
systemctl enable docker

# Create virtual environment
print_status "Creating Python virtual environment..."
VENV_DIR="/opt/stalwart-manager/venv"
mkdir -p /opt/stalwart-manager
python3 -m venv $VENV_DIR

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install pip packages
print_status "Installing Python dependencies..."
pip install wheel setuptools

# Create installation directory
INSTALL_DIR="/opt/stalwart-manager"
mkdir -p $INSTALL_DIR

# Download Stalwart Manager
print_status "Downloading Stalwart Manager..."
if [ -f "stalwart_manager-1.0.0-py3-none-any.whl" ]; then
    pip install stalwart_manager-1.0.0-py3-none-any.whl
else
    print_error "Wheel file not found. Please ensure stalwart_manager-1.0.0-py3-none-any.whl is in the current directory"
    exit 1
fi

# Create systemd service
print_status "Creating systemd service..."
cat > /etc/systemd/system/stalwart-manager.service << EOL
[Unit]
Description=Stalwart Mail Server Manager
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/stalwart-manager
Environment="PATH=/opt/stalwart-manager/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/opt/stalwart-manager/venv/bin/stalwart-manager
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd
systemctl daemon-reload

# Create configuration directory
mkdir -p /etc/stalwart-manager

# Configure firewall
print_status "Configuring firewall..."
if command_exists ufw; then
    ufw allow 25/tcp
    ufw allow 465/tcp
    ufw allow 587/tcp
    ufw allow 143/tcp
    ufw allow 993/tcp
    ufw allow 8080/tcp
    ufw allow 8000/tcp
fi

# Start service
print_status "Starting Stalwart Manager..."
systemctl start stalwart-manager
systemctl enable stalwart-manager

# Create convenience script
cat > /usr/local/bin/stalwart-manager-cli << EOL
#!/bin/bash
source /opt/stalwart-manager/venv/bin/activate
stalwart-manager "\$@"
EOL
chmod +x /usr/local/bin/stalwart-manager-cli

# Print installation summary
print_status "Installation completed successfully!"
echo -e "\nStalwart Manager has been installed with the following configuration:"
echo -e "- Web Interface: http://YOUR-SERVER-IP:8000"
echo -e "- Mail Server Ports:"
echo -e "  * SMTP: 25"
echo -e "  * SMTP Submission: 587"
echo -e "  * SMTP Submission SSL: 465"
echo -e "  * IMAP: 143"
echo -e "  * IMAP SSL: 993"
echo -e "  * Management API: 8080"
echo -e "\nTo manage the service:"
echo -e "- Start: systemctl start stalwart-manager"
echo -e "- Stop: systemctl stop stalwart-manager"
echo -e "- Status: systemctl status stalwart-manager"
echo -e "- Logs: journalctl -u stalwart-manager"
echo -e "\nCommand-line interface:"
echo -e "stalwart-manager-cli"

# Check service status
if systemctl is-active --quiet stalwart-manager; then
    print_status "Service is running"
    echo -e "\nAccess the web interface at: http://$(curl -s ifconfig.me):8000"
else
    print_error "Service failed to start. Check logs with: journalctl -u stalwart-manager"
fi

# Security recommendations
print_warning "Security Recommendations:"
echo -e "1. Configure SSL/TLS certificates"
echo -e "2. Set up DNS records (SPF, DKIM, DMARC)"
echo -e "3. Configure firewall rules"
echo -e "4. Set strong passwords"
echo -e "5. Keep system updated"

# Cleanup
print_status "Cleaning up..."
apt-get clean
apt-get autoremove -y
