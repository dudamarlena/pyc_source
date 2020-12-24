# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/Products/CMFResource/adapter.py
# Compiled at: 2018-05-16 18:23:05
import datetime, json, logging, os, re
from io import BytesIO
import barcode
from Products.CMFResource.interfaces import IReportHelper
from Products.CMFResource.interfaces import IReportTemplate
from Products.CMFResource.utils import FILE_TYPES
from plone import api
from plone.app.textfield import RichTextValue
from plone.dexterity.utils import iterSchemataForType
from plone.i18n import normalizer
from plone.stringinterp.interfaces import IStringInterpolator
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.browser import BrowserView
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IVocabularyFactory
__all__ = [
 'BaseReportTemplate', 'BaseReportHelperView',
 'get_vocabulary_value']
logger = logging.getLogger(__name__)

@implementer(IReportTemplate)
class BaseReportTemplate(object):

    def __init__(self, context):
        self.context = context

    def update_config(self, interface=None):
        naming_rules = api.portal.get_registry_record('naming_rules', interface=interface, default='')
        default_template = api.portal.get_registry_record('default_template', interface=interface, default=None)
        bcc_addrs = api.portal.get_registry_record('bcc_addrs', interface=interface, default='')
        conditions = api.portal.get_registry_record('conditions', interface=interface, default=[])
        template_queue = [
         None, None, None, default_template]
        to_addrs_queue = ['', '', '', '']
        print_queue = [False, False, False, False]
        sample_source = getattr(self.context, 'sample_source', '')
        submission_hospital = getattr(self.context, 'submission_hospital', '')
        for item in conditions:
            if sample_source == item['sample_source'] and submission_hospital == item['submission_hospital']:
                template_queue[0] = item['template_name']
                to_addrs_queue[0] = item['to_addrs']
                print_queue[0] = item['print_report']
            elif sample_source == item['sample_source'] and not item['submission_hospital']:
                template_queue[1] = item['template_name']
                to_addrs_queue[1] = item['to_addrs']
                print_queue[1] = item['print_report']
            elif not item['sample_source'] and submission_hospital == item['submission_hospital']:
                template_queue[2] = item['template_name']
                to_addrs_queue[2] = item['to_addrs']
                print_queue[2] = item['print_report']

        template_name = filter(None, template_queue)
        template_name = template_name[0] if template_name else None
        to_addrs = filter(None, to_addrs_queue)
        to_addrs = to_addrs[0] if to_addrs else ''
        position = template_queue.index(template_name) if template_name else -1
        printing = print_queue[position]
        self.naming_rules = naming_rules
        self.template_name = template_name
        self.to_addrs = to_addrs
        self.bcc_addrs = bcc_addrs
        self.print_report = printing
        return

    @property
    def to_bcc(self):
        return (self.to_addrs, self.bcc_addrs)

    def values(self):
        return (
         self.template,
         (
          self.to_addrs, self.bcc_addrs),
         self.print_report)

    def items(self):
        return {'template_name': self.template_name, 
           'to_bcc': (
                    self.to_addrs, self.bcc_addrs), 
           'printing': self.print_report}


