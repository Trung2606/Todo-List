import tkinter as tk
from tkinter import font, Menu, ttk

# Khởi tạo cửa sổ chính
root = tk.Tk()

# Font chữ đẹp
font_style = font.Font(family="Helvetica", size=12)

# Thanh công cụ
toolbar = ttk.Frame(root)

# Frame nền cho danh sách công việc (định nghĩa trước khi sử dụng)
task_background = ttk.Frame(root, style="Task.TFrame")

# Tạo Treeview để hiển thị danh sách công việc
task_tree = ttk.Treeview(task_background, columns=("Tên Công Việc", "Thời Gian", "Hoàn thành", "Chức Năng"), show="headings", style="Treeview")

# Menu dropdown
add_menu = Menu(root, tearoff=0)

# Menu cho từng công việc
task_menu = Menu(root, tearoff=0)

# Menu lọc công việc
filter_menu = Menu(root, tearoff=0)

# Menu sắp xếp công việc
sort_menu = Menu(root, tearoff=0)
