import os
import pytest
import subprocess
from pathlib import Path

def test_installation_script_exists():
    """Test that installation script exists and is executable."""
    install_script = Path("install.sh")
    assert install_script.exists()
    assert os.access(install_script, os.X_OK)

def test_bootstrap_script_exists():
    """Test that bootstrap script exists and is executable."""
    bootstrap_script = Path("bootstrap.sh")
    assert bootstrap_script.exists()
    assert os.access(bootstrap_script, os.X_OK)

@pytest.mark.skipif(os.getuid() != 0, reason="requires root")
def test_installation_dry_run():
    """Test installation script in dry-run mode."""
    result = subprocess.run(
        ["./install.sh", "--dry-run"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Dry run completed" in result.stdout

def test_docker_compose_file():
    """Test that docker-compose.yml is valid."""
    compose_file = Path("docker-compose.yml")
    assert compose_file.exists()
    result = subprocess.run(
        ["docker-compose", "config"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_systemd_service_file():
    """Test that systemd service file is present and valid."""
    service_file = Path("stalwart-manager.service")
    assert service_file.exists()
    with open(service_file) as f:
        content = f.read()
        assert "[Unit]" in content
        assert "[Service]" in content
        assert "[Install]" in content

@pytest.mark.skipif(os.getuid() != 0, reason="requires root")
def test_firewall_configuration():
    """Test firewall configuration in dry-run mode."""
    ports = [25, 465, 587, 143, 993, 8080, 8000]
    for port in ports:
        result = subprocess.run(
            ["ufw", "status", "numbered"],
            capture_output=True,
            text=True
        )
        assert str(port) in result.stdout

def test_python_dependencies():
    """Test that all required Python packages are listed."""
    requirements = Path("requirements.txt")
    assert requirements.exists()
    with open(requirements) as f:
        deps = f.read().splitlines()
        assert "fastapi" in deps
        assert "uvicorn" in deps
        assert "docker-compose" in deps
