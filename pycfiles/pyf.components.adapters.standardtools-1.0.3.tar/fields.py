# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/componentized/configuration/fields.py
# Compiled at: 2010-10-18 09:04:54


class Field(object):
    type = 'input'
    default_classname = ''

    def __init__(self, name, default=None, classname='', label=None, help_text=None, description=None):
        self.name = name
        self.default = default
        self.value = ''
        self.classname = classname or self.default_classname
        self.label = label
        self.help_text = help_text
        self.description = description

    def get_display_info(self):
        return {'type': self.type, 
           'inputParams': dict(label=self.label, name=self.name, wirable=False, className=self.classname, value=self.default, description=self.description, **self.get_additional_info())}

    def get_additional_info(self):
        return dict(typeInvite=self.help_text)


class InputField(Field):
    pass


class URLField(InputField):
    type = 'url'


class EMailField(InputField):
    type = 'email'


class BooleanField(InputField):
    type = 'boolean'


class TextAreaField(Field):
    type = 'text'


class SingleSelectField(Field):
    type = 'select'

    def __init__(self, name, values=None, **kwargs):
        super(SingleSelectField, self).__init__(name, **kwargs)
        if values is None:
            raise ValueError, 'You should define possible values for a select list'
        self.values = values
        return

    def get_additional_info(self):
        return dict(selectValues=self.values)


class MultipleFields(Field):
    type = 'group'

    def __init__(self, name, fields=None, collapsible=False, collapsed=False, **kwargs):
        super(MultipleFields, self).__init__(name, **kwargs)
        if fields is None:
            raise ValueError, 'You should define content sub widgets for a multiple field'
        self.fields = fields
        self.collapsible = collapsible
        self.collapsed = collapsed
        return

    def get_display_info(self):
        return {'type': self.type, 
           'label': self.label, 
           'inputParams': dict(name=self.name, legend=self.label, wirable=False, value=self.default, collapsible=self.collapsible, collapsed=self.collapsed, fields=[ field.get_display_info() for field in self.fields ])}


class InlineMultipleFields(MultipleFields):
    default_classname = 'inline'


class ListField(Field):
    type = 'list'

    def __init__(self, name, content=None, collapsible=False, **kwargs):
        super(ListField, self).__init__(name, **kwargs)
        if content is None:
            raise ValueError, 'You should define content sub widgets for a multiple field'
        self.content = content
        self.collapsible = collapsible
        return

    def get_display_info(self):
        return {'type': self.type, 
           'collapsible': self.collapsible, 
           'label': self.label, 
           'inputParams': dict(label=self.label, name=self.name, wirable=False, value=self.default, collapsible=self.collapsible, elementType=self.content.get_display_info())}