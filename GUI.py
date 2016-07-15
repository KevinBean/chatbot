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
from translate import Translator
from Tkinter import *
import datetime
import time
from ScrolledText import ScrolledText #文本区加滑动条

from worklog import *

#发送按钮事件
def sendmessage(k):
    raw_msg = text_msg.get().encode('utf-8') # 获取输入框信息

    msg = jiebacut(raw_msg) #分词后用空格分隔，进行匹配
    print msg

    #在聊天内容上方加一行 显示发送人及发送时间
    if msg:
        msgcontent = unicode('我:', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        text_msglist.insert(END, msgcontent, 'green')
        text_msglist.insert(END, raw_msg + '\n')
        text_msg.delete(0, END)
    else:
        pass
    # msg=>可执行＼无参数的函数调用语句bot_response，如'quit'=>'execexit()'，可以简化这里的ifelse语句，但相应的增加了commands.aiml
    # 文件的维护量 可以用exec(bot_response.replace('exec',''))来执行调用
    if msg == "quit":
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

if __name__ == "__main__":
    # 创建Kernel()和 AIML 学习文件
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
    button_sendmsg = Button(frame_right_bottom, text=unicode('发送', 'utf-8'), command=lambda:sendmessage(k = kernel))
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


