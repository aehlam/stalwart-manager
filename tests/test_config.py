import os
import pytest
from stalwart_manager.config import load_config, validate_config

def test_config_loading():
    """Test basic configuration loading."""
    config = load_config()
    assert config is not None
    assert "server" in config
    assert "smtp" in config["server"]
    assert "imap" in config["server"]

def test_smtp_config():
    """Test SMTP configuration validation."""
    config = load_config()
    assert config["server"]["smtp"]["port"] == 25
    assert config["server"]["smtp"]["submission_port"] == 587
    assert config["server"]["smtp"]["submission_ssl_port"] == 465

def test_imap_config():
    """Test IMAP configuration validation."""
    config = load_config()
    assert config["server"]["imap"]["port"] == 143
    assert config["server"]["imap"]["ssl_port"] == 993

def test_web_interface_config():
    """Test web interface configuration."""
    config = load_config()
    assert config["web"]["port"] == 8000
    assert config["web"]["host"] == "0.0.0.0"

def test_api_config():
    """Test API configuration."""
    config = load_config()
    assert config["api"]["port"] == 8080
    assert config["api"]["host"] == "0.0.0.0"

def test_invalid_config():
    """Test configuration validation with invalid values."""
    with pytest.raises(ValueError):
        validate_config({
            "server": {
                "smtp": {"port": -1}  # Invalid port
            }
        })

def test_missing_required_config():
    """Test configuration validation with missing required fields."""
    with pytest.raises(KeyError):
        validate_config({})  # Empty config

def test_environment_override():
    """Test environment variable configuration override."""
    os.environ["STALWART_SMTP_PORT"] = "2525"
    config = load_config()
    assert config["server"]["smtp"]["port"] == 2525
    del os.environ["STALWART_SMTP_PORT"]
