# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ROC\Analyze.py
# Compiled at: 2018-08-20 02:35:42
import xml.dom.minidom, os.path
from read import read
from IOU import IOU
import os

def Analyze(standard_path, test_path):
    """
    return:pos_num,ratio_info
    ratio_info:wrong,right,ratio/sore
    
    """
    print 'is doing analyze'
    wrong, right, num_pos = (0, 0, 0)
    ratio = 0.0
    ratio_info = []
    frame_stand = frame_test = []
    folder_stand = standard_path
    folder_test = test_path
    files_stand = os.listdir(folder_stand)
    files_test = os.listdir(folder_test)
    files_all = files_test
    files_temp = []
    temp_y = 0
    for File in files_stand:
        path_test = os.path.join(folder_test, File)
        path_stand = path_test.replace(folder_test, folder_stand)
        if not os.path.isfile(path_test):
            files_all.append(File)
            files_temp.append(File)

    for File in files_all:
        if File in files_temp:
            path_stand = os.path.join(folder_stand, File)
            dom_stand = xml.dom.minidom.parse(path_stand)
            root_stand = dom_stand.documentElement
            frame_stand = read(root_stand)
            boxnum_stand = len(frame_stand)
            num_pos += boxnum_stand
            num_info = len(frame_test[0])
            wrong = 0
            right = 0
            ratio = 0.0
            for i in range(0, boxnum_stand):
                if num_info == 5:
                    temp_y = 1
                    ratio_info.append([wrong, right, frame_test[i][4]])
                else:
                    ratio_info.append([wrong, right, ratio])

        else:
            path_test = os.path.join(folder_test, File)
            path_stand = path_test.replace(folder_test, folder_stand)
            if not os.path.isfile(path_stand):
                dom_test = xml.dom.minidom.parse(path_test)
                root_test = dom_test.documentElement
                frame_test = read(root_test)
                boxnum_test = len(frame_test)
                num_info = len(frame_test[0])
                wrong = 1
                right = 0
                ratio = 0.0
                for i in range(0, boxnum_test):
                    if num_info == 5:
                        ratio_info.append([wrong, right, frame_test[i][4]])
                    else:
                        ratio_info.append([wrong, right, ratio])

            else:
                dom_test = xml.dom.minidom.parse(path_test)
                root_test = dom_test.documentElement
                frame_test = read(root_test)
                boxnum_test = len(frame_test)
                num_info = len(frame_test[0])
                dom_stand = xml.dom.minidom.parse(path_stand)
                root_stand = dom_stand.documentElement
                frame_stand = read(root_stand)
                boxnum_stand = len(frame_stand)
                num_pos += boxnum_stand
                for i in range(0, boxnum_test):
                    boxnum_stand = len(frame_stand)
                    wrong = right = 0
                    if boxnum_stand == 0:
                        wrong = 1
                        ratio = 0.0
                        if num_info == 5:
                            ratio_info.append([wrong, right, frame_test[i][4]])
                        else:
                            ratio_info.append([wrong, right, ratio])
                    else:
                        for j in range(0, boxnum_stand):
                            ratio = IOU(frame_test[i], frame_stand[j])
                            if ratio >= 0.5:
                                right = 1
                                if num_info == 5:
                                    ratio_info.append([wrong, right, frame_test[i][4]])
                                else:
                                    ratio_info.append([wrong, right, ratio])
                                del frame_stand[j]
                                break

                    if right == 0:
                        wrong = 1
                        if num_info == 5:
                            ratio_info.append([wrong, right, frame_test[i][4]])
                        else:
                            ratio_info.append([wrong, right, ratio])

    print ' Analyze is OK'
    return (num_pos, ratio_info, temp_y)


if __name__ == '__main__':
    Analyze('D:\\python_work\\bndbox_test\\roc-2.1.1\\ROC\\truth', 'D:\\python_work\\bndbox_test\\roc-2.1.1\\ROC\\test')