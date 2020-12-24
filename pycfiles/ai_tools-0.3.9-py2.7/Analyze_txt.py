# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/Analyze_txt.py
# Compiled at: 2018-08-23 09:57:22
import xml.dom.minidom, os.path
from read import read, readgt
from IOU import IOU
import os

def txt2xml(txtfilename, xmlfilename):
    with open(txtfilename, 'r') as (fs):
        managerList = []
        doc = xml.dom.minidom.Document()
        root = doc.createElement('Recognition')
        root.setAttribute('type', 'face')
        doc.appendChild(root)
        str = fs.read()
        line = str.split()
        print line
        for i in range(0, int(line[1])):
            managerList.append([{'xmin': line[(3 + i * 5)], 'ymin': line[(2 + i * 5)], 'xmax': line[(5 + i * 5)], 'ymax': line[(4 + i * 5)], 'score': line[(6 + i * 5)]}])

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
                nodeScore = doc.createElement('score')
                nodeScore.appendChild(doc.createTextNode(i[j]['score']))
                nodeManager.appendChild(nodeXmin)
                nodeManager.appendChild(nodeYmin)
                nodeManager.appendChild(nodeXmax)
                nodeManager.appendChild(nodeYmax)
                nodeManager.appendChild(nodeScore)
                root.appendChild(nodeManager)

        print line[0]
        fp = open(xmlfilename, 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding='utf-8')


def Analyze_txt(standard_path, test_path):
    wrong, creat, pos = (0, 0, 0)
    ratio = 0.0
    list1 = []
    Reframe = GTframe = []
    path1 = standard_path
    path2 = test_path
    files1 = os.listdir(path2)
    cc1 = 0
    cc2 = 0
    for xmlFile in files1:
        print xmlFile
        testpath_txt = os.path.join(path2, xmlFile)
        testpath_xml = 'tmp.xml'
        print testpath_txt
        print testpath_xml
        txt2xml(testpath_txt, testpath_xml)
        standpath_xml = testpath_txt.replace(path2, path1)
        standpath_xml = standpath_xml.replace('.txt', '.xml')
        print '**********'
        print standpath_xml
        print testpath_xml
        if os.path.isfile(standpath_xml):
            dom_test = xml.dom.minidom.parse(testpath_xml)
            dom_stand = xml.dom.minidom.parse(standpath_xml)
            root1 = dom_test.documentElement
            root2 = dom_stand.documentElement
            Reframe = read(root1)
            GTframe = readgt(root2)
            print GTframe
            print Reframe
            pos += len(GTframe)
            cc1 += 1
            for i in range(len(Reframe)):
                wrong = creat = 0
                score = float(Reframe[i][4])
                print 'score=%f' % score
                for j in range(len(GTframe)):
                    ratio = IOU(Reframe[i], GTframe[j])
                    if ratio >= 0.5:
                        del GTframe[j]
                        creat = 1
                        list1.append([creat, wrong, score])
                        break

                if creat == 0:
                    wrong = 1
                    list1.append([creat, wrong, score])

        else:
            print 'file not exist!'
            cc2 += 1
            creat = wrong = 0
            dom_test = xml.dom.minidom.parse(testpath_xml)
            root1 = dom_test.documentElement
            Reframe = read(root1)
            for i in range(len(Reframe)):
                ratio = 0
                wrong = 1
                list1.append([creat, wrong, ratio])

        print cc1, cc2

    return (
     list1, pos)


if __name__ == '__main__':
    txtfilename = 'Analyze_test.txt'
    xmlfilename = 'Analyze_test.xml'
    txt2xml(txtfilename, xmlfilename)