# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/template/cheetah.py
# Compiled at: 2012-05-23 13:18:32
from __future__ import unicode_literals, absolute_import
from threading import RLock
from marrow.templating.core import Engine
try:
    from Cheetah.Template import Template
except ImportError:
    raise ImportError(b'You must install the cheetah package.')

__all__ = [
 b'Cheetah']

class Cheetah(Engine):

    def prepare(self, filename, **options):
        return (
         Template(file=filename), RLock())

    def render(self, template, data, **options):
        (template, lock) = template
        lock.acquire()
        template.searchList().append(data)
        result = unicode(template)
        template.searchList()[0:(-1)] = []
        lock.release()
        return (
         options.get(b'content_type', b'text/html'), result)