# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refinables/properties/refinable_mixin.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 948 bytes


class RefinableMixin(object):
    __doc__ = '\n    Mixing for the ~:class:`mvc.models.properties.LabeledProperty` descriptor\n    that allows the property to be refinable.\n    When this Mixin is used, the user should pass 4 additional keyword \n    arguments to the descriptor:\n        - refinable: boolean set to True if the property is refinable\n        - refinable_info_format: the format for the refinement info attribute\n        - minimum: the minimum allowed value (or None as default)\n        - maximum: the maximum allowed value (or None as default) \n    '
    refinable = True
    refinable_info_format = '%(label)s_ref_info'
    minimum = None
    maximum = None

    def get_refinement_info_name(self):
        return self.refinable_info_format % {'label': self.label}