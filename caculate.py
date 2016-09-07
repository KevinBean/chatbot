# -*- coding=utf-8 -*-
'''
根据正则表达式提取信息；
建立模板，根据替换生成新的资料。
2016-09-03
根据系统提资，提取出载流量信息。
'''
import jieba
import re
from attract import *
import pickle
import pprint
import pypandoc

class shuomingshu:
    dianlanxinghao = ''
    def __init__(self,n):
        self.dianlanxinghao = n
        # 提取提资信息？？？
        #filename = u'doc/互提资料单03（送电）.doc'
        if os.name == 'nt':
            filename = u'D:\Personal\我的文档\GitHub\chatbot\doc\X9348K-X-02 互提资料单 送电.docx'
            filename = os.path.normpath(filename)
        else:
            filename = u'doc/X9348K-X-02 互提资料单 送电.docx'
        dictpath =u'dict/dict.txt'
        # 生成txt文件
        if '.docx' in filename:
            docx2txt(filename) #改为使用pandoc
            newfilename = filename.replace(u'.docx', u'.txt')
            #pypandoc.convert_file(filename, 'markdown', 'docx', outputfile=newfilename)
        elif '.doc' in filename:
            doc2txt(filename) #改为使用pandoc
            newfilename = filename.replace(u'.doc', u'.txt')
            #pypandoc.convert_file(filename, 'txt', 'doc', outputfile=newfilename)

        self.info = projectinfo(newfilename, '', '', dictpath)
    def dianlanxuanxing(self):
        return '故本工程选用' + self.dianlanxinghao +'电缆。 '
    def dianlan(self):
        cs = cableSystem()
        cs.Cable['电压等级'] = int(raw_input(u'请输入电压等级(kV)：'))
        cs.Cable['载流量'] = int(raw_input(u'请输入载流量(A)：'))
        cs = jiemianxuanze(cs,'s') #进行截面选择
        print cs.Cable['截面']
        cs.Cable['电缆型号'] = 'ZC-YJLW02-' + str(int(round(cs.Cable['电压等级']/1.732))) + '/' + str(cs.Cable['电压等级']) + 'kV-1×' + str(cs.Cable['截面']) + 'mm2'
        cs.MaterialType['电缆'] = cs.Cable['电缆型号']
        cs.MaterialType['GIS终端'] = str(cs.Cable['电压等级']) + '/' + str(cs.Cable['截面'])
        cs.MaterialType['户外终端'] = str(cs.Cable['电压等级']) + '/' + str(cs.Cable['截面']) + u'爬电距离不小于' + str(cs.System['爬电比距'] * cs.Cable['电压等级']) + 'mm' + u'，建议使用' + cs.ZHONGDUANLEIXING[str(cs.Cable['电压等级'])] + u'产品'
        cs.MaterialType['避雷器'] = cs.BILEIQILEIXING[str(cs.Cable['电压等级'])] + u'爬电距离不小于' + str(cs.System['爬电比距'] * cs.Cable['电压等级']) + 'mm'
        # cs = dianlanlujing(cs)
        print(cs.startPoint.values(),cs.endPoint.values())
        return cs


def jiemianxuanze(cs, type):
    print type, type == 's',cs.Cable['载流量'] ,cs.Cable['载流量'] in range(0,750)
    if type == '':
        type = int(raw_input('请输入载流量计算模式：s（简单）h（复杂）'))
    if type == 's':
        if cs.Cable['电压等级'] == 110:
            if cs.Cable['载流量'] in range(0,750):
                cs.Cable['截面'] = 400
                cs.Cable['最大载流量'] = 750
            elif cs.Cable['载流量'] in range(750,950):
                cs.Cable['截面'] = 630
                cs.Cable['最大载流量'] = 950
            elif cs.Cable['载流量'] in range(950,1150):
                cs.Cable['截面'] = 800
                cs.Cable['最大载流量'] = 1150
            cs.Cable['波节'] = 6
    print cs.Cable['截面']
    return cs

