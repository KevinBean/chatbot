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
'''
from xml.dom import minidom
import traceback
import xlrd
from wordscut import jiebacut

def format(file,patterns,templates):
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
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = keyword + apart + basepattern # 模式2
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = basepattern + ' ' + keyword       # 模式3
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = keyword + ' ' + basepattern      # 模式4
            patterns = patterns + [pattern]
            templates = templates + [template]

            pattern = basepattern      # 模式5
            patterns = patterns + [pattern]
            templates = templates + [template]

    print patterns
    format(filename, patterns, templates)
    return




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


