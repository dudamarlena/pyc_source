# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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