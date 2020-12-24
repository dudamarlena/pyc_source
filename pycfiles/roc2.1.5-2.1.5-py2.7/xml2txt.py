# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\transform\xml2txt.py
# Compiled at: 2018-08-09 07:30:44
import os, os.path, xml.dom.minidom

def xml2txt(pre_file='xml_file', after_file='txt_file'):
    files1 = os.listdir(pre_file)
    count = 0
    for xmlFile in files1:
        if not os.path.isdir(xmlFile) and xmlFile.endswith('.xml'):
            count += 1
            print 'file %d is opened successfully' % count
            dom = xml.dom.minidom.parse(os.path.join(pre_file, xmlFile))
            root = dom.documentElement
            if len(root.getElementsByTagName('xmin')) == 0:
                continue
            filename = root.getElementsByTagName('filename')
            score = root.getElementsByTagName('score')
            xmin = root.getElementsByTagName('xmin')
            xmax = root.getElementsByTagName('xmax')
            ymin = root.getElementsByTagName('ymin')
            ymax = root.getElementsByTagName('ymax')
            rectnum = len(xmin)
            n0 = filename[0]
            Name = n0.firstChild.data
            meg = Name[:-4] + ' ' + str(rectnum)
            for i in range(0, rectnum):
                n1 = xmin[i]
                n2 = xmax[i]
                n3 = ymin[i]
                n4 = ymax[i]
                Xmin = n1.firstChild.data
                Xmax = n2.firstChild.data
                Ymin = n3.firstChild.data
                Ymax = n4.firstChild.data
                if len(score) >= 1:
                    n5 = score[i]
                    Score = n5.firstChild.data
                    meg += ' ' + str(Xmin) + ' ' + str(Ymin) + ' ' + str(Xmax) + ' ' + str(Ymax) + ' ' + str(Score)
                else:
                    meg += ' ' + str(Xmin) + ' ' + str(Ymin) + ' ' + str(Xmax) + ' ' + str(Ymax)

            if not os.path.exists(after_file):
                os.mkdir(after_file)
            full_path = os.path.join(after_file, Name)
            file = open(full_path, 'w')
            file.write(meg)
            file.close()

    print '\n\nxml2txt is OK!'


xml2txt('xml_file', 'txt_file')