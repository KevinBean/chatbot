# -*- coding: latin-1 -*-
# 命令行版的起始欢迎界面。

import aiml
from translate import Translator

# 创建Kernel()和 AIML 学习文件
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

# 按组合键 CTRL-C 停止循环
'''
while True:
    translator = Translator(to_lang='en', from_lang='zh')
    backtranslator = Translator(to_lang='zh',from_lang='en')
    original = raw_input(u"请输入信息 >> ")
    print original
    message = translator.translate(original)
    print message
    response = kernel.respond(message)
    print backtranslator.translate(response)

'''
while True:
    message = raw_input("Enter your message to the bot: ")
    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response = kernel.respond(message)
        print bot_response
        # bot_response() 回复某些信息
