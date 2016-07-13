# 聊天机器人

## AIML
研究AIML的源文件。/Users/bianbin/anaconda/lib/python2.7/UserDict.py

### Util.py
用来切分句子。可以处理中文,但是要注意先把中文标点替换为英文标点。
使用    print sents[1].decode('utf-8') 可以正常输出中文。

### aiml/WordSub.py
用来替换单词,适应中文。
示例:
```
subber = WordSub()
    subber["apple"] = "苹果"
    subber["orange"] = "pear"
    subber["banana" ] = "apple"
    subber["he"] = "she"
    subber["I'd"] = "I would"

    # test case insensitivity
    inStr =  "I'd like one apple, one Orange and one BANANA."
    outStr = "I Would like one 苹果, one Pear and one APPLE."
    if subber.sub(inStr) == outStr: print "Test #1 PASSED"    
    else: print "Test #1 FAILED: '%s'" % subber.sub(inStr)

    inStr = "He said he'd like to go with me"
    outStr = "She said she'd like to go with me"
    if subber.sub(inStr) == outStr: print "Test #2 PASSED"    
    else: print "Test #2 FAILED: '%s'" % subber.sub(inStr)

```
### aiml/DefaultSubs.py
预设的替换字典。

### aiml/PatternMgr.py
模式匹配。提取XML标签结构,不涉及输入内容?
主要的是match(),被核心模块aiml/Kernel.py调用。

### aiml/AimlParser.py
AIML解析器?

### aiml/Kernel.py
程序主要界面。
最常用的就是respond()。

### 使用std-zhihu.aiml测试了中文结果,测试文件来自 [这里](https://github.com/Elvis-Zhou/zhihuDM/blob/master/%E7%9F%A5%E4%B9%8E%E9%87%91%E8%9E%8D%E9%97%AE%E9%A2%98%E8%A7%A3%E6%9E%90%E6%88%90aiml%E6%A0%BC%E5%BC%8F.txt)

### formataiml.py中format()可以通过输入pattern和template值创建一个最基本的AIML。

### 用Tkinter做了用户界面,进一步使用pygubu进行界面设计,详见pygubu.md介绍(使用不是特别顺利)

### worklog.py 实现将输入的文字转换为格式化的工作记录条目，并汇入excel文件
- 使用pandas做数据条目的汇总，包括读取原excel文件，读取数据后增加新条目，再写回文件
- newsheet.to_excel('newworklog.xlsx',engine='openpyxl') #engine改为'openpyxl'即可写入unicode

### 可以通过翻译工具解决AIML对中文的处理,比如输入内容先经过翻译处理后变成英文内容,英文内容经AIML处理后输出,输出再翻译成中文显示。
输入中文->翻译为英文->AIML处理->英文结果->翻译成中文
经测,可实现。
因为要用到翻译api,没有网络的情况下,较难实现。
代码如下:
```
import aiml
from translate import Translator

# 创建Kernel()和 AIML 学习文件
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

# 按组合键 CTRL-C 停止循环
while True:
    translator = Translator(to_lang='en', from_lang='zh')
    backtranslator = Translator(to_lang='zh',from_lang='en')
    original = raw_input(u"请输入信息 >> ")
    print original
    message = translator.translate(original)
    print message
    response = kernel.respond(message)
    print backtranslator.translate(response)
```


## TODOS

### 语料库的来源问题

#### 翻译standard语料库

#### 爬取文档,实现aiml自动生成。
- 爬取文档使用jieba和nltk
- 可利用formataiml.py中format(file,pattern,template)
- 关于输入与pattern的匹配问题
    - 思路一:建立AIML时,pattern可以进行简单处理。这需要一定总结。形成固定格式。比如关于关系的问题,标准化为"A与B的关系如何?"或"*A*B*关系*"
    - 思路二:利用DefaultSubs对输入进行处理。与上面pattern建立时类似,关于关系的问题统一转化为"A与B的关系如何?"
    - 思路三:利用<srai>BYE</srai>标签创建同义替换
    
### 回答计算问题
- 获取参数是个问题。利用session进行获取操作?
- 后台计算生成aiml然后作答。
- 检测到计算问题,就转入另外的处理程序。

### 界面滚动条,自动下移
探索ScrolledText的方法

或者 

内容显示控件由Text改为Listbox。
参考[使用 Python 的 Tkinter模块 开发 IRC 客户端](http://www.jianshu.com/p/70ae0a523869)



## 注意问题

### 中文的*匹配和英文的不同,在于*前后是否加_空格_。
英文要写成<pattern> * BYE</pattern>可以匹配"mike,bye",
而中文要写成<pattern> *再见</pattern>来匹配"迈克,再见"。
如加空格写成<pattern> * 再见</pattern>则匹配的是"迈克, 再见"

### Tkinter用lambda传递函数
button_sendmsg = Button(frame_right_bottom, text=unicode('发送', 'utf-8'), command=lambda:sendmessage(k = kernel))
def sendmessage(k):

