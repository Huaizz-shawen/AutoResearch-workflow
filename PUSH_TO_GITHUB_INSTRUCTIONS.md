# Instructions to Upload Repository to GitHub

You need to manually create a private repository on GitHub and push the files. Here's how to do it:

## Step 1: Prepare Your GitHub Personal Access Token
You already have a GitHub Personal Access Token from setting up the MCP server. Make sure it has the `repo` scope.

## Step 2: Create a Private Repository on GitHub
1. Go to https://github.com/new
2. Enter a repository name (e.g., "AutoResearch-workflow")
3. Select "Private" visibility
4. Do NOT initialize with a README, .gitignore, or license
5. Click "Create repository"

## Step 3: Copy the Repository URL
After creating the repository, you'll see a quick setup page. Copy the URL in this format:
`https://github.com/your-username/your-repository-name.git`

## Step 4: Add the Remote Origin and Push
Run these commands in your terminal:

```bash
cd /media/user/B29202FA9202C2B91/AutoReaserch-workflow

# Add the remote origin
git remote add origin YOUR_REPOSITORY_URL

# Push the repository
git branch -M main
git push -u origin main
```

## Alternative Method Using Personal Access Token
If you get authentication errors, you might need to use your token:

```bash
git remote add origin https://your-username:your-token@github.com/your-username/your-repository-name.git
git branch -M main
git push -u origin main
```

## Verification
After pushing, you can verify by:
1. Visiting your GitHub repository page to see the files
2. Checking that the sensitive token files are not included due to .gitignore

## Important Notes
- The following files containing actual tokens will NOT be pushed due to .gitignore:
  - github-mcp/github-mcp-config.json
  - github-mcp/github-mcp-config-full.json
- The following template files (without tokens) WILL be pushed:
  - github-mcp/github-mcp-config-template.json
  - github-mcp/github-mcp-config-full-template.json
- This keeps your tokens secure while still sharing the configuration templates