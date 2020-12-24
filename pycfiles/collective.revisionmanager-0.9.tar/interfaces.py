# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/collective/resume/interfaces.py
# Compiled at: 2019-12-11 22:17:29
__doc__ = 'Module where all interfaces, events and exceptions live.'
from collective.reflex.interfaces import IBaseTemplateConditions
from collective.reflex.interfaces import IBaseTemplateConfigure
from collective.resume import _
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform import directives
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class ICollectiveResumeLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IBpoTemplateConditions(IBaseTemplateConditions):
    """Bot settings stored in the registry
    Describes registry records
    """
    project_type = schema.Choice(title=_('Project type'), description=_('Condition Project type'), vocabulary='collective.resume.bpo_project', required=False)
    submission_company = schema.Choice(title=_('Submission company'), description=_('Condition submission company'), vocabulary='collective.ant.submission_company', required=False)
    template_name = schema.Choice(title=_('Report template'), description=_('Submission company and Project type template'), vocabulary='collective.resume.bpo_templates', required=False)
    naming_rules = schema.TextLine(title=_('Naming rules'), description=_('Report file name naming rules.'), default='', required=False)
    out_type = schema.Choice(title=_('Output type'), description=_('Template output type'), vocabulary='collective.reflex.output_type', required=False)
    note = schema.TextLine(title=_('Note'), description=_('Option notes'), default='', required=False)


class IChipTemplateConditions(IBaseTemplateConditions):
    """Bot settings stored in the registry
    Describes registry records
    """
    project_type = schema.Choice(title=_('Project type'), description=_('Condition Project type'), vocabulary='collective.resume.chip_project', required=False)
    submission_company = schema.Choice(title=_('Submission company'), description=_('Condition submission company'), vocabulary='collective.ant.submission_company', required=False)
    template_name = schema.Choice(title=_('Report template'), description=_('Submission company and Project type template'), vocabulary='collective.resume.chip_templates', required=False)
    naming_rules = schema.TextLine(title=_('Naming rules'), description=_('Report file name naming rules.'), default='', required=False)
    out_type = schema.Choice(title=_('Output type'), description=_('Template output type'), vocabulary='collective.reflex.output_type', required=False)
    note = schema.TextLine(title=_('Note'), description=_('Option notes'), default='', required=False)


class IBpoTemplateConfigure(IBaseTemplateConfigure):
    """"""
    default_template = schema.Choice(title=_('Default template'), description=_('If there is no condition to match, this is the default template'), vocabulary='collective.resume.bpo_templates', required=False)
    directives.widget(conditions=DataGridFieldFactory)
    conditions = schema.List(title=_('Condition template'), description=_('Project type and submission company combination must be unique.'), value_type=DictRow(title='combinations of conditions', schema=IBpoTemplateConditions), default=[], required=False)


class IChipTemplateConfigure(IBaseTemplateConfigure):
    """"""
    default_template = schema.Choice(title=_('Default template'), description=_('If there is no condition to match, this is the default template'), vocabulary='collective.resume.chip_templates', required=False)
    directives.widget(conditions=DataGridFieldFactory)
    conditions = schema.List(title=_('Condition template'), description=_('Project type and submission company combination must be unique.'), value_type=DictRow(title='combinations of conditions', schema=IChipTemplateConditions), default=[], required=False)