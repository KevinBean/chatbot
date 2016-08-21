# -*- coding=utf-8 -*-
'''
根据tfidf提取信息。
'''
from gensim import corpora, models, similarities
import logging
import jieba # 利用jieba进行中文分词
import os
import csv
import pandas as pd
import time
from readdoc import *
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#对文件进行分句
def cutlines(filename):
    read_file = open(filename, 'r')
    lines = []
    for line in read_file.readlines():
        line = line.replace('	', ' ') #去掉tab键
        line = line.replace('  ', ' ')
        line = line.replace(' ', '')
        line = line.replace('\n', '') #去掉换行符
        if line != '': #去掉空白行
            lines.append(line)
    read_file.close()
    return lines

#对文件进行分词
def cutwords(filename):
    lines = cutlines(filename)
    print lines
    words = []
    for line in lines:
        words.append(jieba.lcut(line, cut_all=False))
    return words

# 建立语料 函数
def filetoDict(filename, dictpath):
    dictionary = corpora.Dictionary()
    for file in filename:
        # 将列表中的词转为word-id映射字典 bag of words 词袋
        words = cutwords(file)
        # words =[['neatest', 'little', 'guide', 'stock', 'market', 'investing'], ['investing', 'dummies,', '4th', 'edition'], ['little', 'book', 'common', 'sense', 'investing:', 'way', 'guarantee', 'fair', 'share', 'stock', 'market', 'returns'], ['little', 'book', 'value', 'investing'], ['value', 'investing:', 'graham', 'buffett', 'beyond'], ['rich', "dad's", 'guide', 'investing:', 'rich', 'invest', 'in,', 'poor', 'middle', 'class', 'not!'], ['investing', 'real', 'estate,', '5th', 'edition'], ['stock', 'investing', 'dummies'], ['rich', "dad's", 'advisors:', "abc's", 'real', 'estate', 'investing:', 'secrets', 'finding', 'hidden', 'profits', 'investors', 'miss']]
        dictionary.merge_with(corpora.Dictionary(words))
    dictionary.save_as_text(dictpath)
    return dictionary

def findinFile(filename, dictionary, sample): #使用tfidf
    lines = cutlines(filename)
    words = cutwords(filename)
    corpus = [dictionary.doc2bow(word) for word in words]
    # 转化成tfidf
    # class gensim.models.tfidfmodel.TfidfModel(corpus=None, id2word=None, dictionary=None, wlocal=<function identity>, wglobal=<function df2idf>, normalize=True)¶
    # 转化成类
    tfidf = models.TfidfModel(corpus)
    # 调用类TfidfModel中的tfidf函数
    corpus_tfidf = tfidf[corpus]
    # 观察结果
    # for doc in corpus_tfidf:
    #    print doc

    # 将查询文档转到tfidf
    sample_tfidf = tfidf[dictionary.doc2bow(jieba.lcut(sample, cut_all=False))]

    # 查询相似度
    index = similarities.MatrixSimilarity(corpus_tfidf)
    sims = index[sample_tfidf]
    print list(enumerate(sims))

    # 排序输出,查询文档和0，7，2，3号文档相似性较高
    sims = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)
    print sims
    print sims[0]
    (x, y) = sims[0]
    return lines[x].decode('utf-8')

def findinFiles(filename, samples): #使用tfidf
    dictionary = filetoDict(filename, dictpath)
    for file in filename:
        lines = cutlines(file)
        words = cutwords(file)
        corpus = [dictionary.doc2bow(word) for word in words]
        # 转化成tfidf
        # class gensim.models.tfidfmodel.TfidfModel(corpus=None, id2word=None, dictionary=None, wlocal=<function identity>, wglobal=<function df2idf>, normalize=True)¶
        # 转化成类
        tfidf = models.TfidfModel(corpus)
        # 调用类TfidfModel中的tfidf函数
        corpus_tfidf = tfidf[corpus]
        # 观察结果
        # for doc in corpus_tfidf:
        #    print doc

        # 查询相似度
        index = similarities.MatrixSimilarity(corpus_tfidf)

        # 将查询文档转到tfidf
        sample_tfidf = tfidf[dictionary.doc2bow(jieba.lcut(sample, cut_all=False))]
        sims = index[sample_tfidf]
        # print list(enumerate(sims))

        # 排序输出,查询文档和0，7，2，3号文档相似性较高
        sims = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)
        # print sims
        # print sims[0]
        (x, y) = sims[0]
        # print file
        return lines[x]

