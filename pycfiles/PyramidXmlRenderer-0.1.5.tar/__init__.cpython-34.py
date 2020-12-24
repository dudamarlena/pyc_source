# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python34\lib\site-packages\pyramid_ueditor\pyramid_ueditor\__init__.py
# Compiled at: 2015-06-05 03:33:47
# Size of source mod 2**32: 579 bytes
__all__ = []
__author__ = 'lfblogs (email:13701242710@163.com)'
__version__ = '1.0.1'
from .views import ueditor, ueditorupload

def includeme(config):
    config.add_route('ueditor', '/ueditor/')
    config.add_route('ueditorupload', '/ueditorupload/')
    config.add_view(ueditor, route_name='ueditor', renderer='templates/ueditor.pt')
    config.add_view(ueditorupload, route_name='ueditorupload')