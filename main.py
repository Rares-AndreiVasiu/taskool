import json
from tkinter import *
from tkinter import ttk, messagebox


class TaskSchedulerApp:
    def __init__(self, root, style):
        self.period_var = None

        self.wcet_var = None

        self.name_var = None

        self.task_count_var = None

        self.root = root

        self.root.title("Task Scheduler")

        self.root.geometry("500x400")

        self.tasks = []

        self.current_task_index = 0

        self.total_tasks = 0

        self.style = ttk.Style()

        self.assign_style(style)

        self.show_task_count_screen()

    def assign_style(self, style):
        if style in self.style.theme_names():
            self.style.theme_use(style)
        else:
            self.style.theme_use("alt")

    def show_task_count_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")

        frame.pack(expand=True)

        ttk.Label(frame, text="How many tasks do you want to create?",
                  font=('Arial', 14)).pack(pady=20)

        self.task_count_var = StringVar()

        entry = ttk.Entry(frame, textvariable=self.task_count_var,
                          font=('Arial', 11), width=15)

        entry.pack(pady=10)

        entry.focus()

        ttk.Button(frame, text="Next", command=self.validate_and_start).pack(pady=20)

        entry.bind('<Return>', lambda e: self.validate_and_start())

    def validate_and_start(self):
        try:
            n = int(self.task_count_var.get())

            if n <= 0:
                raise ValueError()

            self.total_tasks = n

            self.current_task_index = 0

            self.tasks = []

            self.show_task_entry_screen()
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter a positive natural number")

    def create_progress_label(self, frame):
        progress_text = f"Task {self.current_task_index + 1} of {self.total_tasks}"

        ttk.Label(frame, text=progress_text, font=('Arial', 14, 'bold')).pack(pady=(0, 20))

    def show_task_entry_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")

        self.create_progress_label(frame)

        frame.pack(expand=True)

        ttk.Label(frame, text="Task Name:", font=('Arial', 11)).pack(anchor='w')

        self.name_var = StringVar()

        name_entry = ttk.Entry(frame, textvariable=self.name_var,
                               font=('Arial', 12), width=30)

        name_entry.pack(pady=(5, 15), fill='x')

        name_entry.focus()

        ttk.Label(frame, text="WCET (Worst Case Execution Time):",
                  font=('Arial', 11)).pack(anchor='w')

        self.wcet_var = StringVar()

        wcet_entry = ttk.Entry(frame, textvariable=self.wcet_var,
                               font=('Arial', 12), width=30)

        wcet_entry.pack(pady=(5, 15), fill='x')

        ttk.Label(frame, text="Period:", font=('Arial', 11)).pack(anchor='w')

        self.period_var = StringVar()

        period_entry = ttk.Entry(frame, textvariable=self.period_var,
                                 font=('Arial', 12), width=30)

        period_entry.pack(pady=(5, 20), fill='x')

        button_frame = ttk.Frame(frame)

        button_frame.pack(fill='x')

        if self.current_task_index < self.total_tasks - 1:
            button_text = "Next Task"
        else:
            button_text = "Finish & Save"

        ttk.Button(button_frame, text=button_text,
                   command=self.save_current_task).pack(side='right')

        if self.current_task_index > 0:
            ttk.Button(button_frame, text="Previous",
                       command=self.go_to_previous_task).pack(side='left')

        period_entry.bind('<Return>', lambda e: self.save_current_task())

    def save_current_task(self):
        try:
            name = self.name_var.get().strip()

            if not name:
                raise ValueError("Task name cannot be empty")

            wcet = int(self.wcet_var.get())

            if wcet <= 0:
                raise ValueError("WCET must be a positive natural number")

            period = int(self.period_var.get())

            if period <= 0:
                raise ValueError("Period must be a positive natural number")

            task = {
                "name": name,
                "wcet": wcet,
                "period": period
            }

            if self.current_task_index < len(self.tasks):
                self.tasks[self.current_task_index] = task
            else:
                self.tasks.append(task)

            if self.current_task_index < self.total_tasks - 1:
                self.current_task_index += 1

                self.show_task_entry_screen()
            else:
                self.save_to_json()

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def go_to_previous_task(self):
        if self.current_task_index > 0:
            self.current_task_index -= 1

            self.show_task_entry_screen()

            if self.current_task_index < len(self.tasks):
                task = self.tasks[self.current_task_index]

                self.name_var.set(task["name"])

                self.wcet_var.set(str(task["wcet"]))

                self.period_var.set(str(task["period"]))

    def save_to_json(self):
        data = {
            "total_tasks": self.total_tasks,
            "tasks": self.tasks
        }

        filename = "tasks.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Success", f"Tasks saved successfully to {filename}")

        self.show_completion_screen()

    def show_completion_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")

        frame.pack(expand=True)

        ttk.Label(frame, text="All tasks saved!",
                  font=('Arial', 16, 'bold')).pack(pady=20)

        ttk.Label(frame, text=f"Saved {self.total_tasks} tasks to tasks.json",
                  font=('Arial', 11)).pack(pady=10)

        button_frame = ttk.Frame(frame)

        button_frame.pack(pady=30)

        ttk.Button(button_frame, text="Create New Tasks",
                   command=self.show_task_count_screen).pack(side='left', padx=5)

        ttk.Button(button_frame, text="Exit",
                   command=self.root.quit).pack(side='left', padx=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = Tk()

    style_name = "clam"

    app = TaskSchedulerApp(root, style_name)

    root.mainloop()

