import requests
import tkinter as tk
from tkinter import messagebox

class WebSearcherGUI():
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
        return
    
if __name__ == "__main__":
    trying_window = WebSearcherGUI()
    trying_window.mainpage()
