# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/txt2xml.py
# Compiled at: 2018-08-04 12:32:06
import xml.dom.minidom, os

def txt2xml(xmlfilename, txtfilename):
    with open(xmlfilename, 'r') as (fs):
        managerList = []
        doc = xml.dom.minidom.Document()
        root = doc.createElement('Recognition')
        root.setAttribute('type', 'face')
        doc.appendChild(root)
        str = fs.read()
        line = str.split()
        for i in range(0, int(line[1])):
            managerList.append([{'xmin': line[(2 + i * 4)], 'ymin': line[(3 + i * 4)], 'xmax': line[(4 + i * 4)], 'ymax': line[(5 + i * 4)]}])

        for i in managerList:
            for j in range(len(i)):
                nodeManager = doc.createElement('bndbox')
                nodeXmin = doc.createElement('xmin')
                nodeXmin.appendChild(doc.createTextNode(i[j]['xmin']))
                nodeYmin = doc.createElement('ymin')
                nodeYmin.appendChild(doc.createTextNode(i[j]['ymin']))
                nodeXmax = doc.createElement('xmax')
                nodeXmax.appendChild(doc.createTextNode(i[j]['xmax']))
                nodeYmax = doc.createElement('ymax')
                nodeYmax.appendChild(doc.createTextNode(i[j]['ymax']))
                nodeManager.appendChild(nodeXmin)
                nodeManager.appendChild(nodeYmin)
                nodeManager.appendChild(nodeXmax)
                nodeManager.appendChild(nodeYmax)
                root.appendChild(nodeManager)

        print line[0]
        fp = open(txtfilename, 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding='utf-8')


def Transform_txt_xml(pre_file='txt_file', after_file='xml_file'):
    line = []
    files1 = os.listdir(pre_file + '//*.txt')
    for xmlFile in files1:
        with open(os.path.join(pre_file, xmlFile), 'r') as (fs):
            managerList = []
            doc = xml.dom.minidom.Document()
            root = doc.createElement('Recognition')
            root.setAttribute('type', 'face')
            doc.appendChild(root)
            str = fs.read()
            line = str.split()
            for i in range(0, int(line[1])):
                managerList.append([{'xmin': line[(2 + i * 4)], 'ymin': line[(3 + i * 4)], 'xmax': line[(4 + i * 4)], 'ymax': line[(5 + i * 4)]}])

            for i in managerList:
                for j in range(len(i)):
                    nodeManager = doc.createElement('bndbox')
                    nodeXmin = doc.createElement('xmin')
                    nodeXmin.appendChild(doc.createTextNode(i[j]['xmin']))
                    nodeYmin = doc.createElement('ymin')
                    nodeYmin.appendChild(doc.createTextNode(i[j]['ymin']))
                    nodeXmax = doc.createElement('xmax')
                    nodeXmax.appendChild(doc.createTextNode(i[j]['xmax']))
                    nodeYmax = doc.createElement('ymax')
                    nodeYmax.appendChild(doc.createTextNode(i[j]['ymax']))
                    nodeManager.appendChild(nodeXmin)
                    nodeManager.appendChild(nodeYmin)
                    nodeManager.appendChild(nodeXmax)
                    nodeManager.appendChild(nodeYmax)
                    root.appendChild(nodeManager)

            print line[0]
            pathn = os.path.join(after_file, line[0])
            pathn += '.xml'
            fp = open(pathn, 'w')
            doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding='utf-8')

    print 'Transform_txt_xml() is OK'


if __name__ == '__main__':
    Transform_txt_xml()