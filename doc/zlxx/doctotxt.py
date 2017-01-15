# -*- coding=utf-8 -*-
from readdoc import *
import sys,os

docdir = sys.path[0]
print docdir
doclist = os.walk(docdir)
for root, dirs, files in doclist:
    for name in files:
        print os.path.join(root, name)
        # 预留位置。要保证所有的文档都有对应的txt，目前采用手动保存模式。
        filename = os.path.join(root, name)
        if '.docx' in filename:
            docx2txt(filename)
            newfilename = filename.replace(u'.docx', u'.txt')
        elif '.doc' in filename:
            doc2txt(filename)
            newfilename = filename.replace(u'.doc', u'.txt')
