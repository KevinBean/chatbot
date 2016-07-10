# -*- coding=utf-8 -*-

import string
import re
punctuation = "\"`~!@#$%^&*()-_=+[{]}\|;:',<.>/?"
_puncStripRE = re.compile("[" + re.escape(punctuation) + "]")
_whitespaceRE = re.compile("\s+", re.LOCALE | re.UNICODE)
#测试upper会不会改变中文输入内容。答案是不会,hello->HELLO,你好->你好
pattern = raw_input('Enter:')
print str(pattern)
print pattern.decode('utf-8')
input = string.upper(pattern)
print input.decode('utf-8')
input = re.sub(_puncStripRE, " ", input) # 用正则替换input,特殊符号变成空格
print input.decode('utf-8')
input = re.sub(_whitespaceRE, " ", input) # 用正则替换input,特殊符号变成空格
print input.decode('utf-8')

'''Enterhello friend,毕业!
hello friend,毕业!
HELLO FRIEND,毕业!
HELLO FRIEND 毕业
HELLO FRIEND 毕业 '''