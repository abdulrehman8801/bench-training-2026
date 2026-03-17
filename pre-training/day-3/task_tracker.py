import json
import argparse
import datetime
import uuid

class Task_Tracker:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No valid data found, starting fresh.")
            return {"tasks": []}

    def save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def add_task(self, title):
        data = self.load_data()
        data["tasks"].append({"id": str(uuid.uuid4())[:8], "title": title, "status": "todo", "created_at": str(datetime.datetime.now())})
        self.save_data(data)

    def complete_task(self, id):
        print("Completing task: ", id)
        data = self.load_data()
        updated = False

        for task in data["tasks"]:
            if task["id"] == id:
                task["status"] = "done"
                updated = True
                break

        if updated:
            self.save_data(data)
            print(f"Task '{id}' marked as done.")
        else:
            print(f"No task found with id={id}.")

    def delete_task(self, id):
        data = self.load_data()
        updated = False
        for task in data["tasks"]:
            if task["id"] == id:
                data["tasks"].remove(task)
                updated = True
                break

        if updated:
            self.save_data(data)
            print(f"Task '{id}' was removed.")
        else:
            print(f"No task found with id={id}.")

    def list_tasks(self, filter=None):
        data = self.load_data()
        tasks = data["tasks"]

        if filter:
            filtered_tasks = [task for task in tasks if task["status"].lower() == filter.lower()]
            return filtered_tasks
        else:
            return tasks


def main():
    parser = argparse.ArgumentParser(description="Task Tracker")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("title", type=str, help="title of the task")

    parser_done = subparsers.add_parser("done")
    parser_done.add_argument("id", type=str, help="id of the task")

    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("id", type=str, help="id of the task")

    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--filter", type=str, help="filter of the task")

    args = parser.parse_args()
    task = Task_Tracker("tasks.json")

    if args.command == "add":
        task.add_task(args.title)
    elif args.command == "done":
        task.complete_task(args.id[:8])
    elif args.command == "delete":
        task.delete_task(args.id[:8])
    elif args.command == "list":
        print(task.list_tasks(args.filter))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
