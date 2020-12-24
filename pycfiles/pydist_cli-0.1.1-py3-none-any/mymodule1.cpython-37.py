# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/package/mymodule1.py
# Compiled at: 2020-03-21 13:51:45
# Size of source mod 2**32: 264 bytes
import pkgutil

def main():
    data = pkgutil.get_data(__name__, 'templates/temp_file')
    print('data:', repr(data))
    text = pkgutil.get_data(__name__, 'templates/temp_file').decode()
    print('text:', repr(text))