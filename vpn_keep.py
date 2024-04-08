#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/8 9:20
# @Author  : syy
# @File    : vpn_keep.py
# @Software: PyCharm
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from requests.exceptions import Timeout
import tkinter as tk
import requests,time,threading,pystray,ctypes


class application(Frame):
    """一个内置gui的写法"""

    def __init__(self, master,web_url="http://10.12.117.3/xtbg/index.htm"):
        super().__init__(master)
        self.master = master
        self.website_url = web_url
        self.configure(bg="#ADD8E6")  # 设置窗口背景颜色为淡蓝色
        self.pack()
        self.clicked = False  #判断按钮是否被点击
        menu = pystray.Menu(
            pystray.MenuItem("显示", self.show_window,default=True),
            pystray.MenuItem("退出", self.on_exit),
        )
        # 判断图标
        self.set_icon = False
        self.message_count = 0  # 计数器，用于清除第一条信息
        self.creat_widget() # 引用下面的creatwidgwt函数

    def creat_widget(self):
        """创建组件"""
        self.btn01 = Button(self)
        self.btn01["text"] = "开始"
        self.btn01["command"] = self.keep_status
        self.btn01.place(x=10, y=10,width=44,height=30)
        """创建第二个按钮"""
        self.btn02 = Button(self,text="状态",command=self.check_staus)
        self.btn02.pack()
        self.btn02.place(x=60,y=10,width=44,height=30)
        """创建第三个按钮"""
        self.btn03 = Button(self, text="最小化", command=self.mini_mize)
        self.btn03.pack()
        self.btn03.place(x=110, y=10, width=44, height=30)
        """创建第四个按钮"""
        self.btn04 = Button(self, text="清除", command=self.clear_status)
        self.btn04.pack()
        self.btn04.place(x=160, y=10, width=44, height=30)
        """创建一个退出按钮"""
        self.btnquit = Button(self, text="退出", command=root.destroy)
        self.btnquit.pack(side='right')
        self.btnquit.place(x=210, y=10, width=44, height=30)
        """创建一个标签"""
        self.label = tk.Label(self, text="Design By yangyang")
        self.label.pack()
        self.label.place(x=330,y=10,width=140, height=30)
        self.label.config(bg="#ADD8E6",bd=0)
        """创建第二个标签"""
        self.label = tk.Label(self, text="友情提示：点击按钮开始，结束点击退出即可，5min输出一次状态信息 \n 代码200为正常运行 最终解释权归syy所有 \n 显示状态信息即运行正常~" )
        self.label.pack()
        self.label.place(x=10, y=240, width=580, height=60)
        self.label.config(bg="#ADD8E6",bd=5)
        """创建文本框"""
        self.text_box = tk.Text(self,wrap=tk.WORD)
        self.text_box.pack()
        self.text_box.place(x=10, y=50, width=580, height=180)
        self.text_box.config(bg="#ADD8E6")
        self.text_box.config(state="disable")

        # 开始访问网站
    def visit_website(self):
        try:
            headers={
               "User - Agent":"Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 123.0.0.0 Safari / 537.36 Edg / 123.0.0.0"
            }
            response = requests.get(url=self.website_url, headers=headers,timeout=5)
            status_code = response.status_code
            if status_code == 200:
                message = f"在 {time.strftime('%Y-%m-%d %H:%M:%S')} 访问网站成功 - 状态码: {status_code}"
                return message
            else:
                message = f"在 {time.strftime('%Y-%m-%d %H:%M:%S')} 访问网站成失败 - 状态码: {status_code}"
                return message
        except Timeout:
            message = "超时: 访问网站失败，请求超时，请先登录VPN。"
            return message
        except Exception as e:
            message = f"程序报错: {str(e)}，请联系yangyang"
            return message
        self.text_box.config(state="normal")
        self.text_box.insert(tk.END, message+ "\n")
        self.text_box.config(state="disabled")

    def update_status(self):
        global count # 全局变量
        status = self.visit_website()
        self.text_box.config(state="normal")  # 设置文本框为可编辑状态
        self.text_box.insert(tk.END, status + "\n")
        self.text_box.see(tk.END)
        self.message_count += 1
        if self.message_count >= 10:
            self.clear_first_message()
        self.text_box.config(state="disabled")  # 设置文本框为不可编辑状态
        root.after(interval * 1000, self.update_status)  # 每隔interval秒更新一次状态
    def clear_first_message(self):
        self.text_box.config(state="normal")
        self.text_box.delete('1.0', '2.0')
        self.text_box.config(state="disabled")
    def keep_status(self):
        if not self.clicked:  # 如果按钮未被点击过
            update_status_thread = threading.Thread(target=self.update_status)
            update_status_thread.daemon = True
            update_status_thread.start()
            self.clicked= True
        else:
                self.tishi_info()
        # 弹窗
    def tishi_info(self):
        messagebox.showinfo("提示","程序已经运行啦")

    def clear_info(self):
        messagebox.showinfo("info", "success")
        # 清除信息
    def check_staus(self):
        if not self.clicked:
            messagebox.showinfo("提示", "请先点击开始运行程序")
        else:
            messagebox.showinfo("提示", "程序已经运行啦")
    def clear_status(self):
        self.text_box.config(state="normal")
        self.text_box.delete('1.0', tk.END)
        self.text_box.config(state="disable")
    def mini_mize(self):
        # 隐藏窗口
        self.master.withdraw()
        image = Image.open("ico/yang.ico")
        if self.set_icon == False:
            self.set_icon = True
            menu = pystray.Menu(
                pystray.MenuItem("显示", self.show_window, default=True),
                pystray.MenuItem("退出", self.on_exit),
            )
            self.icon = pystray.Icon("yangyang", image, "yangyang", menu)
        else:
            return
        threading.Thread(target=self.icon.run, daemon=True).start()

    def on_exit(self, icon, item):
        # 处理退出事件的代码
        icon.stop()
        self.master.destroy()
    def show_window(self, icon, item):
        # 显示窗口
        self.master.deiconify()
        self.master.update()
        time.sleep(0.5)

if __name__ == '__main__':
    root = Tk()
    root.geometry("600x300+660+390")
    root.title("中交集团Atrust存活工具 ------ Design By yangyang".center(10))
    root.iconbitmap('ico/yang.ico')
    root.resizable(False, False)  # 禁止调整窗口大小
    interval = 300


    app = application(master=root)
    app.pack_propagate(False)  # 禁止Frame自动调整大小
    app.pack(fill="both", expand=True)  # 将Frame填充到整个窗口

    root.mainloop()
# pyinstaller -D -w --version-file=vpn_keep_info.txt -i yang.ico vpn_keep.py