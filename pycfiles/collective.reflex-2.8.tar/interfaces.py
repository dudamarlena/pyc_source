# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jian/Plone46/zinstance/src/collective.reflex/src/collective/reflex/interfaces.py
# Compiled at: 2019-12-12 03:42:00
"""Module where all interfaces, events and exceptions live."""
import inspect, os, re
from Products.CMFPlone.utils import safe_unicode
from collective.reflex import _
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform import directives
from plone.resource.manifest import ManifestFormat
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component.interfaces import IObjectEvent
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface.common.mapping import IIterableMapping
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import ValidationError
from zope.schema._bootstrapinterfaces import WrongType

class ICollectiveReflexLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    pass


REPORT_RESOURCE_NAME = 'reportpkg'
REPORT_TPLFILE_NAME = 'index.odt'
REPORT_OUTTYPE_NAME = 'pdf'
REPORT_PREVIEW_NAME = 'preview.png'
REPORT_EXAMPLE_NAME = 'example.pdf'
REPORT_MANIFEST_FORMAT = ManifestFormat(REPORT_RESOURCE_NAME, keys=[
 'title', 'description', 'fortype',
 'tplfile', 'outtype', 'preview',
 'example', 'created', 'version'], defaults={'tplfile': REPORT_TPLFILE_NAME, 
   'outtype': REPORT_OUTTYPE_NAME, 
   'preview': REPORT_PREVIEW_NAME, 
   'example': REPORT_EXAMPLE_NAME})
TEMP_STORAGE = 'Temp'
email_expr = re.compile("^(\\w&.%#$&'\\*+-/=?^_`{}|~]+!)*[\\w&.%#$&'\\*+-/=?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?\\.)+[a-z]{2,6}|([0-9]{1,3}\\.){3}[0-9]{1,3})$", re.IGNORECASE)

def check_for_email(value):
    if value:
        values = value.split(',')
        for email in values:
            if not email_expr.match(email):
                raise WrongType()

    return True


def check_for_uno(value):
    """
    """
    try:
        inspect.isabstract(ICollectiveReflexSettings)
    except Exception:
        return True

    if 'python' not in value and os.system(value + ' -V') != 0:
        raise InvalidPythonPath()
    if os.system(value + ' -c "import unohelper"') != 0:
        raise InvalidUnoPath()
    return True


class InvalidPythonPath(ValidationError):
    __doc__ = _('Invalid Python path')


class InvalidUnoPath(ValidationError):
    __doc__ = _("Can't import uno with the python path")


class IReportPkg(Interface):
    """A report package, loaded from a resource directory
    """
    __name__ = schema.TextLine(title=_('Name'))
    title = schema.TextLine(title=_('Title'), required=False)
    description = schema.TextLine(title=_('Description'), required=False)
    fortype = schema.ASCIILine(title=_('For type'), required=False, default='*')
    tplfile = schema.TextLine(title=_('Template file'), required=False)
    outtype = schema.ASCIILine(title=_('Out type'), required=False, default='pdf')
    example = schema.TextLine(title=_('Example image'), required=False)
    preview = schema.TextLine(title=_('Preview pdf'), required=False)
    created = schema.TextLine(title=_('Created'))
    version = schema.TextLine(title=_('Version'))
    zipfile = schema.Bytes(title=_('File data'))


class ICollectiveReflexSettings(Interface):
    """Settings stored in the registry
    Describes registry records
    """
    uno_path = schema.TextLine(title=_('Python path'), description=_('Path of python with OO'), required=False, default=safe_unicode(os.getenv('PYTHON_UNO', '/usr/bin/python3')), constraint=check_for_uno)
    oo_server = schema.TextLine(title=_('oo address'), description=_('Server address of OO'), required=False, default=safe_unicode(os.getenv('OO_SERVER', 'localhost')))
    oo_port = schema.Int(title=_('oo port'), description=_('Port Number of OO'), required=False, default=int(os.getenv('OO_PORT', 2002)))
    storage_type = schema.Choice(title=_('Storage type'), description=_('Temp storage stored in temp directory not stored in database. File storage store on the filesystem with link in the database. Blob storage store in the database with a blob.'), vocabulary='collective.reflex.storage_type', default='File')
    storage_location = schema.TextLine(title=_('Storage location'), description=_('Only for file storage with disk. Client must have write access to directory.'), default='/srv/report_files')
    naming_rules = schema.TextLine(title=_('Naming rules'), description=_('Report file name naming rules.'), default='', required=False)
    versioning_support = schema.Bool(title=_('Versioning support'), description=_('Creating a new version preserves the old version instead of overwriting.'), default=False)
    auto_create = schema.Bool(title=_('Auto create'), description=_('Automatically create files on review complete.'), default=False)
    directives.widget('enabled_types', CheckBoxFieldWidget, multiple='multiple', size=15)
    enabled_types = schema.List(title=_('Types of enabled'), description=_('Select for which types the report will be enabled'), value_type=schema.Choice(vocabulary='collective.reflex.available_types', required=True), default=[], required=False)


