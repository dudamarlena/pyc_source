# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/template/cheetah_.py
# Compiled at: 2010-03-18 15:13:51
from threading import RLock
from alacarte.core import Engine
try:
    from Cheetah.Template import Template
except ImportError:
    raise ImportError('You must install the cheetah package.')

__all__ = [
 'Cheetah']

class Cheetah(Engine):

    def prepare(self, filename, **options):
        return (
         Template(file=filename), RLock())

    def render(self, template, data, **options):
        template, lock = template
        lock.acquire()
        template.searchList().append(data)
        result = unicode(template)
        template.searchList()[0:(-1)] = []
        lock.release()
        return (
         options.get('content_type', self.mimetype), result)