# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/forms.py
# Compiled at: 2013-03-09 13:14:07
from treedict import TreeDict
from orm.datatypes import CustomType, SubmitType, make_form_element
from uuid import uuid4

class BasicForm(object):
    _environment = None

    def __init__(self, model, data=None):
        self.model = model
        self.structure = model.structure
        self.structure_tree = TreeDict(model.structure)
        self.data = data
        self.data_tree = TreeDict(data) if data else None
        return

    def open_item_group(self, prefix):
        return self._environment.get_template('forms/open_item_group.html').render(title=prefix.title())

    def close_item_group(self):
        return self._environment.get_template('forms/close_item_group.html').render()

    def render(self, action, fields=None, failed_items=[], buttons=[SubmitType()], method='post', disable_validation=False, new=False, **kwargs):
        """
                Generates HTML forms and, eventually, JavaScript validation to go along with
                those forms. Hopefully this will be a real time saver for CRUD.
                """
        elements = []
        data = dict(kwargs)
        if 'id' not in data:
            data['id'] = uuid4()
        if fields:
            last_prefix = None
            for i in fields:
                if '.' in i:
                    split = i.split('.')
                    prefix = split[(-2)]
                    name = split[(-1)].replace('_', ' ').title()
                    if prefix != last_prefix:
                        if last_prefix:
                            elements.append(self.close_item_group())
                        elements.append(self.open_item_group(prefix))
                        last_prefix = prefix
                else:
                    last_prefix = None
                    name = i.replace('_', ' ').title()
                failed = i in failed_items
                item = self.structure_tree[i]
                if isinstance(item, CustomType):
                    if self.data_tree and i in self.data_tree:
                        value = self.data_tree[i]
                    else:
                        value = None
                    elements.append(item.make_form_element(name, i, value, new=new, failed=failed))
                else:
                    elements.append(make_form_element(name, i, new=new, failed=failed))

            if last_prefix:
                elements.append(self.close_item_group())
        else:
            for key, value in self.structure_tree.iteritems():
                title = key.replace('_', ' ').title()
                failed = key in failed_items
                if isinstance(value, CustomType):
                    if self.data_tree and key in self.data_tree:
                        data_item = self.data_tree[key]
                    else:
                        data_item = None
                    elements.append(value.make_form_element(title, key, data_item, failed=failed))
                else:
                    elements.append(make_form_element(title, key, None, failed=failed))

            for i in buttons:
                elements.append(i.make_form_element())

        validation_structure = (disable_validation or self.model.serialize)() if 1 else None
        return self._environment.get_template('forms/wrapper.html').render(action=action, form_elements=('').join(elements), method=method, validation_structure=validation_structure, **data)