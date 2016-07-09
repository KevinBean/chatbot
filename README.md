## 聊天机器人

### AIML
研究AIML的源文件。/Users/bianbin/anaconda/lib/python2.7/UserDict.py
#### Util.py
用来切分句子。可以处理中文,但是要注意先把中文标点替换为英文标点。
使用    print sents[1].decode('utf-8') 可以正常输出中文。
#### aiml/WordSub.py
用来替换

### idea
#### 是否可以通过翻译工具解决AIML对中文的处理,比如输入内容先经过翻译处理后变成英文内容,英文内容经AIML处理后输出,输出再翻译成中文显示。
输入中文->翻译为英文->AIML处理->英文结果->翻译成中文
经测,可实现。
因为要用到翻译api,没有网络的情况下,较难实现。

代码如下

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

#### 已实现功能
- 基本的图形绘制,包括起始站点,出线和线路名

#### TODOS
- 修复有两个同方向出线的情况下(如两条数据方向均为"南"),线条重复的错误。

    - 基本思路1:建立线路起始点列表,使用过的起始点位置列为不可用,避免重复。
    - 基本思路2:更进一步避免交叉,进行网格规划,整张画布分为10*10的网格,网格上的节点(0,0)、(0,10)、(10,0)、(10,10)间连线,已经使用/经过
    的点不再走线。

- 设置不能走线的范围

- 走线非直线,需要转弯的情况,并且需要避免交叉

- 每6回线并为一个线束,找出最优布线策略,使得线束组数最少。
