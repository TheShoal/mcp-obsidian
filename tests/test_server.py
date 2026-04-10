"""Tests for mcp-obsidian server instantiation and metadata."""

import pytest


class TestServerInstantiation:
    """Test server creates and initializes correctly."""

    async def test_server_creates_without_error(self, mcp_server):
        """Server instance should be created without errors."""
        assert mcp_server is not None
        assert hasattr(mcp_server, "name")

    async def test_server_has_correct_name(self, mcp_server):
        """Server should have the correct name."""
        assert mcp_server.name == "mcp-obsidian"

    async def test_server_has_list_tools_handler(self, mcp_server):
        """Server should have list_tools handler registered."""
        assert hasattr(mcp_server, "list_tools")

    async def test_server_has_call_tool_handler(self, mcp_server):
        """Server should have call_tool handler registered."""
        assert hasattr(mcp_server, "call_tool")


class TestServerConfiguration:
    """Test server configuration and environment."""

    async def test_api_key_required(self, monkeypatch):
        """Server should require OBSIDIAN_API_KEY."""
        monkeypatch.delenv("OBSIDIAN_API_KEY", raising=False)

        with pytest.raises(ValueError, match="OBSIDIAN_API_KEY"):
            # Re-import to trigger the check
            import importlib
            import mcp_obsidian.server

            importlib.reload(mcp_obsidian.server)

    async def test_api_key_loaded(self, mock_env):
        """Server should load API key from environment."""
        from mcp_obsidian.tools import api_key

        assert api_key == "test_api_key_123"


class TestToolHandlers:
    """Test tool handler registration."""

    async def test_list_tools_returns_tools(self, mcp_server):
        """list_tools should return available tools."""
        from mcp_obsidian.server import list_tools

        tools = await list_tools()

        assert isinstance(tools, list)
        assert len(tools) > 0
        # Check that tools have required fields
        for tool in tools:
            assert hasattr(tool, "name")
            assert hasattr(tool, "description")

    async def test_expected_tools_registered(self, mcp_server):
        """Server should have expected tools registered."""
        from mcp_obsidian.server import list_tools

        tools = await list_tools()
        tool_names = [tool.name for tool in tools]

        # Check for key tools
        expected_tools = [
            "list_files_in_vault",
            "list_files_in_dir",
            "get_file_contents",
            "search",
        ]

        for expected_tool in expected_tools:
            assert expected_tool in tool_names, f"Expected tool {expected_tool} not found"
