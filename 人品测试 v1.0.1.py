# -*- coding: utf-8 -*-
#import math 
import random
import tkinter as tk

def random_maker():
    value = int(random.random() * 100 + 1)
    return value

def button1_pressed():
    #result = 0
    #lebal2_text_glo = 0
    global result
    global lebal2_text_glo
    result = random_maker()
    label1.config(text=f"你的今日人品是：{result}")
    lebal2_text_glo = suggester()
    label2.config(text=lebal2_text_glo)
    return

def close_all():
    luck.destroy()
    root.quit()
    return

def close_luck():
    luck.destroy()
    return

def luck_window():
    global luck
    luck = tk.Tk()
    luck.title("隐藏款！！！")
    luck.geometry("200x100")
    label3 = tk.Label(luck,text=f"🎉恭喜你，人品达到{result}")
    label3.pack(pady=5)
    button2 = tk.Button(luck,text="心满意足",command=close_all)
    button2.pack(padx=5)
    button3 = tk.Button(luck,text="激流勇进",command=close_luck)
    button3.pack()

root = tk.Tk()
root.title("今日人品生成器")
root.geometry("400x300")
button1 = tk.Button(root,text="今日人品",command=button1_pressed)
button1.pack(pady=20)
label1 = tk.Label(root,text=None)
label1.pack(pady=20)

def suggester():
    if result >= 90:
        lebal2_text = str("欧皇转世！！！")
        luck_window()
    elif result >= 60:
        lebal2_text = str("还算幸运！")
    elif result >= 30:
        lebal2_text = ("其实还好啦……")
    else:
        lebal2_text = ("emm……这是百分制哦")
    return lebal2_text

label2 = tk.Label(root,text=None)
label2.pack()

root.mainloop()
