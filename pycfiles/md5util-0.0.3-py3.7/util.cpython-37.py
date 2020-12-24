# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/md5util/util.py
# Compiled at: 2020-03-16 04:50:18
# Size of source mod 2**32: 890 bytes
import hashlib

class Md5Util(object):

    @classmethod
    def get_data_md5(cls, data: dict, md5_fields: list):
        """
        按照md5_fields 指定key 的顺序，
        返回data 中value 拼接形式的字符串md5 值

        :param data: dict
        :param md5_fields: list
        :return: str 返回32位md5值
        """
        md5 = hashlib.md5()
        for field in md5_fields:
            value = data[field]
            if not isinstance(value, str):
                value = str(value)
            md5.update(value.encode())

        return md5.hexdigest()

    @classmethod
    def get_md5(cls, value):
        """
        快速的返回字符串32位md5值
        """
        return hashlib.md5(value.encode()).hexdigest()


if __name__ == '__main__':
    print(Md5Util.get_data_md5({'name': 96377047}, ['name']))