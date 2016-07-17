#encoding:utf-8
'''
根据一个给定的XML Schema，使用DOM树的形式从空白文件生成一个XML。
创建最基本的AIML。形式:
<?xml version="1.0" encoding="GB2312"?>
<aiml>
<category>
    <pattern>你好</pattern>
    <template>好</template>
</category>
</aiml>
通过输入template写成<srai>BYE</srai>,可以进行同义替换
输入改为列表

TODOS: 研究如何向已有的aiml文件中增加条目、合并条目。
'''
from xml.dom import minidom
import traceback
import xlrd
from wordscut import jiebacut
import jieba # 利用jieba进行中文分词
import nltk  # 利用nltk进行其他处理
import re
import pandas

def format(file,patterns,templates):
    '''
    通过输入pattern和template值创建一个最基本的AIML。利用xml.dom生成结构化的aiml文本
    :param file:
    :param patterns:
    :param templates:
    :return:
    '''
    try:
        f = open(file, "w")

        try:
            doc = minidom.Document()

            #创建aiml标签
            aimlNode = doc.createElement("aiml")
            aimlNode.setAttribute('version', "1.0")
            doc.appendChild(aimlNode)

            #创建meta标签
            metaNode = doc.createElement("meta")
            metaNode.setAttribute("author", "KevinBean")
            metaNode.setAttribute("language", "zh")
            aimlNode.appendChild(metaNode)

            for x in range(len(patterns)):
                # 创建category标签
                categoryNode = doc.createElement("category")
                aimlNode.appendChild(categoryNode)

                # 创建pattern标签
                patternNode = doc.createElement("pattern")
                pattern_text = doc.createTextNode(patterns[x].upper())# pattern的英文字符设为大写
                patternNode.appendChild(pattern_text)
                categoryNode.appendChild(patternNode)

                # 创建template标签
                templateNode = doc.createElement("template")
                template_text = doc.createTextNode(templates[x])
                templateNode.appendChild(template_text)
                categoryNode.appendChild(templateNode)

            doc.writexml(f, "\t", "\t", "\n", "utf-8")
        except:
            traceback.print_exc()
        finally:
            f.close()
        return
    except IOError:
        print "open file failed"

