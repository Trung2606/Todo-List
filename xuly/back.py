import tkinter as tk
from tkinter import ttk



# Hàm tạo nút back
def create_back_button(toolbar, user_id, is_list_filtered_or_searched):
    back_button = ttk.Button(toolbar, text="<", style="ToolbarButton.TButton", command=lambda: go_back(user_id), width=3)
    if is_list_filtered_or_searched:
        back_button.grid(row=0, column=0, sticky='w')
    else:
        back_button.grid_forget()
    return back_button

# Hàm trở lại trang trước
def go_back(user_id):
    global is_list_filtered_or_searched
    is_list_filtered_or_searched = False
    from xuly.show import show_tasks
    show_tasks(user_id, None)