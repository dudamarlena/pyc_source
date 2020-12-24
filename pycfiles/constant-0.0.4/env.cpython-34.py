# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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