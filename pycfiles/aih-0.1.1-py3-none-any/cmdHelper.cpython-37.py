# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\cmdHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 4788 bytes
__doc__ = '\n@File    :   cmdHelper.py\n@Time    :   2019/02/27\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import sys
from enum import Enum
from colorama import init
init(autoreset=True)

def isInputYes(inputstr):
    """Return: bool"""
    if inputstr is None:
        return False
    inputstr = str(inputstr).lower()
    if inputstr == 'yes' or inputstr == 'y':
        return True
    return False


def myinput(desc):
    if sys.version_info[0] > 2:
        return input(desc)
    ret = raw_input(desc)
    if len(ret) > 0:
        if '\r' == ret[len(ret) - 1:]:
            ret = ret[:len(ret) - 1]
    return ret


def myinputInt(desc, default):
    try:
        stri = myinput(desc)
        ret = int(stri)
        return ret
    except:
        return default


def myinputFloat(desc, default):
    try:
        stri = myinput(desc)
        ret = float(stri)
        return ret
    except:
        return default


def myprintNoEnter(desc):
    sys.stdout.write(desc)


def findInArgv(stri):
    if sys.argv is None or len(sys.argv) == 0:
        return
    for item in sys.argv:
        if item == sys.argv[0]:
            continue
        if item.find(stri) >= 0:
            return item


def converArgvToStr(array):
    stri = ''
    for item in array:
        if stri != '':
            stri = stri + ' '
        stri = stri + '"' + item + '"'

    return stri


class TextColor(Enum):
    """TextColor"""
    Black = 30
    Blue = 34
    Green = 32
    Red = 31
    Yellow = 33
    White = 37


class BackGroundColor(Enum):
    Black = 40
    Blue = 44
    Green = 42
    Red = 41
    Yellow = 43
    White = 47


def myprint(desc, textColor=None, bgColor=None):
    if textColor is None and bgColor is None:
        sys.stdout.write(desc)
    else:
        color = ''
        if textColor is not None:
            color = str(textColor.value)
        if bgColor is not None:
            if color != '':
                color = color + ';'
            color = color + str(bgColor.value)
        color = color + 'm'
        sys.stdout.write('\x1b[' + color + str(desc) + '\x1b[0m')


def showTable(columns, rows, colheadColor=None, colsColor=[]):
    """Display a table
    - columns: str[y] contains of all columns name
    - rows: str[x][y] table value
    - colheadColor: #TextColor# columns headColor color
    - colsColor: #TextColor# columns color, default is None  
    """
    try:
        widths = []
        for item in columns:
            name = str(item)
            widths.append(len(name))

        for rObj in rows:
            index = 0
            for item in rObj:
                if len(str(item)) > widths[index]:
                    widths[index] = len(str(item))
                index = index + 1
                if len(widths) <= index:
                    break

        boardstr = '-'
        for item in widths:
            for i in range(item + 2 + 1):
                boardstr = boardstr + '-'

        print(boardstr)
        index = 0
        for item in columns:
            item = item.center(widths[index] + 2)
            myprintNoEnter('|')
            myprint(item, colheadColor)
            index = index + 1
            if len(widths) <= index:
                break

        print('|')
        print(boardstr)
        for rObj in rows:
            index = 0
            for index in range(len(columns)):
                if len(rObj) > index:
                    item = rObj[index]
                else:
                    item = ''
                color = None
                if len(colsColor) > index:
                    color = colsColor[index]
                item = (' ' + str(item)).ljust(widths[index] + 2)
                myprintNoEnter('|')
                myprint(item, color)
                index = index + 1
                if len(widths) <= index:
                    break

            print('|')

        print(boardstr)
        return True
    except:
        return False