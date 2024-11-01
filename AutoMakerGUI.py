import tkinter as tk
from tkinter import messagebox

import tkinter as tk
from tkinter import messagebox

def on_button_click():
    messagebox.showinfo("信息", "按钮被点击了！")

# 创建主窗口
root = tk.Tk()
root.title("简单的GUI程序")
root.geometry("720x480")



# 创建标签
label = tk.Label(root, text="这是一个标签")
label.pack(pady=10)

# 创建按钮
button = tk.Button(root, text="点击我", command=on_button_click)
button.pack(pady=10)

# 运行主事件循环
root.mainloop()

