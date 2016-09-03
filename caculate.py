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

class shuomingshu:
    dianlanxinghao = ''
    def __init__(self,n):
        self.dianlanxinghao = n
        # 提取提资信息？？？
        filename = u'doc/SK372K-AA-01.docx'
        dictpath =u'dict/dict.txt'
        if '.docx' in filename:
            docx2txt(filename)
            newfilename = filename.replace(u'.docx', u'.txt')
        elif '.doc' in filename:
            doc2txt(filename)
            newfilename = filename.replace(u'.doc', u'.txt')
        self.info = projectinfo(newfilename, '', '', dictpath)
    def dianlanxuanxing(self):
        return '故本工程选用' + self.dianlanxinghao +'电缆。 '
    def dianlan(self):
        cs = cableSystem()
        cs.Cable['电压等级'] = int(raw_input(u'请输入电压等级(kV)：'))
        cs.Cable['载流量'] = int(raw_input(u'请输入载流量(A)：'))
        cs = jiemianxuanze(cs,'s') #进行截面选择
        cs.Cable['电缆型号'] = 'ZC-YJLW02-' + str(int(round(cs.Cable['电压等级']/1.732))) + '/' + str(cs.Cable['电压等级']) + 'kV-1×' + str(cs.Cable['截面']) + 'mm2'
        cs = dianlanlujing(cs)
        print(cs.startPoint.values(),cs.endPoint.values())
        return cs


def jiemianxuanze(cs, type):
    if type == '':
        type = raw_input('请输入载流量计算模式：s（简单）h（复杂）')
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

    cs.Tunnel['里程'] = BPoint['里程'] - APoint['里程']
    cs.Tunnel['金具'] = cs.Tunnel['里程'] / cs.Cable['波节']
    cs.Tunnel['电缆'] = cs.Tunnel['里程'] * cs.System['裕度']
    return cs



class ref:
    '''
    提资
    '''
    system = '' # 系统提资

class cableSystem:
    #定义基本属性
    bojie = {110:12, 220:6} #波节 m
    System ={'回路数':2, '裕度':1.05}
    zailiuliang = {'750' :400, '950':630}
    startPoint = {'名称':'','类型':'户外', '高度':10, '平面长度':10,'里程':0} #起点类型
    endPoint = {'名称':'','类型':'户外', '高度':10, '平面长度':10,'里程':0} #终点类型
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
                '接地电缆': 0
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
                '接地电缆': 0
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