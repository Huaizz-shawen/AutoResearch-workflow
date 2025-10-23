# Configuring Qwen Code to Connect to GitHub MCP Server

This document explains how to configure Qwen Code to connect to the GitHub MCP (Model Context Protocol) server.

## Prerequisites

1. Docker installed and running
2. GitHub Personal Access Token (PAT) with appropriate permissions
3. GitHub MCP Server Docker image (already pulled: `ghcr.io/github/github-mcp-server`)

## Configuration Steps

### Step 1: Create GitHub Personal Access Token

Before configuring Qwen Code, you need a GitHub PAT with appropriate scopes:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Add a note like "Qwen Code MCP Server"
4. Select these scopes:
   - `repo` - Repository operations
   - `read:org` - Organization team access
   - `read:packages` - Docker image access
5. Click "Generate token"
6. Copy the token and keep it secure

### Step 2: Qwen Code MCP Configuration

Add the following configuration to your Qwen Code MCP settings:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "github_token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ],
  "servers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}"
      }
    }
  }
}
```

### Step 3: Alternative Configuration with Specific Toolsets

For more control over GitHub API capabilities available to Qwen Code, use this configuration with specific toolsets:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "github_token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ],
  "servers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "-e",
        "GITHUB_TOOLSETS",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}",
        "GITHUB_TOOLSETS": "default,repos,issues,pull_requests,actions,code_security,users"
      }
    }
  }
}
```

### Step 4: Available Toolsets

The GitHub MCP Server supports enabling or disabling specific groups of functionalities:

- `context` - Provides context about the current user and GitHub context
- `repos` - GitHub Repository related tools
- `issues` - GitHub Issues related tools
- `pull_requests` - GitHub Pull Request related tools
- `actions` - GitHub Actions workflows and CI/CD operations
- `code_security` - Code security related tools (GitHub Code Scanning)
- `users` - GitHub User related tools
- `discussions` - GitHub Discussions related tools
- And more (see full list in documentation)

## How It Works

Once configured, Qwen Code will be able to:

- Read repositories and code files
- Manage issues and pull requests
- Analyze code
- Automate workflows
- Monitor GitHub Actions workflow runs
- Access security findings
- And much more through natural language interactions

## Troubleshooting

1. Make sure Docker is running: `sudo systemctl status docker`
2. Verify the GitHub PAT has the correct permissions
3. Check that the Docker image is accessible: `docker images | grep github-mcp-server`
4. Verify that Qwen Code supports MCP servers

## Security Note

Keep your GitHub Personal Access Token secure and never commit it to version control.