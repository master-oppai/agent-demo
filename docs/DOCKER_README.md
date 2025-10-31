# Docker Setup Guide

This guide explains how to run the NDIS Fraud Detection API using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- `.env` file with your `OPENAI_API_KEY`

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

### 2. Access the API

The API will be available at:
- Health Check: http://localhost:5000/health
- API Root: http://localhost:5000/

### 3. Stop the Container

```bash
# Stop the running container
docker-compose down
```

## Docker Commands

### Build the Image

```bash
docker build -t ndis-fraud-detection-api .
```

### Run the Container

```bash
docker run -p 5000:5000 \
  -e OPENAI_API_KEY="your-api-key" \
  -v $(pwd)/data:/app/data:ro \
  ndis-fraud-detection-api
```

### View Logs

```bash
# View logs from docker-compose
docker-compose logs -f

# View logs from specific container
docker logs -f ndis-fraud-detection-api
```

### Check Health Status

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

## Environment Variables

Configure the following environment variables in your `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key-here
FLASK_ENV=production
PORT=5000
```

## Docker Compose Services

### API Service
- **Container Name**: `ndis-fraud-detection-api`
- **Port**: 5000
- **Health Check**: Enabled (checks every 30s)
- **Restart Policy**: unless-stopped
- **Network**: ndis-network

## Volumes

- `./data:/app/data:ro` - Mounts NIDS CSV data files (read-only)
- `./.env:/app/.env:ro` - Mounts environment variables (read-only)

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs api

# Rebuild without cache
docker-compose build --no-cache
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use port 5001 instead
```

### Health check failing
```bash
# Check if Flask is running
docker exec -it ndis-fraud-detection-api curl http://localhost:5000/health

# View detailed logs
docker-compose logs -f api
```

## Development Mode

To run in development mode with hot-reload:

1. Update `docker-compose.yml`:
```yaml
environment:
  - FLASK_ENV=development
volumes:
  - .:/app  # Mount entire directory
```

2. Run:
```bash
docker-compose up
```

## Production Deployment

For production deployment, consider:

1. Use environment-specific `.env` files
2. Set `FLASK_ENV=production`
3. Configure proper logging
4. Use a reverse proxy (nginx/traefik)
5. Enable HTTPS
6. Set resource limits in docker-compose.yml

Example with resource limits:
```yaml
services:
  api:
    # ...existing config...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Cleaning Up

Remove all containers, images, and volumes:

```bash
# Stop and remove containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker rmi ndis-fraud-detection-api

# Clean up everything (use with caution)
docker system prune -a --volumes
```