def xls2aiml(filename,xlsname,apart,keyword):
    '''
    利用xlrd读取2列xls文件，并利用format函数写入aiml文件
    :param filename: 输出aiml文件名＼路径
    :param xlsname: 输入xls文件名、路径
    :param apart: 分隔符
    :param keyword: 关键词
    :return: 无。生成特定aiml文件

    五种模式：
    1。 模式 * 关键字
    2。 关键字 * 模式
    3。 模式关键字
    4。 关键字模式
    5。 模式
    '''
    workbook = xlrd.open_workbook(xlsname)
    sheet = workbook.sheet_by_index(0)
    patterns = []
    templates = []

    for i in range(sheet.nrows):
        pattern = sheet.cell_value(i, 0)
        if pattern != '':

            if isinstance(pattern, unicode):
                pattern = str(pattern.encode('utf-8'))  # 特殊处理。将unicode统一处理成字符串
            pattern = pattern.replace(' ', '')  # 处理掉空格
            basepattern = jiebacut(pattern)

            template = sheet.cell_value(i, 1)
            if isinstance(template, unicode):
                template = str(template.encode('utf-8'))  # 特殊处理。将unicode统一处理成字符串
            elif isinstance(template, float):
                template = str(int(template))

            pattern = basepattern + apart + keyword # 模式1
            pattern = pattern.replace('  ',' ').replace('* *','*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = ' * ' + basepattern + apart + keyword # 模式1
            pattern = pattern.replace('  ',' ').replace('* *','*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = basepattern + apart + keyword + ' * '# 模式1
            pattern = pattern.replace('  ',' ').replace('* *','*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = ' * ' + basepattern + apart + keyword + ' * '# 模式1
            pattern = pattern.replace('  ',' ').replace('* *','*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = keyword + apart + basepattern # 模式2
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = ' * ' +keyword + apart + basepattern # 模式2
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = keyword + apart + basepattern + ' * ' # 模式2
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = ' * ' +keyword + apart + basepattern + ' * ' # 模式2
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = basepattern + ' ' + keyword      # 模式3
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = ' * ' +basepattern + ' ' + keyword       # 模式3
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = basepattern + ' ' + keyword + ' * '      # 模式3
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = ' * ' +basepattern + ' ' + keyword + ' * '      # 模式3
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = keyword + ' ' + basepattern    # 模式4
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = ' * ' +keyword + ' ' + basepattern     # 模式4
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = keyword + ' ' + basepattern + ' * '     # 模式4
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = ' * ' +keyword + ' ' + basepattern + ' * '     # 模式4
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = basepattern    # 模式5
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            template = keyword + ' ' + template
            templates = templates + [template]

            pattern = ' * ' +basepattern      # 模式5
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            template = keyword + ' ' + template
            templates = templates + [template]

            pattern = basepattern + ' * '     # 模式5
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            template = keyword + ' ' + template
            templates = templates + [template]

            pattern = ' * ' +basepattern + ' * '     # 模式5
            pattern = pattern.replace('  ', ' ').replace('* *', '*')
            patterns = patterns + [pattern]
            template = keyword + ' ' + template
            templates = templates + [template]





    print patterns
    format(filename, patterns, templates)
    return

def txt2aiml(txtname):
    '''
    从txt文件中寻找有用信息，存入xls，再调用xls2aiml转换为aiml
    目前有以下不足：
    1。只能匹配一句回答，而且不一定是最准确的那一句；
    2。必须提前人工提取关键词去对文件建立aiml；
    3。匹配的模式变种还不够，会漏掉一些情况，需要改进xls2aiml
    :param txtname: txt文件名
    :return: 无
    '''

    # 1. 读取txt文件，并存为字符串格式
    read_file = open(txtname, 'r')
    text = read_file.read()
    text = text.replace('  ',' ')
    text = text.replace(' ','')
    text = text.decode('utf-8')


    # 2. 以工程说明书为例 分词＼分句
    project = re.compile(ur'.*[k][V].*[工][程]',re.U)
    # seg_list = jieba.cut(text, cut_all=False)
    # print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    seg_list = jieba.lcut(text, cut_all=False) #jieba分成了词
    tok = nltk.word_tokenize(text)  #nltk分成了句子

    keyword = ''
    # 3. 寻找工程名称作为输出模式关键字，因为说明书封面都会有工程名称，因此以第一次出现的工程名称为准
    for i in range(len(tok)):
        if re.match(project,tok[i]):
            m = re.findall(project, tok[i])
            keyword = m[0]
            keyword = keyword[:2].encode('utf-8')
            print keyword
            break


        '''if u'工程' in tok[i]:
            print tok[i]
            break'''
    '''
    # xlwt中文编码有问题  UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 0: ordinal not in range(128)
    workbook = xlwt.Workbook()
    sheetname = 'aiml'
    sheet = workbook.add_sheet(sheetname)

    # 寻找信息"位于"，"电缆长度"，"终端塔" 找到信息后，写入xls的行
    locate = re.compile(ur'.*[位][于].*',re.U)
    cablelengh = re.compile(ur'.*[电][缆].*［长][度].*',re.U)
    tower = re.compile(ur'.*[终][端][塔].*',re.U)
    j = 0
    for i in range(len(tok)):
        if re.match(locate,tok[i]):
            m = re.findall(locate, tok[i])
            sheet.write(j,0,u"位于")
            sheet.write(j,1,m[0].encode('utf-8'))
            j = j+1
        elif re.match(cablelengh,tok[i]):
            m = re.findall(cablelengh, tok[i])
            sheet.write(j,0,u"电缆 * 长度")
            sheet.write(j,1,m[0].encode('utf-8'))
            j = j + 1
        elif re.match(tower,tok[i]):
            m = re.findall(tower, tok[i])
            sheet.write(j,0,u"终端塔")
            sheet.write(j,1,m[0].encode('utf-8'))
            j = j + 1
    # print sheet.cell_value(2,1)
    xlsname = txtname.replace('txt','xls').encode('utf-8')# 保存成xls文件，便于xls2aiml函数调用
    workbook.save(xlsname)

    '''

    locate = re.compile(ur'.*[位][于].*', re.U)
    cablelengh = re.compile(ur'.*[电][缆].*［长][度].*', re.U)
    tower = re.compile(ur'.*[终][端][塔].*', re.U)

    locatesheet = '无信息'
    cablelenghsheet = '无信息'
    towersheet = '无信息'
    # 4. 根据搜索关键字，寻找对应信息
    for i in range(len(tok)):
        if re.match(locate, tok[i]):
            m = re.findall(locate, tok[i])
            locatesheet = m[0]
        elif re.match(cablelengh, tok[i]):
            m = re.findall(cablelengh, tok[i])
            cablelenghsheet = m[0]
        elif re.match(tower, tok[i]):
            m = re.findall(tower, tok[i])
            towersheet = m[0]
    sheet = [locatesheet,cablelenghsheet,towersheet]
    print sheet

    # 5. 写成2列的xls文件
    '''fdict = dict(sheet)
    print fdict
    sheet = pandas.DataFrame(fdict,index=[0])'''
    pd = pandas.DataFrame(sheet,index=[u" 位于 ",u" 电缆 * 长度 ",u" 终端塔 "])

    xlsname = txtname.replace('txt', 'xls') # 保存成xls文件，便于xls2aiml函数调用
    sheetname = 'aiml'
    pd.to_excel(xlsname, sheetname, engine='openpyxl')  # engine改为'openpyxl'即可写入unicode
    # ew.save()  #需要用变量代替

    filename = txtname.replace('txt', 'aiml').replace('doc/','standard/cn-')  # 保存成aiml文件，便于aiml函数调用
    apart = ' * '  # 分隔符
    # 6. 利用xls2aiml将xls文件变为aiml
    xls2aiml(filename,xlsname,apart,keyword)

    # print seg_list
    print seg_list
    print tok

def writetoaiml(aimlfile,cat):
    '''
    非结构化的aiml规则库生成方法
    :param aimlfile:
    :param cat:
    :return:
    '''
    out = open(aimlfile,'w')
    out.write('<?xml version="1.0" encoding="utf-8"?>\n')
    out.write('< aiml version = "1.0" >\n')
    out.write("  <category>\n")
    out.write("    <pattern>")
    pat = cat.pattern.encode("utf-8")
    if not pat.strip():
        return
    else:
        pat = pat.replace("&", "&amp;")
        pat = pat.replace("<", "&lt;")
        pat = pat.replace(">", "&gt;")
        pat = pat.replace("'", "&apos;")
        pat = pat.replace('"', "&quot;")
        out.write(pat)
    out.write("</pattern>\n")
    out.write("    <template>\n")
    print cat.pattern
    if len(cat.tempaltes) > 1:
        out.write("      <random>\n")
        for template in cat.tempaltes:
            print template
            out.write("        <li>")
            temp = template.encode("utf-8").replace("&", "&amp;")
            temp = temp.replace("<", "&lt;")
            temp = temp.replace(">", "&gt;")
            temp = temp.replace("'", "&apos;")
            temp = temp.replace('"', "&quot;")
            out.write(temp)
            out.write("</li>\n")
            # count += 1
            out.write("      </random>\n")
    else:
        template = cat.tempaltes("utf-8")
        print template
        temp = template.replace("&", "&amp;")
        temp = temp.replace("<", "&lt;")
        temp = temp.replace(">", "&gt;")
        temp = temp.replace("'", "&apos;")
        temp = temp.replace('"', "&quot;")
        # charset=chardet.detect(words)["encoding"]
        out.write(temp + '\n')
    out.write("    </template>\n")
    out.write("  </category>\n")
    out.write('< /aiml >\n')
    out.flush()

if __name__ == "__main__":
    '''
     # Run some self-tests
     filename = "standard/cn-xmlstuff.aiml"
     patterns = ["wenti1","wenti2","再见"]
     templates = ["daan1","daan2","<srai>BYE</srai>"]
     format(filename, patterns, templates)
     # 生成commands文件
     filename = "standard/cn-commands.aiml"
     patterns = ["quit","worklog*","再见"]
     templates = ["exe"+"cexit()","exec"+"writelog(msg)","<srai>BYE</srai>"]
     format(filename, patterns, templates)
     # quit:exit()
     # worklog:worklog(msg) msg是调用时的输入函数
     '''

    filename = "standard/cn-phone.aiml"
    xlsname = "doc/phone.xls"
    apart = ' * ' #分隔符
    keyword = "电话" #关键字
    xls2aiml(filename,xlsname,apart,keyword)


    filename = u'doc/SL351C-A11-01.txt'
    txt2aiml(filename)