class IReportStorage(IIterableMapping):
    """A Storage about a report.
    """
    total_reports = schema.Int(title=_('Total number of public reports on this item'), min=0, readonly=True)
    last_report = schema.Field(title=_('Recent public report'), readonly=True)
    last_report_time = schema.Datetime(title=_('Time of the most recent public report'), readonly=True)

    def addReport(report):
        """Adds a new report to the list of reports, and returns the
        report id that was assigned. The report_id property on the report
        will be set accordingly.
        """
        pass

    def __delitem__(key):
        """Delete the report with the given key. The key is a long id.
        """
        pass


class IReport(Interface):
    """A report.

    Report are indexed in the catalog and subject to workflow and security.
    """
    report_id = schema.Int(title=_('A report id unique to reports'))
    storage_type = schema.TextLine(title=_('Storage type'))
    content = schema.Field(title=_('name file or file path'), required=False)
    creator = schema.TextLine(title=_('Username of the report'))
    creation_time = schema.Datetime(title=_('Creation time'))

    def filename(self):
        """
        report file name
        :return: file name
        """
        pass

    def size(self):
        """
        file length
        :return: file size
        """
        pass

    def data(self):
        """
        file byte
        :return: file byte
        """
        pass

    def clear(self):
        """
        clear report content
        """
        pass


class IReportHelper(Interface):
    """View implementing all the helpers method needed for report generation."""

    def get_value(field_name, default=None, as_utf8=False):
        """
            Return the content stored in the object field_name attribute.
            If content is None, a default can be used.
            If content is unicode and flag as_utf8 is True, it will be encoded.
        """
        pass


unique_msg = _('Project type and submission company combinations are not unique. In line ${line_a} and line ${line_b}: ${project_type} - ${submission_company}.')
unique_msg = 'Project type and submission company combinations are not unique. In line ${line_a} and line ${line_b}: ${project_type} - ${submission_company}.'
plan_msg = _('Plan RegExp and template name combinations are not unique. In line ${line_a} and line ${line_b}: ${plan} - ${template}.')
plan_msg = 'Plan RegExp and template name combinations are not unique. In line ${line_a} and line ${line_b}: ${plan} - ${template}.'

class IBaseTemplateConditions(Interface):
    """
    """
    project_type = schema.Choice(title=_('Project type'), description=_('Match Project type'), vocabulary='collective.reflex.project_type', required=False)
    submission_company = schema.Choice(title=_('Submission company'), description=_('Match submission company'), vocabulary='collective.reflex.submission_company', required=False)
    template_name = schema.Choice(title=_('Report template'), description=_('Project type and Submission company template'), vocabulary='collective.reflex.report_templates', required=False)
    naming_rules = schema.TextLine(title=_('Naming rules'), description=_('Report file name naming rules.'), default='', required=False)
    out_type = schema.Choice(title=_('Output type'), description=_('Template output type'), vocabulary='collective.reflex.output_type', required=False)
    note = schema.TextLine(title=_('Note'), description=_('Option notes'), default='', required=False)


