import tkinter as tk
from tkinter import messagebox, font, Menu, simpledialog, ttk
from tkcalendar import DateEntry
from datetime import datetime

from db.db import get_db_connection
from xuly.config import root, font_style, task_menu
from xuly.edit_todo import edit_task



# Hàm sửa công việc
def show_edit_task_gui(user_id):
    task_id = task_menu.task_id
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()

    if task:
        edit_task_window = tk.Toplevel(root)
        edit_task_window.title("Sửa công việc")

        # Frame chứa các ô nhập liệu
        input_frame = ttk.Frame(edit_task_window)
        input_frame.pack(fill='x', padx=10, pady=10)

        # Tên công việc
        ttk.Label(input_frame, text="Tên công việc:", style="AddEdit.TLabel").grid(row=0, column=0, sticky='w')
        task_entry = ttk.Entry(input_frame, width=50, font=font_style, style="AddEdit.TEntry")
        task_entry.grid(row=0, column=1, sticky='ew', pady=5)
        task_entry.insert(0, task['task_name'])

        # Mô tả
        ttk.Label(input_frame, text="Mô tả:", style="AddEdit.TLabel").grid(row=1, column=0, sticky='w')
        description_entry = tk.Text(input_frame, width=50, height=5, font=font_style)
        description_entry.grid(row=1, column=1, sticky='ew', pady=5)
        description_entry.insert(tk.END, task['description'])

        # Thời gian bắt đầu
        ttk.Label(input_frame, text="Thời gian bắt đầu:", style="AddEdit.TLabel").grid(row=2, column=0, sticky='w')
        start_time_entry = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        start_time_entry.grid(row=2, column=1, sticky='ew', pady=5)
        if task['start_time']:
            start_time_entry.set_date(datetime.strptime(task['start_time'], "%d-%m-%Y").date()) # corrected line

        # Thời gian kết thúc
        ttk.Label(input_frame, text="Thời gian kết thúc:", style="AddEdit.TLabel").grid(row=3, column=0, sticky='w')
        end_time_entry = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        end_time_entry.grid(row=3, column=1, sticky='ew', pady=5)
        if task['end_time']:
            end_time_entry.set_date(datetime.strptime(task['end_time'], "%d-%m-%Y").date()) # corrected line
        

        # Tạo frame chứa nút
        button_frame = ttk.Frame(edit_task_window)
        button_frame.pack(pady=10)

        # Hàm xử lý sự kiện khi nhấn nút "Lưu"
        def edit_task_and_close(user_id):
            edit_task(task_entry, description_entry, start_time_entry, end_time_entry, task_id, user_id)
            edit_task_window.destroy()  # Thêm lệnh đóng cửa sổ

        # Nút Lưu
        ttk.Button(button_frame, text="Lưu", command=lambda: edit_task_and_close( user_id), style="AddEdit.TButton").pack(side=tk.LEFT, padx=5)
        # Nút Hủy
        ttk.Button(button_frame, text="Hủy", command=edit_task_window.destroy, style="AddEdit.TButton").pack(side=tk.LEFT, padx=5)
