# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdktool/demo.py
# Compiled at: 2020-03-25 05:48:31
from util.utils import *
from upload import *
from checkout import *

def demoUp():
    with open('basic.json', 'r') as (f):
        fp_list = json.load(f).get('fp_list')
    a = Upload(erp='zhangyuhao25', fp_list=fp_list)
    a.get_objects()
    a.put_file()


def demoDown():
    a = Checkout(version='master', erp='zhangyuhao25', id='1', mnt_path='/mnt/cfs/')
    result = a.checkout()
    for k, v in result.items():
        print k, v


def demoDel():
    pass


if __name__ == '__main__':
    BasicConfig.usage()