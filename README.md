# Todo App

A simple todo application with both CLI and GUI interfaces, using JSON persistence.

## Features

- Add new todos
- List all todos
- Complete todos
- Delete todos
- JSON persistence for todos data
- Graphical user interface (GUI) via tkinter

## Installation

1. Make sure you have Python 3 installed
2. Save the `todo_app.py` and `todo_gui.py` files to your system

## Usage

### Command Line Interface (CLI)

```bash
python todo_app.py [command] [arguments]
```

#### Commands

- `add "description"` - Add a new todo
- `list` - List all todos
- `complete ID` - Mark a todo as completed
- `delete ID` - Delete a todo

### Graphical User Interface (GUI)

```bash
python todo_gui.py
```

The GUI provides a visual interface for managing your todos with:
- Add new todos via the input field
- View all todos in a table format
- Complete or delete todos by selecting an action and entering the ID

## Examples

### CLI Usage

Add a todo:
```bash
python todo_app.py add "Buy groceries"
```

List all todos:
```bash
python todo_app.py list
```

Complete a todo (e.g., todo with ID 1):
```bash
python todo_app.py complete 1
```

Delete a todo (e.g., todo with ID 1):
```bash
python todo_app.py delete 1
```

## Testing

Run tests with pytest:
```bash
pytest test_todo_app.py -v
```