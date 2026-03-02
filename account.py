import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import hashlib
import secrets

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from db.db import get_db_connection, init_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    return hash_password(password) == hashed_password

def generate_reset_code():
    return secrets.token_hex(6)

def login(email, password):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn:
            cursor = conn.execute(
                'SELECT id, email, password_hash FROM users WHERE email = ?', (email,)
            )
            user = cursor.fetchone()
            if user and verify_password(password, user['password_hash']):
                return user['email']
            else:
                return None
    except sqlite3.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {e}")
        return None
    finally:
        conn.close()

def register(email, password, confirm_password):
    if not email or not password or not confirm_password:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
        return False
    if password != confirm_password:
        messagebox.showerror("Lỗi", "Mật khẩu không khớp.")
        return False
    email_pattern = r"^[a-zA-Z0-9._%+-]+@(gmail\.com|sgu\.edu\.vn)$"
    if not re.match(email_pattern, email):
        messagebox.showerror("Lỗi", "Định dạng email không hợp lệ.\nVui lòng sử dụng @gmail.com hoặc @sgu.edu.vn.")
        return False
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not re.match(password_pattern, password):
        messagebox.showerror("Lỗi", "Mật khẩu không hợp lệ.\nMật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt.")
        return False

    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror("Lỗi", f"Email '{email}' đã tồn tại.")
                return False
            hashed_password = hash_password(password)
            cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hashed_password))
            return True
    except sqlite3.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi đăng ký: {e}")
        return False
    finally:
        conn.close()

def forgot_password(email, new_password):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Lỗi", " ")
                return False
            email_pattern = r"^[a-zA-Z0-9._%+-]+@(gmail\.com|sgu\.edu\.vn)$"
            if not re.match(email_pattern, email):
                messagebox.showerror("Lỗi", "Email không hợp lệ.")
                return False
            password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
            if not re.match(password_pattern, new_password):
                messagebox.showerror("Lỗi", "Mật khẩu phải ít nhất 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt.")
                return False
            hashed_new_password = hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (hashed_new_password, email))
            return True
    except sqlite3.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi đặt lại mật khẩu: {e}")
        return False
    finally:
        conn.close()

def show_account_gui():
    def switch_to_register():
        frame_login.pack_forget()
        frame_register.pack(pady=10)

    def switch_to_login():
        frame_forgot_password.pack_forget()
        frame_register.pack_forget()
        frame_login.pack(pady=10)

    def switch_to_forgot_password():
        frame_login.pack_forget()
        frame_forgot_password.pack(pady=10)

    def do_login():
        email = login_email.get()
        password = login_password.get()
        logged_in_email = login(email, password)
        if logged_in_email:
            messagebox.showinfo("Thành công", f"Chào {logged_in_email}!")
            root.destroy()
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (logged_in_email,))
            user_id = cursor.fetchone()[0]
            conn.close()
            import fake_todo
            fake_todo.main(user_id)
        else:
            messagebox.showerror("Thất bại", "Sai email hoặc mật khẩu.")

    def do_register():
        email = reg_email.get()
        password = reg_password.get()
        confirm_password = reg_confirm_password.get()
        if register(email, password, confirm_password):
            messagebox.showinfo("Thành công", "Đăng ký thành công. Mời bạn đăng nhập.")
            switch_to_login()

    def do_forgot_password():
        email = entry_email.get()
        new_pass = entry_pass.get()

        if forgot_password(email, new_pass):
            messagebox.showinfo("Thành công", "Mật khẩu đã được cập nhật.")
            switch_to_login()

    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("400x300")
    container_frame = tk.Frame(root)
    container_frame.pack(expand=True)

    # Đăng nhập
    frame_login = tk.Frame(container_frame)
    frame_login.pack(pady=10)

    tk.Label(frame_login, text="Đăng Nhập", font=("Arial", 14)).pack(pady=5)

    login_email_frame = tk.Frame(frame_login)
    login_email_frame.pack(pady=3)
    tk.Label(login_email_frame, text="Email:", width=15, anchor='w').pack(side="left")
    login_email = tk.Entry(login_email_frame, width=20)
    login_email.pack(side="left")

    login_pass_frame = tk.Frame(frame_login)
    login_pass_frame.pack(pady=3)
    tk.Label(login_pass_frame, text="Mật khẩu:", width=15, anchor='w').pack(side="left")
    login_password = tk.Entry(login_pass_frame, show="*", width=20)
    login_password.pack(side="left")

    login_button_frame = tk.Frame(frame_login)
    login_button_frame.pack(pady=5)
    tk.Button(login_button_frame, text="Đăng nhập", width=15, command=do_login).grid(row=0, column=0, padx=5)
    tk.Button(login_button_frame, text="Quên mật khẩu", width=15, command=switch_to_forgot_password).grid(row=0, column=1, padx=5)

    tk.Button(frame_login, text="Chưa có tài khoản? Đăng ký", command=switch_to_register).pack(pady=5)

    # Đăng ký
    frame_register = tk.Frame(container_frame)
    tk.Label(frame_register, text="Đăng Ký", font=("Arial", 14)).pack(pady=5)

    reg_email_frame = tk.Frame(frame_register)
    reg_email_frame.pack(pady=3)
    tk.Label(reg_email_frame, text="Email:", width=15, anchor='w').pack(side="left")
    reg_email = tk.Entry(reg_email_frame, width=20)
    reg_email.pack(side="left")

    reg_pass_frame = tk.Frame(frame_register)
    reg_pass_frame.pack(pady=3)
    tk.Label(reg_pass_frame, text="Mật khẩu:", width=15, anchor='w').pack(side="left")
    reg_password = tk.Entry(reg_pass_frame, show="*", width=20)
    reg_password.pack(side="left")

    reg_confirm_pass_frame = tk.Frame(frame_register)
    reg_confirm_pass_frame.pack(pady=3)
    tk.Label(reg_confirm_pass_frame, text="Nhập lại mật khẩu:", width=15, anchor='w').pack(side="left")
    reg_confirm_password = tk.Entry(reg_confirm_pass_frame, show="*", width=20)
    reg_confirm_password.pack(side="left")

    tk.Button(frame_register, text="Đăng ký", width=20, command=do_register).pack(pady=5)
    tk.Button(frame_register, text="Quay lại đăng nhập", command=switch_to_login).pack(pady=2)

    # Quên mật khẩu
    frame_forgot_password = tk.Frame(container_frame)
    tk.Label(frame_forgot_password, text="Quên Mật Khẩu", font=("Arial", 14)).pack(pady=5)
    form_frame = tk.Frame(frame_forgot_password)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Email:", width=15, anchor='w').grid(row=0, column=0, padx=5, pady=3, sticky="w")
    entry_email = tk.Entry(form_frame, width=25)
    entry_email.grid(row=0, column=1, pady=3)

    tk.Label(form_frame, text="Mật khẩu mới:", width=15, anchor='w').grid(row=2, column=0, padx=5, pady=3, sticky="w")
    entry_pass = tk.Entry(form_frame, show="*", width=25)
    entry_pass.grid(row=2, column=1, pady=3)

    tk.Button(frame_forgot_password, text="Đặt lại mật khẩu", width=20, command=do_forgot_password).pack(pady=5)
    tk.Button(frame_forgot_password, text="Quay lại đăng nhập", command=switch_to_login).pack(pady=2)

    frame_login.pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    init_db()
    reset_codes = {}
    show_account_gui()