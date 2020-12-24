# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/MyFirstPythonPackage/MyThirdPythonFile.py
# Compiled at: 2019-08-16 05:18:05
# Size of source mod 2**32: 175 bytes
from MyFirstPythonPackage.FirstPythonFile import MyClass
if __name__ == '__main__':
    my_obj = MyClass('DJ', 2)
    print(my_obj.returnId())
    print(my_obj.returnName())