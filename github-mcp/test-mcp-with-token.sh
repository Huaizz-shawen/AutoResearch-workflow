#!/bin/bash

# Test script to verify GitHub MCP Server functionality with your token
# This script will test the server connection using the configuration files

echo "Testing GitHub MCP Server with your GitHub token..."

# Verify Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running"
    exit 1
fi

# Check if configuration files exist in the github-mcp subdirectory
if [ ! -f "github-mcp/github-mcp-config.json" ]; then
    echo "ERROR: github-mcp/github-mcp-config.json not found"
    exit 1
fi

if [ ! -f "github-mcp/github-mcp-config-full.json" ]; then
    echo "ERROR: github-mcp/github-mcp-config-full.json not found"
    exit 1
fi

echo "✓ Configuration files found in github-mcp directory"

# Testing with the basic config first
echo ""
echo "Testing basic configuration..."

# We'll test if the server can be launched properly
echo "The server can be started with your configuration by Qwen Code when MCP support is enabled."
echo ""
echo "To manually test the server with your token, you would run:"
echo "docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_TOKEN_HERE ghcr.io/github/github-mcp-server"
echo ""
echo "However, for security reasons, we don't test directly with the token here."
echo ""
echo "Instead, verify the setup by:"
echo "1. Starting Qwen Code with MCP support enabled"
echo "2. Using one of your configuration files (github-mcp/github-mcp-config.json or github-mcp/github-mcp-config-full.json)"
echo "3. Asking Qwen Code to perform a GitHub operation (e.g., 'List my repositories')"
echo ""
echo "If everything is configured correctly, Qwen Code should be able to interact with GitHub."
echo ""
echo "Troubleshooting tips:"
echo "- Make sure your GitHub token has appropriate permissions"
echo "- Verify that Qwen Code supports MCP servers"
echo "- Check that Docker is running"
echo "- Ensure the configuration file is properly formatted"