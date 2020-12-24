# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/core/modifiers.py
# Compiled at: 2010-09-27 04:07:05
from pyf.componentized import ET

def apply_modifier(modifier, target_tree):

    def get_target(name):
        for parent in target_tree.getiterator():
            for child in parent:
                if child.tag == 'node' and child.get('name') == name:
                    return (parent, child)

    target_name = modifier.get('target')
    if get_target(target_name) is None:
        raise ValueError('Cannot find target %s' % target_name)
    (parent, target) = get_target(target_name)
    action = modifier.get('action', 'modify')
    if action == 'modify':
        for element in modifier:
            if element.tag != 'children':
                other_elem = target.find(element.tag)
                if other_elem is not None:
                    other_elem_index = target.getchildren().index(other_elem)
                    target[other_elem_index] = element
                else:
                    target.insert(len(target), element)
            else:
                other_elem = target.find(element.tag)
                for child in element:
                    other_elem.insert(len(other_elem), child)

    elif action == 'remove':
        parent.remove(target)
    else:
        if action == 'enclose':
            new_node = modifier.find('node')
            if new_node is None:
                raise ValueError('You should always provide at least a "node" element in a "%s" modifier.' % action)
            old_index = parent.getchildren().index(target)
            new_children = new_node.find('children')
            if new_children is None:
                new_children = ET.SubElement(new_node, 'children')
            new_children.insert(len(new_children), target)
            parent.insert(old_index, new_node)
        elif action == 'add_children':
            new_node = modifier.findall('node')
            if not new_node or new_node is None:
                raise ValueError('You should always provide at least one "node" element in a "%s" modifier.' % action)
            other_elem = target.find('children')
            if other_elem is None:
                other_elem = ET.SubElement(target, 'children')
            for child in modifier:
                other_elem.insert(len(other_elem), child)

        else:
            raise NotImplementedError, 'Modifier type "%s" is not implemented (yet ?)' % action
        return


def apply_modifier_set(modifiers_tree, target_tree):
    config_node = modifiers_tree.find('config')
    ftarget_tree = target_tree.find('process')
    if config_node is not None:
        target_config = ftarget_tree.find('config')
        if target_config is None:
            ftarget_tree.insert(0, config_node)
        else:
            for element in config_node:
                other_elem = target_config.find(element.tag)
                if other_elem is not None:
                    other_elem_index = target_config.getchildren().index(other_elem)
                    target_config[other_elem_index] = element
                else:
                    target_config.insert(len(target_config), element)

    modifiers = modifiers_tree.findall('modifier')
    for modifier in modifiers:
        apply_modifier(modifier, target_tree)

    return