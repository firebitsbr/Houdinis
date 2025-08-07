#!/bin/bash
# Houdinis Framework - Script to build the Houdinis framework Docker image
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT

# Houdinis Framework Docker Build Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="houdinis-framework"
IMAGE_TAG="latest"
DOCKERFILE_PATH="./Dockerfile"
BUILD_CONTEXT="../"  # Context at project root

echo -e "${BLUE} Houdinis Framework Docker Build Script${NC}"
echo -e "${BLUE}===========================================${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED} Docker is not installed or not in PATH${NC}"
    echo -e "${YELLOW} Install Docker using: dnf install -y docker${NC}"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED} Docker is not running${NC}"
    echo -e "${YELLOW} Start Docker using: sudo systemctl start docker${NC}"
    exit 1
fi

echo -e "${GREEN} Docker is available${NC}"

# Check if Dockerfile exists
if [ ! -f "$DOCKERFILE_PATH" ]; then
    echo -e "${RED} Dockerfile not found at $DOCKERFILE_PATH${NC}"
    exit 1
fi

echo -e "${GREEN} Dockerfile found${NC}"

# Clean old images (optional)
echo -e "${YELLOW}[CLEAN] Cleaning old Docker images...${NC}"
docker image prune -f || true

# Build the image
echo -e "${BLUE}[BUILD] Building Docker image...${NC}"
echo -e "${YELLOW} Image: ${IMAGE_NAME}:${IMAGE_TAG}${NC}"

docker build \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    -f "$DOCKERFILE_PATH" \
    "$BUILD_CONTEXT" \
    --no-cache \
    --progress=plain

if [ $? -eq 0 ]; then
    echo -e "${GREEN} Docker image built successfully!${NC}"
    
    # Show image information
    echo -e "${BLUE} Image information:${NC}"
    docker images "${IMAGE_NAME}:${IMAGE_TAG}"
    
    # Create additional tags
    echo -e "${YELLOW}[TAG]  Creating additional tags...${NC}"
    docker tag "${IMAGE_NAME}:${IMAGE_TAG}" "${IMAGE_NAME}:v1.0.0"
    docker tag "${IMAGE_NAME}:${IMAGE_TAG}" "${IMAGE_NAME}:rocky9"
    
    echo -e "${GREEN} Build completed!${NC}"
    echo -e "${BLUE} To run the container, use:${NC}"
    echo -e "${YELLOW}   docker run -it ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
    echo -e "${YELLOW}   or run: ./run-docker.sh${NC}"
else
    echo -e "${RED} Docker image build failed${NC}"
    exit 1
fi
