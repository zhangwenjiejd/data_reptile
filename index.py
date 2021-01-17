#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pickle
from tkinter.filedialog import asksaveasfilename

from PIL import Image,ImageTk

from jd.JdSeacher import JdSearcher
from utils.file_util import ExcelUtil


class tmal():
    def __init__(self, ):
        self.window = tk.Tk()
        self.window.title('信息采集系统')

    def login(self):
        # 获取屏幕宽度和高度
        self.scn_w, self.scn_h = self.window.maxsize()
        # 计算中心坐标
        self.cen_x = (self.scn_w - 300) / 3
        self.cen_y = (self.scn_h - 300) / 3

        # 设置窗口初始大小和位置
        self.size_xy = '%dx%d+%d+%d' % (460, 400, self.cen_x, self.cen_y)
        self.window.geometry(self.size_xy)  # 设置窗口坐标
        self.window.wm_attributes('-topmost', 1)  # 窗口置顶
        self.window.attributes('-alpha',0.9)

        # 画布放置图片
        self.canvas = tk.Canvas(self.window, height=400, width=500)
        self.im = Image.open("d:/lytmal/image/2.png")
        self.imagefile = ImageTk.PhotoImage(self.im)
        # imagefile=tk.PhotoImage(file='71.gif')
        image = self.canvas.create_image(0, 0, anchor='nw', image=self.imagefile)
        self.canvas.pack(side='top')
        # 标签 用户名密码
        tk.Label(self.window, text='用户名:').place(x=100, y=150)
        tk.Label(self.window, text='密码:').place(x=100, y=190)
        # 用户名输入框
        self.var_usr_name = tk.StringVar()
        entry_usr_name = tk.Entry(self.window, textvariable=self.var_usr_name)
        entry_usr_name.place(x=160, y=150)
        # 密码输入框
        self.var_usr_pwd = tk.StringVar()
        entry_usr_pwd = tk.Entry(self.window, textvariable=self.var_usr_pwd, show='*')
        entry_usr_pwd.place(x=160, y=190)

        # 登录 注册按钮
        bt_login = tk.Button(self.window, text='登录', command=self.usr_log_in)
        bt_login.place(x=140, y=230)
        # bt_logup = tk.Button(self.window, text='注册', command=self.usr_sign_up)
        # bt_logup.place(x=210, y=230)
        bt_logquit = tk.Button(self.window, text='退出', command=self.usr_sign_quit)
        bt_logquit.place(x=280, y=230)
    #登录函数
    def usr_log_in(self):

        #输入框获取用户名密码
        usr_name=self.var_usr_name.get()
        usr_pwd=self.var_usr_pwd.get()
        #从本地字典获取用户信息，如果没有则新建本地数据库
        try:
            with open('usr_info.pickle','rb') as usr_file:
                usrs_info=pickle.load(usr_file)
        except FileNotFoundError:
            with open('usr_info.pickle','wb') as usr_file:
                usrs_info={'admin':'admin'}
                pickle.dump(usrs_info,usr_file)
        #判断用户名和密码是否匹配
        if usr_name in usrs_info:
            if usr_pwd == usrs_info[usr_name]:
                self.show_info()
            else:
                tk.messagebox.showerror(message='密码错误')
        #用户名密码不能为空
        elif usr_name=='' or usr_pwd=='' :
            tk.messagebox.showerror(message='用户名或密码为空')
        #不在数据库中弹出是否注册的框
        else:
            self.window.wm_attributes('-topmost',0)
            tk.messagebox.showinfo('欢迎','您还没有注册请联系管理员')
            # is_signup=tk.messagebox.askyesno('欢迎','您还没有注册，是否现在注册')
            # if is_signup:
            #     self.usr_sign_up()
    #登陆成功展示函数
    def show_info(self):
        #新建登陆成功界面
        self.window.withdraw()
        self.window_info_up=tk.Toplevel(self.window)
        size_xy = '%dx%d+%d+%d' % (800, 650, self.cen_x, self.cen_y)
        self.window_info_up.geometry(size_xy)  #设置窗口坐标
        self.window_info_up.wm_attributes('-topmost',1)# 窗口置顶
        self.window_info_up.title('欢迎使用信息采集系统')
        self.window_info_up.attributes('-alpha', 0.9)

        #画布放置图片
        self.canvas=tk.Canvas(self.window_info_up,height=800,width=850)
        self.im=Image.open("d:/lytmal/image/5.jpg")
        self.imagefile=ImageTk.PhotoImage(self.im)
        # imagefile=tk.PhotoImage(file='71.gif')
        self.canvas.create_image(0,0,anchor='nw',image=self.imagefile)
        self.canvas.pack(side='top')

        tk.Label(self.window_info_up, text='搜索信息').place(x=25, y=20)
        tk.Label(self.window_info_up, text='搜索页码').place(x=245, y=20)
        tk.Label(self.window_info_up, text='间隔时间').place(x=465, y=20)

        self.searchinfo = tk.StringVar()
        searchinfoinput = tk.Entry(self.window_info_up,textvariable=self.searchinfo,width=10)
        searchinfoinput.place(x=90, y=20)

        self.pagenum = tk.StringVar()
        pagenuminput=tk.Entry(self.window_info_up,textvariable=self.pagenum,width=10)
        pagenuminput.place(x=310, y=20)

        self.delayTime=tk.StringVar()
        delayTimeinput=tk.Entry(self.window_info_up,textvariable=self.delayTime , width=10)
        delayTimeinput.place(x=530, y=20)

        self.flag=False

        ck1 = tk.Checkbutton(self.window_info_up, text='是否展示全部数据', command=self.click_1)
        ck1.place(x=635,y=18)

        scrollbar = tk.Scrollbar(self.window_info_up)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bt_start = tk.Button(self.window_info_up, text='开始采集', command=self.excute)
        bt_start.place(x=30, y=500)

        bt_stop = tk.Button(self.window_info_up, text='停止采集', command=self.stop)
        bt_stop.place(x=130, y=500)

        bt_clear = tk.Button(self.window_info_up, text='清空记录', command=self.delButton)
        bt_clear.place(x=230, y=500)

        # bt_logquit = tk.Button(self.window_info_up, text='退出', command=self.usr_sign_quit)
        # bt_logquit.place(x=720, y=10)

        bt_export = tk.Button(self.window_info_up, text='数据导出', command=self.export)
        bt_export.place(x=330, y=500)
        if self.var_usr_name.get() == 'admin':
            bt_export = tk.Button(self.window_info_up, text='添加用户', command=self.usr_sign_up)
            bt_export.place(x=430, y=500)

        self.scrollbar = tk.Scrollbar(self.window_info_up )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        title = ['1', '2', '3','4', ]
        self.box = ttk.Treeview(self.window_info_up, columns=title,height = 20,
                                yscrollcommand=self.scrollbar.set,
                                show='headings')

        self.box.column('1', width=300, anchor='center')
        self.box.column('2', width=150, anchor='center')
        self.box.column('3', width=150, anchor='center')
        self.box.column('3', width=150, anchor='center')
        self.box.heading('1', text='店铺名称')
        self.box.heading('2', text='电话1')
        self.box.heading('3', text='电话2')
        self.box.heading('4', text='电话3')

        # 对象处理
        self.box.pack(fill=tk.BOTH)
        self.box.place(x=10, y=60)

        self.window_info_up.protocol("WM_DELETE_WINDOW", self.callback)
        self.window_info_up.mainloop()

    def click_1(self):
        self.flag = True

    def callback(self):
        self.window.destroy()

    def excute(self):
        self.service = JdSearcher(self.searchinfo.get(),self.box,self.flag,self.pagenum.get(),self.delayTime.get())
        self.service.start()

    def stop(self):
        self.service.stop()

    def delButton(self):
        x = self.box.get_children()
        for item in x:
            self.box.delete(item)

    def export(self):
        items = self.box.get_children()
        self.file_opt = options = {}
        options['defaultextension'] = '.xls'
        options['filetypes'] = [('all files', '.*'), ('text files', '.xls')]
        options['initialdir'] = 'D:\\'
        options['initialfile'] = self.searchinfo.get()+'.xls'
        options['parent'] = self.window_info_up
        options['title'] = 'This is a title'

        excel = ExcelUtil()
        excel.writeExcel(0, 0, "店铺名称")
        excel.writeExcel(0, 1, "电话1")
        excel.writeExcel(0, 2, "电话2")
        excel.writeExcel(0, 3, "电话3")
        row = 0
        for i in items:
            row = row + 1
            values = self.box.item(i).get("values")
            print(values)
            excel.writeExcel(row,0,values[0])
            excel.writeExcel(row,1,str(values[1]))
            excel.writeExcel(row,2,str(values[2]))
            excel.writeExcel(row,3,str(values[3]))

        filename = asksaveasfilename(**self.file_opt)
        if filename:
            excel.save(filename)


    #注册函数
    def usr_sign_up(self):
        #确认注册时的相应函数
        def signtowcg():
            #获取输入框内的内容
            nn=new_name.get()
            np=new_pwd.get()
            npf=new_pwd_confirm.get()

            #本地加载已有用户信息,如果没有则已有用户信息为空
            try:
                with open('usr_info.pickle','rb') as usr_file:
                    exist_usr_info=pickle.load(usr_file)
            except FileNotFoundError:
                exist_usr_info={}

            #检查用户名存在、密码为空、密码前后不一致
            if nn in exist_usr_info:
                tk.messagebox.showerror('错误','用户名已存在')
            elif np =='' or nn=='':
                tk.messagebox.showerror('错误','用户名或密码为空')
            elif np !=npf:
                tk.messagebox.showerror('错误','密码前后不一致')
            #注册信息没有问题则将用户名密码写入数据库
            else:
                exist_usr_info[nn]=np
                with open('usr_info.pickle','wb') as usr_file:
                    pickle.dump(exist_usr_info,usr_file)
                tk.messagebox.showinfo('欢迎','注册成功')
                #注册成功关闭注册框
                window_sign_up.destroy()
        #新建注册界面
        window_sign_up=tk.Toplevel(self.window)
        window_sign_up.geometry(self.size_xy)  #设置窗口坐标
        window_sign_up.wm_attributes('-topmost',1)# 窗口置顶
        window_sign_up.title('注册界面')
        #画布放置图片
        canvas=tk.Canvas(window_sign_up,height=300,width=500)
        im=Image.open("d:/lytmal/image/2.png")
        imagefile=ImageTk.PhotoImage(im)
        # imagefile=tk.PhotoImage(file='71.gif')
        image1=canvas.create_image(0,0,anchor='nw',image=imagefile)
        canvas.pack(side='top')
        #用户名变量及标签、输入框
        new_name=tk.StringVar()
        tk.Label(window_sign_up,text='用户名：').place(x=100,y=100)
        tk.Entry(window_sign_up,textvariable=new_name).place(x=240,y=100)
        #密码变量及标签、输入框
        new_pwd=tk.StringVar()
        tk.Label(window_sign_up,text='请输入密码：').place(x=100,y=140)
        tk.Entry(window_sign_up,textvariable=new_pwd,show='*').place(x=240,y=140)
        #重复密码变量及标签、输入框
        new_pwd_confirm=tk.StringVar()
        tk.Label(window_sign_up,text='请再次输入密码：').place(x=100,y=180)
        tk.Entry(window_sign_up,textvariable=new_pwd_confirm,show='*').place(x=240,y=180)
        #确认注册按钮及位置
        bt_confirm_sign_up=tk.Button(window_sign_up,text='确认注册',
                                     command=signtowcg)
        bt_confirm_sign_up.place(x=240,y=220)
        window_sign_up.mainloop()
    #退出的函数
    def usr_sign_quit(self):
        self.window.destroy()

    def run(self):
        self.login()
        self.window.mainloop()


if __name__ == '__main__':
    info=tmal()
    info.run()