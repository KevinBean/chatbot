# -*- coding=utf-8 -*-
''' scrapemark无法从pip获得，本地安装成功，但是找不到地址
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

'''
import chardet
from scrapely import Scraper
from scrapely.htmlpage import HtmlPage
s = Scraper()
url1 = '/Users/bianbin/PycharmProjects/chatbot/doc/zlxx/01质量信息反馈单－刘毅梅.txt'
input_file = open(url1, 'r')
txt = input_file.read()
# print txt, chardet.detect(txt)
# body = txt.decode('gb2312')
# print body, chardet.detect(body), type(body)
input_file.close()
page1 = HtmlPage(body=txt.decode('utf-8'), encoding='utf-8')
print txt, page1.body, 'body', page1.url, page1.encoding
data = {
        'description': u'在陈官屯220kV变电站工程通信施工图设计中，秦皇岛供电公司提出站内除光缆外的所有线缆均要求选用阻燃铠装电缆，此要求是冀北公司统一要求。'}
s.train_from_htmlpage(page1, data)

url2 = '/Users/bianbin/PycharmProjects/chatbot/doc/zlxx/01质量信息反馈单－李雪男.txt'
input_file = open(url2, 'r')
txt = input_file.read()
input_file.close()
page2 = HtmlPage(body=txt.decode('utf-8'), encoding='utf-8')
data = s.scrape_page(page2)
print data, 'end'

'''
url1 = 'http://pypi.python.org/pypi/w3lib/1.1'
data = {'name': 'w3lib 1.1', 'author': 'Scrapy project', 'description': 'Library of web-related functions'}
s.train(url1, data)

url2 = 'http://pypi.python.org/pypi/Django/1.3'
data = s.scrape(url2)
'''