# Deployment Guide — DoIt Admin API

## Prerequisites

- Python 3.11+
- Redis server running and accessible
- Systemd (for socket activation)

## 1. Set up the application

```bash
# Copy the admin_api directory to /opt
sudo cp -r admin_api /opt/admin_api

# Create a virtual environment and install dependencies
cd /opt/admin_api
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set a strong ADMIN_TOKEN, REDIS_URL, and REDIS_PREFIX
nano .env
```

## 3. Install systemd units

```bash
sudo cp deploy/admin-api.socket /etc/systemd/system/
sudo cp deploy/admin-api.service /etc/systemd/system/
sudo systemctl daemon-reload
```

## 4. Enable and start

Socket activation starts the service on first request and stops it after idle
timeout (zero memory when idle).

```bash
sudo systemctl enable --now admin-api.socket
```

Verify:

```bash
# Should return {"status":"ok"} with correct Admin-Token
curl -H "Admin-Token: YOUR_TOKEN" http://127.0.0.1:8000/health
```

## 5. Managing the service

```bash
# Check status
systemctl status admin-api.socket admin-api.service

# View logs
journalctl -u admin-api.service -f

# Restart after config changes
sudo systemctl restart admin-api.service
```
