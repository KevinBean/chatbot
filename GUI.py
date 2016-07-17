# -*- coding=utf-8 -*-
'''
聊天机器人的ＧＵＩ入口文件
使用python的tkinter布局简单的聊天窗口。
输入输出处理主要使用AIML。

关于tkinter：
最简单的Tkinter用法
import Tkinter
root=Tkinter.Tk()  %创建主窗体
MainLabel=Tkinter.Label(root,text="I am so ugly. -- Tkinter",font="Times 16 bold")  %创建元件
MainLabel.pack()  %显示元件
root.mainloop()  %进入窗体的主循环

关于ＡＩＭＬ：
基本用法
import aiml
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")
msg = "***"
bot_response = kernel.respond(msg)
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
    获取输入框信息msg并返回'utf-8'
    :return: raw_msg
    '''
    return text_msg.get().encode('utf-8')  # 获取输入框信息

def insert_msg(author,imsg,with_title = True):
    '''
    在信息展示区域显示信息内容，如果with_title = True，则同时显示信息标签（包括发送人，时间），
    :param author: 信息发送人
    :param imsg: 信息内容
    :param with_title: 是否显示时间标签
    :return: 无
    '''
    if with_title:
        msgcontent = unicode(author+':', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        text_msglist.insert(END, msgcontent, 'green')
    text_msglist.insert(END, imsg + '\n')
    text_msglist.yview(END)  # 文本区滚动条自动下滑

### 以下是特殊响应函数 ###
def worklog():
    '''
    特殊响应函数。通过WORKLOG * 触发。通过调用writelog函数将工作记录写入对应xls文件。
    :return:
    '''
    filename = 'doc/worklog.xlsx'
    sheetname = u'工作记录单'
    raw_msg = read_msg() #读取输入信息
    # msg = jiebacut(raw_msg)
    print raw_msg,type(raw_msg)
    writelog(filename,sheetname,raw_msg)
    insert_msg('Robot','已执行记录操作')

def brainsave():
    '''
    特殊响应函数。通过SAVE触发。执行kernel.saveBrain("bot_brain.brn")。
    :return:
    '''
    kernel.saveBrain("bot_brain.brn")

def searchfor():
    '''
    特殊响应函数。通过SEARCH *触发。检查不到输入问题答案时，就从doc文件夹下面的txt文件中进行信息提取，寻找答案。信息提取结果通过txt2aiml
    函数存储到aiml文件中。调用新的aiml规则库，返回搜索结果。
    :return:
    '''
    print 'searchfor'
    # 1. 读取输入信息并分词
    raw_msg = read_msg().upper()  # 读取输入信息
    msg = jiebacut(raw_msg)

    # 2. 剥去SEARCH 搜索标记，先判断msg中是否有既定答案
    msg = msg.replace('SEARCH','')
    print msg
    # 3. 如果有既定答案，则显示
    bot_response = kernel.respond(msg)  # bot_response() 信息回复
    print bot_response
    if bot_response != '':  # bot_response == ''就是没有找到有效匹配
        insert_msg('Robot', bot_response)
    # 4.如果没有既定答案，显示'正在查找'，同时遍历doc文件夹，从其中的txt文件里寻找信息，生成aiml规则库
    else:
        insert_msg('Robot', '正在查找...' )

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
        # 5. 重新读取aiml库,重新查找回复,如果还找不到匹配，那就显示抱歉,如果找到就显示'找到以下信息：'
        kernel.respond("load aiml b")
        bot_response = kernel.respond(msg)  # bot_response() 信息回复 重新查找回复
        if bot_response != '':  # 如果还找不到匹配，那就显示抱歉 bot_response == ''就是没有找到有效匹配
            insert_msg('Robot','找到以下信息：'+ '\n' + bot_response, with_title=False)
        else:
            insert_msg('Robot','抱歉，未能找到您要的信息', with_title=False)

### 以上是特殊响应函数 ###



#发送按钮事件
def sendmessage():
    '''
    按下发送按钮后，触发sendmessage函数
    进行输入输出数据处理。
    :param k: aiml处理核心参数kernel
    :return:
    '''
    # 1. 读取输入数据，并分词
    raw_msg = read_msg()
    msg = jiebacut(raw_msg)
    print msg

    # 2. 如果输入信息为空，显示'请问有什么可以帮您'，否则在聊天内容上方加一行 显示发送人及发送时间，以及输入信息内容
    if msg == '':
        insert_msg('Ｒobot', '请问有什么可以帮您')
    else:
        insert_msg('我', raw_msg)

        '''旧的分类处理，根据信息输入内容分类处理
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
                '''
        # 3. 获取ＡＩＭＬ的响应bot_response
        bot_response = kernel.respond(msg)  # bot_response() 信息回复
        # 新的分类处理，根据响应信息内容分类处理
        # msg=>可执行＼无参数的函数调用语句bot_response，如'quit'=>'execexit()'，可以简化这里的ifelse语句，但相应的增加了commands.aiml
        # 文件的维护量 可以用exec(bot_response.replace('exec',''))来执行调用
        # 4. 如果是含exec-的可执行响应，则用exec（）进行执行，调用对应特殊响应函数完成功能。msg与调用函数的对应关系在commands.aiml中定义，调用的函数体在本文件中。
        if 'exec-' in bot_response:
            exec (bot_response.replace('exec-', ''))
            text_msglist.yview(END)  # 文本区滚动条自动下滑
            text_msg.delete(0, END)  # 清除信息发送框，因为下面处理中有些函数要调用信息发送框中内容，因此放在处理函数之后再清除
        # 5. 如果是文本响应，则直接展示响应信息
        elif bot_response:
            insert_msg('Robot',bot_response)
            text_msg.delete(0, END) # 清除信息发送框，因为下面处理中有些函数要调用信息发送框中内容，因此放在处理函数之后再清除
        else:
            pass

if __name__ == "__main__":
    # 1. 创建Kernel()和 并学习AIML 规则库文件
    global kernel #kernel作为全局变量，方便调用
    kernel = aiml.Kernel()
    kernel.learn("std-startup.xml")
    kernel.respond("load aiml b")

    # 2. 创建主窗体
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
    # text_msglist作为对话信息展示区域，在sendmessage函数中处理
    text_msglist = ScrolledText(frame_top,wrap=WORD)  #加滑动条的文本区，wrap自动换行
    msg_lable = Label(frame_left_bottom,text='请输入')
    # text_msg作为信息输入框按钮，其中信息被read_msg()函数读取
    text_msg = Entry(frame_left_bottom,width=24)
    select_lable =Label(frame_center_bottom,text='请选择')
    text_select = Listbox(frame_center_bottom,width=20,height = 2)
    button_lable = Label(frame_right_bottom,text='按我')
    # button_sendmsg作为发送按钮，触发sendmessage函数
    button_sendmsg = Button(frame_right_bottom, text=unicode('发送', 'utf-8'), command=sendmessage)
    # 不显示的标签
    text_respond = Label(frame_top)

    # 创建一个绿色的tag
    text_msglist.tag_config('green', foreground='#008B00')
    # 3. 显示欢迎信息
    insert_msg('Robot',u'您好,请问有什么可以帮您:)')

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


    # 4. 主事件(窗体)循环，等待事件触发
    root.mainloop()


