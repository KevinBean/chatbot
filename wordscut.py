# -*- coding: latin-1 -*-
# 使用jieba进行分词，同时用在建立amil数据库pattern生成和使用amil的msg匹配上，以达到一致的目的。
import jieba

def jiebacut(sentence):
    sentence = sentence.replace(' ', '')  # 处理掉空格
    jieba.load_userdict('user.dict')  # file_name 为文件类对象或自定义词典的路径
    word_list = jieba.cut(sentence, cut_all=False)  # 分词
    words = '' + ' '.join(word_list) # 分词后用空格分隔，进行匹配
    words = str(words.encode('utf-8'))  # 特殊处理。将unicode统一处理成字符串
    return words


