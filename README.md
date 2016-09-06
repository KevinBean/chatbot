# 聊天机器人结构设计

## TODOS 

### readdoc调试记录
os.name == nt
使用win32com进行处理，注意转换后默认编码为gbk
    if os.name == 'nt':
        print 'nt'
        word = wc.Dispatch('Word.Application')
        doc = word.Documents.Open(filename)
        doc.SaveAs(newfilename, 4)  # 17对应于下表中的
        doc.Close()
        word.Quit()
os.name != nt
使用pandoc进行处理

### 语料库的来源问题 
#### **Waiting 翻译standard语料库**  
#### 爬取文档,实现aiml自动生成。 

- 爬取文档使用jieba和nltk 

- 使用jieba的关键词提取以及搜索引擎分词功能？

- 可利用formataiml.py中format(file,pattern,template) 

- 关于输入与pattern的匹配问题     

- 思路一:建立AIML时,pattern可以进行简单处理。这需要一定总结。形成固定格式。比如关于关系的问题,标准化为"A与B的关系如何?"或"*A*B*关系*"     

- 思路二:利用DefaultSubs对输入进行处理。与上面pattern建立时类似,关于关系的问题统一转化为"A与B的关系如何?"    

- 思路三:利用<srai>BYE</srai>标签创建同义替换 - 练习：从文档库中（具体SL351C-A11-01文件中），提取下列信息："旺控35kV工程位于哪里？" "旺控35kV工程电缆长度多少？" "旺控35kV工程所用的终端塔是什么型号？"     
- 第一种方法：根据问题，去寻找特定答案；问题找答案     
- 第二种方法：先根据文档建立aiml，再尝试去匹配问题。答案找问题         
- 寻找关键词keyword,在这个例子中是"工程名"＝》找到”%%35kV线路入地工程"         
- 寻找信息，这个例子中为"位于"，"电缆长度"，"终端塔"         
- 经测，目前有以下问题：1。只能匹配一句回答，而且不一定是最准确的那一句；2。必须提前人工提取关键词去对文件建立aiml；3。匹配的模式变种还不够，会漏掉一些情况，需要改进xls2aiml - aiml文件的合并问题 
### 回答计算问题 - 获取参数是个问题。利用session进行获取操作? - 后台计算生成aiml然后作答。 - 检测到计算问题,就转入另外的处理程序。 

## 注意问题

### 使用std-zhihu.aiml测试了中文结果,测试文件来自 [这里](https://github.com/Elvis-Zhou/zhihuDM/blob/master/%E7%9F%A5%E4%B9%8E%E9%87%91%E8%9E%8D%E9%97%AE%E9%A2%98%E8%A7%A3%E6%9E%90%E6%88%90aiml%E6%A0%BC%E5%BC%8F.txt)

### 为了实现中文输入与模式的对应关系。
 建立模式时，和处理输入时，均使用相同的分词工具进行预处理。  
### readdoc.py中doc2txt函数，目前可以处理docx文件的读取  
### 用Tkinter做了用户界面,进一步使用pygubu进行界面设计,详见pygubu.md介绍(使用不是特别顺利)  
### worklog.py 实现将输入的文字转换为格式化的工作记录条目，并汇入excel文件
- 使用pandas做数据条目的汇总，包括读取原excel文件，读取数据后增加新条目，再写回文件
- newsheet.to\_excel('newworklog.xlsx',engine='openpyxl') #engine改为'openpyxl'即可写入unicode
- 函数中有些参数需要改为函数输入变量表述

### 中文的\*匹配和英文的不同,在于\*前后是否加_空格_。 英文要写成<pattern> \* BYE</pattern>可以匹配"mike,bye", 而中文要写成<pattern> \*再见</pattern>来匹配"迈克,再见"。 如加空格写成<pattern> \* 再见</pattern>则匹配的是"迈克, 再见" 对于＊的匹配认识仍然不足，比如"姓名 \* 电话"只能匹配"姓名 a 电话"，'姓名\*电话'无法匹配"姓名的电话" 中文匹配前后必须加空格，原因位置，比如" 
### 可以通过翻译工具解决AIML对中文的处理,比如输入内容先经过翻译处理后变成英文内容,英文内容经AIML处理后输出,输出再翻译成中文显示。
 输入中文->翻译为英文->AIML处理->英文结果->翻译成中文
 经测,可实现。
 因为要用到翻译api,没有网络的情况下,较难实现。
 代码如下:
