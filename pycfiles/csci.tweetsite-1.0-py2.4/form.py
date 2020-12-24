# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/form.py
# Compiled at: 2009-11-19 10:42:43
from Products.Five.formlib import formbase
from zope import interface, schema
from zope.formlib import form
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

def failing_constraint(value):
    return 1 == 2


def successfull_constraint(value):
    return 1 == 1


class IObjectSchema(interface.Interface):
    __module__ = __name__
    test_field = schema.Text(title='Test field', description='field description', required=True, readonly=False, default='default', missing_value='missing value')


class IExampleSchema(interface.Interface):
    """
    Field types:
        Datetime - Field containing a DateTime
        Date - Field containing a date
        Timedelta - Field containing a timedelta
        Password - Field containing a unicode string without newlines that is a
            password
        Object - Field containing an Object value
        URI - A field containing an absolute URI
        ASCII - Field containing a 7-bit ASCII string. No characters > DEL
            (chr(127)) are allowed
        ASCIILine - Field containing a 7-bit ASCII string without newlines
        Bytes - Field containing a byte string (like the python str)
        BytesLine - Field containing a byte string without newlines
        Tuple - Field containing a value that implements the API of a
            conventional Python tuple
        List - Field containing a value that implements the API of a
            conventional Python list
        Set - Field containing a value that implements the API of a
            conventional Python standard library sets
        FrozenSet - Field containing a value that implements the API of a
            conventional Python 2.4+ frozenset
        Dict - Field containing a conventional dict
        SourceText - Field for source text of object
        Id - A field containing a unique identifier
            A unique identifier is either an absolute URI or a dotted name.
            If it's a dotted name, it should have a module/package name as a
            prefix
        DottedName - Dotted name field
        InterfaceField - Fields with a value that is an interface (implementing
            zope.interface.Interface)

    Field types arguments:
        title - A short summary or label
        description - A description of the field (to be displayed as a hint)
        required - Tells whether a field requires its value to exist
        readonly - If true, the field's value cannot be changed
        default - The field default value may be None or a legal field value
        missing_value - If a field has no assigned value, set it to this value
        constraint - function checking a constraint on the field
    """
    __module__ = __name__
    text_field = schema.Text(title='Text field', description='field description', required=True, readonly=False, default='default value', missing_value='missing value')
    textline_field = schema.TextLine(title='Textline field', description='field description', required=True, readonly=False, default='default value', missing_value='missing value', constraint=successfull_constraint)
    int_field = schema.Int(title='Integer field', description='field description', required=True, readonly=False, default=0, missing_value=1, min=0, max=10)
    bool_field = schema.Bool(title='Boolean field', description='field description', required=True, readonly=False, default=True, missing_value=True)
    float_field = schema.Float(title='Float field', description='field description', required=True, readonly=False, default=0.0, missing_value=0.0)
    choice_field = schema.Choice(title='Choice field', description='field description', required=True, readonly=False, default='Title 2', missing_value='Option 2', vocabulary=SimpleVocabulary((SimpleTerm(value=1, token='Option 1', title='Title 1'), SimpleTerm(value=2, token='Option 2', title='Title 2'))), source=VocabularyExample, values=['Option 1', 'Option 2'])
    object_field = schema.Object(title='Object field', description='field description', required=True, readonly=False, default=None, missing_value=None, schema=IObjectSchema)


class ExampleForm(formbase.PageForm):
    __module__ = __name__
    form_fields = form.FormFields(IExampleSchema)
    label = 'Form label'
    description = 'Form short description'

    @form.action('Submit button', failure='handle_failure')
    def handle_success(self, action, data):
        """
        Called when the action was submitted and there are NO validation
        errors.

        This form is generated with ZopeSkel. Please make sure you fill in
        the implementation of the form processing.

        """
        self.status = 'The handle_success method of the %s form is not             implemented.' % self.__class__.__name__

    def handle_failure(self, action, data, errors):
        """
        Called when the action was submitted and there are validation errors.

        """
        self.status = 'Errors occured while submitting the form'