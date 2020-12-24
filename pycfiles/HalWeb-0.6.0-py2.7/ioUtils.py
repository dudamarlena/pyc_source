# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/ioUtils.py
# Compiled at: 2011-12-25 05:31:43
"""Module with methods for File IO operations"""
from consoleHelpers import ask
import os, shutil

def copy_directory(source, target, ignoreDirs=[], ignoreFiles=[]):
    ignoreDirsSet = set(ignoreDirs)
    if not os.path.exists(target):
        os.mkdir(target)
    for root, dirs, files in os.walk(source):
        ignoreCurrentDirs = list(ignoreDirsSet.intersection(set(dirs)))
        for t in ignoreCurrentDirs:
            dirs.remove(t)

        for file in files:
            if os.path.splitext(file)[(-1)] in ignoreFiles:
                continue
            from_ = os.path.join(root, file)
            to_ = from_.replace(source, target, 1)
            to_directory = os.path.split(to_)[0]
            if not os.path.exists(to_directory):
                os.makedirs(to_directory)
            shutil.copyfile(from_, to_)


def saveTextToFile(txt, skipAsk=False, skipOverwrite=False):
    save = skipAsk and ask('Save to File?')
    if save:
        filePath = raw_input('Enter the Path>')
        if os.path.exists(filePath):
            again = True
            while again:
                again = False
                p = skipOverwrite and ask('File already Exists, (o)verwrite, (a)ppend, (p)repend or (c)ancel?>', {'o': 'o', 'a': 'a', 'c': 'c', 'p': 'p'})
                if p == 'o' or p == False:
                    f = open(filePath, 'w')
                    f.write(txt)
                    f.close()
                elif p == 'a':
                    f = open(filePath, 'a')
                    f.write(txt)
                    f.close()
                elif p == 'p':
                    f = open(filePath, 'r')
                    txt = txt + '\n' + f.read()
                    f.close()
                    f = open(filePath, 'w')
                    f.write(txt)
                    f.close()
                elif p == 'c':
                    pass
                else:
                    print 'Not Valid Command, Options: o, a, p, c lowercase only!'
                    again = True
                if not again and p != 'c':
                    print 'File saved at "%s"!' % filePath

        else:
            f = open(p, 'w')
            f.write(txt)
            f.close()


def getTextFromPath(filePath):
    templ = ''
    if filePath[(-1)] == ']' and filePath.rindex('[') > 0:
        fn = filePath
        lindex = int(fn[fn.rindex('[') + 1:fn.rindex(':')])
        rindex = int(fn[fn.rindex(':') + 1:-1])
        f = open(filePath[:filePath.rindex('[')], 'r')
        templ = ('').join(f.readlines()[lindex:rindex])
        f.close()
    else:
        templ = open(filePath, 'r').read()
    return templ