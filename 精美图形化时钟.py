#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精美图形化时钟 - 多功能现代化时钟
具有多种主题、动画效果和实用功能
['苹方_中等', '@苹方_中等', '苹方_常规', '@苹方_常规', '苹方_粗体', '@苹方_粗体', 
'苹方_特粗', '@苹方_特粗', '苹方_细体', '@苹方_细体', '苹方_特细', '@苹方_特细']
"""

import tkinter as tk
from tkinter import font
from datetime import datetime
import time

class BeautifulClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("刘朴迪")
        self.root.geometry("500x350")
        
        # 初始化设置
        self.theme_index = 0
        self.is_24h = True
        self.is_topmost = True
        self.show_seconds = True
        
        # 定义主题
        self.themes = [
            {
                'name': '深色科技',
                'bg': '#0d1b2a',
                'time_fg': '#00ff9d',
                'date_fg': '#4cc9f0',
                'info_fg': '#adb5bd'
            },
            {
                'name': '浅色简约',
                'bg': "#26313B",
                'time_fg': '#0077b6',
                'date_fg': '#0096c7',
                'info_fg': '#495057'
            },
            {
                'name': '紫色梦幻',
                'bg': '#1a1a2e',
                'time_fg': '#9d4edd',
                'date_fg': '#c77dff',
                'info_fg': '#e0aaff'
            },
            {
                'name': '蛋黄饼模式'
                '',
                'bg': '#2d2d2d',
                'time_fg': '#ff9e00',
                'date_fg': '#ffd166',
                'info_fg': '#fefae0'
            }
        ]
        
        # 应用初始主题
        self.apply_theme()
        
        # 窗口置顶
        self.root.attributes('-topmost', self.is_topmost)
        
        # 创建界面
        self.create_widgets()
        
        # 居中显示
        self.center_window()
        
        # 开始时钟
        self.update_clock()
        
        # 启动淡入动画
        self.fade_in()
    
    def apply_theme(self):
        """应用当前主题"""
        theme = self.themes[self.theme_index]
        self.current_bg = theme['bg']
        self.current_time_fg = theme['time_fg']
        self.current_date_fg = theme['date_fg']
        self.current_info_fg = theme['info_fg']
        self.root.configure(bg=self.current_bg)
    
    def create_widgets(self):
        """创建所有界面组件"""
        # 主容器
        main_container = tk.Frame(self.root, bg=self.current_bg)
        main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(
            main_container,
            text="刘朴迪",
            font=('苹方_常规', 16),
            fg=self.current_info_fg,
            bg=self.current_bg
        )
        title_label.pack(pady=(0, 20))
        
        # 时间显示框架
        time_frame = tk.Frame(main_container, bg=self.current_bg)
        time_frame.pack(expand=True)
        
        # 时间标签
        self.time_label = tk.Label(
            time_frame,
            text="00:00:00",
            font=('苹方_特粗', 96),
            fg=self.current_time_fg,
            bg=self.current_bg
        )
        self.time_label.pack()
        
        # 日期标签
        self.date_label = tk.Label(
            time_frame,
            text="2026年01月01日 星期一",
            font=('苹方_常规', 20),
            fg=self.current_date_fg,
            bg=self.current_bg
        )
        self.date_label.pack(pady=10)
        
        # 控制面板
        control_frame = tk.Frame(main_container, bg=self.current_bg)
        control_frame.pack(pady=20)
        
        # 主题切换按钮
        theme_btn = tk.Button(
            control_frame,
            text=f"切换主题 ({self.themes[self.theme_index]['name']})",
            command=self.next_theme,
            bg='#4361ee',
            fg='white',
            font=('苹方_常规', 15),
            relief='flat',
            padx=15,
            pady=8
        )
        theme_btn.grid(row=0, column=0, padx=5)
        
        # 时间格式按钮
        self.format_btn = tk.Button(
            control_frame,
            text="24小时制",
            command=self.toggle_format,
            bg='#4cc9f0',
            fg='white',
            font=('苹方_常规', 15),
            relief='flat',
            padx=15,
            pady=8
        )
        self.format_btn.grid(row=0, column=1, padx=5)
        
        # 秒显示按钮
        self.seconds_btn = tk.Button(
            control_frame,
            text="显示秒",
            command=self.toggle_seconds,
            bg='#7209b7',
            fg='white',
            font=('苹方_常规', 15),
            relief='flat',
            padx=15,
            pady=8
        )
        self.seconds_btn.grid(row=0, column=2, padx=5)
        
        # 置顶按钮
        self.topmost_btn = tk.Button(
            control_frame,
            text="取消置顶",
            command=self.toggle_topmost,
            bg="#ff3791",
            fg='white',
            font=('苹方_常规', 15),
            relief='flat',
            padx=15,
            pady=8
        )
        self.topmost_btn.grid(row=0, column=3, padx=5)
        
        # 信息栏
        info_frame = tk.Frame(main_container, bg=self.current_bg)
        info_frame.pack()
        
        info_label = tk.Label(
            info_frame,
            text="ESC退出 | 空格切换主题 | F1切换格式 | F2切换秒显示",
            font=('苹方_常规', 9),
            fg=self.current_info_fg,
            bg=self.current_bg
        )
        info_label.pack()
        
        # 绑定键盘事件
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.bind('<space>', lambda e: self.next_theme())
        self.root.bind('<F1>', lambda e: self.toggle_format())
        self.root.bind('<F2>', lambda e: self.toggle_seconds())
        
        # 存储按钮引用以便更新
        self.theme_button = theme_btn
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def fade_in(self):
        """淡入动画效果"""
        alpha = 0.0
        def increase_alpha():
            nonlocal alpha
            alpha += 0.05
            if alpha <= 1.0:
                try:
                    self.root.attributes('-alpha', alpha)
                    self.root.after(30, increase_alpha)
                except:
                    pass
        
        self.root.attributes('-alpha', 0.0)
        increase_alpha()
    
    def update_clock(self):
        """更新时钟显示"""
        now = datetime.now()
        
        # 格式化时间
        if self.is_24h:
            if self.show_seconds:
                time_str = now.strftime("%H:%M:%S")
            else:
                time_str = now.strftime("%H:%M")
        else:
            if self.show_seconds:
                time_str = now.strftime("%I:%M:%S %p")
            else:
                time_str = now.strftime("%I:%M %p")
        
        # 格式化日期
        date_str = now.strftime("%Y年%m月%d日 %A")
        
        # 更新显示
        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)
        
        # 每秒更新
        self.root.after(1000, self.update_clock)
    
    def next_theme(self):
        """切换到下一个主题"""
        self.theme_index = (self.theme_index + 1) % len(self.themes)
        self.apply_theme()
        
        # 更新所有组件的颜色
        for widget in [self.time_label, self.date_label]:
            widget.config(bg=self.current_bg, fg=self.current_time_fg)
        
        self.date_label.config(fg=self.current_date_fg)
        
        # 更新按钮文本
        self.theme_button.config(text=f"切换主题 ({self.themes[self.theme_index]['name']})")
    
    def toggle_format(self):
        """切换12/24小时制"""
        self.is_24h = not self.is_24h
        self.format_btn.config(text="12小时制" if self.is_24h else "24小时制")
    
    def toggle_seconds(self):
        """切换秒显示"""
        self.show_seconds = not self.show_seconds
        self.seconds_btn.config(text="隐藏秒" if self.show_seconds else "显示秒")
    
    def toggle_topmost(self):
        """切换窗口置顶"""
        self.is_topmost = not self.is_topmost
        self.root.attributes('-topmost', self.is_topmost)
        self.topmost_btn.config(text="窗口置顶" if not self.is_topmost else "取消置顶")
    
    def run(self):
        """运行时钟"""
        self.root.mainloop()

def main():
    """主函数"""
    clock = BeautifulClock()
    clock.run()

if __name__ == "__main__":
    main()