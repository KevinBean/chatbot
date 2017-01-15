# -*- coding=utf-8 -*-
from scrapemark import scrape

docdir = sys.path[0]
print docdir
doclist = os.walk(docdir)
for root, dirs, files in doclist:
    for name in files[:3]:
        print os.path.join(root, name)
        # 预留位置。要保证所有的文档都有对应的txt，目前采用手动保存模式。
        filename = os.path.join(root, name) # .decode('gbk').encode('utf-8')
        print filename.decode('gbk').encode('utf-8')
        input_file = open(filename, 'r')
        txt = input_file.read()
        input_file.close()

        scrape("""
               your pattern here
               """,
               url='http://someurl.com/')



