# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pirogov/.virtualenvs/paid/local/lib/python2.7/site-packages/kladr/__init__.py
# Compiled at: 2014-05-23 05:50:14
"""
Приложение для работы с КЛАДР
"""
from fill_kladr import fill_kladr

def import_kladr(region_only=None, dbf_path=''):
    u"""
    Импортирует кладр из папки dbf_path. Если не задавать dbf_path,
    то система возьмет путь m3/externals.
    
    В случае если необходимо загрузить данные только по одному региону,
    то необходимо в region передать строку с двумя символами региона.
    Например, region_only = '16'
    """
    fill_kladr(region_only, dbf_path)