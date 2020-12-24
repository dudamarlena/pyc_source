# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lymon/core/metatag.py
# Compiled at: 2008-06-29 11:50:22
__all__ = [
 'MetaTag']
__default__ = dict(slot='', tag='div', attrs={}, name='__default__', html='', id=True, widgets=False)

class MetaTag(type):
    """
        Metaclass extending type.
        """

    def __new__(meta, name, bases, dct):
        for (key, value) in dct.items():
            if '_' in key:
                dct.pop(key)

        items = dct.copy()

        def __init__(cls, **kw):
            if 'name' not in kw.keys():
                kw.update({'name': name})
            default = __default__.copy()
            default.update(items)
            default.update(kw)
            if '#' not in default['slot']:
                default['slot'] += '#%s' % name
            if default['id']:
                if 'id' not in default['attrs'].keys():
                    slot = default['slot'][:default['slot'].index('#')]
                    if slot:
                        id = slot.split('.')[(-1)]
                        t = default['attrs'].copy()
                        t.update({'id': id})
                        default['attrs'] = t.copy()
            cls.update(default)

        dct.update({'__init__': __init__})
        return type.__new__(meta, name, bases, dct)