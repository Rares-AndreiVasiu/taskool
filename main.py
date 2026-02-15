import json
from tkinter import *
from tkinter import ttk, messagebox
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

@dataclass
class Task:
    name: str
    
    wcet: int
    
    period: int

    def to_dict(self):
        return {
            "name": self.name,

            "wcet": self.wcet,

            "period": self.period
        }

    @classmethod
    def from_dict(cls, data):
        return cls(name = data["name"], wcet = data["wcet"], period = data["period"])


class Config:
    WINDOW_WIDTH = 500

    WINDOW_HEIGHT = 400
                   
    WINDOW_TITLE = "Task Scheduler"

    DEFAULT_STYLE = "classic"

    PADDING = "20"

    FONT_TITLE = ("Arial", 16, "bold")

    FONT_LARGE = ("Arial", 14, "bold")

    FONT_MEDIUM = ("Arial", 14)

    FONT_SMALL = ("Arial", 11)

    FONT_ENTRY = ("Arial", 12)

    ENTRY_WIDTH = 30

    BUTTON_WIDTH_SMALL = 15
    
    PAD_STANDARD = 20

    PAD_SMALL = 10

    PAD_ENTRY_STANDARD = (5, 15)

    PAD_ENTRY_LAST = (5, 20)

    MESSAGES = {
        "invalid_input": "Invalid Input",
        
        "positive_number": "Please enter a positive natural number",
        
        "task_name_empty": "Task name cannot be empty",
        
        "wcet_invalid": "WCET must be a positive natural number",
        
        "period_invalid": "Period must be a positive natural number",
        
        "success": "Success",
        
        "tasks_saved": "Tasks saved successfully to tasks.json",
        
        "all_saved": "All tasks saved!",
        
        "saved_count": "Saved {count} tasks to tasks.json"
    }
    
    FILES = {
        "tasks_output": "tasks.json"
    }


class Screen(Enum):
    TASK_COUNT = "task_count"

    TASK_ENTRY = "task_entry"

    COMPLETIONO = "completion"