@implementer(IReportHelper)
class BaseReportHelperView(BrowserView):
    field_alias = dict()

    def __init__(self, context, request):
        super(BaseReportHelperView, self).__init__(context, request)
        self.action_context = None
        self.pod_renderer = None
        self.portal_state = getMultiAdapter((
         self.context, self.request), name='plone_portal_state')
        self.plone_tools = getMultiAdapter((
         self.context, self.request), name='plone_tools')
        return

    def __getitem__(self, key):
        return self.get_value(key)

    def __getattr__(self, item):
        pass

    @property
    def report_filename(self):
        filename = ''
        template_cfg = IReportTemplate(self.context)
        naming_rules = template_cfg.naming_rules
        if naming_rules:
            filename = self.generate_filename(naming_rules)
        if not filename:
            naming_rules = api.portal.get_registry_record('Products.CMFResource.interfaces.CMFResourceSettings.naming_rules', default='')
            if naming_rules:
                filename = self.generate_filename(naming_rules)
        if not filename:
            filename = self.default_filename()
        return filename

    def generate_filename(self, filename):
        interpolator = IStringInterpolator(self.context)
        try:
            filename = interpolator(filename).strip()
        except Exception as error:
            filename = ''
            logger.warn(error)

        name, ext = os.path.splitext(filename)
        if name:
            if ext[1:] not in FILE_TYPES:
                filename = ('{0}.pdf').format(filename)
            if not filename.endswith('.pdf'):
                filename = ('{0}.pdf').format(filename)
        else:
            filename = ''
        filename = self.normalize(filename)
        return filename

    def default_filename(self):
        barcode = self.get_value('barcode')
        name = self.get_value('name')
        now = datetime.datetime.now().isoformat().translate(None, '-T:.')
        filename = ('{barcode}-{name}-{now}.pdf').format(barcode=barcode, name=name, now=now)
        filename = self.normalize(filename)
        return filename

    @staticmethod
    def normalize(text):
        text = normalizer.IGNORE_REGEX.sub('-', text)
        text = normalizer.DANGEROUS_CHARS_REGEX.sub('-', text)
        text = normalizer.MULTIPLE_DASHES_REGEX.sub('-', text)
        text = normalizer.EXTRA_DASHES_REGEX.sub('', text)
        text = re.sub('\\s', '', text)
        return text

    def report_pre(self, template_obj=None):
        """"""
        pass

    def report_post(self, document_path=None, template_obj=None):
        """"""
        pass

    def report_error(self):
        pass

    def get_value(self, field_name, default=None, as_utf8=False):
        value = getattr(self.context, field_name, None)
        if value is None and field_name in self.field_alias:
            value = getattr(self.context, self.field_alias[field_name])
        if value is None:
            return default
        else:
            if isinstance(value, RichTextValue):
                value = value.output
            if as_utf8 and isinstance(value, unicode):
                value = value.encode('utf8')
            return value

    def format_date(self, field_name, long_format=None, time_only=None, custom_format=None):
        date = self.get_value(field_name)
        if date is None:
            return ''
        else:
            if type(date) == datetime.date:
                date = datetime.datetime(date.year, date.month, date.day)
            if not custom_format:
                formatted_date = api.portal.get_localized_time(date, long_format, time_only)
            else:
                formatted_date = date.strftime(custom_format).decode('utf8')
            return formatted_date

    def render_xhtml(self, field_name):
        if not self.pod_renderer:
            return ''
        html_text = self.get_value(field_name)
        display = self.pod_renderer.renderXhtml(html_text)
        return display

    def render_choice(self, field_name, sep=', '):
        fields = get_type_fields(self.context.portal_type)
        fields = dict(fields)
        field_obj = fields[field_name]
        field_value = self.get_value(field_name)
        if field_obj.__class__ is schema.Choice:
            field_value = get_vocabulary_value(self.context, field_obj, field_value)
        elif field_obj.__class__ is schema.List and field_obj.value_type.__class__ is schema.Choice:
            for value in field_value:
                field_value = get_vocabulary_value(self.context, field_obj.value_type, value)

            field_value = sep.join(field_value)
        return field_value

    @property
    def today(self):
        return datetime.datetime.now().date().isoformat()

    @property
    def now(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    def zhcn_date(self, field_name):
        return self.format_date(field_name, custom_format='%Y年%m月%d日')

    @property
    def age(self):
        age = self.get_value('age')
        if age:
            return age
        sampling = self.get_value('sampling_time')
        birthday = self.get_value('birthday')
        if birthday:
            delta = sampling.date() - birthday
            return delta.days // 365

    def barcode_image(self):
        fp = BytesIO()
        code = self['barcode']
        barcode.generate('code128', code, writer=barcode.writer.ImageWriter(), output=fp, writer_options={'module_height': 2.62, 'module_width': 0.125, 
           'write_text': False})
        return fp


def get_vocabulary_value(obj, field_obj, value):
    if not value:
        return value
    else:
        vocabulary = field_obj.vocabulary
        if not vocabulary:
            vocabularyName = field_obj.vocabularyName
            if vocabularyName:
                vocabulary = getUtility(IVocabularyFactory, name=vocabularyName)(obj)
        if vocabulary:
            try:
                term = vocabulary.getTermByToken(value)
            except LookupError:
                term = None

        else:
            term = None
        if term:
            title = term.title
            if not title:
                return value
            title = translate(title, context=api.portal.getRequest())
            return title
        else:
            return value
        return


def get_type_fields(portal_type):
    schemas = iterSchemataForType(portal_type)
    fields_list = []
    for schema_ in schemas:
        _fields = getFieldsInOrder(schema_)
        fields_list.extend(_fields)

    return fields_list