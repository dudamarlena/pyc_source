# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refinables/wrapper.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 7650 bytes
import logging
logger = logging.getLogger(__name__)
from mvc.models.properties import LabeledProperty, StringProperty, BoolProperty, ReadOnlyMixin
from pyxrd.generic.models.base import ChildModel
from .mixins import _RefinementBase, RefinementValue, RefinementGroup

class RefinableWrapper(ChildModel):
    __doc__ = '\n        Wrapper class for refinables easing the retrieval of certain\n        properties for the different types of refinables.\n        Can be used with an ObjectTreeStore.\n    '

    class Meta(ChildModel.Meta):
        parent_alias = 'mixture'

    obj = LabeledProperty(default=None,
      text='Wrapped object',
      tabular=True)
    prop_descr = LabeledProperty(default=None,
      text='Property descriptor',
      tabular=True)

    @StringProperty(default='',
      text='Property label',
      tabular=True,
      mix_with=(ReadOnlyMixin,))
    def label(self):
        return self.prop_descr.label

    is_grouper = BoolProperty(default=False,
      text='Is grouper',
      tabular=True,
      mix_with=(ReadOnlyMixin,))

    @LabeledProperty(default=None,
      text='Inherit from label',
      mix_with=(ReadOnlyMixin,))
    def inherit_from(self):
        if self.prop_descr:
            return self.prop_descr.inherit_from

    @StringProperty(default='',
      text='Title',
      tabular=True,
      mix_with=(ReadOnlyMixin,))
    def title(self):
        if isinstance(self.obj, RefinementGroup) and self.is_grouper or isinstance(self.obj, RefinementValue):
            return self.obj.refine_title
        else:
            if getattr(self.prop_descr, 'math_text', None) is not None:
                return self.prop_descr.math_text
            return self.prop_descr.text

    @StringProperty(default='',
      text='Text title',
      tabular=True,
      mix_with=(ReadOnlyMixin,))
    def text_title(self):
        if isinstance(self.obj, RefinementGroup) and self.is_grouper or isinstance(self.obj, RefinementValue):
            return self.obj.refine_title
        else:
            return self.prop_descr.text

    @StringProperty(default='',
      text='Descriptor',
      tabular=True,
      mix_with=(ReadOnlyMixin,))
    def text_descriptor(self):
        """ Return a longer title that also describes this property's relations """
        data = self.obj.refine_descriptor_data
        data['property_name'] = self.text_title
        return '%(phase_name)s | %(component_name)s | %(property_name)s' % data

    @LabeledProperty(default=None,
      text='Value',
      tabular=True)
    def value(self):
        if isinstance(self.obj, RefinementValue):
            return self.obj.refine_value
        else:
            if not self.is_grouper:
                return getattr(self.obj, self.label)
            return ''

    @value.setter
    def value(self, value):
        value = max(min(value, self.value_max), self.value_min)
        if self.is_grouper:
            raise AttributeError('Cannot set the value for a grouping RefinableWrapper')
        else:
            if isinstance(self.obj, RefinementValue):
                self.obj.refine_value = value
            else:
                setattr(self.obj, self.label, value)

    @BoolProperty(default=False,
      text='Inherited',
      tabular=True,
      mix_with=(ReadOnlyMixin,))
    def inherited(self):
        return self.inherit_from is not None and hasattr(self.obj, self.inherit_from) and getattr(self.obj, self.inherit_from)

    @BoolProperty(default=False,
      text='Refinable',
      tabular=True,
      mix_with=(ReadOnlyMixin,))
    def refinable(self):
        if isinstance(self.obj, _RefinementBase):
            if isinstance(self.obj, RefinementGroup):
                if self.is_grouper:
                    return False
                else:
                    return not self.inherited and self.obj.children_refinable
            else:
                if isinstance(self.obj, RefinementValue):
                    return not self.inherited and self.obj.is_refinable
        else:
            return not self.inherited

    @LabeledProperty(default=None,
      text='Refinement info',
      tabular=True,
      mix_with=(ReadOnlyMixin,))
    def ref_info(self):
        if isinstance(self.obj, RefinementGroup) and self.is_grouper or isinstance(self.obj, RefinementValue):
            return self.obj.refine_info
        name = self.prop_descr.get_refinement_info_name()
        if name is not None:
            ref_info = getattr(self.obj, name)
            return ref_info
        raise AttributeError("Cannot find refine info model for attribute '%s' on '%s'" % (self.label, self.obj))

    @LabeledProperty(default=None,
      text='Minimum value',
      tabular=True)
    def value_min(self):
        if self.ref_info:
            return self.ref_info.minimum

    @value_min.setter
    def value_min(self, value):
        if self.ref_info:
            self.ref_info.minimum = value

    @LabeledProperty(default=None,
      text='Maximum value',
      tabular=True)
    def value_max(self):
        if self.ref_info:
            return self.ref_info.maximum

    @value_max.setter
    def value_max(self, value):
        if self.ref_info:
            self.ref_info.maximum = value

    @BoolProperty(default=False,
      text='Refine',
      tabular=True)
    def refine(self):
        if self.ref_info:
            return self.ref_info.refine
        else:
            return False

    @refine.setter
    def refine(self, value):
        if self.ref_info:
            self.ref_info.refine = value and self.refinable

    def __init__(self, *args, **kwargs):
        my_kwargs = self.pop_kwargs(kwargs, 'obj', 'prop', 'prop_descr', 'is_grouper')
        (super(RefinableWrapper, self).__init__)(**kwargs)
        kwargs = my_kwargs
        self.obj = self.get_kwarg(kwargs, None, 'obj')
        self.prop_descr = self.get_kwarg(kwargs, None, 'prop_descr', 'prop')
        self._is_grouper = self.get_kwarg(kwargs, False, 'is_grouper')