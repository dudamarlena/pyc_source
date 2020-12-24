# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thot/template.py
# Compiled at: 2013-03-05 21:43:25
import pkg_resources
__all__ = [
 'TemplateException', 'get_templating_cls']

class TemplateException(Exception):
    pass


templating_map = dict()

def get_templating_cls(shortname):
    if shortname in templating_map:
        return templating_map[shortname]
    for entrypoint in pkg_resources.iter_entry_points('thot.templating_engines'):
        if entrypoint.name == shortname:
            cls = entrypoint.load()
            templating_map[shortname] = cls
            return cls