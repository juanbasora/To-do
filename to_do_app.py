import customtkinter
from tkinter import Menu
from backend import Database

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
        

        self.due_date_entry = customtkinter.CTkEntry(master=self)
        self.due_date_entry.grid(row=2, column=1)

        # replace this with a calendar widget
        # use the widget from the ttkbootstrap library
        # youtube video: https://www.youtube.com/watch?v=jACXHXaGLqQ

        self.notes_label = customtkinter.CTkLabel(master=self, text="Notes: ")
        self.notes_label.grid(row=3, column=0)

        self.notes_entry = customtkinter.CTkTextbox(master=self, fg_color="gray22")
        self.notes_entry.grid(row=3, column=1)


        # submit button
        self.submit_button = customtkinter.CTkButton(master=self, text="Submit", fg_color="transparent", text_color=("gray10", "gray90"), command=self.add_task)
        self.submit_button.grid(row=7, column=0, columnspan=3, sticky="s")
        
    def test(self, title=None, due_date=None, description=None, priority=None):
        self.task_entry_box.insert(0, title)
        self.due_date_entry.insert(0, due_date)
        self.notes_entry.insert(0.0, description)
        self.priority_dropdown.set(priority)

        # Changed button text from "submit" to "update"
        self.submit_button.configure(text="Update")

    def update_task(self):
        pass

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
        #from datetime import datetime

        self.database.add_entry(due_date, name, notes, priority, completed)
        self.task_entry_box.delete(0, "end")
        self.due_date_entry.delete(0, "end")
        self.notes_entry.delete(0.0, "end")

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

        # create a frame for the buttons
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
    
        # Building a second frame to display the task details
        self.second_frame = customtkinter.CTkFrame(master=self)
        self.second_frame.grid(row=0, column=1, sticky="nsew")

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
        description = entries[number][3]
        priority = entries[number][4]

        # Clear the second frame before adding new widgets
        for widget in self.second_frame.winfo_children():
            widget.destroy()

        self.name_label = customtkinter.CTkLabel(master=self.second_frame, text=task_name)
        self.name_label.grid(row=0, column=0, padx=10)

        self.date_label = customtkinter.CTkLabel(master=self.second_frame, text=f"Due date: {due_date}")
        self.date_label.grid(row=1, column=0, padx=10)

        self.priority_label = customtkinter.CTkLabel(master=self.second_frame, text=f"Priority: {priority}")
        self.priority_label.grid(row=2, column=0, padx=10)

        self.description_text_box = customtkinter.CTkTextbox(master=self.second_frame, fg_color="gray22")
        self.description_text_box.grid(row=3, column=0, padx=10)

        self.description_text_box.insert(0.0, description)
        self.description_text_box.configure(state="disabled")

        for button in button_list:
            button.configure(fg_color=("gray75", "gray25") if button == button_list[number] else "transparent")

    def open_new_window(self):
        if customtkinter.CTkToplevel is None or not customtkinter.CTkToplevel.winfo_exists():
            customtkinter.CTkToplevel = Add_new_task()
            # self.add_button_to_frame()
        else:
            customtkinter.CTkToplevel.focus()

    def delete_task(self):
        pass

    def edit_task(self):
        name = entries[number][2]
        description = entries[number][3]
        due_date = entries[number][1]

        for task in self.database.view_all():
            if task[2] == name and task[3] == description and task[1] == due_date:
                print(task)
                
                if customtkinter.CTkToplevel is None or not customtkinter.CTkToplevel.winfo_exists():
                    self.Add_new_task = Add_new_task()
                    customtkinter.CTkToplevel = self.Add_new_task.test(name, due_date, description, task[4])
                else:
                    customtkinter.CTkToplevel.focus()

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    app = App()
    app.mainloop()
