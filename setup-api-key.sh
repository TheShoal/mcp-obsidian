#!/bin/bash

# Obsidian MCP Server - API Key Setup Script
# Run this after installing the Obsidian Local REST API plugin

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Obsidian MCP Server - API Key Configuration             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Obsidian is running
echo "📋 Step 1: Checking if Obsidian is running..."
if ! pgrep -x "Obsidian" > /dev/null; then
    echo "⚠️  Obsidian is not running!"
    echo "   Please open Obsidian with your vault: ~/pantheon/notes"
    echo "   Then run this script again."
    exit 1
fi
echo "✅ Obsidian is running"
echo ""

# Instructions for getting API key
echo "📋 Step 2: Get your API key from Obsidian"
echo ""
echo "   1. In Obsidian, go to: Settings → Community Plugins → Local REST API"
echo "   2. Find the 'API Key' field"
echo "   3. Copy the API key"
echo ""
echo "   💡 If the plugin isn't installed:"
echo "      - Go to Settings → Community Plugins → Browse"
echo "      - Search for 'Local REST API'"
echo "      - Install and enable it"
echo ""

# Prompt for API key
read -p "🔑 Enter your Obsidian API key: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ No API key provided. Exiting."
    exit 1
fi

# Add to shell config
SHELL_CONFIG="$HOME/.zshrc"
if [ ! -f "$SHELL_CONFIG" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

echo ""
echo "📋 Step 3: Adding API key to shell config"
echo ""

# Check if already exists
if grep -q "OBSIDIAN_API_KEY" "$SHELL_CONFIG" 2>/dev/null; then
    echo "⚠️  OBSIDIAN_API_KEY already exists in $SHELL_CONFIG"
    echo "   Updating the value..."
    sed -i.bak "s/export OBSIDIAN_API_KEY=.*/export OBSIDIAN_API_KEY=\"$API_KEY\"/" "$SHELL_CONFIG"
else
    echo "" >> "$SHELL_CONFIG"
    echo "# Obsidian MCP Server API Key" >> "$SHELL_CONFIG"
    echo "export OBSIDIAN_API_KEY=\"$API_KEY\"" >> "$SHELL_CONFIG"
fi

echo "✅ API key added to $SHELL_CONFIG"
echo ""

# Export for current session
export OBSIDIAN_API_KEY="$API_KEY"
export OBSIDIAN_HOST="127.0.0.1"
export OBSIDIAN_PORT="27124"
export OBSIDIAN_PROTOCOL="http"

echo "📋 Step 4: Testing connection..."
echo ""

# Test the connection
cd ~/pantheon/tools/mcp-obsidian

# Simple test with curl
echo "Testing Obsidian REST API connection..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $API_KEY" \
    "http://127.0.0.1:27124/" 2>/dev/null || echo "000")

if [ "$RESPONSE" = "200" ] || [ "$RESPONSE" = "401" ]; then
    echo "✅ Obsidian REST API is responding (HTTP $RESPONSE)"
    if [ "$RESPONSE" = "401" ]; then
        echo "⚠️  API key may be incorrect. Please verify in Obsidian settings."
    fi
else
    echo "⚠️  Could not connect to Obsidian REST API (HTTP $RESPONSE)"
    echo "   Make sure the Local REST API plugin is enabled in Obsidian"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete! 🎉                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 Next steps:"
echo ""
echo "   1. Reload your shell config:"
echo "      source $SHELL_CONFIG"
echo ""
echo "   2. Restart Hermes gateway:"
echo "      hermes gateway restart"
echo ""
echo "   3. Test the integration:"
echo "      hermes mcp call obsidian list_files_in_vault"
echo ""
echo "📖 For troubleshooting, see:"
echo "   ~/pantheon/tools/mcp-obsidian/SETUP_INSTRUCTIONS.md"
echo ""