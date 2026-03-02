
import tkinter as tk
from tkinter import ttk
from datetime import datetime

from db.db import get_db_connection
from xuly.config import root, font_style, task_menu



# Hàm hiển thị thông tin chi tiết công việc
def show_task_details():
    task_id = task_menu.task_id
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()

    if task:
        details_window = tk.Toplevel(root)
        details_window.title("Thông tin công việc")

        content_frame = ttk.Frame(details_window, style="Details.TFrame")
        content_frame.pack(fill='both', expand=True)

        content_text = tk.Text(content_frame, font=font_style, wrap='word')
        content_text.pack(fill='both', expand=True)

        content_text.insert(tk.END, f"- Tên công việc: {task['task_name']}\n")
        content_text.insert(tk.END, f"- Mô tả công việc: {task['description']}\n")
        content_text.insert(tk.END, f"- Thời gian bắt đầu: {task['start_time']}\n")
        content_text.insert(tk.END, f"- Thời gian kết thúc: {task['end_time']}\n")
        content_text.insert(tk.END, f"- Trạng thái công việc: {'Đã hoàn thành' if task['is_completed'] else 'Chưa hoàn thành'}\n")

        content_text.config(state='disabled')