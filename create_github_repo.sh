#!/bin/bash

# Script to create GitHub repository
# Make sure GH_TOKEN is set in your environment

cd /Users/pqz/Code/peloton-analysis

echo "Creating GitHub repository..."
gh repo create peloton-analysis \
  --public \
  --source=. \
  --remote=origin \
  --description="Extract and analyze Peloton ride data"

if [ $? -eq 0 ]; then
  echo "✓ Repository created successfully!"
  echo "Pushing initial commit..."
  git push -u origin main
  echo "✓ Done! Repository: https://github.com/pqzdev/peloton-analysis"
else
  echo "✗ Failed to create repository. Make sure GH_TOKEN is set:"
  echo "  export GH_TOKEN=your_token_here"
fi
