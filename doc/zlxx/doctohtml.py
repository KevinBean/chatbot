
# -*- coding=utf-8 -*-
from readdoc import *
import sys,os
import time

docdir = sys.path[0]
print docdir
doclist = os.walk(docdir)
for root, dirs, files in doclist:
    for name in files:
        print os.path.join(root, name)
        # 预留位置。要保证所有的文档都有对应的txt，目前采用手动保存模式。
        filename = os.path.join(root, name) # .decode('gbk').encode('utf-8')
        # print filename.decode('gbk').encode('utf-8')
        # print chardet.detect(filename)
        # print filename.replace('.doc', '.txt')
        if filename[-5:] == '.docx':
            newfilename = filename.replace('.docx', '.htm')
            if os.path.exists(newfilename):
                pass
            else:
                docx2html_utf8(filename)
                time.sleep(1)
        elif filename[-4:] == '.doc':
            newfilename = filename.replace('.doc', '.htm')
            if os.path.exists(newfilename):
                pass
            else:
                doc2html_utf8(filename)
                time.sleep(1)



