from db.db import get_db_connection
from tkinter import messagebox
import xuly.show as show #import show.py
from xuly.config import task_menu

def delete_task(user_id):
    print(f"Task ID to delete: {task_menu.task_id}") 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Kiểm tra xem người dùng có quyền xóa công việc hay không (tùy chọn)
        cursor.execute('SELECT user_id FROM tasks WHERE id = ?', (task_menu.task_id,))
        task_user_id = cursor.fetchone()
        if task_user_id and task_user_id[0] != user_id:
            messagebox.showerror("Lỗi", "Bạn không có quyền xóa công việc này.")
            conn.close()
            return

        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_menu.task_id,))
        conn.commit()
        print(f"Rows affected: {cursor.rowcount}")
        if cursor.rowcount > 0:
            messagebox.showinfo("Thông báo", "Công việc đã được xóa thành công!")
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy công việc để xóa.")

        conn.close()
        show.show_tasks(user_id, user_id) 

    except Exception as e:
        print(f"Error deleting task: {e}")
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")