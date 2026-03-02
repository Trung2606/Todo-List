import random
import tkinter as tk
import threading
import gpt4all

from db.db import get_today_tasks

model = gpt4all.GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf")

def ask_gpt4all(prompt):
    try:
        response = model.generate(prompt)
        return response
    except Exception as e:
        return f"Lỗi: {e}"

class ChatboxAI(tk.Toplevel):

    def __init__(self, master, user_id):
        super().__init__(master)
        self.user_id = user_id
        self.title("Trợ lý AI (GPT4All)")
        self.geometry("400x500")

        self.chat_area = tk.Text(self, wrap="word", state="disabled")
        self.chat_area.pack(padx=10, pady=10, fill="both", expand=True)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(padx=10, pady=(0, 10), fill="x")

        self.entry = tk.Entry(self.input_frame)
        self.entry.pack(side=tk.LEFT, fill="x", expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.input_frame, text="➤", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        # self.morning_greeting(user_id)

    def send_message(self, event=None):
        user_msg = self.entry.get()
        if not user_msg.strip():
            return
        self.show_message(f"Bạn: {user_msg}")
        self.entry.delete(0, "end")

        threading.Thread(target=self.get_ai_response, args=(user_msg,)).start()

    def get_ai_response(self, user_msg):

        greetings_input = ["xin chào", "chào", "hello", "hi", "chào bạn", "hey", "yo"]
        greetings_response = ["Chào bạn!", "Hello!", "Hi!", "Xin chào!", "Rất vui được gặp bạn!"]

        # Tạo prompt dựa trên yêu cầu của người dùng
        if any(greet in user_msg.lower() for greet in greetings_input):
            response = random.choice(greetings_response)
            self.show_message(f"AI: {response}")
            return
        elif "bạn là ai" in user_msg.lower():
            prompt = "Tôi là trợ lý ảo dùng mô hình GPT4All. Tôi ở đây để hỗ trợ bạn quản lý công việc!"
        elif "liệt kê danh sách công việc" in user_msg.lower():
            prompt = """
            Hãy liệt kê tất cả các công việc trong danh sách.
            - Tên công việc: [Tên công việc]
            """
        elif "thêm công việc mới" in user_msg.lower():
            prompt = """
            Hãy thêm một công việc mới.
            - Tên công việc: [Tên công việc]
            - Mô tả: [Mô tả công việc]
            - Thời gian bắt đầu: [Thời gian bắt đầu]
            - Thời gian kết thúc: [Thời gian kết thúc]
            """
        elif "công việc ưu tiên" in user_msg.lower():
            prompt = """
            Hãy tạo danh sách công việc ưu tiên cho tôi.
            Tôi có các công việc sau:
            - [Thay thế bằng công việc của bạn]
            - [Thay thế bằng công việc của bạn]
            - [Thay thế bằng công việc của bạn]
            ...

            Hãy sắp xếp các công việc này theo mức độ ưu tiên và giải thích lý do cho sự sắp xếp đó.
          """
        
        else:
            prompt = user_msg 

        response = ask_gpt4all(prompt)
        self.show_message(f" AI: {response}")

    def show_message(self, msg):
        self.chat_area.config(state="normal")
        self.chat_area.insert("end", msg + "\n\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see("end")
    
    def morning_greeting(self, user_id):
        tasks = get_today_tasks(user_id)
        num_tasks = len(tasks)

        if num_tasks == 0:
            message = "Chào bạn! Hôm nay bạn không có công việc nào. Nghỉ ngơi thôi 😄"
        else:
            first_task = tasks[0]
            task_name = first_task[0]
            task_time = first_task[1].split("T")[-1] if "T" in first_task[1] else first_task[1]

            message = f"Chào bạn! Hôm nay bạn có {num_tasks} việc. Mình gợi ý bạn bắt đầu với \"{task_name}\" của ngày {task_time}."

        self.show_message(f"AI: {message}")