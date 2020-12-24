# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/ifcfg/ifcfg/meta.py
# Compiled at: 2018-07-11 18:15:31
"""Ifcfg core meta functionality.  Barrowed from http://slumber.in/."""

class Meta(object):
    """
    Model that acts as a container class for a meta attributes for a larger
    class. It stuffs any kwarg it gets in it's init as an attribute of itself.

    """

    def __init__(self, **kw):
        self._merge(kw)

    def _merge(self, dict_obj):
        for key, value in dict_obj.items():
            setattr(self, key, value)


class MetaMixin(object):
    """
    Mixin that provides the Meta class support to add settings to instances
    of slumber objects. Meta settings cannot start with a _.

    """

    def __init__(self, *args, **kw):
        metas = reversed([ x.Meta for x in self.__class__.mro() if hasattr(x, 'Meta')
                         ])
        final_meta = {}
        for meta in metas:
            final_meta.update(dict([ x for x in list(meta.__dict__.items()) if not x[0].startswith('_')
                                   ]))

        for key in list(final_meta.keys()):
            if key in kw:
                final_meta[key] = kw.pop(key)

        self._meta = Meta(**final_meta)
        super(MetaMixin, self).__init__()