class IBaseTemplateConfigure(Interface):
    naming_rules = schema.TextLine(title=_('Naming rules'), description=_('Report file name naming rules.'), default='', required=False)
    default_template = schema.Choice(title=_('Default template'), description=_('If there is no condition to match, this is the default template'), vocabulary='collective.reflex.report_templates', required=False)
    template_name = Attribute('Report template name')
    out_type = Attribute('Report template output type')
    directives.widget(conditions=DataGridFieldFactory)
    conditions = schema.List(title=_('Condition template'), description=_('Project type and submission company combination must be unique.'), value_type=DictRow(title='combinations of conditions', schema=IBaseTemplateConditions), default=[], required=False)

    @invariant
    def condition_valid(data_obj):
        """Single"""
        if data_obj.conditions:
            seen = []
            for index, src in enumerate(data_obj.conditions, start=1):
                cond = (
                 src['project_type'], src['submission_company'])
                if cond in seen:
                    line = seen.index(cond) + 1
                    raise Invalid(_(unique_msg, mapping={'line_a': line, 'line_b': index, 
                       'project_type': cond[0], 
                       'submission_company': cond[1]}))
                seen.append(cond)

    def condition_unique_valid(data_obj):
        """Multiple"""
        if data_obj.conditions:
            seen = []
            for index, src in enumerate(data_obj.conditions, start=1):
                cond = (
                 src['project_type'], src['submission_company'])
                if cond in seen:
                    line = seen.index(cond) + 1
                    raise Invalid(_(unique_msg, mapping={'line_a': line, 'line_b': index, 
                       'project_type': cond[0], 
                       'submission_company': (',').join(cond[1])}))
                seen.append(cond)
                project_type = src['project_type']
                for line, dst in enumerate(data_obj.conditions[index:], 2):
                    if project_type == dst['project_type']:
                        intersection = src['submission_company'] & dst['submission_company']
                        if intersection:
                            raise Invalid(_(unique_msg, mapping={'line_a': index, 'line_b': line, 
                               'project_type': project_type, 
                               'submission_company': (',').join(intersection)}))


class IReportListing(Interface):
    report_state = schema.Choice(title=_('Report state'), vocabulary='collective.reflex.report_states', required=False, readonly=True)
    result_tags = schema.TextLine(title=_('Result tag'), required=False, readonly=True)
    portal_type = schema.Choice(title=_('Portal type'), vocabulary='collective.reflex.available_types', required=False, readonly=True)
    project_type = schema.TextLine(title=_('Project type'), required=False, readonly=True)
    detection_plan = schema.TextLine(title=_('Detection plan'), required=False)
    sample_id = schema.TextLine(title=_('Sample number'), required=False, readonly=True)
    barcode = schema.TextLine(title=_('Barcode'), required=False, readonly=True)
    chip_num = schema.TextLine(title=_('Chip number'), required=True, readonly=False)
    chip_idx = schema.TextLine(title=_('Chip index'), required=True, readonly=False)
    external_num = schema.TextLine(title=_('External number'), required=False)
    sample_name = schema.TextLine(title=_('Sample name'), required=False)
    name = schema.TextLine(title=_('Name'), required=False, readonly=True)
    submission_company = schema.TextLine(title=_('Submission company'), required=False, readonly=True)
    download_count = schema.Int(title=_('Report download count'), required=False, readonly=True)
    sampling_time = schema.Datetime(title=_('Sampling time'), required=False, readonly=True)
    received_time = schema.Datetime(title=_('Received time'), required=False, readonly=True)
    detect_end_time = schema.Datetime(title=_('Detect end time'), required=False)
    report_time = schema.Datetime(title=_('Report time'), required=False, readonly=True)
    created = schema.Datetime(title=_('Creation time'), required=False, readonly=True)
    modified = schema.Datetime(title=_('Modify time'), required=False, readonly=True)


class IStateTransition(model.Schema):
    """Report State Transition"""
    uuid = schema.TextLine(title=_('UUID'), required=True, readonly=False)
    portal_type = schema.Choice(title=_('Portal type'), vocabulary='collective.reflex.available_types', required=False, readonly=False)
    sample_id = schema.TextLine(title=_('Sample number'), required=False, readonly=False)
    barcode = schema.TextLine(title=_('Barcode'), required=False, readonly=False)
    name = schema.TextLine(title=_('Name'), required=False, readonly=False)
    project_type = schema.TextLine(title=_('Project type'), required=False, readonly=False)
    detection_plan = schema.TextLine(title=_('Detection plan'), required=False)
    submission_company = schema.TextLine(title=_('Submission company'), required=False, readonly=False)
    report_state = schema.TextLine(title=_('Report state'), required=False, readonly=False)
    directives.widget('transition_state', CheckBoxFieldWidget)
    transition_state = schema.Choice(title=_('State transition'), vocabulary='collective.reflex.report_transition', required=False)
    changeNote = schema.TextLine(title=_('label_change_note', default='Change Note'), description=_('help_change_note', default='Enter a comment that describes the changes you made.'), required=False)


class IStateTransitionList(model.Schema):
    batch_list = schema.List(title=_('Report State Transition'), value_type=DictRow(title='Report', schema=IStateTransition), required=True)


