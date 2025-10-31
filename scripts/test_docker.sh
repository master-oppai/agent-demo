#!/bin/bash
# Test script for Docker setup

echo "======================================"
echo "NDIS Fraud Detection API - Docker Test"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi
echo "✓ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    exit 1
fi
echo "✓ Docker Compose is installed"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Creating example .env file..."
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    echo "FLASK_ENV=production" >> .env
    echo "PORT=5000" >> .env
    echo "   Please update .env with your actual API key"
fi

echo ""
echo "======================================"
echo "Building Docker Image..."
echo "======================================"
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi
echo "✓ Docker image built successfully"

echo ""
echo "======================================"
echo "Starting Container..."
echo "======================================"
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start container"
    exit 1
fi
echo "✓ Container started successfully"

echo ""
echo "Waiting for service to be ready..."
sleep 5

echo ""
echo "======================================"
echo "Testing Health Endpoint..."
echo "======================================"
HEALTH_RESPONSE=$(curl -s http://localhost:5000/health)
echo "Response: $HEALTH_RESPONSE"

if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
    echo "✓ Health check passed"
else
    echo "❌ Health check failed"
    docker-compose logs api
    docker-compose down
    exit 1
fi

echo ""
echo "======================================"
echo "Testing Root Endpoint..."
echo "======================================"
ROOT_RESPONSE=$(curl -s http://localhost:5000/)
echo "Response: $ROOT_RESPONSE"

if echo "$ROOT_RESPONSE" | grep -q "healthy"; then
    echo "✓ Root endpoint passed"
else
    echo "❌ Root endpoint failed"
fi

echo ""
echo "======================================"
echo "Container Status"
echo "======================================"
docker-compose ps

echo ""
echo "======================================"
echo "All tests completed!"
echo "======================================"
echo ""
echo "To stop the container, run:"
echo "  docker-compose down"
echo ""
echo "To view logs, run:"
echo "  docker-compose logs -f api"
echo ""

