#encoding:utf-8
'''
根据一个给定的XML Schema，使用DOM树的形式从空白文件生成一个XML。
'''
from xml.dom import minidom
import traceback

try:
    f = open("xmlstuff.aiml", "w")

    try:
        doc = minidom.Document()

        aimlNode = doc.createElement("aiml")
        aimlNode.setAttribute('version', "1.0")
        doc.appendChild(aimlNode)

        metaNode = doc.createElement("meta")
        metaNode.setAttribute("author","KevinBean")
        metaNode.setAttribute("language", "zh")
        aimlNode.appendChild(metaNode)

        categoryNode = doc.createElement("category")
        aimlNode.appendChild(categoryNode)

        patternNode = doc.createElement("pattern")
        pattern_text = doc.createTextNode("问题")
        patternNode.appendChild(pattern_text)
        categoryNode.appendChild(patternNode)

        templateNode = doc.createElement("template")
        template_text = doc.createTextNode("回答")
        templateNode.appendChild(template_text)
        categoryNode.appendChild(templateNode)



        doc.writexml(f, "\t", "\t", "\n", "utf-8")
    except:
        traceback.print_exc()
    finally:
        f.close()

except IOError:
    print "open file failed"