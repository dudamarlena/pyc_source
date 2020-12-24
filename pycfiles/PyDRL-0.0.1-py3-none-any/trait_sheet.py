# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\trait_sheet.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
from types import StringType, ListType, TupleType
from trait_base import SequenceTypes
from trait_handlers import TraitPrefixList
from traits import Trait, HasTraits, ReadOnly
from string import lowercase, uppercase
none_or_string = Trait(None, None, StringType)
true_trait = Trait('true', {'true': 1, 
   't': 1, 'yes': 1, 'y': 1, 'on': 1, 1: 1, 'false': 0, 
   'f': 0, 'no': 0, 'n': 0, 'off': 0, 0: 0})
style_trait = Trait(None, None, TraitPrefixList('simple', 'custom', 'text', 'readonly'))
object_trait = Trait(None, None, HasTraits)
basic_sequence_types = [
 ListType, TupleType]

class TraitSheetHandler:

    def position(self, trait_sheet, object):
        return 0

    def close(self, trait_sheet, object):
        return 1

    def changed(self, object, trait_name, new_value, old_value, is_set):
        pass

    def init(self, trait_sheet, object):
        return


default_trait_sheet_handler = TraitSheetHandler()

class TraitEditor:

    def text_editor(self, object, trait_name, description, handler, parent):
        raise NotImplementedError

    def simple_editor(self, object, trait_name, description, handler, parent):
        raise NotImplementedError

    def custom_editor(self, object, trait_name, description, handler, parent):
        return self.simple_editor(object, trait_name, description, handler, parent)

    def set(self, object, trait_name, value, handler):
        original_value = getattr(object, trait_name)
        setattr(object, trait_name, value)
        handler.changed(object, trait_name, value, original_value, True)

    def str(self, object, trait_name):
        return self.str_value(getattr(object, trait_name))

    def str_value(self, value):
        return str(value)


class TraitMonitor:

    def __init__(self, object, trait_name, control, on_trait_change_handler):
        self.control = control
        self.on_trait_change_handler = on_trait_change_handler
        object.on_trait_change(self.on_trait_change, trait_name)

    def on_trait_change(self, object, trait_name, new):
        try:
            self.on_trait_change_handler(self.control, new)
        except:
            object.on_trait_change(self.on_trait_change, trait_name, remove=True)


class TraitGroupItem(HasTraits):
    __traits__ = {'name': none_or_string, 
       'label': none_or_string, 
       'style': style_trait, 
       'editor': Trait(None, None, TraitEditor), 
       'object': object_trait}

    def __init__(self, *value, **traits):
        HasTraits.__init__(self, **traits)
        if len(value) == 1 and type(value[0]) in SequenceTypes:
            value = value[0]
        for data in value:
            if type(data) is StringType:
                if self.name is None:
                    self.name = data
                elif self.label is None:
                    self.label = data
                else:
                    self.style = data
            elif isinstance(data, TraitEditor):
                self.editor = data
            else:
                self.object = data

        return

    def clone(self):
        clone = self.__class__()
        clone.clone_traits(self)
        return clone

    def label_for(self, object):
        return self.label or (self.object or object)._base_trait(self.name).label or self.user_name_for(self.name)

    def user_name_for(self, name):
        name = name.replace('_', ' ').capitalize()
        result = ''
        last_lower = 0
        for c in name:
            if c in uppercase and last_lower:
                result += ' '
            last_lower = c in lowercase
            result += c

        return result

    def editor_for(self, object):
        return self.editor or (self.object or object)._base_trait(self.name).editor


class TraitGroup(HasTraits):
    __traits__ = {'values': ReadOnly, 
       'label': none_or_string, 
       'style': style_trait, 
       'orientation': Trait('vertical', TraitPrefixList('vertical', 'horizontal')), 
       'show_border': true_trait, 
       'show_labels': true_trait, 
       'object': object_trait}

    def __init__(self, *values, **traits):
        HasTraits.__init__(self, **traits)
        _values = []
        for value in values:
            if isinstance(value, TraitGroup) or isinstance(value, TraitGroupItem):
                _values.append(value)
            else:
                _values.append(TraitGroupItem(value))

        self.values = _values

    def clone(self):
        clone = self.__class__()
        clone.clone_traits(self, [
         'label', 'style', 'orientation', 'show_border', 'show_labels'])
        clone_values_append = clone.values.append
        for value in self.values:
            clone_values_append(value.clone())

        return clone

    def __add__(self, other):
        return merge_trait_groups(self, other)


class TraitGroupList(list):

    def __add__(self, other):
        return merge_trait_groups(self, other)


class MergeTraitGroups:

    def __call__(self, group1, group2):
        return getattr(self, '%s_%s' % (
         self._kind(group1), self._kind(group2)))(group1, group2)

    def _kind(self, group):
        if isinstance(group, TraitGroup):
            return 'tg'
        if isinstance(group, TraitGroupList) or type(group) in basic_sequence_types:
            if len(group) == 0 or type(group[0]) is StringType:
                return 'strl'
            return 'tgl'
        return 'str'

    def _merge(self, dest_group, src_group):
        values = dest_group.values
        n = len(values)
        for value in src_group.values:
            if isinstance(value, TraitGroupItem) or value.label is None:
                values.append(value)
            else:
                label = value.label
                for i in range(n):
                    merge_item = values[i]
                    if isinstance(merge_item, TraitGroup) and label == merge_item.label:
                        self._merge(merge_item, value)
                        break
                else:
                    values.append(value)

        return

    def str_str(self, group1, group2):
        return TraitGroupList([group1, group2])

    def str_strl(self, group1, group2):
        return TraitGroupList([group1] + group2)

    def str_tg(self, group1, group2):
        return TraitGroupList([TraitGroup(group1, label='Main'),
         group2])

    def str_tgl(self, group1, group2):
        return TraitGroupList([TraitGroup(group1, label='Main')] + group2)

    def strl_str(self, group1, group2):
        return TraitGroupList(group1 + [group2])

    def strl_strl(self, group1, group2):
        return TraitGroupList(group1 + group2)

    def strl_tg(self, group1, group2):
        return TraitGroupList([TraitGroup(label='Main', *group1),
         group2])

    def strl_tgl(self, group1, group2):
        return TraitGroupList([TraitGroup(label='Main', *group1)] + group2)

    def tg_str(self, group1, group2):
        return TraitGroupList([group1,
         TraitGroup(group2, label='Other')])

    def tg_strl(self, group1, group2):
        return TraitGroupList([group1,
         TraitGroup(label='Other', *group2)])

    def tg_tg(self, group1, group2):
        return self.tgl_tgl([group1], [group2])

    def tg_tgl(self, group1, group2):
        return self.tgl_tgl([group1], group2)

    def tgl_str(self, group1, group2):
        return TraitGroupList([group1,
         TraitGroup(group2, name='Other')])

    def tgl_strl(self, group1, group2):
        return TraitGroupList([group1,
         TraitGroup(name='Other', *group2)])

    def tgl_tg(self, group1, group2):
        return self.tgl_tgl(group1, [group2])

    def tgl_tgl(self, group1, group2):
        result = TraitGroupList()
        page = 0
        for group in group1:
            group = group.clone()
            if group.label is None:
                page += 1
                group.label = 'Page %d' % page
            result.append(group)

        for group in group2:
            label = group.label
            if label is None:
                page += 1
                group.label = 'Page %d' % page
                result.append(group)
            else:
                for merge_group in result:
                    if label == merge_group.label:
                        self._merge(merge_group, group)
                        break
                else:
                    result.append(group)

        return result


merge_trait_groups = MergeTraitGroups()