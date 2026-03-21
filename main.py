import tkinter as tk
from tkinter import messagebox
import random
import lucktest
import websearcher

#tk._debug=True

'''
实现主窗口
'''

class Mainloop():
    @classmethod

    def remind(self):
        messagebox.showinfo("提示","该功能尚未完成")

    def rootpage(self):
        page = lucktest.AllPage()
        rootpage = tk.Tk()
        rootpage.title("常用功能整合包 0.0.1")
        rootpage.geometry("400x300")
        rootpage.resizable(True,True)
        button1 = tk.Button(rootpage,text="今日人品",command=page.mainpage)
        button1.pack(padx=10)
        button2 = tk.Button(rootpage,text = "请求网络内容",command=self.remind)
        button2.pack()
        rootpage.mainloop()
        return
    
if __name__ == "__main__":
    man = Mainloop()
    man.rootpage()

