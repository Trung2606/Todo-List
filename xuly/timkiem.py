import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import unicodedata

from db.db import get_db_connection
from xuly.config import root, task_tree, toolbar
# from xuly.back import create_back_button


current_user_id = 1

# Hàm tìm kiếm công việc theo tên/mô tả
def search_tasks_by_name():
    search_name_window = tk.Toplevel(root)
    search_name_window.title("Tìm kiếm theo tên công việc")

    button_frame = ttk.Frame(search_name_window)
    button_frame.pack(pady=10)

    # Đặt nhãn và ô nhập liệu vào cùng một hàng
    ttk.Label(button_frame, text="Nhập tên công việc:", style="AddEdit.TLabel").grid(row=0, column=0, sticky='w', padx=5)
    search_entry = ttk.Entry(button_frame)
    search_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=5)

    def search_tasks_local():  # Tạo hàm cục bộ để gọi search_tasks
        search_tasks(search_entry)  # Gọi search_tasks với search_entry

    ttk.Button(button_frame, text="Tìm kiếm", command=search_tasks_local, style="AddEdit.TButton").grid(row=1, column=0, sticky='ew', pady=5, padx=5)
    ttk.Button(button_frame, text="Hủy", command=search_name_window.destroy, style="AddEdit.TButton").grid(row=1, column=1, sticky='ew', pady=5, padx=5)

# Hàm tìm kiếm công việc theo tên/mô tả (định nghĩa bên ngoài search_tasks_by_name)
def search_tasks(entry_widget):
    global is_on_main_page
    is_on_main_page = False
    global is_filtered_or_searched
    is_filtered_or_searched = True

    search_term = unicodedata.normalize('NFC', entry_widget.get())  # Chuẩn hóa Unicode
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks WHERE task_name LIKE ? AND user_id = ?", ('%' + search_term + '%', current_user_id)).fetchall()  # Thêm user_id vào truy vấn
    conn.close()
    
    # Xóa tất cả các mục cũ trong Treeview
    for item in task_tree.get_children():
        task_tree.delete(item)

    # Thêm các mục tìm kiếm vào Treeview
    for task in tasks:
        task_id = task['id']
        task_name = task['task_name']
        is_completed = task['is_completed']
        end_time = task['end_time']

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
        else:
            time_left_str = "Không có thời hạn"

        task_tree.insert("", tk.END, values=(task_name, time_left_str, "✓" if is_completed else "", "⋮"), iid=task_id)

    # Đóng cửa sổ tìm kiếm
    entry_widget.winfo_toplevel().destroy()
    # Nút "<"
    # update_back_button()
    from xuly.back import create_back_button
    create_back_button(toolbar, current_user_id, is_filtered_or_searched)

def search_tasks_by_time():
    search_time_window = tk.Toplevel(root)
    search_time_window.title("Tìm kiếm theo thời gian")

    ttk.Label(search_time_window, text="Chọn khoảng thời gian tìm kiếm:", style="AddEdit.TLabel").pack(pady=5)

    # Frame chứa ngày bắt đầu và kết thúc
    date_frame = ttk.Frame(search_time_window)
    date_frame.pack(pady=5)

    # Ngày bắt đầu
    ttk.Label(date_frame, text="Từ ngày:", style="AddEdit.TLabel").pack(side=tk.LEFT, padx=5)
    start_date_entry = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
    start_date_entry.pack(side=tk.LEFT, padx=5)

    # Ngày kết thúc
    ttk.Label(date_frame, text="Đến ngày:", style="AddEdit.TLabel").pack(side=tk.LEFT, padx=5)
    end_date_entry = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
    end_date_entry.pack(side=tk.LEFT, padx=5)

    # Tạo frame chứa nút
    button_frame = ttk.Frame(search_time_window)
    button_frame.pack(pady=10)

    # Nút Tìm kiếm
    ttk.Button(button_frame, text="Tìm kiếm", command=lambda: search_time(start_date_entry, end_date_entry, search_time_window), style="AddEdit.TButton").pack(side=tk.LEFT, padx=5)
    # Nút Hủy
    ttk.Button(button_frame, text="Hủy", command=search_time_window.destroy, style="AddEdit.TButton").pack(side=tk.LEFT, padx=5)

def search_time(start_date_entry, end_date_entry, window):
    global is_on_main_page
    is_on_main_page = False
    global is_filtered_or_searched
    is_filtered_or_searched = True

    start_date = start_date_entry.get_date().strftime("%d-%m-%Y")
    end_date = end_date_entry.get_date().strftime("%d-%m-%Y")

    print(f"Tìm kiếm từ {start_date} đến {end_date}")

    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks WHERE end_time >= ? AND end_time <= ? AND user_id = ?", (start_date, end_date, current_user_id)).fetchall()  # Thêm user_id vào truy vấn
    conn.close()

    print(f"Tìm thấy {len(tasks)} công việc")

    for item in task_tree.get_children():
        task_tree.delete(item)

    for task in tasks:
        task_id = task['id']
        task_name = task['task_name']
        is_completed = task['is_completed']
        end_time = task['end_time']
        time_left_str = "Không có thời hạn"

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

    # Đóng cửa sổ tìm kiếm
    window.destroy()
    # Nút "<"
    # update_back_button()
    from xuly.back import create_back_button
    create_back_button(toolbar, current_user_id, is_filtered_or_searched)