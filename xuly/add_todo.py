import tkinter as tk
from tkinter import messagebox, font, Menu, simpledialog, ttk
from tkcalendar import DateEntry

import datetime
import time

from db.db import get_db_connection
from xuly.config import root, font_style
import xuly.show as show 


def add_task(task_entry, description_entry, start_time_entry, end_time_entry, user_id):
    task_name = task_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    try:
        start_time = datetime.datetime.strptime(start_time, "%d-%m-%Y").strftime("%d-%m-%Y") 
    except ValueError:
        pass

    try:
        end_time = datetime.datetime.strptime(end_time, "%d-%m-%Y").strftime("%d-%m-%Y")
    except ValueError:
        pass

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO tasks (task_name, description, start_time, end_time, user_id) VALUES (?, ?, ?, ?, ?)',
        (task_name, description, start_time, end_time, user_id)
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Thông báo", "Công việc đã được thêm thành công!")
    show.show_tasks(user_id ,user_id)