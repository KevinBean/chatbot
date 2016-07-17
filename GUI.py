# -*- coding=utf-8 -*-
'''
使用python的tkinter布局的简单聊天窗口。作为AIML的窗口
最简单的Tkinter用法
import Tkinter

root=Tkinter.Tk()  %创建主窗体
MainLabel=Tkinter.Label(root,text="I am so ugly. -- Tkinter",font="Times 16 bold")  %创建元件
MainLabel.pack()  %显示元件
root.mainloop()  %进入窗体的主循环
'''

import aiml
from wordscut import jiebacut
# from translate import Translator #利用翻译模块转换中英文
from Tkinter import *
import datetime
import time
import os
from ScrolledText import ScrolledText #文本区加滑动条

from worklog import *
from formataiml import *

def read_msg():
    '''
    获取输入框信息msg
    :return: raw_msg
    '''
    return text_msg.get().encode('utf-8')  # 获取输入框信息

def worklog():
    filename = 'doc/worklog.xlsx'
    sheetname = u'工作记录单'
    raw_msg = read_msg() #读取输入信息
    # msg = jiebacut(raw_msg)
    print raw_msg,type(raw_msg)
    writelog(filename,sheetname,raw_msg)
    msgcontent = unicode('Robot:', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
    text_msglist.insert(END, msgcontent, 'green')
    text_msglist.insert(END, '已执行记录操作' + '\n')

def brainsave():
    kernel.saveBrain("bot_brain.brn")

def searchfor():
    '''
    目前的search ＊ 是一个强制搜索工具，就是每次处理时都
    :return:
    '''
    print 'searchfor'
    raw_msg = read_msg().upper()  # 读取输入信息
    msg = jiebacut(raw_msg)
    # msg = str(raw_msg.encode('utf-8'))  # 特殊处理。将unicode统一处理成字符串
    msg = msg.replace('SEARCH','') # 剥去SEARCH 搜索标记，先判断msg中是否有既定答案？？？这一步有必要吗？
    print msg

    bot_response = kernel.respond(msg)  # bot_response() 信息回复
    print bot_response
    if bot_response != '':  # bot_response == ''就是没有找到有效匹配
        msgcontent = unicode('Robot:', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        text_msglist.insert(END, msgcontent, 'green')
        text_msglist.insert(END, bot_response + '\n')
        text_msglist.yview(END)  # 文本区滚动条自动下滑
    else:
        msgcontent = unicode('Robot:', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        text_msglist.insert(END, msgcontent, 'green')
        text_msglist.insert(END, '正在查找...' + '\n')
        text_msglist.yview(END)  # 文本区滚动条自动下滑

        # 遍历目录，从所有txt中生成aiml
        docdir = 'doc/'
        doclist = os.walk(docdir)
        for root, dirs, files in doclist:
            for name in files:
                print os.path.join(root, name)
                # 预留位置。要保证所有的文档都有对应的txt，目前采用手动保存模式。
                filename = os.path.join(root, name)
                if '.txt' in filename:
                    txt2aiml(filename)  # 下一步应该增加搜索关键词到这个函数

        kernel.respond("load aiml b") # 重新读取aiml库
        bot_response = kernel.respond(msg)  # bot_response() 信息回复 重新查找回复
        if bot_response != '':  # 如果还找不到匹配，那就显示抱歉 bot_response == ''就是没有找到有效匹配
            text_msglist.insert(END, '找到以下信息：'+ '\n' + bot_response + '\n')
        else:
            text_msglist.insert(END, '抱歉，未能找到您要的信息' + '\n')
        text_msglist.yview(END)  # 文本区滚动条自动下滑

#发送按钮事件
def sendmessage():
    '''
    :param k: aiml处理核心参数kernel
    :return:
    '''

    raw_msg = read_msg()
    msg = jiebacut(raw_msg)
    print msg

    #在聊天内容上方加一行 显示发送人及发送时间
    if msg:
        msgcontent = unicode('我:', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        text_msglist.insert(END, msgcontent, 'green')
        text_msglist.insert(END, raw_msg + '\n')
        text_msglist.yview(END)  # 文本区滚动条自动下滑
        # text_msg.delete(0, END) # 清除信息发送框，因为下面处理中有些函数要调用信息发送框中内容，因此放在处理函数之后再清除
    else:
        pass

    # msg=>可执行＼无参数的函数调用语句bot_response，如'quit'=>'execexit()'，可以简化这里的ifelse语句，但相应的增加了commands.aiml
    # 文件的维护量 可以用exec(bot_response.replace('exec',''))来执行调用
    '''if msg == "quit":
        exit()
    elif msg == "save":
        k.saveBrain("bot_brain.brn")
    elif 'log' in msg:
        writelog(msg)
    else:
        bot_response = k.respond(msg) # bot_response() 回复某些信息
        print bot_response,type(bot_response)
        if bot_response:
            msgcontent = unicode('Robot:', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
            text_msglist.insert(END, msgcontent, 'green')
            text_msglist.insert(END, bot_response + '\n')
            text_msglist.yview(END)  # 文本区滚动条自动下滑
            text_msg.delete(0, END)
            '''
    bot_response = kernel.respond(msg)  # bot_response() 信息回复
    if 'exec-' in bot_response:
        exec (bot_response.replace('exec-', ''))
        text_msglist.yview(END)  # 文本区滚动条自动下滑
        text_msg.delete(0, END)  # 清除信息发送框，因为下面处理中有些函数要调用信息发送框中内容，因此放在处理函数之后再清除
    elif bot_response:
        msgcontent = unicode('Robot:', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        text_msglist.insert(END, msgcontent, 'green')
        text_msglist.insert(END, bot_response + '\n')
        text_msglist.yview(END)  # 文本区滚动条自动下滑
        text_msg.delete(0, END)
    else:
        pass
    return msg

if __name__ == "__main__":
    # 创建Kernel()和 AIML 学习文件
    global kernel #kernel左权全局变量，方便调用
    kernel = aiml.Kernel()
    kernel.learn("std-startup.xml")
    kernel.respond("load aiml b")

    # 创建主窗体
    root = Tk()
    root.title(unicode('对话窗口', 'utf-8'))

    # 创建几个frame作为容器
    frame_top = Frame(width=380, height=270, bg='red')
    # frame_left_center  = Frame(width=380, height=100, bg='yellow')
    frame_left_bottom = Frame(width=250, height=50)
    frame_center_bottom = Frame(width = 70,height =50)
    frame_right_bottom = Frame(width=60, height=50)
    # frame_right     = Frame(width=170, height=400, bg='white')

    ##创建需要的几个元素
    text_msglist = ScrolledText(frame_top,wrap=WORD)  #加滑动条的文本区，wrap自动换行
    msg_lable = Label(frame_left_bottom,text='请输入')
    text_msg = Entry(frame_left_bottom,width=24)
    select_lable =Label(frame_center_bottom,text='请选择')
    text_select = Listbox(frame_center_bottom,width=20,height = 2)
    button_lable = Label(frame_right_bottom,text='按我')
    button_sendmsg = Button(frame_right_bottom, text=unicode('发送', 'utf-8'), command=sendmessage)
    # 不显示的标签
    text_respond = Label(frame_top)

    # 创建一个绿色的tag
    text_msglist.tag_config('green', foreground='#008B00')
    msgcontent = unicode('Robot:', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
    text_msglist.insert(END, msgcontent, 'green')
    text_msglist.insert(END, unicode('您好,请问有什么可以帮您:)', 'utf-8') + '\n')

    # 使用grid设置各个容器位置
    frame_top.grid(row=0, column=0, padx=2, pady=5, columnspan=3,sticky=N)
    # frame_left_center.grid(row=1, column=0, padx=2, pady=5)
    frame_left_bottom.grid(row=1, column=0,sticky=W)
    frame_center_bottom.grid(row=1,column=1,sticky=E)
    frame_right_bottom.grid(row=1, column=2, padx=1, pady=2,sticky=E)
    frame_top.grid_propagate(0)
    frame_left_bottom.grid_propagate(0)
    frame_right_bottom.grid_propagate(0)

    # 把元素填充进frame
    text_msglist.pack(expand=True, fill='both') #文本区加滑动条
    msg_lable.grid()
    text_msg.grid()
    select_lable.grid()
    text_select.grid()
    button_lable.grid(sticky=W)
    button_sendmsg.grid(sticky=E)


    # 主事件循环
    root.mainloop()


