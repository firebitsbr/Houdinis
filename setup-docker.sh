#!/bin/bash
# Houdinis Framework - Quick Setup Access
# Corporate wrapper script for Docker setup operations
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT

# Navigate to docker directory and execute setup
cd "$(dirname "$0")/docker" && ./setup-docker.sh "$@"
