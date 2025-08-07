# Docker Deployment - Houdinis Framework

This directory contains Docker containerization infrastructure for the Houdinis Framework, providing enterprise-grade deployment capabilities.

## Docker Environment Overview

The Houdinis Framework Docker environment is built on Rocky Linux 9 Enterprise, providing a secure and stable foundation for quantum cryptography testing operations.

### Container Architecture
- **Base Image**: Rocky Linux 9 (Enterprise Linux)
- **Python Runtime**: Python 3.9+
- **Security**: Non-root user execution
- **Performance**: Multi-stage build optimization
- **Scalability**: Docker Compose orchestration

## Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Minimum 4GB RAM
- 10GB available disk space

### Basic Deployment
```bash
# Setup and build
./setup-docker.sh

# Run container
./docker.sh run

# Execute tests
./docker.sh test
```

## Available Scripts

### Primary Scripts
- **setup-docker.sh** - Initial environment setup and image build
- **docker.sh** - Quick access wrapper for common operations
- **docker-manager.sh** - Comprehensive container management
- **run-docker.sh** - Container execution with various modes

### Utility Scripts
- **build-docker.sh** - Image building and optimization
- **install-docker.sh** - Docker installation automation
- **demo-docker.sh** - Demonstration environment

## Container Management

### Image Operations
```bash
# Build enterprise image
./setup-docker.sh

# Build with custom tag
docker build -t houdinis-framework:custom .

# List images
docker images houdinis-framework
```

### Container Operations
```bash
# Run interactive session
./docker.sh shell

# Run background service
./docker.sh daemon

# Execute specific command
./docker.sh exec "python3 main.py"

# View logs
./docker.sh logs
```

### Environment Management
```bash
# Start development environment
docker-compose up -d development

# Start production environment
docker-compose up -d production

# Scale services
docker-compose up --scale houdinis=3
```

## Configuration

### Environment Variables
```bash
# Framework configuration
HOUDINIS_VERSION=2.0.0
HOUDINIS_LOG_LEVEL=INFO
HOUDINIS_DATA_DIR=/opt/houdinis/data

# Quantum backend configuration
IBM_QUANTUM_TOKEN=your_token_here
AWS_ACCESS_KEY_ID=your_key_here
AZURE_SUBSCRIPTION_ID=your_subscription_here
```

### Volume Mounts
```bash
# Data persistence
-v ./data:/opt/houdinis/data

# Configuration files
-v ./configs:/opt/houdinis/configs

# Results and reports
-v ./reports:/opt/houdinis/reports
```

## Security Considerations

### Container Security
- Non-privileged user execution
- Read-only root filesystem
- Resource limitations
- Network isolation
- Secrets management via Docker secrets

### Network Security
```bash
# Internal network only
docker network create houdinis-internal

# Expose specific ports only
-p 127.0.0.1:8080:8080
```

## Production Deployment

### Resource Requirements
- **Minimum**: 2 CPU, 4GB RAM, 20GB storage
- **Recommended**: 4 CPU, 8GB RAM, 50GB storage
- **High Performance**: 8+ CPU, 16GB+ RAM, 100GB+ storage

### Health Monitoring
```bash
# Container health check
docker exec houdinis-container python3 tests/test_houdinis.py

# Resource monitoring
docker stats houdinis-container

# Log monitoring
docker logs -f houdinis-container
```

### Backup and Recovery
```bash
# Export container state
docker export houdinis-container > houdinis-backup.tar

# Backup data volumes
docker run --rm -v houdinis_data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz /data
```

## Integration

### CI/CD Pipeline Integration
```yaml
# GitHub Actions example
- name: Build Docker Image
  run: ./docker/setup-docker.sh

- name: Run Tests
  run: ./docker/docker.sh test

- name: Security Scan
  run: docker scan houdinis-framework:latest
```

### Kubernetes Deployment
```yaml
# Basic deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: houdinis-framework
spec:
  replicas: 3
  selector:
    matchLabels:
      app: houdinis
  template:
    metadata:
      labels:
        app: houdinis
    spec:
      containers:
      - name: houdinis
        image: houdinis-framework:latest
        resources:
          limits:
            memory: "8Gi"
            cpu: "4"
          requests:
            memory: "4Gi"
            cpu: "2"
```

## Troubleshooting

### Common Issues

**Build Failures**
```bash
# Clean build cache
docker builder prune -f

# Build with no cache
docker build --no-cache -t houdinis-framework .
```

**Permission Issues**
```bash
# Fix volume permissions
sudo chown -R $(id -u):$(id -g) ./data
```

**Resource Constraints**
```bash
# Increase Docker memory limit
# Docker Desktop: Settings > Resources > Memory

# Check system resources
docker system df
docker system prune
```

### Debug Mode
```bash
# Debug container
./docker.sh debug

# Interactive troubleshooting
docker run -it --entrypoint /bin/bash houdinis-framework:latest
```

## Support

For technical support and advanced configuration:
- Review container logs: `./docker.sh logs`
- Check system requirements in main documentation
- Verify Docker installation: `docker --version`
- Test basic functionality: `./docker.sh test`

## Enterprise Features

### High Availability
- Load balancing with multiple container instances
- Health checks and automatic restart
- Data replication across nodes

### Monitoring Integration
- Prometheus metrics collection
- Grafana dashboard integration
- Log aggregation with ELK stack

### Security Compliance
- CIS Docker Benchmark compliance
- Vulnerability scanning integration
- Audit logging capabilities
