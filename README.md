## event-broker
A simple Event-Customer based broker.

event_file_diff.py tracks file changes for specified file:

Usage: `python3 event_file_diff.py [tracking_file] [user_name] [CMD]`

Example: `python3 event_file_diff.py test.txt usr_1 ADD`

CMD:
- `ADD` [Adds the user to the event]
- `REMOVE` [Removes the user from the event]
- `KILL` [Kills all the child processes and cleans the dir]

# Example:

![Example_](demo/enlyze_demo.gif)