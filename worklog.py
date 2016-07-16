# -*- coding=utf-8 -*-
'''
假定已知工作记录单的组织结构
文件名'工作记录单.xlsx'；表单名'工作记录单'
表头'序号 	名称/关键词	类型	日期/时间 	持续时间（小时）	折合工日（自动计算）	具体内容	后续处理情况	额外工作量？	调整变更比率
备注1	备注2'
先只实现 名称 时间 具体内容 的记录

！！！！！！！放弃操作xls以及所有的office文件！！！！！！！！！！！！！

不管以前的xls文件，直接从头开始创建一个csv文件，并且添加内容。

pandas的to_excel，to_csv等输出函数不能处理unicode字符。好崩溃！！！！！！！！！！
newsheet.to_excel('newworklog.xlsx',engine='openpyxl') #engine改为'openpyxl'即可写入unicode

'''


from __future__ import division
import pandas
import xlrd
import time

def jointPoint(filename,sheetname):
    # Read the file
    xls = xlrd.open_workbook(filename) #需要用变量代替
    sheet = xls.sheet_by_name(sheetname)   #需要用变量代替
    print(str(sheet.cell(2,2)).decode('utf-8'),sheet.nrows)  #需要用变量代替
    # 寻找记录起始位置行，也就是第1列名称为空的位置
    # for i in range(sheet.nrows):
    #    if sheet.cell_value(i,2) == '' and sheet.cell_value(i,2) == '':
    #        row = i
    return sheet.nrows

def writelog(filename,sheetname,talktoMe):
    logTypes = ['出版/记录',
                '工程节点/记录',
                '其他记录',
                '会议/沟通',
                '电话/沟通',
                '其他沟通']

    outofPlans = ['计划内',
                  '额外',
                  '调整变更']
    num = jointPoint(filename,sheetname)  # 寻找记录起始位置行，也就是第1列名称为空的位置
    name = talktoMe[:8]   #以下需要用变量代替
    logType = logTypes[0]
    datetime = time.strftime("%Y / %m / %d %H:%M", time.localtime())
    howmanyHours = 5
    howmanyDays = float(howmanyHours/5)
    detail = talktoMe[11:]
    deal = ''
    outofPlan =outofPlans[0]
    changeRate = ''
    other = ''
    another = ''
    # 使用变量字典生成数据，需要加index=[0]参数，否则会报错If using all scalar values, you must pass an index
    worklog = {u'序号':num,
                   u'名称/关键词':name,
                                u'类型':logType,
                                u'日期/时间':datetime,
                                u'持续时间（小时）':howmanyHours,
                                u'折合工日（自动计算）':howmanyDays,
                                u'具体内容':detail,
                                u'后续处理情况':deal,
                                u'额外工作量？':outofPlan,
                                u'调整变更比率':changeRate,
                                u'备注1':other,
                                u'备注2':another}
    workFrame = pandas.DataFrame(worklog,index=[0])
    # 后面append开启ignore_index=True，就不用这里columns参数控制显示顺序了
    columns = [u'序号',u'名称/关键词',u'类型',u'日期/时间',u'持续时间（小时）',
    u'折合工日（自动计算）',u'具体内容',u'后续处理情况',u'额外工作量？',u'调整变更比率',u'备注1',u'备注2'] #需要用变量代替
    print num
    print worklog.keys()[0],len(worklog.keys())
    sheet = pandas.read_excel(filename,sheetname) #需要用变量代替
    sheet =pandas.DataFrame(sheet)
    sheethead = sheet[:num-1]
    # sheettail = sheet[num+1:]
    print sheet[num-1:num+1]
    sheethead = sheethead.append(worklog,ignore_index=True) # 开启ignore_index=True 则按照列标题匹配增加行数据
    newsheet = sheethead # .append(sheettail,ignore_index=True)
    # print newsheet.loc[0, columns[0]]
    # changeencode(newsheet,columns)

    print newsheet[num-1:num+1]
    # ew = pandas.ExcelWriter('worklog.xlsx')
    newsheet.to_excel(filename,sheetname,engine='openpyxl') #engine改为'openpyxl'即可写入unicode
    # ew.save()  #需要用变量代替



#转换代编码用，目前未使用
def changeencode(data,cols):
    for col in cols:
        data[col] = data[col].str.decode('iso-8859-1').str.encode('utf-8')
    return data

if __name__ == "__main__":
    filename = 'doc/worklog.xlsx'
    sheetname = u'工作记录单'
    print type(sheetname),type(filename)
    writelog(filename,sheetname,u'＊＊输变电工程，电话沟通，需要修改站址。')