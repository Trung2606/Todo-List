import sqlite3
import tkinter as tk
from tkinter import messagebox
import datetime
from datetime import date

# Hàm kết nối tới cơ sở dữ liệu
def get_db_connection():
    """Establishes a database connection."""
    try:
        conn = sqlite3.connect('todo.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return None

def init_db():
    """Initializes the database tables."""
    try:
        conn = get_db_connection()
        if not conn:
            return

        with conn:  # Use context manager for connection
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL ,
                    reset_code TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT NOT NULL,
                    description TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    is_completed INTEGER DEFAULT 0,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
    except sqlite3.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khởi tạo cơ sở dữ liệu: {e}")
    finally:
        if conn:
            conn.close()

def get_today_tasks(user_id):
    conn = get_db_connection()
    c = conn.cursor()

    today = date.today().strftime("%d-%m-%Y")

    c.execute('''
        SELECT task_name, start_time FROM tasks
        WHERE start_time = ?
        AND is_completed = 0
        AND user_id = ?
    ''', (today, user_id))

    tasks = c.fetchall()
    conn.close()
    return tasks

# Nếu có công việc thì sẽ nhắc nhở
if __name__ == "__main__":
    # Thay thế 1 bằng user_id thực tế từ đăng nhập hoặc nơi khác
    current_user_id = 1

    today_tasks = get_today_tasks(current_user_id)
    if today_tasks:
        print("Các công việc của ngày hôm nay:")
        for task in today_tasks:
            print(f"  - Tên: {task['task_name']}, Bắt đầu: {task['start_time']}")
    else:
        print("Không có công việc nào cho ngày hôm nay.")