''  import aiml from translate import Translator # 创建Kernel()和 AIML 学习文件 kernel = aiml.Kernel() kernel.learn("std-startup.xml") kernel.respond("load aiml b") # 按组合键 CTRL-C 停止循环 while True:     translator = Translator(to_lang='en', from_lang='zh')     backtranslator = Translator(to_lang='zh',from_lang='en')     original = raw_input(u"请输入信息 >> ")     print original     message = translator.translate(original)     print message     response = kernel.respond(message)     print backtranslator.translate(response) 
### Tkinter用lambda传递函数
''' button_sendmsg = Button(frame_right_bottom, text=unicode('发送', 'utf-8'), command=lambda:sendmessage(k = kernel)) def sendmessage(k):
'''

### 界面滚动条,自动下移 
探索ScrolledText的方法.一条语句搞定
''' text_msglist.yview(END)  # 文本区滚动条自动下滑''' 
或者  内容显示控件由Text改为Listbox。 参考[使用 Python 的 Tkinter模块 开发 IRC 客户端](http://www.jianshu.com/p/70ae0a523869)

## hello.py
命令行版的起始欢迎界面。

## GUI.py

### 主程序流程
1. 创建Kernel()和 并学习AIML 规则库文件
2. 创建主窗体
	- text\_msglist作为对话信息展示区域，在sendmessage函数中处理
	- text\_msg作为信息输入框按钮，其中信息被read_msg()函数读取
	- button\_sendmsg作为发送按钮，触发sendmessage函数
3. 显示欢迎信息
4. 主事件(窗体)循环，等待事件触发

### 按下发送按钮后，触发sendmessage函数
进行输入输出数据处理。
1. 读取输入数据，并{分词}
2. 如果输入信息为空，显示'请问有什么可以帮您'，否则在聊天内容上方加一行 显示发送人及发送时间，以及输入信息内容
3. 获取ＡＩＭＬ的响应bot\_response
4. 如果是含exec-的可执行响应，则用exec（）进行执行，调用对应特殊响应函数完成功能。msg与调用函数的对应关系在commands.aiml中定义，调用的函数体在本文件中。
5. 如果是文本响应，则直接展示响应信息

### read\_msg函数
获取输入框信息msg并返回'utf-8'

### insert\_msg函数
在信息展示区域显示信息内容，如果with\_title = True，则同时显示信息标签（包括发送人，时间）

### worklog函数
特殊响应函数。通过调用writelog函数将工作记录写入对应xls文件。

### brainsave函数
特殊响应函数。通过SAVE触发。执行kernel.saveBrain("bot\_brain.brn")。

### searchfor函数
特殊响应函数。通过SEARCH \*触发。检查不到输入问题答案时，就从doc文件夹下面的txt文件中进行信息提取，寻找答案。信息提取结果通过txt2aiml 函数存储到aiml文件中。调用新的aiml规则库，返回搜索结果。

1. 读取输入信息并分词
2. 剥去SEARCH 搜索标记，先判断msg中是否有既定答案
3. 如果有既定答案，则显示
4. 如果没有既定答案，显示'正在查找'，同时遍历doc文件夹，从其中的txt文件里寻找信息，生成aiml规则库。
5. 重新读取aiml库,重新查找回复,如果还找不到匹配，那就显示抱歉,如果找到就显示'找到以下信息：'

## formataiml.py
根据一个给定的XML Schema，使用DOM树的形式从空白文件生成一个XML。
 创建最基本的AIML。形式:

'' <?xml version="1.0" encoding="GB2312"?> <aiml> <category>     <pattern>你好</pattern>     <template>好</template> </category> </aiml> 通过输入template写成<srai>BYE</srai>,可以进行同义替换
''
 输入改为列表

### TODOS
研究如何向已有的aiml文件中增加条目、合并条目。

### txt2aiml函数
从txt文件中寻找有用信息，存入xls，再调用xls2aiml转换为aiml
 1. 读取txt文件，并存为字符串格式
2. 以工程说明书为例 分词＼分句
3. 寻找工程名称作为输出模式关键字，因为说明书封面都会有工程名称，因此以第一次出现的工程名称为准
4. 根据搜索关键字，寻找对应信息
5. 写成2列的xls文件
6. 利用xls2aiml将xls文件变为aiml

#### TODOS
目前有以下不足：
1. 只能匹配一句回答，而且不一定是最准确的那一句；
2. 必须提前人工提取关键词去对文件建立aiml；
3. 匹配的模式变种还不够，会漏掉一些情况，需要改进xls2aiml
4. 调用的txt2aiml应该把搜索关键词也作为输入参数 
### xls2aiml函数
利用xlrd读取2列xls文件，并利用format函数写入aiml文件
 :param filename: 输出aiml文件名＼路径
 :param xlsname: 输入xls文件名、路径
 :param apart: 分隔符
 :param keyword: 关键词
 :return: 无。生成特定aiml文件  五种模式：（基本模式；模式＋任意字符＋关键字；关键字＋任意字符＋模式；模式＋关键字；关键字＋模式）
2. 模式 \* 关键字
3. 关键字 \* 模式
4. 模式关键字
5. 关键字模式
6. 模式

### format函数
通过输入pattern和template值创建一个最基本的AIML。利用xml.dom生成结构化的aiml文本

### writetoaiml函数
非结构化的aiml规则库生成方法








## worklog.py
假定已知工作记录单的组织结构：「 文件名'工作记录单.xlsx'；表单名'工作记录单' 表头'序号 	名称/关键词	类型	日期/时间 	持续时间（小时）	折合工日（自动计算）	具体内容	后续处理情况	额外工作量？	调整变更比率 备注1	备注2’」 先只实现 名称 时间 具体内容 的记录。
### 注意
- pandas的to\_excel，to\_csv等输出函数不能处理unicode字符。好崩溃！！！！！！！！！！
- xlwt不能处理unicode字符，弃用！！！
-  newsheet.to\_excel('newworklog.xlsx',engine='openpyxl') #engine改为'openpyxl'即可写入unicode
### TODOS
- ！！！！！！！放弃操作xls以及所有的office文件！！！！！！！！！！！！！
- 不管以前的xls文件，直接从头开始创建一个csv文件，并且添加内容。

### writelog函数
使用pandas将worklog内容记录到filename文件的sheetname表单。

#### TODOS
对输入内容做信息提取处理。

### jointPoint函数
找到新添加的worklog从哪一行开始。

## generate.py
生成说明书。
写成markdown格式，然后用pandoc来转换成docx




## wordscut.py
使用jieba进行分词，同时用在建立amil数据库pattern生成和使用amil的msg匹配上，以达到一致的目的。
 为了实现中文输入与模式的对应关系。建立模式时，和处理输入时，均使用相同的分词工具进行预处理。

### jiebacut函数
输入句子，用jieba分词后返回'utf-8'分词结果，用空格分隔

使用jieba进行分词，同时用在建立amil数据库pattern生成和使用amil的msg匹配上，以达到一致的目的。
 为了实现中文输入与模式的对应关系。建立模式时，和处理输入时，均使用相同的分词工具进行预处理。

### jieba的用户自定义词典
 解决方案是在词典中补充“君意”这个词，并给予一个词频，不用太大，比如3即可。 ==user.dict=== 用法： 
'''jieba.load_userdict(file_name) # file_name 为文件类对象或自定义词典的路径'''

#### user.dict
为自定义词典。基本格式：单词 词频 词性

## attract.py
根据模板从文档中提取特定段落信息

## readdoc.py

直接改成用pandoc转换更便捷

### doc2txt函数
从word（docx格式、doc）中提取text，保存为txt

### doc2txt函数
doc格式读取只能在windows下实现

# AIML
研究AIML的源文件。/Users/bianbin/anaconda/lib/python2.7/UserDict.py 
## Util.py

用来切分句子。可以处理中文,但是要注意先把中文标点替换为英文标点。 使用    print sents[1].decode('utf-8') 可以正常输出中文。  
## aiml/WordSub.py
 用来替换单词,适应中文。
 示例:
 ``` subber = WordSub()     subber["apple"] = "苹果"     subber["orange"] = "pear"     subber["banana" ] = "apple"     subber["he"] = "she"     subber["I'd"] = "I would"      # test case insensitivity     inStr =  "I'd like one apple, one Orange and one BANANA."     outStr = "I Would like one 苹果, one Pear and one APPLE."     if subber.sub(inStr) == outStr: print "Test #1 PASSED"         else: print "Test #1 FAILED: '%s'" % subber.sub(inStr)      inStr = "He said he'd like to go with me"     outStr = "She said she'd like to go with me"     if subber.sub(inStr) == outStr: print "Test #2 PASSED"         else: print "Test #2 FAILED: '%s'" % subber.sub(inStr)  ``` 
## aiml/DefaultSubs.py 预设的替换字典。  
## aiml/PatternMgr.py
 模式匹配。提取XML标签结构,不涉及输入内容? 主要的是match(),被核心模块aiml/Kernel.py调用。  
## aiml/AimlParser.py
 AIML解析器?  
## aiml/Kernel.py
 程序主要界面。 最常用的就是respond()。  
  
   
         
