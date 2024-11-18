from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import yaml
import requests
from pydantic import BaseModel
from typing import Optional
import docker
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Models
class ServerConfig(BaseModel):
    hostname: str
    domain: str
    admin_email: str

class CloudflareConfig(BaseModel):
    api_token: str
    zone_id: str

class StalwartConfig(BaseModel):
    max_connections: int = 150
    max_message_size: int = 25
    worker_processes: int = 2

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/setup")
async def setup_server(
    hostname: str = Form(...),
    domain: str = Form(...),
    admin_email: str = Form(...),
    cf_api_token: str = Form(...),
    cf_zone_id: str = Form(...)
):
    try:
        # Create Docker Compose file
        create_docker_compose()
        
        # Create Stalwart config
        create_stalwart_config(hostname, domain, admin_email)
        
        # Setup DNS in Cloudflare
        setup_cloudflare_dns(cf_api_token, cf_zone_id, hostname, domain)
        
        # Start services
        client = docker.from_env()
        os.system('docker-compose up -d')
        
        return {"status": "success", "message": "Stalwart Mail Server deployed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_docker_compose():
    compose = {
        'version': '3.8',
        'services': {
            'stalwart-mail': {
                'image': 'stalwartlabs/mail-server:latest',
                'ports': [
                    '25:25',
                    '465:465',
                    '587:587',
                    '143:143',
                    '993:993',
                    '8080:8080'
                ],
                'volumes': [
                    './config:/etc/stalwart',
                    './data:/var/lib/stalwart',
                    './logs:/var/log/stalwart'
                ],
                'environment': ['TZ=UTC'],
                'restart': 'unless-stopped'
            }
        }
    }
    
    os.makedirs('config', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    with open('docker-compose.yml', 'w') as f:
        yaml.dump(compose, f)

def create_stalwart_config(hostname: str, domain: str, admin_email: str):
    config = {
        'server': {
            'hostname': f"{hostname}.{domain}",
            'greeting': f"{hostname}.{domain} ESMTP Stalwart"
        },
        'storage': {
            'data_dir': '/var/lib/stalwart'
        },
        'smtp': {
            'enabled': True,
            'host': '0.0.0.0',
            'port': 25
        },
        'submission': {
            'enabled': True,
            'host': '0.0.0.0',
            'port': 587
        },
        'imap': {
            'enabled': True,
            'host': '0.0.0.0',
            'port': 143
        },
        'api': {
            'enabled': True,
            'host': '0.0.0.0',
            'port': 8080
        },
        'tls': {
            'enabled': True
        }
    }
    
    with open('config/config.toml', 'w') as f:
        yaml.dump(config, f)

def setup_cloudflare_dns(api_token: str, zone_id: str, hostname: str, domain: str):
    import requests
    import json
    
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    # Get the public IP
    ip_address = get_public_ip()
    print(f"Using IP address: {ip_address}")
    
    # Create A record
    dns_record = {
        'name': f"{hostname}.{domain}",  # Use full domain name
        'type': 'A',
        'content': ip_address,
        'proxied': False,
        'ttl': 1,  # Auto TTL
        'comment': 'Created by Stalwart Manager'
    }
    
    print(f"Creating DNS record: {json.dumps(dns_record, indent=2)}")
    
    try:
        # First check if record exists
        existing_records = requests.get(
            f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records',
            headers=headers,
            params={'name': f"{hostname}.{domain}"}
        )
        existing_records.raise_for_status()
        existing_data = existing_records.json()
        
        if existing_data['success']:
            records = existing_data.get('result', [])
            if records:
                # Delete existing record
                record_id = records[0]['id']
                print(f"Deleting existing DNS record with ID: {record_id}")
                delete_response = requests.delete(
                    f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}',
                    headers=headers
                )
                delete_response.raise_for_status()
        
        # Create new record
        response = requests.post(
            f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records',
            headers=headers,
            json=dns_record
        )
        
        # Print full response for debugging
        print(f"Cloudflare API Response: {response.text}")
        
        response.raise_for_status()
        response_data = response.json()
        
        if not response_data['success']:
            error_messages = [error.get('message', 'Unknown error') for error in response_data.get('errors', [])]
            raise Exception(f"Cloudflare API errors: {', '.join(error_messages)}")
            
        print(f"Successfully created DNS record: {hostname}.{domain} -> {ip_address}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Cloudflare API: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Failed to create DNS record: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create DNS record: {str(e)}")

def get_public_ip():
    import urllib.request
    return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')

if __name__ == "__main__":
    print("Starting Stalwart Manager on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
