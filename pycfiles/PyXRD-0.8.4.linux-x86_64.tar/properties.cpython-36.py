# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/probabilities/models/properties.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 614 bytes
from mvc.models.properties import FloatProperty

class ProbabilityProperty(FloatProperty):
    __doc__ = "\n     A descriptor that will invoke the 'update' method on the instance\n     it belongs to.\n    "

    def __init__(self, clamp=False, **kwargs):
        (super(ProbabilityProperty, self).__init__)(**kwargs)

    def __set__(self, instance, value):
        super(ProbabilityProperty, self).__set__(instance, value)
        instance.update()