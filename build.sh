#!/bin/bash

# Build script for Render deployment
# This script handles the installation of dependencies

echo "🔧 Starting build process..."

# Upgrade pip to latest version
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install system dependencies that might be needed
echo "🔧 Installing system dependencies..."
apt-get update -qq && apt-get install -y -qq \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "✅ Build completed successfully!" 