# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/xmlschema_acue/components/xmlschema_acue/tests/xmlschema_acue_tests/testtools/schema_observers.py
# Compiled at: 2019-05-15 06:01:07
"""
Observers for XMLSchema classes.
"""
from functools import wraps
from xmlschema_acue.validators import XMLSchema10, XMLSchema11

class SchemaObserver(object):
    """
    Observer that registers created components. Run the 'clear' method after each usage.
    """
    components = []

    @classmethod
    def observed_builder(cls, builder):
        if isinstance(builder, type):

            class BuilderProxy(builder):

                def __init__(self, *args, **kwargs):
                    super(BuilderProxy, self).__init__(*args, **kwargs)
                    cls.components.append(self)

            BuilderProxy.__name__ = builder.__name__
            return BuilderProxy
        if callable(builder):

            @wraps(builder)
            def builder_proxy(*args, **kwargs):
                result = builder(*args, **kwargs)
                cls.components.append(result)
                return result

            return builder_proxy

    @classmethod
    def clear(cls):
        del cls.components[:]


class ObservedXMLSchema10(XMLSchema10):
    BUILDERS = {k:SchemaObserver.observed_builder(getattr(XMLSchema10.BUILDERS, k)) for k in getattr(XMLSchema10.BUILDERS, '_fields')}


class ObservedXMLSchema11(XMLSchema11):
    BUILDERS = {k:SchemaObserver.observed_builder(getattr(XMLSchema11.BUILDERS, k)) for k in getattr(XMLSchema11.BUILDERS, '_fields')}