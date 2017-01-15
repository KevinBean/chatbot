# coding=utf-8
import sys,os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import json

# 使用结巴中文分词
analyzer = ChineseAnalyzer()

# 使用Whoosh的第一步就是要建立索引对象schema（Json模式）。首先要定义索引模式，以字段的形式列在索引中。
# itle/path/content就是所谓的字段。每个字段对应索引查找目标文件的一部分信息，
# 下面的例子中就是建立索引的模式：索引内容包括title/path/content。
# 一个字段建立了索引，意味着它能够被搜索；也能够被存储，意味着返回结果。
# stored为True表示能够被检索;这里在某些字段后面添加了(stored=True)，意味着将返回该字段的搜索结果
schema = Schema(title = TEXT(stored=True,analyzer=analyzer),path = ID(stored=True),
                content = TEXT(stored=True,analyzer=analyzer))

# 存储schema信息至'indexdir'目录下
indexdir = 'indexdir/'
if not os.path.exists(indexdir):
    os.mkdir(indexdir)

# 按照schema模式建立索引目录
ix = create_in(indexdir, schema)

# 写索引文件
# 按照schema定义信息，增加需要建立索引的文档
# 注意：字符串格式需要为unicode格式
writer = ix.writer()

# 读zlxx的内容并存入搜索数据库
thisdir = sys.path[0]
docdir = thisdir+os.sep +'doc'+os.sep + 'zlxx' # 用os.sep表示系统文件夹分隔符
doclist = os.walk(docdir)
for root, dirs, files in doclist:
    print files
    for name in files:
        print os.path.join(root, name)
        # 预留位置。要保证所有的文档都有对应的txt，目前采用手动保存模式。
        filename = os.path.join(root, name)  # .decode('gbk').encode('utf-8')
        # print filename.decode('gbk').encode('utf-8')
        # print chardet.detect(filename)
        # print filename.replace('.doc', '.txt')
        title = u''
        if filename[-5:] == '.docx':
            title = filename.replace('.docx', '')
            newfilename = filename.replace('.docx', '.txt')
            # 读取文件内容
            input_file = open(newfilename, 'r')
            txt = input_file.read()
            input_file.close()

            writer.add_document(title=title.decode('utf-8'),
                                path=filename.decode('utf-8'), content=txt.decode('utf-8'))
        elif filename[-4:] == '.doc':
            title = filename.replace('.doc', '')
            newfilename = filename.replace('.doc', '.txt')
            # 读取文件内容
            input_file = open(newfilename, 'r')
            txt = input_file.read()
            input_file.close()

            writer.add_document(title=title.decode('utf-8'),
                                path=filename.decode('utf-8'), content=txt.decode('utf-8'))



writer.add_document(title=u"第一篇文档", path=u"/a",
                    content=u"这是我们增加的第一篇文档")
writer.add_document(title=u"第二篇文档", path=u"/b",
                    content=u"第二篇文档也很interesting！")
writer.commit()

# 检索方式1
try:
    searcher = ix.searcher()  # 创建一个检索器
    # 检索标题中出现'文档'的文档
    results = searcher.find("title", u"文档")
    # 检索出来的第一个结果，数据格式为dict{'title':.., 'content':...}
    firstdoc = results[0].fields()
    # python2中，需要使用json来打印包含unicode的dict内容
    jsondoc = json.dumps(firstdoc, ensure_ascii=False)

    print jsondoc  # 打印出检索出的文档全部内容
    print results[0].highlights("title")  # 高亮标题中的检索词
    print results[0].score  # bm25分数

finally:
    searcher.close()

# 检索方式2
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse(u"电缆终端")
    results = searcher.search(query)
    for result in results:
        print result['path'], '\n-------------------', \
            result.highlights('content'), '\n-------------------\n-------------------'
print ix.doc_count()