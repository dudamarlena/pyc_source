# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/MyFirstPythonPackage/FirstPythonFile.py
# Compiled at: 2019-08-16 02:48:31
# Size of source mod 2**32: 327 bytes


class MyClass:

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def returnId(self):
        return self.id

    def returnName(self):
        return self.name


if __name__ == '__main__':
    my_obj = MyClass('Divya Jyoti Das', 1)
    print(my_obj.returnId())
    print(my_obj.returnName())