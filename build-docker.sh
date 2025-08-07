#!/bin/bash
# Houdinis Framework - Corporate banner utility for Houdinis framework.
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT
# Houdinis Framework - Quick Build Access
# Corporate wrapper script for Docker build operations

# Navigate to docker directory and execute build
cd "$(dirname "$0")/docker" && ./build-docker.sh "$@"
