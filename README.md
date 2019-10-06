# trello-timebox
A script made for people who use Trello as a to-do list / organization app and Google Calendar to plan their days.
The main idea is to streamline productivity and organizing tasks by minimizing the manual actions to inputting tasks, due dates, and time estimates into Trello.
In turn, trello-timebox sorts the tasks by urgency and schedules time to complete them during unfilled working hours, helping ensure all tasks get done.

This script (provided API and username info) gets starred boards from a Trello user and all cards on that board, then sorts them by due date (the benefit of which is it sorts together cards from all lists rather than within each list).

Planned future features include:
- locale-specific datetime display in sorted list
- get work hours from Google Calendar
- add time estimate input for Trello cards
- automatically add Google Calendar events for each card during unfilled working hours
- fleshed-out CLI

Development in progress.