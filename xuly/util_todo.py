
import json
import tkinter as tk
from tkinter import ttk

import datetime
from datetime import date
import os


from db.db import get_db_connection
from xuly.config import  task_tree, toolbar, task_menu, filter_menu, sort_menu

current_user_id = 1

# Biến theo dõi trạng thái lọc/tìm kiếm
is_filtered_or_searched = False

# Biến theo dõi trang hiện tại
is_on_main_page = True

# Hàm hiển thị danh sách công việc
def show_tasks(user_id, filter_completed=None):  # Thêm tham số user_id
    global is_on_main_page
    is_on_main_page = True

    conn = get_db_connection()
    global is_filtered_or_searched
    is_filtered_or_searched = True

    if filter_completed is None:
        tasks = conn.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,)).fetchall()  # Lọc theo user_id
    else:
        tasks = conn.execute('SELECT * FROM tasks WHERE user_id = ? AND is_completed = ?', (user_id, filter_completed)).fetchall()  # Lọc theo user_id và trạng thái hoàn thành
    conn.close()

    # Xóa tất cả các mục cũ trong Treeview
    for item in task_tree.get_children():
        task_tree.delete(item)

    for task in tasks:
        task_id = task['id']
        task_name = task['task_name']
        is_completed = task['is_completed']
        end_time = task['end_time']
        time_left_str = "Không có thời hạn"

        # Tính toán thời gian còn lại
        if end_time:
            try:
                end_time_obj = datetime.datetime.strptime(end_time, "%d-%m-%Y").date()
                end_datetime = datetime.datetime.combine(end_time_obj, datetime.time.max)
                time_left = end_datetime - datetime.datetime.now()
                days_left = time_left.days
                hours_left = time_left.total_seconds() / 3600

                if days_left == 1 and hours_left > 24:
                    time_left_str = "Ngày mai hết hạn"
                elif days_left == 0 and hours_left > 0:
                    time_left_str = "Hết hạn hôm nay"
                elif days_left > 1:
                    time_left_str = f"Còn {days_left} ngày"
                elif days_left > 0:
                    time_left_str = "Hết hạn hôm nay"
                else:
                    time_left_str = "Đã hết hạn"
            except ValueError:
                time_left_str = "Thời gian không hợp lệ"

        # Thêm công việc vào Treeview
        task_tree.insert("", tk.END, values=(task_name, time_left_str, "✓" if is_completed else "", "⋮"), iid=task_id)
        # Nút "<"
        from xuly.back import create_back_button
        create_back_button(toolbar, current_user_id, is_filtered_or_searched)

# Hàm hiển thị menu chuột phải
def show_task_menu(event, task_id):
    task_menu.task_id = task_id
    task_menu.post(event.x_root, event.y_root)

# Hàm hiển thị menu Lọc
def show_filter_menu(event):
    widget = event.widget
    x = widget.winfo_rootx() + widget.winfo_width()
    y = widget.winfo_rooty()
    filter_menu.post(x, y)

# Hàm hiển thị menu Sắp xếp
def show_sort_menu(event):
    widget = event.widget
    x = widget.winfo_rootx() + widget.winfo_width()
    y = widget.winfo_rooty()
    sort_menu.post(x, y)

