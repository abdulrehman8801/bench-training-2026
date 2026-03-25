# Day-3

Usage examples:
`python tasks.py add "Fix login bug"`
`python tasks.py done 3`
`python tasks.py list`
`python tasks.py list --filter done`

I used a `TaskManager` class because it centralizes persistence (loading/saving `tasks.json`) and the task operations (add/complete/delete/list). That keeps the CLI thin and makes the logic easier to reuse and test without duplicating file-handling code in multiple places.
