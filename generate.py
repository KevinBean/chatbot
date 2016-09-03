# -*- coding=utf-8 -*-
'''
生成一份docx格式的说明书。
使用md格式书写文档，使用pypandoc输出docx文件。
'''
'''
from docx import Document #使用python-docx包

document = Document()

# 电缆路径
document.add_heading(u'电缆路径',level=1)
p = document.add_paragraph(u'本工程新建')
p.add_run(u'双回110kV电缆')

# 电缆电气部分
'''
import pypandoc as pydoc
from caculate import *

sms = shuomingshu(n=1)
cs = sms.dianlan()
print(cs.Cable['电缆型号'])

lujing = ''
lujing += u'## 电缆路径'
lujing += '\n'
lujing += u'本工程新建'
lujing += u'双回110kV电缆'
lujing += u'自' + cs.startPoint['名称'] # 替换成起点名称
lujing += '' #替换成路径描述 电缆路径描述是可以根据地图自动生成的
lujing += u'至' + u'终点名称' + u'。' # 替换成终点名称
lujing += '\n'
lujing += '\n'

dianqibufen = ''
dianqibufen += u'## 电缆电气部分'
dianqibufen += '\n'
dianqibufen += '\n'
dianqibufen += u'### 电缆及附件选型'
dianqibufen += '\n'
dianqibufen += '\n'
dianqibufen += u'#### 电缆选型'
dianqibufen += '\n'
dianqibufen += '\n'
dianqibufen += u'根据系统要求'
dianqibufen += u'，建议本期新建110kV电缆线路载流量按不小于6.3MVA选取并考虑一定裕度，' #替换成系统专业的提取值
dianqibufen += u'新建电缆'
dianqibufen += u'全线敷设在电力隧道及电缆夹层中，' #替换成敷设环境
dianqibufen += u'在环境温度40℃、线芯运行温度90℃、品字形接触排列的条件下，' #替换成敷设环境
dianqibufen += u'参考现有厂家资料，'
dianqibufen += u'铜芯、交联' + str(cs.Cable['截面']).decode('utf-8') + u'平方毫米截面电缆'
dianqibufen += u'，载流量不小于' + str(cs.Cable['最大载流量']).decode('utf-8') + u'A，' #替换成电缆型号及载流量
dianqibufen += u'满足系统载流量要求，'
dianqibufen += u'故本工程选用'
dianqibufen += cs.Cable['电缆型号'].decode('utf-8') #替换成电缆型号
dianqibufen += u'电缆。'
dianqibufen += '\n'
dianqibufen += '\n'
dianqibufen += u'#### 附件选型'
dianqibufen += '\n'
dianqibufen += '\n'
dianqibufen += u'全线敷设在电力隧道及电缆夹层中，' #替换成敷设环境
dianqibufen += u'全线敷设在电力隧道及电缆夹层中，' #替换成敷设环境
dianqibufen += u'全线敷设在电力隧道及电缆夹层中，' #替换成敷设环境
dianqibufen += u'全线敷设在电力隧道及电缆夹层中，' #替换成敷设环境
dianqibufen += '\n'
dianqibufen += '\n'

gongzuoliang = ''
gongzuoliang += u'主要工作量：'
gongzuoliang += '\n'
gongzuoliang += '\n'
gongzuoliang += '|' + u'敷设：' + '|' + '|' + '|'
gongzuoliang += '\n'
gongzuoliang += '|' + '------' + '|' + '------' + '|' + '------' + '|'
gongzuoliang += '\n'
gongzuoliang += '|' + '12' + '|' + '34' + '|' + '56' + '|'
gongzuoliang += '\n'
gongzuoliang += '|' + '65' + '|' + '43' + '|' + '21' + '|'
gongzuoliang += '\n'
gongzuoliang += '|' + u'安装：' + '|' + '|' + '|'
gongzuoliang += '\n'
gongzuoliang += '\n'

output = lujing + dianqibufen +gongzuoliang

'''
output = open ('test.md', 'w')
output.write(dianlanlujing)
output.close()
'''

pydoc.convert_text(output,to='docx',format = 'md',outputfile='doc/test.docx')