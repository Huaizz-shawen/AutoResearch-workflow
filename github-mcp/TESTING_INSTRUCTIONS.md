# Testing GitHub MCP Server with Qwen Code

Now that you've configured your GitHub token in the configuration files, here's how to test the connection:

## Step 1: Verify Docker is running
```bash
docker info
```

## Step 2: Verify the GitHub MCP Server image is available
```bash
docker images | grep github-mcp-server
```

## Step 3: Configure Qwen Code
1. Open Qwen Code settings
2. Navigate to the MCP Server configuration
3. Use one of these configuration files:
   - `github-mcp/github-mcp-config.json` (for basic toolsets)
   - `github-mcp/github-mcp-config-full.json` (for extended toolsets)

## Step 4: Start Qwen Code with MCP support
1. Enable MCP support in Qwen Code
2. The server should start automatically when Qwen Code requests it
3. When prompted, enter your GitHub token (it will be securely passed to the Docker container)

## Step 5: Test basic functionality
Once connected, try asking Qwen Code to:
- List your repositories: "Show me my GitHub repositories"
- Check issues: "Show open issues in [repository_name]"
- View pull requests: "Show my open pull requests"

## Manual verification (if needed)
If you want to manually verify the server works with your token:
```bash
docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=your_actual_token_here ghcr.io/github/github-mcp-server
```

Note: The server uses stdio protocol, so it will wait for MCP protocol messages.

## Troubleshooting
- If Docker permissions are denied: Add your user to the docker group with `sudo usermod -aG docker $USER`
- If the token doesn't work: Verify the token has the required scopes (repo, read:org, read:packages)
- If Qwen Code doesn't connect: Verify MCP support is enabled in settings

## Security reminder
Never commit your GitHub token to version control or share it publicly.