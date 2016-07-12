# -*- coding=utf-8 -*-
'''
假定已知工作记录单的组织结构
文件名'工作记录单.xlsx'；表单名'工作记录单'
表头'序号 	名称/关键词	类型	日期/时间 	持续时间（小时）	折合工日（自动计算）	具体内容	后续处理情况	额外工作量？	调整变更比率
备注1	备注2'
先只实现 名称 时间 具体内容 的记录

！！！！！！！放弃操作xls以及所有的office文件！！！！！！！！！！！！！
'''
import xlwt
import xlrd
import xlwings
#xlrd 读xls文件; xlwt 写xls文件。
import time

import json #使用json,有点简单有复杂的感觉

def writelog():
    # Read the file
    xls = xlrd.open_workbook('worklog.xlsx')
    sheet = xls.sheet_by_name(u'工作记录单')
    # 寻找记录起始位置行，也就是第1列名称为空的位置
    for i in range(sheet.nrows):
        if sheet.cell_value(i,1) == '' and sheet.cell_value(i,1) == '':
            row = i
            break
    # 时间格式 2016 / 6 / 14 9:00 ，写入(row,3)
    print sheet.cell_value(row,3)
    ctype = 3 # 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    xf = 0  # 扩展的格式化
    sheet.put_cell(row,3,ctype,time.strftime("%Y / %m / %d %H:%M", time.localtime()),xf)
    print sheet.cell_value(row, 3),row
    # xls.save('工作记录单.xlsx')   xls.handle_writeaccess()
    print sheet.name, sheet.nrows, sheet.ncols,sheet.cell_value(0,0).encode('utf-8'),\
        sheet.cell_value(2,3),time.strftime("%Y / %m / %d %H:%M", time.localtime())

    # xlsw = xlwt.Workbook('worklog.xlsx')
    # sheetw = xlsw.get_sheet(1)

if __name__ == "__main__":
    writelog()