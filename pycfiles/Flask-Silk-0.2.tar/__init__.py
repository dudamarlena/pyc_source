# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sublee/labs/flask-silk/flask_silk/icons/__init__.py
# Compiled at: 2013-03-24 07:51:25
"""
.. list-table::
   :widths: 1 99

"""
import os, re
for filename in sorted(os.listdir(os.path.dirname(__file__))):
    if not filename.endswith('.png'):
        continue
    __doc__ += ('   * - .. image:: _static/{0}\n     - {0}\n').format(filename)