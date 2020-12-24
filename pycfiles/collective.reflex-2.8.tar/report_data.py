# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/collective/reflex/behaviors/report_data.py
# Compiled at: 2019-09-16 07:07:06
from collective.reflex import _
from plone import schema
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IEditForm, IAddForm
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider

class IReportDataMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IReportData(model.Schema):
    """
    """
    result_json = schema.JSONField(title=_('Result data'), default={}, required=False)
    result_tags = schema.TextLine(title=_('Result tag'), required=False)
    download_count = schema.Int(title=_('Report download count'), min=0, default=0, required=False)
    report_time = schema.Datetime(title=_('Report time'), description=_('Report issue publish time'), required=False)
    model.fieldset('report data', label=_('label_report', default='Report data'), fields=[
     'result_tags', 'download_count', 'report_time'])
    form.omitted('result_tags', 'download_count', 'report_time')
    form.no_omit(IEditForm, 'report_time')
    form.no_omit(IAddForm, 'report_time')


@implementer(IReportData)
@adapter(IReportDataMarker)
class ReportData(object):

    def __init__(self, context):
        self.context = context

    @property
    def result_tags(self):
        if hasattr(self.context, 'result_tags'):
            return self.context.result_tags
        return ''

    @result_tags.setter
    def result_tags(self, value):
        pass

    @property
    def download_count(self):
        if hasattr(self.context, 'download_count'):
            return self.context.download_count
        return 0

    @download_count.setter
    def download_count(self, value):
        self.context.download_count = value

    @property
    def report_time(self):
        if hasattr(self.context, 'report_time'):
            return self.context.report_time
        return 0

    @report_time.setter
    def report_time(self, value):
        self.context.report_time = value