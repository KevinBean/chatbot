# -*- coding: latin-1 -*-
# 使用jieba进行分词，同时用在建立amil数据库pattern生成和使用amil的msg匹配上，以达到一致的目的。
# 为了实现中文输入与模式的对应关系。 建立模式时，和处理输入时，均使用相同的分词工具进行预处理。
import jieba

def jiebacut(sentence):
    '''
    输入句子，用jieba分词后返回'utf-8'分词结果，用空格分隔
    :param sentence:
    :return: 返回分词后的unicode数据'utf-8'
    '''
    sentence = sentence.replace(' ', '')  # 处理掉空格
    jieba.load_userdict('user.dict')  # file_name 为文件类对象或自定义词典的路径
    word_list = jieba.cut(sentence, cut_all=False)  # 分词
    words = '' + ' '.join(word_list) # 分词后用空格分隔，进行匹配
    words = str(words.encode('utf-8'))  # 特殊处理。将unicode统一处理成字符串
    return words