class TaskValidator:
    @staticmethod
    def validate_task_count(count_str: str) -> int:
        try:
            n = int(count_str)
            
            if n <= 0:
                raise ValueError(Config.MESSAGES["positive_number"])

            return n

        except ValueError:
            raise ValueError(Config.MESSAGES["positive_number"])


    @staticmethod
    def validate_task_name(name: str) -> str:
        name = name.strip()

        if not name:
            raise ValueError(Config.MESSAGES["task_name_empty"])
        
        return name
    

    @staticmethod
    def validate_wcet(wcet_str: str) -> int:
        try:
            wcet = int(wcet_str)

            if wcet <= 0:
                raise ValueError(Config.MESSAGES["wcet_invalid"])
            
            return wcet
        
        except ValueError:
            raise ValueError(Config.MESSAGES["wcet_invalid"])

    



    
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

        self._create_task_count_label(frame)

        self._create_task_count_entry(frame)

    def _create_task_count_label(self, frame):
        ttk.Label(frame, text="How many tasks do you want to create?",
                  font=('Arial', 14)).pack(pady=20)

    def _create_task_count_entry(self, frame):
        self.task_count_var = StringVar()

        entry = ttk.Entry(frame, textvariable=self.task_count_var,
                          font=('Arial', 11), width=15)

        entry.pack(pady=10)

        entry.focus()

        ttk.Button(frame, text="Next", command=self.validate_and_start).pack(pady=20)

        entry.bind('<Return>', lambda e: self.validate_and_start())

    def validate_and_start(self):
        try:
            n = self._get_validated_task_count()

            self._initialize_task_state(n)

            self.show_task_entry_screen()
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter a positive natural number")

    def _get_validated_task_count(self):
        n = int(self.task_count_var.get())

        if n <= 0:
            raise ValueError()
        return n

    def _initialize_task_state(self, total_tasks):
        self.total_tasks = total_tasks
        
        self.current_task_index = 0
        
        self.tasks = []

    def show_task_entry_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")

        frame.pack(expand=True)

        self._create_progress_label(frame)

        self._create_task_input_fields(frame)
        
        self._create_navigation_buttons(frame)

    def _create_progress_label(self, frame):
        progress_text = f"Task {self.current_task_index + 1} of {self.total_tasks}"

        ttk.Label(frame, text=progress_text,
                  font=('Arial', 14, 'bold')).pack(pady=(0, 20))

    def _create_task_input_fields(self, frame):
        self.name_var = StringVar()

        self._create_labeled_entry(frame, "Task Name:", self.name_var, True)

        self.wcet_var = StringVar()

        self._create_labeled_entry(frame, "WCET (Worst Case Execution Time):", self.wcet_var)

        self.period_var = StringVar()

        entry = self._create_labeled_entry(frame, "Period:", self.period_var)

        entry.bind('<Return>', lambda e: self.save_current_task())

    def _create_labeled_entry(self, parent, label_text, string_var, is_focused=False):
        ttk.Label(parent, text=label_text, font=('Arial', 11)).pack(anchor='w')

        entry = ttk.Entry(parent, textvariable=string_var,
                          font=('Arial', 12), width=30)

        pady_value = (5, 20) if label_text == "Period:" else (5, 15)

        entry.pack(pady=pady_value, fill='x')

        if is_focused:
            entry.focus()

        entry.bind('<Return>', lambda e: self.save_current_task())

        return entry

    def _create_navigation_buttons(self, frame):
        button_frame = ttk.Frame(frame)

        button_frame.pack(fill='x')

        if self.current_task_index > 0:
            ttk.Button(button_frame, text="Previous",
                       command=self.go_to_previous_task).pack(side='left')

        button_text = self._get_next_button_text()

        ttk.Button(button_frame, text=button_text,
                   command=self.save_current_task).pack(side='right')

    def _get_next_button_text(self):
        return "Finish & Save" if self.current_task_index == self.total_tasks - 1 else "Next Task"

    def save_current_task(self):
        try:
            task = self._build_task_from_input()

            self._store_task(task)

            self._proceed_to_next_or_save()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def _build_task_from_input(self):
        name = self._validate_task_name()

        wcet = self._validate_wcet()

        period = self._validate_period()

        return {
            "name": name,
            "wcet": wcet,
            "period": period
        }

    def _validate_task_name(self):
        name = self.name_var.get().strip()
        if not name:
            raise ValueError("Task name cannot be empty")
        return name

    def _validate_wcet(self):
        try:
            wcet = int(self.wcet_var.get())
            if wcet <= 0:
                raise ValueError("WCET must be a positive natural number")
            return wcet
        except ValueError:
            raise ValueError("WCET must be a positive natural number")

    def _validate_period(self):
        try:
            period = int(self.period_var.get())
            if period <= 0:
                raise ValueError("Period must be a positive natural number")
            return period
        except ValueError:
            raise ValueError("Period must be a positive natural number")

    def _store_task(self, task):
        if self.current_task_index < len(self.tasks):
            self.tasks[self.current_task_index] = task
        else:
            self.tasks.append(task)

    def _proceed_to_next_or_save(self):
        if self.current_task_index < self.total_tasks - 1:
            self.current_task_index += 1

            self.show_task_entry_screen()
        else:
            self.save_to_json()

    def go_to_previous_task(self):
        if self.current_task_index > 0:
            self.current_task_index -= 1

            self.show_task_entry_screen()

            self._load_task_into_fields()

    def _load_task_into_fields(self):
        if self.current_task_index < len(self.tasks):
            task = self.tasks[self.current_task_index]

            self.name_var.set(task["name"])

            self.wcet_var.set(str(task["wcet"]))

            self.period_var.set(str(task["period"]))

    def save_to_json(self):
        data = self._prepare_save_data()

        self._write_to_file(data)

        self._show_save_success()

        self.show_completion_screen()

    def _prepare_save_data(self):
        return {
            "total_tasks": self.total_tasks,
            "tasks": self.tasks
        }

    def _write_to_file(self, data):
        filename = "tasks.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def _show_save_success(self):
        messagebox.showinfo("Success", f"Tasks saved successfully to tasks.json")

    def show_completion_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")

        frame.pack(expand=True)

        self._create_completion_message(frame)

        self._create_completion_buttons(frame)

    def _create_completion_message(self, frame):
        ttk.Label(frame, text="All tasks saved!",
                  font=('Arial', 16, 'bold')).pack(pady=20)

        ttk.Label(frame, text=f"Saved {self.total_tasks} tasks to tasks.json",
                  font=('Arial', 11)).pack(pady=10)

    def _create_completion_buttons(self, frame):
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

