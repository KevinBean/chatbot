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
from attract import *
import pickle

pkl = '0371'

'''
#生成测试文件
sms = shuomingshu(n=1)
cs = sms.dianlan()
print(cs.Cable['电缆型号'])
# 保存数据以备调用
pklfile = 'dict/' + pkl +'.pkl'
output = open(pklfile, 'wb')
pickle.dump(cs,output)
output.close()
'''
#读取保存的测试数据
readcs = open(pklfile,'r')
cs = pickle.load(readcs)
readcs.close()

#读取提资文件中系统概况
filename = u'D:\Personal\我的文档\GitHub\chatbot\doc\X9348K-X-02 互提资料单 送电.txt' #系统提资文件路径
dictpath = u'D:\Personal\我的文档\GitHub\chatbot\dict\dict.txt'  # 训练数据越多越准确
dictionary = corpora.Dictionary.load_from_text(dictpath)
sample_xitonggaikuang = u'将村齐线“T”接南山的110kV线路破口接入永定变电站，形成永定～南山以及永定～规划园博园的110kV线路。本期工程完成后，南山站电源将由永定站提供；园博园站电源也由永定站主供，吕村站作为备用电源。'
xtgk = findinFile(filename, dictionary, sample_xitonggaikuang)
print xtgk
#生成系统概况段落
xitonggaikuang = ''
xitonggaikuang += u'## 系统概况'
xitonggaikuang += '\n'
xitonggaikuang += xtgk
xitonggaikuang += '\n'
xitonggaikuang += '\n'

lujing = ''
lujing += u'## 电缆路径'
lujing += '\n'
lujing += u'本工程新建'
lujing += u'双回110kV电缆'
lujing += u'自' + cs.startPoint['名称'].decode('utf-8') # 替换成起点名称
lujing += '' #替换成路径描述 电缆路径描述是可以根据地图自动生成的
lujing += u'至' + cs.endPoint['名称'].decode('utf-8')  + u'。' # 替换成终点名称
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

output = xitonggaikuang + lujing + dianqibufen +gongzuoliang

'''
output = open ('test.md', 'w')
output.write(dianlanlujing)
output.close()
'''

pydoc.convert_text(output,to='docx',format = 'md',outputfile='doc/test.docx')