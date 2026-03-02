import datetime
import tkinter as tk

from db.db import get_db_connection
from xuly.config import task_tree

# Biến theo dõi trạng thái sắp xếp
sort_ascending = True

# Hàm sắp xếp công việc theo thời gian tăng dần
def sort_tasks_by_time_ascending(user_id):
    global sort_ascending
    sort_ascending = True
    sort_tasks_by_time(user_id)

# Hàm sắp xếp công việc theo thời gian giảm dần
def sort_tasks_by_time_descending(user_id):
    global sort_ascending
    sort_ascending = False
    sort_tasks_by_time(user_id)

# Hàm sắp xếp công việc theo thời gian và lọc theo user_id
def sort_tasks_by_time(user_id):
    global sort_ascending
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    tasks_with_datetime = []
    for task in tasks:
        try:
            end_time_obj = datetime.datetime.strptime(task['end_time'], "%d-%m-%Y").date()
            end_datetime = datetime.datetime.combine(end_time_obj, datetime.time.max)
            tasks_with_datetime.append((end_datetime, task))
        except ValueError:
            tasks_with_datetime.append((None, task))

    tasks_with_datetime.sort(key=lambda x: x[0], reverse=not sort_ascending)

    # Xóa tất cả các mục cũ trong Treeview
    for item in task_tree.get_children():
        task_tree.delete(item)

    # Thêm các mục đã sắp xếp vào Treeview
    for end_datetime, task in tasks_with_datetime:
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

        task_tree.insert("", tk.END, values=(task_name, time_left_str, "✓" if is_completed else "", "⋮"), iid=task_id)

# Giả sử bạn có user_id của người dùng hiện tại
current_user_id = 1 # Thay 1 bằng user_id thực sự
