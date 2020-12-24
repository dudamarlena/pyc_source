# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refinables/models.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1731 bytes
from mvc.models.properties import FloatProperty, BoolProperty
from pyxrd.generic.models.base import PyXRDModel
from pyxrd.generic.io import storables, Storable
from pyxrd.generic.utils import not_none

@storables.register()
class RefinementInfo(PyXRDModel, Storable):
    __doc__ = '\n        A model that is used to store the refinement information for each\n        refinable value (in other models): minimum and maximum value and\n        a flag to indicate whether this value is selected for refinement.\n    '

    class Meta(PyXRDModel.Meta, Storable.Meta):
        store_id = 'RefinementInfo'

    minimum = FloatProperty(default=0.0, text='Minimum', persistent=True)
    maximum = FloatProperty(default=1.0, text='Maximum', persistent=True)
    refine = BoolProperty(default=False, text='Refine', persistent=True)

    def __init__(self, minimum, maximum, refine, *args, **kwargs):
        super(RefinementInfo, self).__init__()
        self.refine = refine
        self.minimum = not_none(minimum, 0.0)
        self.maximum = not_none(maximum, 1.0)

    def to_json(self):
        return self.json_properties()

    def json_properties(self):
        return [
         self.minimum, self.maximum, self.refine]