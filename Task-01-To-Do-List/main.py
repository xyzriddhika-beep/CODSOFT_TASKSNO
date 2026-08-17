"""
To-Do List Application
------------------------
A simple command-line to-do list manager.

Features:
  1. Add a task
  2. View all tasks
  3. Update a task
  4. Mark a task as complete / incomplete
  5. Delete a task
  6. Exit

Tasks are saved to a local JSON file (tasks.json) so they persist
between runs of the program.
"""

import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------

def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if none exists."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: tasks file was unreadable. Starting with an empty list.\n")
        return []


def save_tasks(tasks):
    """Write the current list of tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


# ---------------------------------------------------------------------------
# Core actions
# ---------------------------------------------------------------------------

def add_task(tasks):
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.\n")
        return

    description = input("Enter description (optional): ").strip()
    due_date = input("Enter due date (optional, e.g. 2026-08-20): ").strip()

    new_id = max((t["id"] for t in tasks), default=0) + 1
    task = {
        "id": new_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task #{new_id} '{title}' added.\n")


def view_tasks(tasks):
    if not tasks:
        print("No tasks yet. Add one to get started!\n")
        return

    print("\n" + "-" * 64)
    print(f"{'ID':<4}{'Status':<10}{'Title':<28}{'Due Date':<12}")
    print("-" * 64)
    for t in tasks:
        status = "Done" if t["completed"] else "Pending"
        title = t["title"] if len(t["title"]) <= 27 else t["title"][:24] + "..."
        print(f"{t['id']:<4}{status:<10}{title:<28}{t.get('due_date', ''):<12}")
    print("-" * 64 + "\n")


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def get_task_id_input(prompt):
    """Safely read an integer task ID from the user."""
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("Please enter a valid numeric ID.\n")
        return None


def update_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    task_id = get_task_id_input("Enter the ID of the task to update: ")
    if task_id is None:
        return

    task = find_task(tasks, task_id)
    if not task:
        print("Task not found.\n")
        return

    print("Leave a field blank to keep its current value.")
    new_title = input(f"New title [{task['title']}]: ").strip()
    new_desc = input(f"New description [{task['description']}]: ").strip()
    new_due = input(f"New due date [{task.get('due_date', '')}]: ").strip()

    if new_title:
        task["title"] = new_title
    if new_desc:
        task["description"] = new_desc
    if new_due:
        task["due_date"] = new_due

    save_tasks(tasks)
    print("Task updated.\n")


def toggle_complete(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    task_id = get_task_id_input("Enter the ID of the task to mark complete/incomplete: ")
    if task_id is None:
        return

    task = find_task(tasks, task_id)
    if not task:
        print("Task not found.\n")
        return

    task["completed"] = not task["completed"]
    save_tasks(tasks)
    state = "complete" if task["completed"] else "incomplete"
    print(f"Task '{task['title']}' marked as {state}.\n")


def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    task_id = get_task_id_input("Enter the ID of the task to delete: ")
    if task_id is None:
        return

    task = find_task(tasks, task_id)
    if not task:
        print("Task not found.\n")
        return

    confirm = input(f"Delete '{task['title']}'? (y/n): ").strip().lower()
    if confirm == "y":
        tasks.remove(task)
        save_tasks(tasks)
        print("Task deleted.\n")
    else:
        print("Cancelled.\n")


# ---------------------------------------------------------------------------
# Menu / main loop
# ---------------------------------------------------------------------------

def print_menu():
    print("=" * 40)
    print("           TO-DO LIST MENU")
    print("=" * 40)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Mark Task Complete/Incomplete")
    print("5. Delete Task")
    print("6. Exit")


def main():
    tasks = load_tasks()
    print("Welcome to your To-Do List!\n")

    actions = {
        "1": add_task,
        "2": view_tasks,
        "3": update_task,
        "4": toggle_complete,
        "5": delete_task,
    }

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "6":
            print("Goodbye! Your tasks have been saved.")
            break
        elif choice in actions:
            actions[choice](tasks)
        else:
            print("Invalid choice, please select a number from 1 to 6.\n")


if __name__ == "__main__":
    main()