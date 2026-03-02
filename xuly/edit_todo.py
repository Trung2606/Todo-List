import tkinter as tk
from tkinter import messagebox, font, Menu, simpledialog, ttk
from tkcalendar import DateEntry
from datetime import datetime

from db.db import get_db_connection
from xuly.config import root, font_style, task_menu
from xuly.show import show_tasks


# Hàm xử lý lưu chỉnh sửa
def edit_task(task_entry, description_entry, start_time_entry, end_time_entry, task_id, user_id):
    task_name = task_entry.get()
    description = description_entry.get("1.0", tk.END).strip()

    # Ép định dạng ngày về dd-mm-yyyy trước khi lưu
    start_time = start_time_entry.get_date().strftime("%d-%m-%Y")
    end_time = end_time_entry.get_date().strftime("%d-%m-%Y")

    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE tasks
            SET task_name = ?, description = ?, start_time = ?, end_time = ?
            WHERE id = ?
        ''', (task_name, description, start_time, end_time, task_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Công việc đã được cập nhật thành công!")
        
        show_tasks(user_id ,user_id)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi cập nhật công việc: {e}")