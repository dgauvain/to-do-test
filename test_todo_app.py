import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from todo_app import (
    load_todos,
    save_todos,
    add_todo,
    list_todos,
    complete_todo,
    delete_todo,
)


def test_load_todos_empty():
    """Test loading todos when file doesn't exist."""
    # Use a temporary file path that doesn't exist
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        todos = load_todos()
        assert todos == []

    # Clean up
    os.unlink(temp_path)


def test_load_todos_invalid_json():
    """Test loading todos when file has invalid JSON."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        f.write("invalid json content")
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        todos = load_todos()
        assert todos == []

    # Clean up
    os.unlink(temp_path)


def test_save_todos():
    """Test saving todos to file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        todos = [{"id": 1, "description": "test todo", "completed": False}]
        result = save_todos(todos)
        assert result is True

        # Verify content was saved correctly
        with open(temp_path, "r") as f:
            saved_content = json.load(f)
            assert saved_content == todos

    # Clean up
    os.unlink(temp_path)


def test_add_todo():
    """Test adding a new todo."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        # Add a todo
        add_todo("Test todo")

        # Verify it was saved
        todos = load_todos()
        assert len(todos) == 1
        assert todos[0]["description"] == "Test todo"
        assert todos[0]["completed"] is False
        assert todos[0]["id"] == 1

    # Clean up
    os.unlink(temp_path)


def test_list_todos_empty():
    """Test listing todos when none exist."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        # Capture print output
        with patch("sys.stdout") as mock_stdout:
            list_todos()
            # Should have printed "No todos found."
            # Note: print() adds a newline, so we expect two calls
            assert mock_stdout.write.call_count == 2
            calls = mock_stdout.write.call_args_list
            assert calls[0][0][0] == "No todos found."
            assert calls[1][0][0] == "\n"

    # Clean up
    os.unlink(temp_path)


def test_complete_todo():
    """Test completing a todo."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        # Add a todo first
        add_todo("Test todo")

        # Complete it
        complete_todo(1)

        # Verify it was completed
        todos = load_todos()
        assert len(todos) == 1
        assert todos[0]["completed"] is True

    # Clean up
    os.unlink(temp_path)


def test_complete_todo_not_found():
    """Test completing a non-existent todo."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        # Try to complete a non-existent todo
        with patch("sys.stdout") as mock_stdout:
            complete_todo(999)
            # Should have printed "Todo 999 not found"
            # Note: print() adds a newline, so we expect two calls
            assert mock_stdout.write.call_count == 2
            calls = mock_stdout.write.call_args_list
            assert calls[0][0][0] == "Todo 999 not found"
            assert calls[1][0][0] == "\n"

    # Clean up
    os.unlink(temp_path)


def test_delete_todo():
    """Test deleting a todo."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        # Add a todo first
        add_todo("Test todo")

        # Delete it
        delete_todo(1)

        # Verify it was deleted
        todos = load_todos()
        assert len(todos) == 0

    # Clean up
    os.unlink(temp_path)


def test_delete_todo_not_found():
    """Test deleting a non-existent todo."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_path = f.name

    # Mock the TODO_FILE to point to our temp file
    with patch("todo_app.TODO_FILE", Path(temp_path)):
        # Try to delete a non-existent todo
        with patch("sys.stdout") as mock_stdout:
            delete_todo(999)
            # Should have printed "Todo not found"
            # Note: print() adds a newline, so we expect two calls
            assert mock_stdout.write.call_count == 2
            calls = mock_stdout.write.call_args_list
            assert calls[0][0][0] == "Todo not found"
            assert calls[1][0][0] == "\n"

    # Clean up
    os.unlink(temp_path)
