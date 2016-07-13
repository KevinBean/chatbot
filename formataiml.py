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
                pattern_text = doc.createTextNode(str(patterns[x]).upper())# pattern的英文字符设为大写
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



if __name__ == "__main__":
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

