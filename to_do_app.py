import customtkinter
from tkinter import Menu
from backend import Database
from tkcalendar import DateEntry


button_list = []

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.button_list = button_list

    def add_button(self, task_name):
        button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=task_name, fg_color="transparent", text_color=("gray10", "gray90"), 
                                         hover_color=("gray70", "gray30"))
        if self.command is not None:
            button.configure(text=task_name, command=lambda: self.command(task_name), require_redraw=True)
        button.grid(row=len(self.button_list), column=0, sticky="ew")
        self.button_list.append(button)


class Add_new_task(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.database = Database()

        self.title("Add a new task")
        self.geometry("300x450")

        self.task_name_label = customtkinter.CTkLabel(master=self,text="Name: ")
        self.task_name_label.grid(row=0, column=0)

        self.task_entry_box = customtkinter.CTkEntry(master=self)
        self.task_entry_box.grid(row=0, column=1)

        self.priority_label = customtkinter.CTkLabel(master=self, text="Priority: ")
        self.priority_label.grid(row=1, column=0)
        self.priority_options = ["High", "Medium", "Low"]
        self.priority_dropdown = customtkinter.CTkComboBox(master=self, values=self.priority_options)
        self.priority_dropdown.grid(row=1, column=1)

        self.due_date_label = customtkinter.CTkLabel(master=self, text="Due Date: ")
        self.due_date_label.grid(row=2, column=0)
        self.due_date_entry = DateEntry(master=self, width=12, normalbackground="grey28", weekendbackground="grey", headersforeground="white", background="grey", borderwidth=2)
        self.due_date_entry.grid(row=2, column=1, columnspan=2, pady=10)
        
        # Got the calendar widget to work but it is not the best looking widget. Need to fix the colors.

        # self.due_date_entry = customtkinter.CTkEntry(master=self)
        # self.due_date_entry.grid(row=2, column=1)

        # convert the date string into a date object.
        # https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime


        # replace this with a calendar widget
        # use the widget from the ttkbootstrap library
        # youtube video: https://www.youtube.com/watch?v=jACXHXaGLqQ

        self.notes_label = customtkinter.CTkLabel(master=self, text="Notes: ")
        self.notes_label.grid(row=3, column=0)

        self.notes_entry = customtkinter.CTkTextbox(master=self, fg_color="gray22")
        self.notes_entry.grid(row=3, column=1)


        # submit button
        # need to add this button to the if statement below so it can be submitted or updated.
        self.submit_button = customtkinter.CTkButton(master=self, text="Submit", fg_color="transparent", text_color=("gray10", "gray90"), command=self.add_task)
        self.submit_button.grid(row=7, column=0, columnspan=3, sticky="s")

        
    def data_insert(self, title, due_date, description, priority):
        self.task_entry_box.insert(0, title)
        self.due_date_entry.insert(0, due_date)
        self.notes_entry.insert(0.0, description)
        self.priority_dropdown.set(priority)

        self.submit_button.configure(text="Update", command=self.update_task)

        # Need to find the data in the database and get the id number to update the task.

        # self.submit_button.configure(command=self.update_task if update else self.add_task)

    def update_task(self):
        name = self.task_entry_box.get()
        priority = self.priority_dropdown.get()
        due_date = self.due_date_entry.get()
        description = self.notes_entry.get(0.0, "end")
        id = entries[number][0]

        if self.database.update(id, name, description, due_date, priority):
            print("Task updated")
        else:
            print("Error: Task not updated")

# ----------------------------------------------------------------------------------------------------
# Need to fix the edit function on the back end. It's mixing up the information.  
# Descriotion is being saved as the due date and the due date is the description.  
# 
# Fixed the issue by changing the order of the variables in the update function in the backend.py file.    
# ----------------------------------------------------------------------------------------------------

    def add_task(self):
        name = self.task_entry_box.get()
        priority = self.priority_dropdown.get()
        due_date = self.due_date_entry.get()
        notes = self.notes_entry.get(0.0, "end")
        completed = "no"

        # Validate the input
        if name == "" or due_date == "":
            print("Please enter all required information")
            # Need to change this to a pop up window

        # how to check if the date is in the correct format
#         from datetime import datetime

        # print(name, priority, due_date, notes, completed)
        self.database.add_entry(due_date, name, notes, priority, completed)
        # Now that I think this works, I need to add a way to close the window after the submit button is clicked.
        self.task_entry_box.delete(0, "end")
        self.due_date_entry.delete(0, "end")
        self.notes_entry.delete(0.0, "end")

# ----------------------------------------------------------------------------------------------------
# Need to add a way to close the window after the submit button is clicked.
# add a radio button labeled "mutiple tasks" that will allow the user to add multiple tasks at once.
# if not selected then the window will close after the submit button is clicked.
# ----------------------------------------------------------------------------------------------------



# This will create a new window and lets you add a new task.
# Need to set the parent window or set this new window as a top layer window
# so that you cannot click back on the old window without closing this one first.


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tasks Tracker.py")
        self.geometry("700x450")

        self.database = Database()

        # Adding a file menu bar
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.open_new_window)
        filemenu.add_command(label="Open", command=None)
        filemenu.add_command(label="Save", command=None)
        filemenu.add_command(label="Refresh", command=self.add_button_to_frame)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)


        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Edit", command=self.edit_task)
        editmenu.add_command(label="Delete", command=None)
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.config(menu=menubar)


        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Add new buttons with scrollable frame window
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, command=self.label_button_frame_event, corner_radius=0)
        self.scrollable_label_button_frame.grid(row=0, column=0, sticky="nsew")
        self.scrollable_label_button_frame.grid_rowconfigure(4, weight=1)

        # ----------------------------------------------------------------------------------------------------
        # probably need to change the code above to a function that can be called to update the buttons
        # A True or False value can be passed to the function to update the buttons.
        # ----------------------------------------------------------------------------------------------------

        # create a frame for the buttons
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # need to add a way to update the buttons when a task is completed.
        # need to add a way to update the buttons when a task is deleted.

    
        # Building a second frame to display the task details
        self.second_frame = customtkinter.CTkFrame(master=self)
        self.second_frame.grid(row=0, column=1, sticky="nsew")
        self.second_frame.grid_columnconfigure(0, weight=1)

        # Add a button to complete the current task and then clear it so it wont show up alone in the frame.
        self.complete_button = customtkinter.CTkButton(master=self.second_frame, text="Complete", fg_color="transparent", text_color=("gray10", "gray90"))
        self.complete_button.grid(row=4, column=0, columnspan=3, sticky="s")
        
        self.complete_button.grid_forget()


        # Add the stuff here for the second frame then hide them until a button is clicked.

        self.name_label = customtkinter.CTkLabel(master=self.second_frame)
        self.name_label.grid(row=0, column=0, padx=10)
        self.name_label.grid_forget()

        self.date_label = customtkinter.CTkLabel(master=self.second_frame)
        self.date_label.grid(row=1, column=0, padx=10)
        self.date_label.grid_forget()

        self.priority_label = customtkinter.CTkLabel(master=self.second_frame)
        self.priority_label.grid(row=2, column=0, padx=10)
        self.priority_label.grid_forget()

        self.description_text_box = customtkinter.CTkTextbox(master=self.second_frame, fg_color="gray22")
        self.description_text_box.grid(row=3, column=0, padx=10)
        self.description_text_box.grid_forget()

        # delete any previous text in the text box
        self.description_text_box.delete(0.0, "end")
        self.description_text_box.configure(state="disabled")
        self.description_text_box.grid_forget()

        # running the function to add the buttons to the scrollable frame
        self.add_button_to_frame()
        customtkinter.CTkToplevel = None

    def add_button_to_frame(self):

        # Clearing the button list before adding new buttons
        self.button_list = button_list
        self.button_list.clear()

        # Destroying all the widgets in the frame for the refresh button to work
        for widget in self.home_frame.winfo_children():
            widget.pack_forget()

        self.new_buttons = self.database.view_all()
        self.names = []
        for task in self.new_buttons:
            if task[5] == "yes":
                pass
            else:
                self.names.append(task[2])

        for button_names in self.names:
            self.scrollable_label_button_frame.add_button(button_names)
        


    def label_button_frame_event(self, task_name):
        global entries
        global number
        entries = self.database.view_all()
        number = self.names.index(task_name)

        due_date = entries[number][1]
        description = entries[number][4]
        priority = entries[number][3]

        # Only cheking for one label since all the labels are hidden at the start
        if not self.name_label.winfo_ismapped():
            self.name_label.grid(row=0, column=0, padx=10)
            self.date_label.grid(row=1, column=0, padx=10)
            self.priority_label.grid(row=2, column=0, padx=10)
            self.description_text_box.grid(row=3, column=0, padx=10)
            self.complete_button.grid(row=4, column=0, columnspan=3, sticky="s")

        self.name_label.configure(text=task_name)
        self.date_label.configure(text=f"Due date: {due_date}")
        self.priority_label.configure(text=f"Priority: {priority}")
        self.description_text_box.configure(state="normal")
        self.description_text_box.delete(0.0, "end")
        self.description_text_box.insert(0.0, description)
        self.description_text_box.configure(state="disabled")
        self.complete_button.configure(command=self.complete_task)

        for button in button_list:
            button.configure(fg_color=("gray75", "gray25") if button == button_list[number] else "transparent")

            # Since I don't have the butons pre set in variables
            # I am saving a list with all buttons names and when a button is slected.
            # the program looks for that button name in the list and gets the index location
            # then I just configure the button in the button list wit the same index number
            # so button name one in the list will be the first button.

    def open_new_window(self):
        if customtkinter.CTkToplevel is None or not customtkinter.CTkToplevel.winfo_exists():
            customtkinter.CTkToplevel = Add_new_task()
        else:
            customtkinter.CTkToplevel.focus()

    def delete_task(self):
        pass
    # find the task in the database by the name and description

    def complete_task(self):
        print("Task completed")

    def edit_task(self):
        name = entries[number][2]
        description = entries[number][4]
        due_date = entries[number][1]
        priority = entries[number][3]

        # print(f"print name: {name}, description: {description}, due date: {due_date}, priority: {priority}")

        for task in self.database.view_all():
            if task[2] == name and task[4] == description and task[1] == due_date:
                if customtkinter.CTkToplevel is None or not customtkinter.CTkToplevel.winfo_exists():
                    self.Add_new_task = Add_new_task()
                    customtkinter.CTkToplevel = self.Add_new_task.data_insert(name, due_date, description, priority)
                else:
                    customtkinter.CTkToplevel.focus()

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    app = App()
    app.mainloop()