def filepart(filename, start, end):
    '''
    提取文件的一部分，写入新文件，返回新文件内容
    :param filename:
    :param start:
    :param end:
    :return: newfilename
    '''
    newfilename = []
    for file in filename:
        lines = cutlines(file)
        docText = '\n'.join(lines[start:end])
        #print docText

        # 保存文件
        # document.save('doc/new-SL351C-A11-01.doc')
        newfile = os.path.dirname(file) + 'part' + str(start) + 'to' +str(end) + os.path.basename(file)
        output_file = open(newfile, 'w')
        output_file.write(docText)
        output_file.close()
        newfilename.append(newfile)
    return newfilename

def projectinfo(filename, excelname, sheetname, dictpath):
    dictionary = corpora.Dictionary.load_from_text(dictpath)
    # 日期
    datetime = time.strftime("%Y / %m / %d %H:%M", time.localtime())
    # 工程名
    sample_gongchengming = u'南营110kV送电工程'
    gongchengming = findinFile(filename,dictionary,sample_gongchengming)
    # 工程编号
    sample_gongchengbianhao = u'SM221C-A11-01'
    gongchengbianhao = findinFile(filename,dictionary,sample_gongchengbianhao)
    # 接地方式
    sample_jiedi = u'新建双回110kV电缆均长约3.1公里，分为六段，采用两组交叉互联、两端直接接地的接地方式，即两侧变电站GIS终端处电缆金属护套经三线接地箱接地；1#、2#、4#、5#绝缘接头处三相电缆金属护层间通过交叉互联箱使得电缆护层换位,再经过交叉互联箱内的护层保护器接地；3#绝缘接头用作直通接头，三相电缆金属护层经六线接地箱接地。'
    jiedi = findinFile(filename,dictionary,sample_jiedi)
    # 工程概况
    sample_gaikuang = u'南营110kV变电站拟建于丰台区长辛店北部地区，长辛店北部地区位于丰台永定河绿色生态发展带，目前处于全面发展的阶段，规划重点项目包括辛庄一级开发项目、201所改造项目、解放军通信团项目、丰台科技园西区II期等。其中，丰台科技园西区II期项目，总建筑面积150万平方米，主要为技术创新基地、科技成果孵化基地、高新技术产业化基地、教育科研、办公等用地，负荷预测约60MW；201所改造项目未来负荷将达到25MW；辛庄土地一级开发项目总建筑面积约129万平方米，主要为居住及配套共建用地，负荷预测约为18MW；解放军通信团项目总建筑面积约10万平方米，主要为军事类用地，负荷预测约15MW；第九届园艺博览会项目，占地267公顷，总建筑面积16万平方米，主要为旅游、商业、公建用地，负荷预测约20MW。未来该区域负荷将达到138MW。详情见下表2-1所示。'
    gaikuang = findinFile(filename, dictionary, sample_gaikuang)
    # 设计人
    shejiren = ''
    # 校核人
    jiaoheren = ''
    # 电缆路径
    sample_dianlanlujing = u'由红军营站出线后，沿北苑东路向南至现状顺白路，沿现状顺白路向东至来广营北路，最后沿来广营北路向北至黄港站，全线需新建电力隧道长度约4.1km。其中，除现状顺白路外，沿线其它道路均为市政规划道路。'
    dianlanlujing = findinFile(filename, dictionary, sample_dianlanlujing)
    # 敷设环境
    sample_fushehuanjing = u'新建双回110kV电缆敷设在电力隧道及电缆夹层中'
    fushehuanjing = findinFile(filename, dictionary, sample_fushehuanjing)
    # 盘长
    sample_panchang = u'旺控线：732米，分2盘，每盘为366米。'
    panchang = findinFile(filename, dictionary, sample_panchang)
    # 设计阶段
    shejijieduan = ''
    info = {u'日期':datetime,
                   u'工程名':gongchengming,
                                u'工程编号':gongchengbianhao,
                                u'接地方式':jiedi,
                                u'工程概况':gaikuang,
                                u'设计人':shejiren,
                                u'校核人':jiaoheren,
                                u'盘长':panchang,
                                u'电缆路径':dianlanlujing,
                                u'敷设环境':fushehuanjing,
                                u'设计阶段':shejijieduan
    }
    print info
    sheet = pd.read_excel(excelname, sheetname)  # 需要用变量代替
    sheet = pd.DataFrame(sheet)
    sheet = sheet.append(info, ignore_index=True)  # 开启ignore_index=True 则按照列标题匹配增加行数据
    sheet.to_excel(excelname, sheetname)  # engine改为'openpyxl'即可写入unicode

