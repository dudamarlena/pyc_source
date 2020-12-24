# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /d3/local/anaconda/lib/python2.7/site-packages/wlab/__wgetfilelist__.py
# Compiled at: 2013-08-11 09:09:31


def IsSubString(SubStrList, Str):
    u"""
    #判断字符串Str是否包含序列SubStrList中的每一个子字符串
    #>>>SubStrList=['F','EMS','txt']
    #>>>Str='F06925EMS91.txt'
    #>>>IsSubString(SubStrList,Str)#return True (or False)
    """
    flag = True
    for substr in SubStrList:
        if substr not in Str:
            flag = False

    return flag


def GetFileList(FindPath, FlagStr=[]):
    u"""
    #获取目录中指定的文件名
    #>>>FlagStr=['F','EMS','txt'] #要求文件名称中包含这些字符
    #>>>FileList=GetFileList(FindPath,FlagStr) #
    """
    import os
    FileList = []
    FileNames = os.listdir(FindPath)
    if len(FileNames) > 0:
        for fn in FileNames:
            if len(FlagStr) > 0:
                if IsSubString(FlagStr, fn):
                    fullfilename = os.path.join(FindPath, fn)
                    FileList.append(fullfilename)
            else:
                fullfilename = os.path.join(FindPath, fn)
                FileList.append(fullfilename)

    if len(FileList) > 0:
        FileList.sort()
    return FileList