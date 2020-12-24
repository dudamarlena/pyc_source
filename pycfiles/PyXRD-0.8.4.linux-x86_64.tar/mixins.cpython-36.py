# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refinables/mixins.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2901 bytes


class _RefinementBase(object):
    __doc__ = "\n    Base class for `RefinementGroup` and `RefinementValue` mixins. It's \n    used to provide common functionality and a way to check for the kind of\n    refinement class we're dealing with when building the refinement tree.\n            \n    .. attribute:: refine_title\n\n        A string used as the title for the group in the refinement tree\n\n    .. attribute:: refine_descriptor\n\n        A longer title string which gives more information (phase, component, etc) \n        \n    .. attribute:: is_refinable\n\n        Whether or not this instance is refinable\n        \n    .. attribute:: refinables\n        \n        An iterable with the names of the refinable properties \n        \n    .. attribute:: refine_value\n    \n        Mapper for the actual refinable value (if available). This should be\n        overriden by deriving classes.\n        \n    "

    @property
    def refine_title(self):
        return 'Refinement Base'

    @property
    def refine_descriptor_data(self):
        return dict()

    @property
    def is_refinable(self):
        return True

    @property
    def refinables(self):
        return []

    @property
    def refine_info(self):
        pass

    @property
    def refine_value(self):
        pass

    @refine_value.setter
    def refine_value(self, value):
        pass


class RefinementGroup(_RefinementBase):
    __doc__ = '\n    Mixin for objects that are not refinable themselves,\n    but have refinable properties. They are presented in the refinement\n    tree using their title value.\n    Subclasses should override refine_title to make it more descriptive.\n    \n    .. attribute:: children_refinable\n\n        Whether or not the child properties of this group can be refinable.\n        This should normally always be True, unless for example if the entire\n        group of properties have a single inherit property.\n    \n    '

    @property
    def refine_title(self):
        return 'Refinement Group'

    @property
    def is_refinable(self):
        return False

    @property
    def children_refinable(self):
        return True

    @property
    def refinables(self):
        return self.Meta.get_refinable_properties()


class RefinementValue(_RefinementBase):
    __doc__ = '\n        Mixin for objects that hold a single refinable property. They are\n        collapsed into one line in the refinement tree. \n        Subclasses should override both the refine_title property to make it\n        more descriptive, and the refine_value property to return and set the\n        correct (refinable) attribute.\n    '

    @property
    def refine_title(self):
        return 'Refinement Value'