if __name__ == "__main__":
    filenames = [u'doc/SL351C-A11-01.txt', u'doc/SL331C-A01-01.txt', u'doc/X9384K-AB-01.txt']  # u'doc/管廊缆线敷设技术条件.docx'
    dictpath = u'dict/dict.txt' #训练数据越多越准确
    dictionary = filetoDict(filenames, dictpath)
    excelname = u'D:\Personal\我的文档\GitHub\chatbot\doc\出图统计.xlsx'
    sheetname = 'Sheet1'
    filename = u'D:\Personal\我的文档\GitHub\chatbot\doc\SK573C-A11-01.doc'
    doc2txt(filename)

    projectinfo(filename.replace(u'.doc', u'.txt'), excelname, sheetname, dictpath)

'''
    filename = [u'doc/SL351C-A11-01.txt']  # u'doc/管廊缆线敷设技术条件.docx'
    print filepart(filename, 0, 20)

    gongchengming = u'南营110kV送电工程'
    gongchengbianhao = u'SM221C-A11-01'
    riqi = '2015年5月26日'
    jiedi = u'本工程单回电缆采用两端直接接地的接地方式，即在电缆线路两端电缆终端处，电缆的金属屏蔽层及铠装层经接地引线分别引出，在灰峪站内与站内接地网做可靠连接、在终端塔侧与铁塔接地极引线做可靠连接。'
    gaikuang = u'南营110kV变电站拟建于丰台区长辛店北部地区，长辛店北部地区位于丰台永定河绿色生态发展带，目前处于全面发展的阶段，规划重点项目包括辛庄一级开发项目、201所改造项目、解放军通信团项目、丰台科技园西区II期等。其中，丰台科技园西区II期项目，总建筑面积150万平方米，主要为技术创新基地、科技成果孵化基地、高新技术产业化基地、教育科研、办公等用地，负荷预测约60MW；201所改造项目未来负荷将达到25MW；辛庄土地一级开发项目总建筑面积约129万平方米，主要为居住及配套共建用地，负荷预测约为18MW；解放军通信团项目总建筑面积约10万平方米，主要为军事类用地，负荷预测约15MW；第九届园艺博览会项目，占地267公顷，总建筑面积16万平方米，主要为旅游、商业、公建用地，负荷预测约20MW。未来该区域负荷将达到138MW。详情见下表2-1所示。'
    samples1 = [gongchengbianhao, gongchengming, riqi]
    samples2 = [jiedi, gaikuang]
    dictionary = filetoDict(filename, dictpath)
    # findinFile(filename[0], dictionary, jiedi)
    for sample in samples2:
        print findinFiles(filename, sample).decode('utf-8') #提取长段落信息时，使用全文本
    for sample in samples1:
        print findinFiles(filepart(filename,0,20), sample).decode('utf-8') # 提取工程名和编号的时候，使用文本前面一部分
'''