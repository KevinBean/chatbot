# -*- coding=utf-8 -*-
import re
import os
import sys

if __name__ == '__main__':
    docdir = sys.path[0]
    doclist = os.walk(docdir)
    for root, dirs, files in doclist:
        fileid = 1
        for name in files:
            # 预留位置。要保证所有的文档都有对应的txt，目前采用手动保存模式。
            filename = os.path.join(root, name)  # .decode('gbk').encode('utf-8')
            if filename[-4:] == '.txt':
                newfilename = filename.replace('.txt', '.md')
                txt = ''
                md = ''
                txtfile = open(filename,'r')
                txt = txtfile.read()
                start = txt.find('信息名称')
                end = txt.find('信息内容')
                md = txt[start:end]
                # 原文件中很多转义字符，主要是制表符\t,\v,还有\r,\n。需要去除！！！
                md = md.replace('\n','').replace('\n','').replace('\n','')
                md = md.replace('\r','').replace('\r','').replace('\r','')
                md = md.replace('\t', '').replace('\t', '').replace('\t', '')
                md = md.replace('\v', '').replace('\v', '').replace('\v', '')
                md = md.replace('信息名称', 'Title:' + str(fileid))
                md = md.replace('填卡人员', '\nAuthors:')
                md = md.replace('信息来源', '\nTags:')
                md = md.replace('填卡日期', '\nDate:')
                md = md.replace('月','-')
                md = md.replace( '年','-')
                md = md.replace('.','-')
                ri = md.find('日')
                md = md[:ri]
                md = md.replace('日','')

                md = 'Category:质量信息\n' + md + '\n'
                print md
                mdfile = open(newfilename,'w')
                mdfile.write(md + txt.replace('\t','\n\n').replace('\r','\n\n').replace('\v','\n\n'))
                fileid +=1



