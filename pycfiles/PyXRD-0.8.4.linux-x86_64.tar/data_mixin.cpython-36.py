# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refinables/properties/data_mixin.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 896 bytes


class DataMixin(object):
    __doc__ = "\n    Mixing for the ~:class:`mvc.models.properties.LabeledProperty` descriptor\n    that allows this property to be set on the `data_object` object of the\n    instance this property belongs to, instead of a private attribute.\n    \n    When this Mixin is used, the user can pass an additional keyword \n    argument to the descriptor:\n        - data_object_label: the private attribute label for the data object,\n          defaults to '_data_object' \n    "
    data_object_label = '_data_object'

    def _get_private_label(self):
        """ Private attribute label (holds the actual value on the model) """
        return '%s.%s' % (
         self.data_object_label,
         self.label)