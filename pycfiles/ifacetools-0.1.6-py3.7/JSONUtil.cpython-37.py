# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\jsonutil\JSONUtil.py
# Compiled at: 2019-08-04 22:14:48
# Size of source mod 2**32: 2166 bytes
import json

class JSONUtil:

    def josnStingToDict(self, str='{}'):
        return json.loads(str)

    def pythonObjectToJosnSting(self, p):
        try:
            j = json.dumps((dict(p)), ensure_ascii=False)
        except TypeError:
            raise TypeError('该对象没有实现 keys和 __getitem__')
        else:
            print(j)
        return j

    def dictToJosnSting(self, dict={'a': 1}):
        try:
            j = json.dumps(p, ensure_ascii=False)
        except TypeError:
            raise TypeError('仅支持字典转换成json串')
        else:
            print(j)
        return j

    def dictToJosnStingWithSort(self, dict={'a': 1}):
        try:
            j = json.dumps(p, sort_keys=True, ensure_ascii=False)
        except TypeError:
            raise TypeError('仅支持字典转换成json串')
        else:
            print(j)
        return j