"""Shared test fixtures for mcp-obsidian."""

import os
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("OBSIDIAN_API_KEY", "test_api_key_123")
    monkeypatch.setenv("OBSIDIAN_HOST", "127.0.0.1")
    return {
        "OBSIDIAN_API_KEY": "test_api_key_123",
        "OBSIDIAN_HOST": "127.0.0.1",
    }


@pytest.fixture
def mock_obsidian_api():
    """Mock Obsidian API client."""
    api = MagicMock()

    # Mock list_files_in_vault
    api.list_files_in_vault = MagicMock(
        return_value={
            "files": ["note1.md", "note2.md", "folder/"],
            "folders": ["folder", "another_folder"],
        }
    )

    # Mock list_files_in_dir
    api.list_files_in_dir = MagicMock(
        return_value={"files": ["nested_note.md"], "folders": []}
    )

    # Mock get_file_contents
    api.get_file_contents = MagicMock(
        return_value="# Test Note\n\nThis is test content.\n\n[[Link]]"
    )

    # Mock search
    api.search = MagicMock(
        return_value=[
            {"filename": "note1.md", "score": 0.95},
            {"filename": "note2.md", "score": 0.85},
        ]
    )

    # Mock patch_content
    api.patch_content = MagicMock(return_value={"success": True})

    # Mock append_content
    api.append_content = MagicMock(return_value={"success": True})

    # Mock put_content
    api.put_content = MagicMock(return_value={"success": True})

    # Mock delete_file
    api.delete_file = MagicMock(return_value={"success": True})

    return api


@pytest.fixture
def mock_obsidian_api_error():
    """Mock Obsidian API that returns errors."""
    api = MagicMock()

    api.list_files_in_vault = MagicMock(side_effect=Exception("API Error"))
    api.get_file_contents = MagicMock(side_effect=Exception("File not found"))
    api.search = MagicMock(side_effect=Exception("Search failed"))

    return api


@pytest.fixture
async def mcp_server(mock_env):
    """Create a test MCP server instance."""
    # Mock the Obsidian class to avoid real API calls
    with patch("mcp_obsidian.tools.obsidian.Obsidian"):
        from mcp_obsidian.server import app

        return app


@pytest.fixture
def sample_file_list() -> Dict[str, List[str]]:
    """Sample file listing data."""
    return {
        "files": [
            "daily/2024-01-01.md",
            "notes/test-note.md",
            "projects/project-a.md",
        ],
        "folders": ["daily", "notes", "projects"],
    }


@pytest.fixture
def sample_note_content() -> str:
    """Sample note content."""
    return """# Test Note

This is a test note with some content.

## Section 1

Some text here.

## Section 2

More content with [[wikilinks]] and #tags.

Links: https://example.com
"""


@pytest.fixture
def sample_search_results() -> List[Dict[str, Any]]:
    """Sample search results."""
    return [
        {"filename": "note1.md", "score": 0.95, "preview": "This matches the search"},
        {"filename": "note2.md", "score": 0.85, "preview": "Another match here"},
        {"filename": "note3.md", "score": 0.75, "preview": "Third result"},
    ]
