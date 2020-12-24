# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\transform\txt2xml.py
# Compiled at: 2018-08-06 22:55:54
import xml.dom.minidom, os, os.path

def txt2xml(pre_file='txt_file', after_file='xml_file'):
    line = []
    temp = 0
    files1 = os.listdir(pre_file)
    for xmlFile in files1:
        temp = temp + 1
        with open(os.path.join(pre_file, xmlFile), 'r') as (fs):
            print 'file %d is opened successfully' % temp
            managerList = []
            doc = xml.dom.minidom.Document()
            root = doc.createElement('annotation')
            root.setAttribute('verified', 'no')
            doc.appendChild(root)
            nodedata = doc.createElement('folder')
            nodedata.appendChild(doc.createTextNode(after_file))
            root.appendChild(nodedata)
            nodedata = doc.createElement('filename')
            nodedata.appendChild(doc.createTextNode(xmlFile))
            root.appendChild(nodedata)
            nodedata = doc.createElement('path')
            nodedata.appendChild(doc.createTextNode(os.path.join(after_file, xmlFile)))
            root.appendChild(nodedata)
            nodedata = doc.createElement('source')
            nodeson = doc.createElement('database')
            nodeson.appendChild(doc.createTextNode('Unknown'))
            nodedata.appendChild(nodeson)
            root.appendChild(nodedata)
            nodedata = doc.createElement('size')
            nodewidth = doc.createElement('width')
            nodewidth.appendChild(doc.createTextNode('0'))
            nodeheight = doc.createElement('height')
            nodeheight.appendChild(doc.createTextNode('0'))
            nodedepth = doc.createElement('depth')
            nodedepth.appendChild(doc.createTextNode('0'))
            nodedata.appendChild(nodewidth)
            nodedata.appendChild(nodeheight)
            nodedata.appendChild(nodedepth)
            root.appendChild(nodedata)
            nodedata = doc.createElement('segmented')
            nodedata.appendChild(doc.createTextNode('0'))
            root.appendChild(nodedata)
            str = fs.read()
            line = str.split()
            for i in range(0, int(line[1])):
                managerList.append([{'xmin': line[(2 + i * 4)], 'ymin': line[(3 + i * 4)], 'xmax': line[(4 + i * 4)], 'ymax': line[(5 + i * 4)]}])

            for i in managerList:
                for j in range(len(i)):
                    nodedata = doc.createElement('object')
                    nodename = doc.createElement('name')
                    nodename.appendChild(doc.createTextNode('NULL'))
                    nodepose = doc.createElement('pose')
                    nodepose.appendChild(doc.createTextNode('Unspecified'))
                    nodetruncated = doc.createElement('truncated')
                    nodetruncated.appendChild(doc.createTextNode('1'))
                    nodedifficult = doc.createElement('difficult')
                    nodedifficult.appendChild(doc.createTextNode('0'))
                    nodedata.appendChild(nodename)
                    nodedata.appendChild(nodepose)
                    nodedata.appendChild(nodetruncated)
                    nodedata.appendChild(nodedifficult)
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
                    nodedata.appendChild(nodeManager)
                    root.appendChild(nodedata)

            if not os.path.exists(after_file):
                os.mkdir(after_file)
            pathn = os.path.join(after_file, line[0])
            pathn += '.xml'
            fp = open(pathn, 'w')
            doc.writexml(fp, indent='\t', addindent='\t', newl='\n')

    print 'Transform_txt_xml() is OK'


if __name__ == '__main__':
    txt2xml()