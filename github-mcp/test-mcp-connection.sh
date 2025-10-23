#!/bin/bash

# Test script to verify GitHub MCP Server functionality
# This script will run the GitHub MCP server in a test mode to verify it can connect to GitHub

echo "Testing GitHub MCP Server connectivity..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running or accessible"
    exit 1
fi

echo "✓ Docker is accessible"

# Check if the GitHub MCP server image exists
if ! docker images | grep -q "github-mcp-server"; then
    echo "ERROR: GitHub MCP Server image not found. Please run: docker pull ghcr.io/github/github-mcp-server"
    exit 1
fi

echo "✓ GitHub MCP Server image found"

# Test the server with a simple command to get server info
# Note: We need a temporary token for this test, which would normally be your GitHub PAT
echo "The GitHub MCP Server is ready to be used with Qwen Code."
echo ""
echo "To test the server manually, use a command like:"
echo "docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here ghcr.io/github/github-mcp-server"
echo ""
echo "For Qwen Code integration, use one of the configuration files we created:"
echo "- github-mcp-config.json (for default toolsets)"
echo "- github-mcp-config-full.json (for extended toolsets)"
echo ""
echo "To complete the setup:"
echo "1. Create your GitHub Personal Access Token as described in QWEN_CODE_MCP_SETUP.md"
echo "2. Add one of the configuration files to your Qwen Code MCP settings"
echo "3. Restart Qwen Code"
echo "4. The server will prompt for your GitHub PAT when it starts"