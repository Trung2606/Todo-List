import tkinter as tk
from tkinter import messagebox, font, Menu, simpledialog, ttk
from tkcalendar import DateEntry

import datetime
import time

from db.db import get_db_connection
from xuly.config import root, font_style
from xuly.add_todo import add_task



# Hàm thêm công việc
def show_add_task_gui(user_id): 
    add_task_window = tk.Toplevel(root)
    add_task_window.title("Thêm công việc")

    # Frame chứa các ô nhập liệu
    input_frame = ttk.Frame(add_task_window)
    input_frame.pack(fill='x', padx=10, pady=10)

    # Tên công việc
    ttk.Label(input_frame, text="Tên công việc:", style="AddEdit.TLabel").grid(row=0, column=0, sticky='w')
    task_entry = ttk.Entry(input_frame, width=50, font=font_style, style="AddEdit.TEntry")
    task_entry.grid(row=0, column=1, sticky='ew', pady=5)

    # Mô tả
    ttk.Label(input_frame, text="Mô tả:", style="AddEdit.TLabel").grid(row=1, column=0, sticky='w')
    description_entry = tk.Text(input_frame, width=50, height=5, font=font_style)
    description_entry.grid(row=1, column=1, sticky='ew', pady=5)

    # Thời gian bắt đầu
    ttk.Label(input_frame, text="Thời gian bắt đầu:", style="AddEdit.TLabel").grid(row=2, column=0, sticky='w')
    start_time_entry = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
    start_time_entry.grid(row=2, column=1, sticky='ew', pady=5)

    # Thời gian kết thúc
    ttk.Label(input_frame, text="Thời gian kết thúc:", style="AddEdit.TLabel").grid(row=3, column=0, sticky='w')
    end_time_entry = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
    end_time_entry.grid(row=3, column=1, sticky='ew', pady=5)

    # Tạo frame chứa nút
    button_frame = ttk.Frame(add_task_window)
    button_frame.pack(pady=10)

    # Hàm xử lý sự kiện khi nhấn nút "Thêm"
    def add_task_and_close():
        add_task(task_entry, description_entry, start_time_entry, end_time_entry, user_id)
        add_task_window.destroy()

    # Nút Thêm
    ttk.Button(button_frame, text="Thêm", command=add_task_and_close, style="AddEdit.TButton").pack(side=tk.LEFT, padx=5)
    # Nút Hủy
    ttk.Button(button_frame, text="Hủy", command=add_task_window.destroy, style="AddEdit.TButton").pack(side=tk.LEFT, padx=5)
