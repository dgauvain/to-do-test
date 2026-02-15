#!/usr/bin/env python3
"""
A simple GUI todo application using tkinter.
Extends the CLI todo app with a graphical interface.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from todo_app import load_todos, save_todos, add_todo, complete_todo, delete_todo


class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo App")
        self.root.geometry("500x400")

        # Load existing todos
        self.todos = load_todos()

        # Create main frame
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Add todo section
        ttk.Label(self.frame, text="Add New Todo:").grid(row=0, column=0, sticky=tk.W)

        self.description_var = tk.StringVar()
        self.entry_add = ttk.Entry(
            self.frame, textvariable=self.description_var, width=40
        )
        self.entry_add.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        self.btn_add = ttk.Button(self.frame, text="Add", command=self.add_todo)
        self.btn_add.grid(row=1, column=1, padx=5, pady=5)

        # Todo list
        ttk.Label(self.frame, text="Todos:").grid(
            row=2, column=0, sticky=tk.W, pady=(10, 0)
        )

        columns = ("id", "description", "status")
        self.tree = ttk.Treeview(
            self.frame, columns=columns, show="headings", height=10
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("description", text="Description")
        self.tree.heading("status", text="Status")
        self.tree.column("id", width=50)
        self.tree.column("description", width=250)
        self.tree.column("status", width=70)
        self.tree.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(
            self.frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        scrollbar.grid(row=3, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Complete/Delete section
        ttk.Label(self.frame, text="Action:").grid(
            row=4, column=0, sticky=tk.W, pady=(10, 0)
        )

        self.action_var = tk.StringVar(value="complete")
        self.combo_action = ttk.Combobox(
            self.frame, textvariable=self.action_var, values=["complete", "delete"]
        )
        self.combo_action.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        self.entry_id = ttk.Entry(self.frame, width=10)
        self.entry_id.grid(row=5, column=0, padx=65, pady=5, sticky=tk.W)
        self.entry_id.insert(0, "ID")

        self.btn_action = ttk.Button(
            self.frame, text="Execute", command=self.execute_action
        )
        self.btn_action.grid(row=5, column=1, padx=5, pady=5)

        # Refresh button
        self.btn_refresh = ttk.Button(
            self.frame, text="Refresh List", command=self.refresh_list
        )
        self.btn_refresh.grid(row=6, column=0, columnspan=2, pady=10)

        # Initialize the list
        self.refresh_list()

    def add_todo(self):
        description = self.description_var.get().strip()
        if not description:
            messagebox.showwarning("Input Error", "Please enter a todo description")
            return

        # Add via CLI function
        add_todo(description)

        # Refresh list
        self.refresh_list()
        self.entry_add.delete(0, tk.END)

    def execute_action(self):
        action = self.action_var.get().strip()
        id_str = self.entry_id.get().strip()

        if not id_str or id_str == "ID":
            messagebox.showwarning("Input Error", "Please enter a Todo ID")
            return

        try:
            todo_id = int(id_str)

            if action == "complete":
                complete_todo(todo_id)
            elif action == "delete":
                delete_todo(todo_id)

            # Refresh list
            self.refresh_list()
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, "ID")

        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid integer ID")

    def refresh_list(self):
        # Clear current list
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reload and populate
        self.todos = load_todos()
        for todo in self.todos:
            status = "✓" if todo["completed"] else "-"
            self.tree.insert(
                "", tk.END, values=(todo["id"], todo["description"], status)
            )


def main():
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