def dianlanlujing(cs):
    APoint = cs.startPoint
    APoint['名称'] = raw_input('请输入起点名称：')
    APoint['类型'] = raw_input('请输入起点类型：1(GIS) 或 2(户外)')
    if APoint['类型'] == '1':
        APoint['类型'] = 'GIS'
    elif APoint['类型'] =='2':
        APoint['类型'] = '户外'
    APoint['高度'] = raw_input('请输入起点引上高度（数字）：')
    APoint['平面长度'] = raw_input('请输入起点平面长度（数字，m）：')
    APoint['里程'] = raw_input('请输入起点平面里程（数字，m）：')

    BPoint = cs.endPoint
    BPoint['名称'] = raw_input('请输入终点名称：')
    BPoint['类型'] = raw_input('请输入终点类型：1(GIS) 或 2(户外)')
    if APoint['类型'] == '1':
        APoint['类型'] = 'GIS'
    elif APoint['类型'] =='2':
        APoint['类型'] = '户外'
    BPoint['高度'] = raw_input('请输入终点引上高度（数字）：')
    BPoint['平面长度'] = raw_input('请输入终点平面长度（数字，m）：')
    BPoint['里程'] = raw_input('请输入终点平面里程（数字，m）：')

    Tunnel = cs.Tunnel
    Tunnel['里程'] = float(BPoint['里程']) - float(APoint['里程'])
    Tunnel['金具'] = float(Tunnel['里程']) / float(cs.Cable['波节'])
    Tunnel['电缆'] = float(Tunnel['里程']) * float(cs.System['裕度'])

    cs.Material['电缆'] = Tunnel['电缆'] + APoint['电缆'] + BPoint['电缆']
    return cs



class ref:
    '''
    提资
    '''
    system = '' # 系统提资

class cableSystem:
    #定义基本属性
    bojie = {110:12, 220:6} #波节 m
    System ={'回路数':2, '裕度':1.05, '爬电比距':3.1}
    ZHONGDUANLEIXING = {'110': u'复合绝缘型', '220': u'瓷套型'}
    BILEIQILEIXING = {'110': u'HY10WZ-108/260S，无间隙氧化锌避雷器', '220': u'瓷套型'}
    zailiuliang = {'750' :400, '950':630}
    startPoint = {'名称':'','类型':'户外', '高度':10, '平面长度':10,'里程':0, '电缆':0} #起点类型
    endPoint = {'名称':'','类型':'户外', '高度':10, '平面长度':10,'里程':0, '电缆':0} #终点类型
    Cable = {'电压等级':0, '波节':0, '载流量':0,'最大载流量':0, '截面':0, '电缆型号':u''}
    Tunnel = {'里程':0, '金具':0, '电缆':0}
    Material = {'电缆':0,
                '电缆（I路）': 0,
                '电缆（Ⅱ路）': 0,
                'GIS终端': 0,
                '户外终端':0,
                '护层保护器': 0,
                '绝缘接头': 0,
                '交叉互联箱': 0,
                '三线接地箱': 0,
                '六线接地箱': 0,
                '交叉互联电缆': 0,
                '接地电缆': 0,
                '避雷器':0
                }
    MaterialType = {'电缆': 0,
                '电缆（I路）': 0,
                '电缆（Ⅱ路）': 0,
                'GIS终端': 0,
                '户外终端': 0,
                '护层保护器': 0,
                '绝缘接头': 0,
                '交叉互联箱': 0,
                '三线接地箱': 0,
                '六线接地箱': 0,
                '交叉互联电缆': 0,
                '接地电缆': 0,
                '避雷器':0
                }
    Ref = ref()

cs1 =cableSystem()
system = cs1.System
cable = cs1.Cable
cs1.Ref.system = '综上所述，统筹考虑电网规划发展及用电负荷的发展情况，建议北宫站～南营站电缆线路按照载流量不小于200MVA（1050A）选择，并考虑一定裕度。'
cable['电压等级'] = 110
pattern = re.compile(r'[0-9]+(A)')
zailiuliang =re.search(pattern,cs1.Ref.system)
print zailiuliang.group()
cable['载流量'] = int(zailiuliang.group().replace('A',''))
if cable['载流量'] < 750:
    cable['截面'] = 400
cable['电缆型号'] = 'ZC-YJLW02-' + '64' + '/' + str(cable['电压等级']) + 'kV-1×' + str(cable['截面']) + 'mm2'
cable['波节'] = cs1.bojie[cable['电压等级']]
print(cable)

tunnel = cs1.Tunnel
tunnel['里程'] = cs1.endPoint['里程'] - cs1.startPoint['里程']
tunnel['金具'] = tunnel['里程']/cable['波节']
tunnel['电缆'] = tunnel['里程']*system['裕度']

start = cs1.startPoint
start['类型'] = 'GIS'

end = cs1.endPoint
end['类型'] = 'GIS'

material = cs1.Material
material['电缆'] = material

sms = shuomingshu(cable['电缆型号'])
print(sms.dianlanxuanxing())

pkl = '0371'

pklfile = 'dict/' + pkl +'.pkl'
output = open(pklfile, 'wb')
pickle.dump(cs1,output)
output.close()

inputfile = open(pklfile,'rb')
cs2 = pickle.load(inputfile)
pprint.pprint(cs2)
inputfile.close()
print cs2.Cable['截面']
print cs2.zailiuliang