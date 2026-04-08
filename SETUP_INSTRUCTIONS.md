# Obsidian MCP Server Setup Instructions

## Step 1: Install Obsidian Local REST API Plugin

### In Obsidian Desktop App:

1. **Open Settings**
   - Open your Obsidian vault: `/Users/ricardoroche/pantheon/notes`
   - Go to Settings → Community Plugins

2. **Enable Community Plugins** (if not already enabled)
   - Turn off "Safe Mode" if prompted
   - Click "Turn on community plugins"

3. **Install Local REST API Plugin**
   - Click "Browse" to open the community plugins browser
   - Search for "Local REST API"
   - Find the plugin by "coddingtonbear"
   - Click "Install"
   - Click "Enable" after installation

4. **Get Your API Key**
   - In Settings → Community Plugins → Local REST API
   - You'll see an "API Key" field
   - **Copy this API key** - you'll need it for configuration
   - Note the port (default: 27124)
   - Note the host (default: 127.0.0.1)

5. **Configure API Settings** (Optional)
   - You can change the port if needed
   - Enable/disable HTTPS (default is HTTPS)
   - For local development, HTTP is fine

## Step 2: Configure Environment Variables

### Option A: Add to Hermes Config (Recommended)

The Hermes config will be updated automatically with these variables:
- `OBSIDIAN_API_KEY`: Your API key from the plugin
- `OBSIDIAN_HOST`: 127.0.0.1 (default)
- `OBSIDIAN_PORT`: 27124 (default)
- `OBSIDIAN_PROTOCOL`: http (for local usage)

### Option B: Create .env File

Create a `.env` file in `~/pantheon/tools/mcp-obsidian/`:

```bash
OBSIDIAN_API_KEY=your_api_key_here
OBSIDIAN_HOST=127.0.0.1
OBSIDIAN_PORT=27124
OBSIDIAN_PROTOCOL=http
```

## Step 3: Restart Hermes Gateway

After completing the Obsidian plugin setup:

```bash
hermes gateway restart
```

## Step 4: Test the Integration

Test that the MCP server is working:

```bash
# Test with Hermes
hermes mcp call obsidian list_files_in_vault

# Or use the MCP inspector for debugging
npx @modelcontextprotocol/inspector uv --directory ~/pantheon/tools/mcp-obsidian run mcp-obsidian
```

## Available Tools

Once configured, you'll have access to:

1. **list_files_in_vault** - List all files in vault root
2. **list_files_in_dir** - List files in specific directory
3. **get_file_contents** - Read a note's content
4. **search** - Search vault for text
5. **patch_content** - Insert content relative to heading/block
6. **append_content** - Append to a note
7. **put_content** - Replace entire note content
8. **delete_file** - Delete a file/directory

## Example Usage

```python
# Search for notes about "multi-agent"
result = mcp_obsidian_search(query="multi-agent")

# Read a specific note
content = mcp_obsidian_get_file_contents(path="30_notes/multi-agent-coordination.md")

# Append to a note
mcp_obsidian_append_content(
    path="40_journal/2024-12-19.md",
    content="\n## New Entry\nAdded via MCP server"
)
```

## Troubleshooting

### API Key Not Found
- Make sure the Local REST API plugin is enabled
- Check that you copied the API key correctly
- Verify the .env file is in the correct directory

### Connection Refused
- Check Obsidian is running
- Verify the port matches the plugin settings
- Try HTTP instead of HTTPS for local connections

### Permission Errors
- Make sure Obsidian has file system permissions
- Check that the vault path is accessible

## Security Notes

- **Never commit your API key** to git
- The `.env` file is in `.gitignore` automatically
- For production, use environment variables in Hermes config
- The API key is specific to your local Obsidian instance

## Next Steps

After setup:
1. Test vault access with basic commands
2. Integrate with Discord capture workflow
3. Use for automated note management
4. Enhance vault consistency checks

---

**Status**: ⏳ Waiting for API key from Obsidian plugin
**Repository**: `~/pantheon/tools/mcp-obsidian`
**Config**: Will be added to `~/.hermes/config.yaml`