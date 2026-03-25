import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass
class Task:
    id: int
    title: str
    status: str
    created_at: datetime

class TaskManager:
    VALID_STATUSES = {"todo", "done"}

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def _load_tasks_raw(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(
                f"Error: tasks.json is corrupt ({self.file_path}). Starting fresh.",
                file=sys.stderr,
            )
            return []

        tasks = payload.get("tasks")
        if tasks is None:
            return []
        if not isinstance(tasks, list):
            print(
                f"Error: tasks.json has unexpected format. Starting fresh.",
                file=sys.stderr,
            )
            return []
        return tasks

    def load_tasks(self) -> List[Task]:
        tasks: List[Task] = []
        for item in self._load_tasks_raw():
            try:
                task_id = int(item["id"])
                title = str(item["title"])
                status = str(item["status"]).lower()
                if status not in self.VALID_STATUSES:
                    status = "todo"
                created_at_raw = item["created_at"]
                created_at = (
                    datetime.fromisoformat(created_at_raw)
                    if isinstance(created_at_raw, str)
                    else datetime.now()
                )
                tasks.append(
                    Task(
                        id=task_id,
                        title=title,
                        status=status,
                        created_at=created_at,
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue
        return tasks

    def save_tasks(self, tasks: List[Task]) -> None:
        payload = {
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                }
                for task in tasks
            ]
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

    def _next_id(self, tasks: List[Task]) -> int:
        return (max((t.id for t in tasks), default=0) + 1) if tasks else 1

    def add_task(self, title: str) -> Task:
        title = (title or "").strip()
        if not title:
            raise ValueError("title cannot be empty")

        tasks = self.load_tasks()
        new_task = Task(
            id=self._next_id(tasks),
            title=title,
            status="todo",
            created_at=datetime.now(),
        )
        tasks.append(new_task)
        self.save_tasks(tasks)
        return new_task

    def _find_task_index(self, tasks: List[Task], task_id: int) -> int:
        for i, task in enumerate(tasks):
            if task.id == task_id:
                return i
        return -1

    def complete_task(self, task_id: int) -> Task:
        tasks = self.load_tasks()
        idx = self._find_task_index(tasks, task_id)
        if idx == -1:
            raise KeyError(f"No task found with id={task_id}")

        tasks[idx].status = "done"
        self.save_tasks(tasks)
        return tasks[idx]

    def delete_task(self, task_id: int) -> None:
        tasks = self.load_tasks()
        idx = self._find_task_index(tasks, task_id)
        if idx == -1:
            raise KeyError(f"No task found with id={task_id}")

        tasks.pop(idx)
        self.save_tasks(tasks)

    def list_tasks(self, filter: Optional[str] = None) -> List[Task]:
        tasks = self.load_tasks()
        if filter is None:
            return tasks

        normalized = str(filter).lower()
        if normalized not in self.VALID_STATUSES:
            raise ValueError("filter must be one of: todo, done")
        return [t for t in tasks if t.status == normalized]


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("title", type=str, help="title of the task")

    parser_done = subparsers.add_parser("done")
    parser_done.add_argument("id", type=int, help="id of the task")

    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("id", type=int, help="id of the task")

    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--filter", type=str, default=None, help="todo or done")

    args = parser.parse_args(argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    tasks_file = os.path.join(script_dir, "tasks.json")
    manager = TaskManager(tasks_file)

    try:
        if args.command == "add":
            task = manager.add_task(args.title)
            print(f"Added task: id={task.id} | {task.title}")
        elif args.command == "done":
            task = manager.complete_task(args.id)
            print(f"Task completed: id={task.id} | {task.title}")
        elif args.command == "delete":
            manager.delete_task(args.id)
            print(f"Task deleted: id={args.id}")
        elif args.command == "list":
            tasks = manager.list_tasks(args.filter)
            if not tasks:
                print("No tasks found.")
            for t in tasks:
                created_at = t.created_at.strftime("%Y-%m-%d %H:%M:%S")
                print(f"{t.id} | {t.title} | {t.status} | created_at={created_at}")
        else:
            parser.print_help()
            return
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
