# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\constant-project\constant\tpl\env.py
# Compiled at: 2017-04-06 16:11:01
# Size of source mod 2**32: 643 bytes
import os
from jinja2 import Environment, PackageLoader
dirpath = os.path.dirname(__file__)
parts = list()
for _ in range(20):
    if os.path.exists(os.path.join(dirpath, '__init__.py')):
        dirpath, basename = os.path.split(dirpath)
        parts.append(basename)
    else:
        break

package_name = '.'.join(parts[::-1])
env = Environment(loader=PackageLoader(package_name, package_path='templates'))
t_class_def = env.get_template('class_def.txt')
t_collection_class_def = env.get_template('collection_class_def.txt')
t_code = env.get_template('code.txt')