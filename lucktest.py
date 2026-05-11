import random
import tkinter as tk
from tkinter import messagebox

class AllPage:
    def __init__(self, parent=None):
        # 保存主窗口引用，用于创建子窗口
        self.parent = parent
        self.result = 0
        self.label2_text = ""

    def random_maker(self):
        return int(random.random() * 100 + 1)

    def button1_pressed(self):
        self.result = self.random_maker()
        self.label1.config(text=f"你的今日人品是：{self.result}")
        self.label2_text = self.suggester()
        self.label2.config(text=self.label2_text)

    def suggester(self):
        if self.result >= 90:
            text = "欧皇转世！！！"
            self.luck_window()
        elif self.result >= 60:
            text = "还算幸运！"
        elif self.result >= 30:
            text = "其实还好啦……"
        else:
            text = "emm……这是百分制哦"
        return text

    def luck_window(self):
        # 确定正确的父窗口：如果有传入的 parent 就用它，否则用自己创建的根窗口
        master = self.parent if self.parent else self.root
        luck = tk.Toplevel(master)
        luck.title("隐藏款！！！")
        luck.geometry("200x100")
        label3 = tk.Label(luck, text=f"🎉恭喜你，人品达到{self.result}")
        label3.pack(pady=5)

        def close_luck():
            luck.destroy()

        def close_all():
            luck.destroy()
            self.root.destroy()

        tk.Button(luck, text="心满意足", command=close_all).pack(pady=2)
        tk.Button(luck, text="激流勇进", command=close_luck).pack(pady=2)

    def mainpage(self):
        if self.parent is None:
            # 独立运行模式：创建自己的 Tk 根窗口
            self.root = tk.Tk()
        else:
            # 作为子模块调用：依附于主窗口
            self.root = tk.Toplevel(self.parent)
            messagebox.showinfo("刘朴迪提示","注意：隐藏提示可能不置顶！")

        self.root.title("今日人品生成器")
        self.root.geometry("400x300")
        self.root.attributes('-topmost', True)

        button1 = tk.Button(self.root, text="今日人品", command=self.button1_pressed)
        button1.pack(pady=20)

        self.label1 = tk.Label(self.root, text="")
        self.label1.pack(pady=20)

        self.label2 = tk.Label(self.root, text="")
        self.label2.pack()

        # 只有独立运行时才需要进入主循环
        if self.parent is None:
            self.root.mainloop()

if __name__ == "__main__":
    app = AllPage()
    app.mainpage()