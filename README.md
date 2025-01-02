# To-do App (WIP)

This is a simple To-Do application built using `customtkinter` for the GUI and `sqlite3` for the database. The application allows users to add, view, edit, and delete tasks.

## Features

- Add new tasks with a title, due date, description, and priority.
- View all tasks in a scrollable frame.
- Edit existing tasks.
- Delete tasks.
- Mark tasks as completed.
- More features to come.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/To-do.git
   cd To-do
  
2. Install the required packages:
   ```sh
   pip install customtkinter

Usage
1. Run the application:
   ```sh
   python to_do_app.py

3. Use the menu to add, edit, or delete tasks.

### Code Overview
`backend.py`
  - `Database`: A class to handle database operations such as adding, viewing, searching, and deleting tasks.

`to_do_app.py`
  - `App`: The main application class that initializes the GUI and handles user interactions.
  -  `Add_new_task`: A class for the window that allows users to add or edit tasks.
  - `ScrollableLabelButtonFrame`: A custom scrollable frame to display task buttons.

### Screenshots
![Screenshot 2024-11-09 135720](https://github.com/user-attachments/assets/309e29db-4098-4509-aebb-d0b2fe8aaf31)

![Screenshot 2024-11-09 140533](https://github.com/user-attachments/assets/437ff3ef-ebb5-4857-980b-3891cb9ad81e)

### Contributing
Contributions are welcome! Please open an issue or submit a pull request.

### License
This project is licensed under the MIT License.





