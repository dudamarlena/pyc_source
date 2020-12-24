# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/collective/ant/interfaces.py
# Compiled at: 2019-12-16 21:32:12
"""Module where all interfaces, events and exceptions live."""
from collective.ant import _
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component.interfaces import IObjectEvent
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleVocabulary

class ICollectiveAntLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    pass


class ICollectiveAntSettings(Interface):
    """"""
    recent_group = schema.Dict(title=_('Content_type recent group'), key_type=schema.Choice(title='Content type', vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'), value_type=schema.List(title='Group ID list', value_type=schema.TextLine(title='Group ID', required=True), default=[]), default={})


unique_msg = _('Content type and Project type combinations are not unique. In line ${line_a} and line ${line_b}: ${content_type} - ${project_type}.')
unique_msg = 'Content type and Project type combinations are not unique. In line ${line_a} and line ${line_b}: ${content_type} - ${project_type}.'

class IExpireCondition(Interface):
    """"""
    content_type = schema.Choice(title=_('Content type'), description=_('Match Project type'), vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes', required=False)
    project_type = schema.TextLine(title=_('Project type'), description=_('Match Project type'), required=False)
    reference_date = schema.Choice(title=_('Reference date'), description=_('Reference date'), vocabulary='collective.ant.date_index', default='created', required=False)
    expire_days = schema.Int(title=_('Expiration days'), description=_('Please fill out an integer range: 1-365'), min=0, max=365, default=7, required=False)
    deadline_days = schema.Int(title=_('Deadline days'), description=_('Please fill out an integer range: 1-365'), min=0, max=365, default=30, required=False)
    user_group = schema.Choice(title=_('Expiration notification user group'), description=_('When the entry has expired, send an email message to inform the user'), vocabulary='plone.app.vocabularies.Groups', required=False)


class IExpireRules(Interface):
    """"""
    directives.widget(conditions=DataGridFieldFactory)
    conditions = schema.List(title=_('Condition Rules'), description=_('Content type and Project type combination must be unique.'), value_type=DictRow(title='combinations of conditions', schema=IExpireCondition), default=[], required=False)

    @invariant
    def condition_valid(data_obj):
        """Single"""
        if data_obj.conditions:
            seen = []
            for index, src in enumerate(data_obj.conditions, start=1):
                cond = (
                 src['content_type'], src['project_type'])
                if cond in seen:
                    line = seen.index(cond) + 1
                    raise Invalid(_(unique_msg, mapping={'line_a': line, 'line_b': index, 
                       'content_type': cond[0], 
                       'project_type': cond[1]}))
                seen.append(cond)


class ISerialCondition(Interface):
    """"""
    content_type = schema.Choice(title=_('Content type'), description=_('Match Project type'), vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes', required=False)
    project_type = schema.TextLine(title=_('Project type'), description=_('Match Project type'), required=False)
    serial_prefix = schema.ASCIILine(title=_('Serial prefix'), min_length=0, max_length=10, default='', required=False)
    serial_suffix = schema.Int(title=_('Serial random suffix'), min=0, max=17, default=0)
    cycle_period = schema.Choice(title=_('Cycle period'), vocabulary=SimpleVocabulary.fromValues([
     'year', 'month', 'week', 'day']), required=False)
    cycle_width = schema.Int(title=_('Cycle characters width'), min=0, max=5, default=4)
    cycle_stage = schema.Int(title=_('Cycle stage'), min=1, default=1)
    cycle_counter = schema.Int(title=_('Cycle counter'), min=0, default=0)


class ISerialRules(Interface):
    """"""
    sample_enabled = schema.Bool(title=_('Sample ID Enabled'), description=_('Enable or disable the option'), default=True, required=False)
    barcode_enabled = schema.Bool(title=_('Barcode Enabled'), description=_('Enable or disable the option'), default=True, required=False)
    default_enabled = schema.Bool(title=_('Default Enabled'), description=_('Enable or disable the option'), default=False, required=False)
    directives.widget(conditions=DataGridFieldFactory)
    conditions = schema.List(title=_('Condition Rules'), description=_('Content type and Project type combination must be unique.'), value_type=DictRow(title='combinations of conditions', schema=ISerialCondition), default=[], required=False)

    @invariant
    def condition_valid(data_obj):
        """Single"""
        if data_obj.conditions:
            seen = []
            for index, src in enumerate(data_obj.conditions, start=1):
                cond = (
                 src['content_type'], src['project_type'])
                if cond in seen:
                    line = seen.index(cond) + 1
                    raise Invalid(_(unique_msg, mapping={'line_a': line, 'line_b': index, 
                       'content_type': cond[0], 
                       'project_type': cond[1]}))
                seen.append(cond)


class IProjectType(Interface):
    """Project type"""
    name_list = schema.List(title='Project type name list', description='A list of project type', value_type=schema.TextLine(title='Project type', required=True), unique=True, default=[])


class ISubmissionCompany(Interface):
    """Submission Company"""
    name_list = schema.List(title='Submission company name list', description='A list of submission company', value_type=schema.TextLine(title='Submission company', required=True), unique=True, default=[])


class ISample(model.Schema):
    """Sample"""
    uuid = schema.TextLine(title=_('UUID'), required=False, readonly=False)
    sample_id = schema.TextLine(title=_('Sample number'), required=True)
    barcode = schema.TextLine(title=_('Barcode'), required=True)
    name = schema.TextLine(title=_('Name'), required=True)
    project_type = schema.Choice(title=_('Project type'), required=True, vocabulary='collective.ant.project_type')
    detection_plan = schema.Choice(title=_('Detection plan'), required=False, vocabulary='collective.ant.detection_plan')


class IResult(model.Schema):
    """Result"""
    uuid = schema.TextLine(title=_('UUID'), required=False, readonly=False)
    sample_id = schema.TextLine(title=_('Sample number'), required=False, readonly=False)


class IFailedRedo(model.Schema):
    """Failed Redo"""
    uuid = schema.TextLine(title=_('UUID'), required=False, readonly=False)
    sample_id = schema.TextLine(title=_('Sample number'), required=False, readonly=False)
    barcode = schema.TextLine(title=_('Barcode'), required=False, readonly=False)
    name = schema.TextLine(title=_('Name'), required=False)
    review_state = schema.TextLine(title=_('Review state'), required=False, readonly=False)
    steps = schema.Choice(title=_('Steps'), default='sample', vocabulary='collective.ant.progress_steps', required=True)
    changeNote = schema.TextLine(title=_('label_change_note', default='Change Note'), description=_('help_change_note', default='Enter a comment that describes the changes you made.'), required=False)


class IChangeSteps(model.Schema):
    """Change Steps"""
    uuid = schema.TextLine(title=_('UUID'), required=False, readonly=False)
    sample_id = schema.TextLine(title=_('Sample number'), required=False, readonly=False)
    barcode = schema.TextLine(title=_('Barcode'), required=False, readonly=False)
    name = schema.TextLine(title=_('Name'), required=False)
    review_state = schema.TextLine(title=_('Review state'), required=False, readonly=False)
    steps = schema.Choice(title=_('Steps'), default='sample', vocabulary='collective.ant.progress_steps', required=True)
    changeNote = schema.TextLine(title=_('label_change_note', default='Change Note'), description=_('help_change_note', default='Enter a comment that describes the changes you made.'), required=False)


class IStateTransition(model.Schema):
    """Change Workflow Status"""
    uuid = schema.TextLine(title=_('UUID'), required=False, readonly=False)
    sample_id = schema.TextLine(title=_('Sample number'), required=False, readonly=False)
    barcode = schema.TextLine(title=_('Barcode'), required=False, readonly=False)
    name = schema.TextLine(title=_('Name'), required=False)
    steps = schema.Choice(title=_('Steps'), default='sample', vocabulary='collective.ant.progress_steps', required=False, readonly=False)
    review_state = schema.TextLine(title=_('Review state'), required=False, readonly=False)
    directives.widget('transition_state', CheckBoxFieldWidget)
    transition_state = schema.Choice(title=_('State transition'), vocabulary='collective.ant.review_transition', required=False)
    changeNote = schema.TextLine(title=_('label_change_note', default='Change Note'), description=_('help_change_note', default='Enter a comment that describes the changes you made.'), required=False)


class ISampleList(model.Schema):
    batch_list = schema.List(title=_('Sample'), value_type=DictRow(title='Sample', schema=ISample), required=True)


class IResultList(model.Schema):
    batch_list = schema.List(title=_('Result'), value_type=DictRow(title='Result', schema=IResult), required=True)


class IFailedRedoList(model.Schema):
    batch_list = schema.List(title=_('Failed redo'), description=_('Select redo steps'), value_type=DictRow(title='Redo', schema=IFailedRedo), required=True)


class IChangeStepsList(model.Schema):
    batch_list = schema.List(title=_('Change steps'), description=_('Select new steps'), value_type=DictRow(title='Steps', schema=IChangeSteps), required=True)


class IStateTransitionList(model.Schema):
    batch_list = schema.List(title=_('State transition'), value_type=DictRow(title='State', schema=IStateTransition), required=True)


class IStepsChangedEvent(IObjectEvent):
    """An event related to an object.

    The object that generated this event is not necessarily the object
    refer to by location.
    """
    oldSteps = Attribute('The old steps value for the object.')
    newSteps = Attribute('The new steps value for the object.')


class IDataConverter(Interface):
    """A data converter from upload file to system internal value."""
    file_handler = Attribute('The list of file handler.')
    request = Attribute('The request object driving the view')

    def extract_data(value):
        """Convert an input value to a system internal value."""
        pass


class IExportPlugin(Interface):
    """Export data"""
    name = Attribute('Name of adapter')
    title = Attribute('Title of adapter')
    filename = Attribute('Filename of attachment')

    def attachment(self):
        """
        file byte
        :return: file-like object
        """
        pass


class IExternalPlugin(Interface):
    """External Plugin"""
    name = Attribute('Name of adapter')
    title = Attribute('Title of adapter')
    filename = Attribute('Filename of attachment')

    def attachment(self):
        """
        file byte
        :return: file-like object
        """
        pass


class ITools(Interface):
    """Common tools"""

    def get_vocab_item(self, vocab_name=None):
        """Returns a list of all (id, title) from the vocab name.

        The template expects a tuple/list of (id, title) of the field.
        """
        pass


class IDataTransform(Interface):
    """The transform objects through a pipeline"""
    name = Attribute('The trans name')
    title = Attribute('The trans title')
    matrix = Attribute('The content data struct')
    portal_type = Attribute('Content type')
    primary_key = Attribute('Primary key')
    primary_title = Attribute('Primary key')

    def __init__(self, context):
        self.context = context
        self.matrix = {'data': {}, 'errs': {}, 'tags': {}, 'json': {}, 'html': {}}

    def __call__(*args, **kwargs):
        """Load and execute the named trans

        Any dictionaries passed in as extra keywords, are interpreted as
        attribute  configuration overrides. Only string keys and values are
        accepted.
        """
        pass

    def extract_data(*args, **kwargs):
        """Extract the data of the form."""
        pass

    def validate_data(set_errors=True):
        """Validate that the given value is a valid field value.

        Returns nothing but raises an error if the value is invalid.
        It checks everything specific to a Field and also checks
        with the additional constraint.
        """
        pass

    def to_tags():
        """Make Data Tags."""
        pass

    def to_json():
        """Convert the Data to a json."""
        pass

    def to_html():
        """Render a Data as an HTML."""
        pass

    def template(self):
        """:return import template"""
        pass


class IDataTransFile(IDataTransform):
    """The transforms data through a file"""

    def __call__(filename):
        """"""
        pass

    def extract_data(filename):
        """Extract the data of the form."""
        pass


class IDataTransPage(IDataTransform):
    """The transforms data through a page"""

    def __call__(self, data):
        """"""
        pass