import tkinter as tk
from tkinter import Menu, ttk

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import openai
from AI.chatbox_ai import ChatboxAI

from db.db import get_db_connection, init_db
# from xuly.add_todo import show_add_task_gui
# from xuly.edit_todo import show_edit_task_gui
from GUI.add_GUI import show_add_task_gui
from GUI.edit_GUI import show_edit_task_gui
from xuly.del_todo import delete_task
from xuly.infor_todo import show_task_details
from xuly.sapxep import sort_tasks_by_time_ascending, sort_tasks_by_time_descending
from xuly.timkiem import search_tasks_by_name, search_tasks_by_time
from xuly.util_todo import show_tasks, show_task_menu
from xuly.config import root, font_style, task_background, task_tree, toolbar, task_menu, filter_menu, sort_menu, add_menu
import account as account # Import account.py

# Hàm cập nhật trạng thái hoàn thành công việc
def toggle_task_completion(task_id, new_value):
    print(f"toggle_task_completion: task_id={task_id}, new_value={new_value}")
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (new_value, task_id))
    conn.commit()
    conn.close()
    show_tasks(current_user_id) # truyền current_user_id

# Hàm xử lý sự kiện click vào Treeview
def on_tree_click(event):
    item = task_tree.identify_row(event.y)
    column = task_tree.identify_column(event.x)
    print(f"on_tree_click: column={column}")
    if item and column == "#3":
        task_id = item
        current_value = task_tree.set(item, "Hoàn thành")
        new_value = 1 if current_value == "" else 0
        task_tree.set(item, "Hoàn thành", "✓" if new_value else "")
        toggle_task_completion(task_id, new_value)
    elif item and column == "#4":
        task_id = item
        show_task_menu(event, task_id)

# Hàm hiển thị dropdown menu
def show_add_menu(event):
    add_menu.delete(0, 'end')
    add_menu.add_command(label="Thêm công việc", command=lambda: show_add_task_gui(current_user_id))

    filter_submenu = Menu(add_menu, tearoff=0)
    filter_submenu.add_command(label="Đã hoàn thành", command=lambda: show_tasks(current_user_id,filter_completed=1))
    filter_submenu.add_command(label="Chưa hoàn thành", command=lambda: show_tasks(current_user_id,filter_completed=0))
    filter_submenu.add_command(label="Tất cả công việc", command=lambda: show_tasks(current_user_id,filter_completed=None))
    add_menu.add_cascade(label="Lọc", menu=filter_submenu)

    sort_submenu = Menu(add_menu, tearoff=0)
    sort_submenu.add_command(label="Tăng dần", command=lambda: sort_tasks_by_time_ascending(current_user_id))
    sort_submenu.add_command(label="Giảm dần", command=lambda: sort_tasks_by_time_descending(current_user_id))
    add_menu.add_cascade(label="Sắp xếp theo thời gian", menu=sort_submenu)

    add_menu.add_command(label="Tìm kiếm theo tên/mô tả", command=search_tasks_by_name)
    add_menu.add_command(label="Tìm kiếm theo thời gian", command=search_tasks_by_time)

    # Thêm nút thoát
    add_menu.add_command(label="Thoát", command=logout_and_return_to_login)

    add_menu.post(event.x_root, event.y_root)

# Hàm xử lý sự kiện xóa công việc
def delete_selected_task(task_id):
    delete_task(current_user_id) 

# Hàm xử lý sự kiện thoát và chuyển về trang đăng nhập
def logout_and_return_to_login():
    root.destroy()
    account.show_account_gui()

# --- Thêm biểu tượng trợ lý AI vào giao diện chính ---
def open_ai_assistant(user_id):
    global chatbox
    if 'chatbox' not in globals() or chatbox.winfo_exists() == 0:
        chatbox = ChatboxAI(root, user_id)
    else:
        chatbox.focus()

# Khởi tạo cửa sổ chính
root.title("To-Do List")
root.geometry("600x500") 
root.configure(bg="#f0f0f0")

# Khởi tạo cơ sở dữ liệu
init_db()

