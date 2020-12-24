# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fez/atcsv/browser/forms.py
# Compiled at: 2009-01-27 15:33:05
from cStringIO import StringIO
from zope import component
from zope import interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from z3c.form import field
from z3c.form import form
from z3c.form import button
from z3c.form import validator
from plone.app.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from fez.atcsv.interfaces import ICSVImport

class ICSVImportForm(interface.Interface):
    __module__ = __name__
    portal_type = schema.Choice(title='Portal type', vocabulary='fez.atcsv.AddableContentTypesFactory', description='The content type that will be created by the import. Note that the AT field names must match the names of the fields in the first line of the CSV.')
    delimiter = schema.TextLine(title='Delimiter', default=',', description='The field delimiter, or \\t for the tab character.')
    csv_file = schema.Bytes(title='CSV File', description='The CSV file to upload.')


class InvalidDelimiterError(schema.ValidationError):
    __module__ = __name__
    __doc__ = 'Invalid delimiter, must be single character or \\t'


class DelimiterValidator(validator.SimpleFieldValidator):
    r"""
    Validate that the field has either only one character, or that the
    character is a tab.
    
    >>> d = DelimiterValidator(None, None, None, ICSVImportForm['delimiter'], None)
    >>> d.validate(u',')
    >>> d.validate(u'aa')
    Traceback (most recent call last):
    ...
    InvalidDelimiterError
    >>> d.validate(u'\\t')
    """
    __module__ = __name__

    def validate(self, value):
        super(DelimiterValidator, self).validate(value)
        if value not in '\\t' and len(value) != 1:
            raise InvalidDelimiterError()


validator.WidgetValidatorDiscriminators(DelimiterValidator, field=ICSVImportForm['delimiter'])

class CSVImportForm(form.Form):
    __module__ = __name__
    fields = field.Fields(ICSVImportForm)
    ignoreContext = True
    ignoreRequest = True
    label = 'Import a CSV file'

    @button.buttonAndHandler('Save')
    def handleSave(self, action):
        (data, errors) = self.extractData()
        if errors:
            return
        if data['delimiter'] == '\\t':
            delimiter = '\t'
        else:
            delimiter = data['delimiter']
        fp = StringIO(data['csv_file'])
        importer = ICSVImport(self.context)
        (count, success, failed) = importer.do_import(data['portal_type'].getId(), delimiter=delimiter, fp=fp)
        status = IStatusMessage(self.request)
        status.addStatusMessage('%s records processed, %s successful' % (count, success), type='info')
        errors = []
        for (record, exception) in failed:
            message = [
             'Record failed: %s' % record]
            message.append('Error was: %s' % str(exception))
            errors.append(('\n').join(message))

        if errors:
            status.addStatusMessage(('\n').join(errors), type='error')
        self.request.RESPONSE.redirect(self.context.absolute_url())


CSVImport = wrap_form(CSVImportForm)