# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/x/sysx.py
# Compiled at: 2018-02-17 07:28:39
# Size of source mod 2**32: 1043 bytes
import os, sys, io, time, re

def reload_sys():
    reload(sys)
    sys.setdefaultencoding('utf8')


def reload_stdout():
    sys.stdout = io.TextIOWrapper((sys.stdout.buffer), encoding='utf8')


strftime = time.strftime('%Y%m%d', time.localtime())

def writelocaltxtfile(dire, local_filename, content):
    fi = os.path.join(dire, local_filename + '.txt')
    with open(fi, 'w', encoding='utf8') as (f):
        f.write(content)


def writelocalbfile(dire, local_filename, content):
    fi = os.path.join(dire, local_filename)
    with open(fi, 'wb') as (f):
        f.write(content)


def joinfoldfilename(fold, filename):
    if not os.path.exists(fold):
        os.makedirs(fold)
    path = os.path.join(fold, filename)
    return path


def textParse(bigString):
    listOfTokens = re.split('\\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]