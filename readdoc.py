# -*- coding=utf-8 -*-
# import pandas
from docx import Document #使用python-docx包
import jieba # 利用jieba进行中文分词
import nltk  # 利用nltk进行其他处理
from win32com import client as wc
import os


def docx2txt(filename):
    # 从word（docx格式）中提取text，保存为txt
    document = Document(filename)
    docText = '\n\n'.join([
                              paragraph.text.encode('utf-8') for paragraph in document.paragraphs
                              ])
    print docText

    # 保存文件
    # document.save('doc/new-SL351C-A11-01.doc')
    newfilename = filename.replace(u'docx', u'txt')
    output_file = open(newfilename, 'w')
    output_file.write(docText)
    output_file.close()

def doc2txt(filename):
    word = wc.Dispatch('Word.Application')
    filename = os.path.normpath(filename)
    print filename
    doc = word.Documents.Open(filename) # 所有Paragraph即段落对象，都是通过Paragraph.Range.Text来访问它的文字的
    docText = '\n\n'.join([
                              paragraph.Range.Text.encode('utf-8') for paragraph in doc.paragraphs
                              ])
    word.Quit()
    newfilename = filename.replace(u'.doc', u'.txt')
    print newfilename
    output_file = open(newfilename, 'w')
    output_file.write(docText)
    output_file.close()

if __name__ == '__main__':
    filename = ur'D:\Personal\我的文档\GitHub\chatbot\doc\X9384K-AB-01.doc' # u'doc/管廊缆线敷设技术条件.docx'
    filename = os.path.normpath(filename)
    print filename
    # filename = r'd:/test1.doc'
    doc2txt(filename)
    newfilename = filename.replace(u'.doc', u'.txt')
    read_file = open(newfilename,'r')
    text = read_file.read()
    text = text.replace('  ',' ')
    text = text.replace(' ','')
    text = text.decode('utf-8')
    # seg_list = jieba.cut(text, cut_all=False)
    # print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    seg_list = jieba.lcut(text, cut_all=False) #jieba分成了词
    tok = nltk.word_tokenize(text)  #nltk分成了句子
    # print seg_list
    print seg_list
    print tok
    #print seg_list.count(u'电缆')

