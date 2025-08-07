#!/bin/bash
# Houdinis Framework - Quick Docker Access
# Corporate wrapper script for Docker operations

# Navigate to docker directory and execute
cd "$(dirname "$0")/docker" && ./docker.sh "$@"
