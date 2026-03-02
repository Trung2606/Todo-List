import tkinter as tk
from tkinter import messagebox, font, Menu, simpledialog, ttk

import datetime

from db.db import get_db_connection
from xuly.config import task_background, task_tree, toolbar
from xuly.back import create_back_button

# Biến theo dõi trang hiện tại
is_on_main_page = True

# Hàm cập nhật nút back
def back_button():
    global is_on_main_page
    if is_on_main_page:
        # Ẩn nút back
        toolbar.grid_forget()
    else:
        # Hiện nút back
        toolbar.grid(row=0, column=0, sticky='w')

# Hàm hiển thị danh sách công việc
def show_tasks(user_id, current_user_id, filter_completed=None):
    global is_on_main_page
    is_on_main_page = True

    conn = get_db_connection()
    global is_filtered_or_searched
    is_filtered_or_searched = True

    if filter_completed is None:
        tasks = conn.execute('SELECT * FROM tasks WHERE user_id=?', (user_id,)).fetchall()
    else:
        tasks = conn.execute('SELECT * FROM tasks WHERE is_completed = ? AND user_id=?', (filter_completed, user_id,)).fetchall()
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

        # Thêm công việc vào Treeview với màu cảnh báo
        if "Đã hết hạn" in time_left_str:
            tag = "overdue"
        elif "Hết hạn hôm nay" in time_left_str or ("Còn" in time_left_str and "phút" in time_left_str):
            tag = "today"
        else:
            tag = "upcoming"
        # Thêm công việc vào Treeview
        task_tree.insert("", tk.END, values=(task_name, time_left_str, "✓" if is_completed else "", "⋮"), iid=task_id)

    # Tạo nút back
    global back_button
    back_button = create_back_button(toolbar, current_user_id, is_filtered_or_searched)
