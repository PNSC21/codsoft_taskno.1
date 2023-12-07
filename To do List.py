import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from datetime import datetime
import threading
import time

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobile-style To-Do List App")

        # Set a custom font
        app_font = ('Helvetica', 14)

        # Entry for adding tasks
        self.entry = ttk.Entry(root, font=app_font)
        self.entry.pack(pady=10, ipady=5, ipadx=10, fill=tk.X)

        # Listbox to display tasks
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=app_font)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Buttons to add, update, delete tasks, and set reminders
        add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        add_button.pack(pady=5, ipady=5, ipadx=10, fill=tk.X)

        update_button = ttk.Button(root, text="Update Task", command=self.update_task)
        update_button.pack(pady=5, ipady=5, ipadx=10, fill=tk.X)

        delete_button = ttk.Button(root, text="Delete Task", command=self.delete_task)
        delete_button.pack(pady=5, ipady=5, ipadx=10, fill=tk.X)

        reminder_button = ttk.Button(root, text="Set Reminder", command=self.set_reminder)
        reminder_button.pack(pady=5, ipady=5, ipadx=10, fill=tk.X)

        # Label to display the current date and time
        self.time_label = tk.Label(root, text="", font=app_font)
        self.time_label.pack()

        # Start a thread to update the time label
        self.update_time_label()

    def add_task(self):
        task = self.entry.get()
        if task:
            self.listbox.insert(tk.END, task)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def update_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            updated_task = simpledialog.askstring("Update Task", "Enter updated task:", initialvalue=self.listbox.get(selected_task_index))
            if updated_task:
                self.listbox.delete(selected_task_index)
                self.listbox.insert(tk.END, updated_task)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to update.")

    def delete_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            self.listbox.delete(selected_task_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def set_reminder(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            selected_task = self.listbox.get(selected_task_index)
            reminder_time = simpledialog.askstring("Set Reminder", "Enter reminder date and time (YYYY-MM-DD HH:MM:SS):")
            if reminder_time:
                self.schedule_reminder(selected_task, reminder_time)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to set a reminder.")

    def schedule_reminder(self, task, reminder_time):
        try:
            reminder_datetime = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S")
            current_datetime = datetime.now()

            time_difference = (reminder_datetime - current_datetime).total_seconds()

            if time_difference > 0:
                threading.Thread(target=self.ring_reminder, args=(task, time_difference)).start()
                messagebox.showinfo("Reminder Set", f"Reminder set for:\n{task} at {reminder_time}")
            else:
                messagebox.showwarning("Warning", "Invalid reminder time. Please enter a future date and time.")

        except ValueError:
            messagebox.showwarning("Warning", "Invalid date and time format. Please use YYYY-MM-DD HH:MM:SS.")

    def ring_reminder(self, task, delay_seconds):
        time.sleep(delay_seconds)
        messagebox.showinfo("Reminder", f"Reminder for:\n{task}")

    def update_time_label(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"Current Date and Time: {current_time}")
        self.root.after(1000, self.update_time_label) 
        
def main():
    root = tk.Tk()
    app = ToDoListApp(root)
    root.geometry("400x600")  
    root.mainloop()

if __name__ == "__main__":
    main()