class IReportIssue(model.Schema):
    """Report Issue"""
    uuid = schema.TextLine(title=_('UUID'), required=True, readonly=False)
    portal_type = schema.Choice(title=_('Portal type'), vocabulary='collective.reflex.available_types', required=False, readonly=False)
    sample_id = schema.TextLine(title=_('Sample number'), required=False, readonly=False)
    barcode = schema.TextLine(title=_('Barcode'), required=False, readonly=False)
    name = schema.TextLine(title=_('Name'), required=False, readonly=False)
    project_type = schema.TextLine(title=_('Project type'), required=False, readonly=False)
    detection_plan = schema.TextLine(title=_('Detection plan'), required=False)
    submission_company = schema.TextLine(title=_('Submission company'), required=False, readonly=False)
    report_state = schema.TextLine(title=_('Report state'), required=False, readonly=False)
    template_name = schema.Choice(title=_('Report template'), vocabulary='collective.reflex.report_template', required=False, readonly=False)
    changeNote = schema.TextLine(title=_('label_change_note', default='Change Note'), description=_('help_change_note', default='Enter a comment that describes the changes you made.'), required=False)


class IReportIssueList(model.Schema):
    batch_list = schema.List(title=_('Report issue'), value_type=DictRow(title='Report', schema=IReportIssue), required=True)


class IPlansTemplateConditions(Interface):
    """Settings stored in the registry
    Describes registry records
    """
    plan_exp = schema.TextLine(title=_('Plan RegExp'), description=_('A RegExp string that specifies the pattern to be matched.'), required=True)
    template_name = schema.Choice(title=_('Report template'), description=_('Plan template'), vocabulary='collective.reflex.report_template', required=True)
    enabled = schema.Bool(title=_('Enabled'), description=_('Enable or disable the option'), default=True, required=False)


class IPlansTemplateConfigure(Interface):
    enabled = schema.Bool(title=_('Enabled'), description=_('Enable or disable the plans report template'), default=False)
    directives.widget(conditions=DataGridFieldFactory)
    conditions = schema.List(title=_('Condition template'), description=_('Plan RegExp and template name combination must be unique.'), value_type=DictRow(title='combinations of conditions', schema=IPlansTemplateConditions), default=[], required=False)

    @invariant
    def condition_valid(data_obj):
        """Single"""
        if getattr(data_obj, 'conditions', None):
            seen = []
            for index, src in enumerate(data_obj.conditions, start=1):
                cond = (
                 src['plan_exp'], src['template_name'])
                if cond in seen:
                    line = seen.index(cond) + 1
                    raise Invalid(_(plan_msg, mapping={'line_a': line, 'line_b': index, 
                       'plan': cond[0], 
                       'template': cond[1]}))
                seen.append(cond)

        return

    def condition_unique_valid(data_obj):
        """Multiple"""
        if data_obj.conditions:
            seen = []
            for index, src in enumerate(data_obj.conditions, start=1):
                cond = (
                 src['plan'], src['template_name'])
                if cond in seen:
                    line = seen.index(cond) + 1
                    raise Invalid(_(plan_msg, mapping={'line_a': line, 'line_b': index, 
                       'plan': cond[0], 
                       'template': (',').join(cond[1])}))
                seen.append(cond)
                project_type = src['plan']
                for line, dst in enumerate(data_obj.conditions[index:], 2):
                    if project_type == dst['plan']:
                        intersection = src['template_name'] & dst['template_name']
                        if intersection:
                            raise Invalid(_(plan_msg, mapping={'line_a': index, 'line_b': line, 
                               'plan': project_type, 
                               'template': (',').join(intersection)}))


class IBeforeReportCreatedEvent(IObjectEvent):
    """Before the report is created.
    """
    renderer_context = Attribute('The renderer context for the object.')


class IAfterReportCreatedEvent(IObjectEvent):
    """ After the report is created.
    """
    renderer_context = Attribute('The renderer context for the object.')


class IBeforeSubReportCreatedEvent(IObjectEvent):
    """Before the individual report is created.
    """
    renderer_context = Attribute('The renderer context for the object.')


class IAfterSubReportCreatedEvent(IObjectEvent):
    """Before the individual report is created.
    """
    renderer_context = Attribute('The renderer context for the object.')


class IReportsAttachment(Interface):
    """Create a report summary table"""
    name = Attribute('Name of adapter')
    title = Attribute('Title of adapter')
    filename = Attribute('filename of attachment')

    def attachment(self, iterator, **kwargs):
        """
        :param iterator: brain, obj, ctx
        :type iterator: generator
        :returns: file byte
        :rtype: file-like object
        """
        pass