# Tạo ttk Style
style = ttk.Style()
style.configure("Task.TFrame", background="#e0e0e0", borderwidth=1, relief="solid")
style.configure("Task.TLabel", font=font_style)
style.configure("Task.TCheckbutton", font=font_style)
style.configure("AddEdit.TLabel", font=font_style)
style.configure("AddEdit.TEntry", font=font_style)
style.configure("AddEdit.TButton", font=("Arial", 12, "bold"))
style.configure("Details.TFrame", padding=10)
style.configure("ToolbarButton.TButton", font=("Arial", 14, "bold"))

# Thanh công cụ
toolbar.pack(fill='x')


ttk.Label(toolbar, text="Quản lý cá nhân", padding=(15, 0), font=("Arial", 14)).grid(row=0, column=1, sticky='w')
add_button = ttk.Button(toolbar, text="⋮", style="ToolbarButton.TButton", command=lambda: add_menu.post(add_button.winfo_rootx(), add_button.winfo_rooty() + add_button.winfo_height()), width=3)
add_button.grid(row=0, column=2, sticky='e')
add_button.bind("<Button-1>", show_add_menu)

toolbar.columnconfigure(1, weight=1)

# Frame nền cho danh sách công việc 
task_background.pack(pady=10, fill='both', expand=True)

# Tạo style cho Treeview
style = ttk.Style()
style.configure("Treeview", background="#e0e0e0", foreground="black", fieldbackground="white", borderwidth=1, relief="solid")
style.configure("Treeview.Heading", background="#d0d0d0", foreground="black", borderwidth=1, relief="solid")

# Tạo Treeview để hiển thị danh sách công việc
task_tree.heading("Tên Công Việc", text="Tên Công Việc")
task_tree.heading("Thời Gian", text="Thời Gian")
task_tree.heading("Hoàn thành", text="Hoàn thành")
task_tree.heading("Chức Năng", text="")
task_tree.pack(pady=10, padx=5, fill='both', expand=True)

# Tạo checkbox cho cột Trạng Thái
task_tree.column("Hoàn thành", width=50, anchor=tk.CENTER)
task_tree.column("Chức Năng", width=10, anchor=tk.CENTER)
task_tree.bind("<ButtonRelease-1>", on_tree_click)

# Menu cho từng công việc
task_menu.add_command(label="Sửa công việc", command=lambda: show_edit_task_gui(current_user_id))
task_menu.add_command(label="Xóa công việc", command=lambda: delete_task(current_user_id))
task_menu.add_command(label="Thông tin công việc", command=show_task_details)

# Menu lọc công việc
filter_menu.add_command(label="Đã hoàn thành", command=lambda: show_tasks(current_user_id,filter_completed=1)) 
filter_menu.add_command(label="Chưa hoàn thành", command=lambda: show_tasks(current_user_id,filter_completed=0)) 
filter_menu.add_command(label="Tất cả công việc", command=lambda: show_tasks(current_user_id,filter_completed=None)) 

# Menu sắp xếp công việc
sort_menu.add_command(label="Tăng dần", command=sort_tasks_by_time_ascending)
sort_menu.add_command(label="Giảm dần", command=sort_tasks_by_time_descending)

# Tạo frame nhỏ để giữ cố định nút trợ lý
assistant_frame = tk.Frame(root, bg="white")
assistant_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-25)

# Tạo icon trợ lý 🤖
icon = tk.PhotoImage(file="images/robot.png") 



# Hàm main để chạy ứng dụng.
def main(user_id):
    global current_user_id
    current_user_id = user_id
    show_tasks(user_id) 

    # Tạo nút trợ lý bên trong frame
    mascot_btn = tk.Button(assistant_frame, image=icon, command=lambda: open_ai_assistant(user_id), bg="lightblue", bd=0, relief="flat")
    mascot_btn.image = icon
    mascot_btn.pack()

     # Luôn tạo ChatboxAI mỗi lần mở app
    chatbox = ChatboxAI(root, user_id) 
    chatbox.after(1000, chatbox.morning_greeting(user_id))

    root.mainloop()