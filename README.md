# trello-timebox
Schedule automation and utilities for people who use Trello as a to-do list and Google Calendar to plan their work days.

The main idea is to streamline productivity and organizing tasks by limiting the manual actions to inputting tasks, due dates, and time estimates into Trello.
In turn, trello-timebox will sort the tasks by urgency and schedules time to complete them during unfilled working hours, helping ensure all tasks get done.

The script trello_retrieval.py (specifically the function get_cards, provided API and user credentials) gets all cards on a Trello user's board and sorts them by due date (the benefit of which is it sorts together cards from all lists rather than within each list).
The function get_tasks_for_days will get all cards with due dates in the next x days, print them all with due dates and time estimates.

The timebox.py is presently purely for interaction with trello_retrieval.py, and calendar_scheduling.py, currently in development, will be used for interaction with Google Calendar.

To Run:
 - Set the following environment variables
   * USERNAME (Trello User ID)
   * API_KEY (obtained from Trello API signup)
   * TOKEN (also obtained from Trello API signup)
   * BOARD_ID (the board you want to get cards from)
   * TIME_EST_FIELD (ID of the Custom Field (of type "number") you create in your Trello board using the Custom Fields Power-Up for entry of time estimate in minutes; this setup will be made easier in the future - for now see Trello API docs on how to make a request for your Custom Fields, then find the ID in the JSON response)
 - Run `python timebox.py` to get all cards from the specified board, or run `python timebox.py days` , replacing "days" with the integer of your choice to get only the cards with due dates within that many days from the present.
 - For maximum convenience, make timebox.py executable (follow OS-specific docs instructions) and add the trello-timebox directory to your user or system PATH variable. If you do so properly, you should be able to simply run `timebox` or `timebox days` from any directory to run the above commmands, respectively.

Planned future features include:
- Get work hours from Google Calendar
- Automatically add Google Calendar events for each card during unfilled working hours

Development in progress.