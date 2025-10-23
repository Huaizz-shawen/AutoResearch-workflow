#!/bin/bash

# Script to create a private repository on GitHub and push the local repository
# You'll need your GitHub Personal Access Token for this process

echo "This script will help you create a private repository on GitHub and push your local files."
echo ""
echo "Before proceeding, please ensure you have a GitHub Personal Access Token with repo scope."
echo "If you don't have one, create it at: https://github.com/settings/tokens"
echo ""

read -p "Enter your GitHub Personal Access Token: " -s token
echo
read -p "Enter the name for your new private repository: " repo_name

# Create the private repository using GitHub API
echo "Creating private repository '$repo_name' on GitHub..."

response=$(curl -s -o response.json -w "%{http_code}" -X POST \
  -H "Authorization: token $token" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$repo_name\",\"private\":true,\"auto_init\":false}")

if [ $response -eq 201 ]; then
    echo "✓ Repository '$repo_name' created successfully!"
    
    # Get the repository URL
    repo_url=$(grep -o '"clone_url": "[^"]*"' response.json | cut -d'"' -f4)
    echo "Repository URL: $repo_url"
    
    # Add the remote origin
    echo "Adding remote origin..."
    git remote add origin $repo_url
    
    # Push the repository
    echo "Pushing repository to GitHub..."
    git push -u origin master
    
    if [ $? -eq 0 ]; then
        echo "✓ Repository pushed successfully!"
        echo "Your private repository is now available at: $repo_url"
    else
        echo "✗ Failed to push repository. Please check the error above."
    fi
else
    echo "✗ Failed to create repository. HTTP response code: $response"
    cat response.json
    echo
fi

# Clean up
rm -f response.json