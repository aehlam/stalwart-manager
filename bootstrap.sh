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

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root"
    exit 1
fi

# Ensure curl is installed
if ! command -v curl > /dev/null; then
    apt-get update
    apt-get install -y curl
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd $TEMP_DIR

# Download installation package
print_status "Downloading Stalwart Manager installation package..."
curl -L -o stalwart-manager.tar.gz https://github.com/yourusername/stalwart-manager/releases/download/v1.0.0/stalwart-manager-1.0.0.tar.gz

# Extract package
print_status "Extracting installation package..."
tar xzf stalwart-manager.tar.gz

# Run installer
print_status "Running installer..."
cd stalwart-manager-1.0.0
bash install.sh

# Cleanup
cd /
rm -rf $TEMP_DIR

print_status "Bootstrap completed!"
