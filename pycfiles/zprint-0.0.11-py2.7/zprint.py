# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zprint.py
# Compiled at: 2018-12-03 00:35:06
import sys, datetime

def get_filename():
    name = []
    a = sys._getframe()
    while a is not None:
        name.append(a.f_code.co_filename)
        a = a.f_back

    return name[(-1)]


def get_tree():
    filename = get_filename()
    name = []
    a = sys._getframe()
    linenum = a.f_back.f_lineno
    while a is not None:
        name.append(a.f_code.co_name + '(line:' + str(a.f_lineno) + ')')
        a = a.f_back

    funclist = '%s main' % filename
    spacelist = '    '
    for i in range(-1, -len(name) + 1, -1):
        funclist += ' - ' + name[i]

    return (funclist, '%s %s %s' % (filename, (len(name) - 2) * ' -  ', name[2]))


def addinfo(message, flag=1):
    funclist, spacelist = get_tree()
    flist = (funclist, spacelist)[flag]
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info = '[%s] %s :: %s' % (nowTime, flist, message)
    return info


def zprintr(message, flag=1):
    info = addinfo(message, flag)
    sys.stdout.write(info + '\r')
    sys.stdout.flush()


def zprint(message, flag=1):
    info = addinfo(message, flag)
    sys.stdout.write(info + '\n')


def eprint(message, flag=1):
    info = addinfo(message, flag)
    sys.stderr.write(info + '\n')


def pprint(i, i_all, width, outstr=sys._getframe().f_code.co_name):
    nn = i % width
    sys.stdout.write('\r %s: ' % outstr + nn * '#' + (width - nn) * ' ' + '%.2f%%' % (float(i) / float(i_all) * 100))
    sys.stdout.flush()


def zhelp():
    sys.stdout.write(' # pip install zprint -i https://pypi.python.org/simple\n')
    sys.stdout.write(' from zprint import *\n')
    sys.stdout.write(' \n')
    sys.stdout.write(' def fun2():\n')
    sys.stdout.write('     zprint(" I am in fun2",1)\n')
    sys.stdout.write('     zprint(" I am in fun2",0)\n')
    sys.stdout.write(' \n')
    sys.stdout.write(' def fun1():\n')
    sys.stdout.write('     zprint(" I am in fun1")\n')
    sys.stdout.write('     fun2()\n')
    sys.stdout.write(' \n')
    sys.stdout.write(' if __name__=="__main__":\n')
    sys.stdout.write('    fun1()\n')


def fun2():
    zprint(' I am in fun2', 1)
    zprint(' I am in fun2', 0)


def fun1():
    zprint(' I am in fun1')
    fun2()


if __name__ == '__main__':
    fun1()
    zhelp()
    zprint('main')