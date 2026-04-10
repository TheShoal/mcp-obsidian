"""Tests for mcp-obsidian tools."""

import pytest
from unittest.mock import patch, MagicMock
from mcp.types import TextContent


class TestListFilesInVault:
    """Test list_files_in_vault tool."""

    async def test_list_files_success(self, mock_env, mock_obsidian_api):
        """Should list files in vault."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import ListFilesInVaultToolHandler

            handler = ListFilesInVaultToolHandler()
            result = handler.run_tool({})

            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], TextContent)
            assert "note1.md" in result[0].text or "note2.md" in result[0].text

    async def test_list_files_api_error(self, mock_env, mock_obsidian_api_error):
        """Should handle API errors."""
        with patch(
            "mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api_error
        ):
            from mcp_obsidian.tools import ListFilesInVaultToolHandler

            handler = ListFilesInVaultToolHandler()

            with pytest.raises(Exception):
                handler.run_tool({})


class TestListFilesInDir:
    """Test list_files_in_dir tool."""

    async def test_list_files_in_dir_success(self, mock_env, mock_obsidian_api):
        """Should list files in specific directory."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import ListFilesInDirToolHandler

            handler = ListFilesInDirToolHandler()
            result = handler.run_tool({"dirpath": "folder"})

            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], TextContent)
            mock_obsidian_api.list_files_in_dir.assert_called_once_with("folder")

    async def test_list_files_in_dir_missing_arg(self, mock_env, mock_obsidian_api):
        """Should raise error when dirpath missing."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import ListFilesInDirToolHandler

            handler = ListFilesInDirToolHandler()

            with pytest.raises(RuntimeError, match="dirpath"):
                handler.run_tool({})


class TestGetFileContents:
    """Test get_file_contents tool."""

    async def test_get_file_contents_success(self, mock_env, mock_obsidian_api):
        """Should get file contents."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import GetFileContentsToolHandler

            handler = GetFileContentsToolHandler()
            result = handler.run_tool({"filepath": "note1.md"})

            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], TextContent)
            assert "Test Note" in result[0].text or "test content" in result[0].text
            mock_obsidian_api.get_file_contents.assert_called_once_with("note1.md")

    async def test_get_file_contents_not_found(self, mock_env, mock_obsidian_api_error):
        """Should handle file not found."""
        with patch(
            "mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api_error
        ):
            from mcp_obsidian.tools import GetFileContentsToolHandler

            handler = GetFileContentsToolHandler()

            with pytest.raises(Exception):
                handler.run_tool({"filepath": "nonexistent.md"})


class TestSearchTool:
    """Test search tool."""

    async def test_search_success(self, mock_env, mock_obsidian_api):
        """Should search vault content."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import SearchToolHandler

            handler = SearchToolHandler()
            result = handler.run_tool({"query": "test query"})

            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], TextContent)
            mock_obsidian_api.search.assert_called_once()

    async def test_search_with_empty_query(self, mock_env, mock_obsidian_api):
        """Should handle empty query."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import SearchToolHandler

            handler = SearchToolHandler()
            # Tool should still work with empty query
            result = handler.run_tool({"query": ""})

            assert isinstance(result, list)


class TestPatchContent:
    """Test patch_content tool."""

    async def test_patch_content_success(self, mock_env, mock_obsidian_api):
        """Should patch file content."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import PatchContentToolHandler

            handler = PatchContentToolHandler()
            result = handler.run_tool(
                {"filepath": "note.md", "content": "updated content", "heading": "Section 1"}
            )

            assert isinstance(result, list)
            mock_obsidian_api.patch_content.assert_called_once()


class TestAppendContent:
    """Test append_content tool."""

    async def test_append_content_success(self, mock_env, mock_obsidian_api):
        """Should append content to file."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import AppendContentToolHandler

            handler = AppendContentToolHandler()
            result = handler.run_tool(
                {"filepath": "note.md", "content": "appended content"}
            )

            assert isinstance(result, list)
            mock_obsidian_api.append_content.assert_called_once()


class TestPutContent:
    """Test put_content tool."""

    async def test_put_content_success(self, mock_env, mock_obsidian_api):
        """Should create or update file content."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import PutContentToolHandler

            handler = PutContentToolHandler()
            result = handler.run_tool(
                {"filepath": "new_note.md", "content": "# New Note\n\nContent"}
            )

            assert isinstance(result, list)
            mock_obsidian_api.put_content.assert_called_once()


class TestDeleteFile:
    """Test delete_file tool."""

    async def test_delete_file_success(self, mock_env, mock_obsidian_api):
        """Should delete file."""
        with patch("mcp_obsidian.tools.obsidian.Obsidian", return_value=mock_obsidian_api):
            from mcp_obsidian.tools import DeleteFileToolHandler

            handler = DeleteFileToolHandler()
            result = handler.run_tool({"filepath": "old_note.md"})

            assert isinstance(result, list)
            mock_obsidian_api.delete_file.assert_called_once_with("old_note.md")


class TestComplexSearch:
    """Test complex_search tool."""

    async def test_complex_search_registered(self, mock_env):
        """Should have complex search handler registered."""
        from mcp_obsidian.tools import ComplexSearchToolHandler

        handler = ComplexSearchToolHandler()
        tool_desc = handler.get_tool_description()

        assert tool_desc.name == "complex_search"
        assert "search" in tool_desc.description.lower()


class TestBatchGetFileContents:
    """Test batch_get_file_contents tool."""

    async def test_batch_get_registered(self, mock_env):
        """Should have batch get handler registered."""
        from mcp_obsidian.tools import BatchGetFileContentsToolHandler

        handler = BatchGetFileContentsToolHandler()
        tool_desc = handler.get_tool_description()

        assert tool_desc.name == "batch_get_file_contents"
        assert "batch" in tool_desc.description.lower()


class TestPeriodicNotes:
    """Test periodic_notes tool."""

    async def test_periodic_notes_registered(self, mock_env):
        """Should have periodic notes handler registered."""
        from mcp_obsidian.tools import PeriodicNotesToolHandler

        handler = PeriodicNotesToolHandler()
        tool_desc = handler.get_tool_description()

        assert tool_desc.name == "periodic_notes"
        assert "periodic" in tool_desc.description.lower()


class TestRecentPeriodicNotes:
    """Test recent_periodic_notes tool."""

    async def test_recent_periodic_notes_registered(self, mock_env):
        """Should have recent periodic notes handler registered."""
        from mcp_obsidian.tools import RecentPeriodicNotesToolHandler

        handler = RecentPeriodicNotesToolHandler()
        tool_desc = handler.get_tool_description()

        assert tool_desc.name == "recent_periodic_notes"


class TestRecentChanges:
    """Test recent_changes tool."""

    async def test_recent_changes_registered(self, mock_env):
        """Should have recent changes handler registered."""
        from mcp_obsidian.tools import RecentChangesToolHandler

        handler = RecentChangesToolHandler()
        tool_desc = handler.get_tool_description()

        assert tool_desc.name == "recent_changes"
        assert "recent" in tool_desc.description.lower()
