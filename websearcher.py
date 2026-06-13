import requests
import tkinter as tk
from tkinter import messagebox

'''class WebSearcherGUI():
    def mainpage(self):
        global mainpage
        mainpage = tk.Tk()
        mainpage.title("网络文本提取器")
        mainpage.geometry("800x600")
        self.mainpage_text()
        mainpage.mainloop()
        #self.mainpage_text()
        return

    def mainpage_text(self):
        entry1 = tk.Entry(mainpage,width=30,font=("Arial",12),state="normal")
        #search_keyword = entry1.get
        entry1.pack(padx=10,pady=10)
        return'''

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QProgressBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class SimpleBrowser(QMainWindow):
    """一个具有基础功能的简单浏览器类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 1024, 768)

        # 核心网页视图组件
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # 创建导航工具栏
        self.create_navigation_bar()
        
        # 创建状态栏进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.statusBar().addPermanentWidget(self.progress_bar)

        # 连接信号与槽
        self.browser.urlChanged.connect(self.update_url_bar)          # 地址栏随页面变化
        self.browser.titleChanged.connect(self.update_window_title)  # 窗口标题随页面标题变化
        self.browser.loadProgress.connect(self.update_progress)      # 更新加载进度

        # 加载初始页面
        self.load_default_page()

    def create_navigation_bar(self):
        """创建包含前进、后退、刷新、地址栏的工具栏"""
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        # 后退按钮
        back_btn = QAction("◀", self)
        back_btn.setToolTip("Back")
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        # 前进按钮
        forward_btn = QAction("▶", self)
        forward_btn.setToolTip("Forward")
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        # 刷新按钮
        reload_btn = QAction("⟳", self)
        reload_btn.setToolTip("Refresh")
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        # 地址栏输入框
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL and press Enter")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

    def navigate_to_url(self):
        """根据地址栏输入跳转到指定 URL"""
        url_text = self.url_bar.text().strip()
        if not url_text:
            return
        # 自动补全协议（http:// 或 https://）
        if not url_text.startswith("http://") and not url_text.startswith("https://"):
            url_text = "http://" + url_text
        self.browser.setUrl(QUrl(url_text))

    def update_url_bar(self, url):
        """当页面 URL 改变时同步地址栏内容"""
        self.url_bar.setText(url.toString())

    def update_window_title(self, title):
        """当页面标题改变时更新窗口标题"""
        self.setWindowTitle(f"{title} - Simple Browser")

    def update_progress(self, progress):
        """更新加载进度条（progress 范围 0-100）"""
        self.progress_bar.setValue(progress)
        # 加载完成后延迟隐藏进度条（可选）
        if progress >= 100:
            self.progress_bar.setValue(0)  # 重置为0，下次加载时重新显示

    def load_default_page(self):
        """启动时默认加载的主页"""
        self.browser.setUrl(QUrl("https://www.bing.com"))

def main():
    # 启用 QtWebEngine 的必须初始化（PyQt5 中自动处理，但显式调用无妨）
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
if __name__ == "__main__":
    trying_window = WebSearcherGUI()
    trying_window.mainpage()
