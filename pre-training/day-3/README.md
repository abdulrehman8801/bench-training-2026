# Day-3

example usage is given below

1. python task_tracker.py list --filter todo
2. python task_tracker.py list
3. python task_tracker.py delete 0d19495b
4. python task_tracker.py add "Fix stats bug"
5. python task_tracker.py done 60b6efc2c

We used a class to group all task-related data and methods (add, complete, delete, list) together, making the code organized and reusable.
It also allows persistent state (like the loaded JSON) to be stored in one object, rather than passing data around between separate functions.
