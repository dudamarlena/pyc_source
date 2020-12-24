# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/Products/CMFResource/interfaces.py
# Compiled at: 2018-05-16 18:23:05
import inspect, os, re
from Products.CMFPlone.utils import safe_unicode
from Products.CMFResource import _
from Products.CMFResource.vocabulary import SampleSourceSourceBinder
from Products.CMFResource.vocabulary import SubmissionHospitalSourceBinder
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform import directives
from plone.resource.manifest import ManifestFormat
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.formwidget.query.widget import QuerySourceFieldRadioWidget
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
REPORT_RESOURCE_NAME = 'reportpkg'
REPORT_DOCFILE_NAME = 'index.odt'
REPORT_PREVIEW_NAME = 'preview.png'
REPORT_EXAMPLE_NAME = 'example.pdf'
REPORT_MANIFEST_FORMAT = ManifestFormat(REPORT_RESOURCE_NAME, keys=[
 'title', 'description', 'fortype', 'docfile',
 'preview', 'example', 'created', 'version'], defaults={'docfile': REPORT_DOCFILE_NAME, 
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
    try:
        inspect.isabstract(CMFResourceSettings)
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


class ICMFResourceLayer(IDefaultBrowserLayer):
    """"""
    pass


class IReportPkg(Interface):
    """
    """
    __name__ = schema.TextLine(title=_('Name'))
    title = schema.TextLine(title=_('Title'), required=False)
    description = schema.TextLine(title=_('Description'), required=False)
    fortype = schema.ASCIILine(title=_('For type'), required=False, default='*')
    docfile = schema.TextLine(title=_('Document file'), required=False)
    example = schema.TextLine(title=_('Example image'), required=False)
    preview = schema.TextLine(title=_('Preview pdf'), required=False)
    created = schema.TextLine(title=_('Created'))
    version = schema.TextLine(title=_('Version'))
    zipfile = schema.Bytes(title=_('File data'))


class CMFResourceSettings(Interface):
    uno_path = schema.TextLine(title='path', required=False, default=safe_unicode(os.getenv('PYTHON_UNO', '/usr/bin/python3')), constraint=check_for_uno)
    oo_server = schema.TextLine(title='address', required=False, default=safe_unicode(os.getenv('OO_SERVER', 'localhost')))
    oo_port = schema.Int(title=_('port'), required=False, default=int(os.getenv('OO_PORT', 2002)))
    storage_type = schema.Choice(title=_('Storage type'), vocabulary='Products.CMFResource.vocabulary.storage_type', default='Blob')
    storage_location = schema.TextLine(title='Storage location', default='/tmp')
    naming_rules = schema.TextLine(title='Naming rules', default='', required=False)
    versioning_support = schema.Bool(title='Versioning support', default=False)
    auto_create = schema.Bool(title='Auto create', default=False)
    send_report = schema.Bool(title='Send report', default=False)
    print_report = schema.Bool(title='Print report', default=False)
    reply_to = schema.TextLine(title=_('Reply to Address'), constraint=check_for_email, default='', required=False)
    subject = schema.TextLine(title='Subject', description='Subject of the message', default='', required=False)
    message = schema.Text(title='Message', description='The message that you want to mail', default='', required=False)


class IReportStorage(IIterableMapping):
    total_reports = schema.Int(title=_('Total number of public reports on this item'), min=0, readonly=True)
    last_report = schema.Field(title=_('Recent public report'), readonly=True)
    last_report_time = schema.Datetime(title=_('Time of the most recent public report'), readonly=True)

    def addReport(report):
        """"""
        pass

    def __delitem__(key):
        """
        """
        pass


class IReport(Interface):
    """
    """
    report_id = schema.Int(title=_('A report id unique to reports'))
    storage_type = schema.TextLine(title=_('Storage type'))
    content = schema.Field(title=_('name file or file path'), required=False)
    creator = schema.TextLine(title=_('Username of the report'))
    creation_time = schema.Datetime(title=_('Creation time'))

    def filename(self):
        """
        """
        pass

    def size(self):
        """
        """
        pass

    def data(self):
        """
        """
        pass

    def clear(self):
        """
        """
        pass


class IReportHelper(Interface):

    def get_value(field_name, default=None, as_utf8=False):
        """
        """
        pass


class IReportTemplate(Interface):
    naming_rules = schema.TextLine(title=_('Naming rules'), description=_('Report file name naming rules.'), default='', required=False)
    template_name = schema.ASCIILine(title=_('Report template name'), description=_('Report template URL'), default='')
    to_addrs = schema.TextLine(title=_('Recipient address'), description=_('A comma-separated list of one or more email addresses'), constraint=check_for_email, default='', required=False)
    bcc_addrs = schema.TextLine(title=_('Blind CarbonCopy recipients'), description=_('A comma-separated list of one or more email addresses'), constraint=check_for_email, default='', required=False)
    print_report = schema.Bool(title=_('Print report'), description=_('Print report'), default=False)
    to_bcc = schema.Tuple(title=_('To, Bcc'), value_type=schema.TextLine(), default=('',
                                                                                     ''), required=False)


class IReportListing(Interface):
    steps = schema.Choice(title=_('Steps'), vocabulary='Products.CMFResource.vocabulary.progress_steps', required=True, readonly=True)
    report_state = schema.Choice(title=_('Report state'), vocabulary='Products.CMFResource.vocabulary.report_state', required=False, readonly=True)
    portal_type = schema.Choice(title=_('Portal type'), vocabulary='Products.CMFResource.vocabulary.allowed_types', required=False, readonly=True)
    detection_plan = schema.TextLine(title=_('Detection plan'), required=False, readonly=True)
    sample_no = schema.TextLine(title=_('Sample number'), required=False, readonly=True)
    barcode = schema.TextLine(title=_('Barcode'), required=False, readonly=True)
    name = schema.TextLine(title=_('Name'), required=False, readonly=True)
    sex = schema.TextLine(title=_('Sex'), required=False, readonly=True)
    submission_hospital = schema.TextLine(title=_('Submission hospital'), required=False, readonly=True)
    submission_department = schema.TextLine(title=_('Submission department'), required=False, readonly=True)
    submission_doctor = schema.TextLine(title=_('Submission doctor'), required=False, readonly=True)
    sample_source = schema.TextLine(title=_('Sample source'), required=False, readonly=True)
    send_count = schema.Int(title=_('Report send count'), required=False, readonly=True)
    print_count = schema.Int(title=_('Report print count'), required=False, readonly=True)
    download_count = schema.Int(title=_('Report download count'), required=False, readonly=True)
    sampling_time = schema.Datetime(title=_('Sampling time'), required=False, readonly=True)
    received_time = schema.Datetime(title=_('Received time'), required=False, readonly=True)
    report_time = schema.Datetime(title=_('Report time'), required=False, readonly=True)
    modified = schema.Datetime(title=_('Modify time'), required=False, readonly=True)


class IReportAudit(model.Schema):
    uuid = schema.TextLine(title=_('UUID'), required=True, readonly=False)
    steps = schema.Choice(title=_('Steps'), vocabulary='Products.CMFResource.vocabulary.progress_steps', required=False, readonly=False)
    portal_type = schema.Choice(title=_('Portal type'), vocabulary='Products.CMFResource.vocabulary.allowed_types', required=False, readonly=False)
    sample_no = schema.TextLine(title=_('Sample number'), required=False, readonly=False)
    barcode = schema.TextLine(title=_('Barcode'), required=False, readonly=False)
    name = schema.TextLine(title=_('Name'), required=False, readonly=False)
    sample_source = schema.TextLine(title=_('Sample source'), required=False, readonly=False)
    submission_hospital = schema.TextLine(title=_('Submission hospital'), required=False, readonly=False)
    detection_plan = schema.TextLine(title=_('Detection plan'), required=False, readonly=False)
    directives.widget('report_state', RadioFieldWidget)
    report_state = schema.Choice(title=_('Report state'), vocabulary='Products.CMFResource.vocabulary.report_state', required=False, readonly=False)
    template_name = schema.List(title=_('Report template'), description=_('Submission hospital and Sample source template'), value_type=schema.Choice(vocabulary='Products.CMFResource.vocabulary.report_template', required=False), default=list(), required=False, readonly=False)
    changeNote = schema.TextLine(title=_('label_change_note', default='Change Note'), description=_('help_change_note', default='Enter a comment that describes the changes you made.'), required=False)


class IReportAuditList(model.Schema):
    batch_list = schema.List(title=_('Report Audit'), value_type=DictRow(title='Report', schema=IReportAudit), required=True)


class IBeforeReportCreatedEvent(IObjectEvent):
    renderer_context = Attribute('The renderer context for the object.')


class IAfterReportCreatedEvent(IObjectEvent):
    renderer_context = Attribute('The renderer context for the object.')


class IBeforeSubReportCreatedEvent(IObjectEvent):
    renderer_context = Attribute('The renderer context for the object.')


class IAfterSubReportCreatedEvent(IObjectEvent):
    renderer_context = Attribute('The renderer context for the object.')


class IReportsAttachment(Interface):
    name = Attribute('Name of adapter')
    title = Attribute('Title of adapter')
    filename = Attribute('filename of attachment')

    def attachment(self):
        """
        """
        pass