# -*- coding=utf-8 -*-
# import pandas
from docx import Document

# 从word中提取text
document = Document(u'doc/管廊缆线敷设技术条件.docx')
docText = '\n\n'.join([
    paragraph.text.encode('utf-8') for paragraph in document.paragraphs
])
print docText

# 保存文件
document.save('doc/new-SL351C-A11-01.doc')