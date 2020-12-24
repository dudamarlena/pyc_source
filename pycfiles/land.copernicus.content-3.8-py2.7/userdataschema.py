# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/userdataschema.py
# Compiled at: 2017-12-07 03:50:15
from zope.component import getUtility
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.browser.register import RegistrationForm
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.app.users.browser.register import CantChoosePasswordWidget
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from zope.browserpage import ViewPageTemplateFile
from zope.formlib.boolwidgets import CheckBoxWidget
from land.copernicus.content.config import EEAMessageFactory as _
import re
professional_thematic_domain_options = SimpleVocabulary([
 SimpleTerm(value='Agriculture', title=_('Agriculture')),
 SimpleTerm(value='Architectural and Landscape Design', title=_('Architectural and Landscape Design')),
 SimpleTerm(value='Atmosphere', title=_('Atmosphere')),
 SimpleTerm(value='Climate Change', title=_('Climate Change')),
 SimpleTerm(value='Demography', title=_('Demography')),
 SimpleTerm(value='Ecology and Environment', title=_('Ecology and Environment')),
 SimpleTerm(value='Emergency Management', title=_('Emergency Management')),
 SimpleTerm(value='Energy, Utilities and Industrial Infrastructure', title=_('Energy, Utilities and Industrial Infrastructure')),
 SimpleTerm(value='Forestry', title=_('Forestry')),
 SimpleTerm(value='Health', title=_('Health')),
 SimpleTerm(value='Hydrography', title=_('Hydrography')),
 SimpleTerm(value='Mapping', title=_('Mapping')),
 SimpleTerm(value='Security', title=_('Security')),
 SimpleTerm(value='Snow and Ice', title=_('Snow and Ice')),
 SimpleTerm(value='Soils and Geology', title=_('Soils and Geology')),
 SimpleTerm(value='Tourism and Recreation', title=_('Tourism and Recreation')),
 SimpleTerm(value='Transport and Routing', title=_('Transport and Routing')),
 SimpleTerm(value='Urban and Spatial Planning', title=_('Urban and Spatial Planning'))])
institutional_domain_options = SimpleVocabulary([
 SimpleTerm(value='Citizen', title=_('Citizen')),
 SimpleTerm(value='Commercial', title=_('Commercial')),
 SimpleTerm(value='Education', title=_('Education')),
 SimpleTerm(value='NGO', title=_('NGO')),
 SimpleTerm(value='Public Authority', title=_('Public Authority')),
 SimpleTerm(value='Research and development', title=_('Research and development'))])

def validateAccept(value):
    if value is not True:
        return False
    return True


def validate_phone(value):
    phone_re = re.compile('(\\d{3})\\D*(\\d{3})\\D*(\\d{4})\\D*(\\d*)$', re.VERBOSE)
    if phone_re.match(value):
        return True
    return False


class DisclaimerWidget(CheckBoxWidget):
    """ Widget for accept terms of use in user registration """
    template = ViewPageTemplateFile('browser/templates/disclaimer-widget.pt')

    def __call__(self):
        val = super(DisclaimerWidget, self).__call__()
        self.val = val
        return self.template()


class CopernicusRegistrationForm(RegistrationForm):

    @property
    def form_fields(self):
        if not self.showForm:
            return []
        portal = getUtility(ISiteRoot)
        defaultFields = super(RegistrationForm, self).form_fields
        if portal.getProperty('validate_email', True):
            defaultFields = defaultFields.omit('password', 'password_ctl')
            defaultFields['mail_me'].custom_widget = CantChoosePasswordWidget
            defaultFields['disclaimer'].custom_widget = DisclaimerWidget
        else:
            defaultFields = defaultFields.omit('mail_me')
        defaultFields = defaultFields.omit('fullname')
        thematic_domain = defaultFields['thematic_domain']
        institutional_domain = defaultFields['institutional_domain']
        thematic_domain.custom_widget = MultiCheckBoxVocabularyWidget
        institutional_domain.custom_widget = MultiCheckBoxVocabularyWidget
        return defaultFields


class CustomizedUserDataPanel(UserDataPanel):

    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('email', 'first_name', 'last_name', 'description', 'disclaimer', 'fax', 'fullname', 'home_page', 'job_title', 'location', 'mobile', 'postal_address', 'portrait', 'pdelete', 'organisation', 'reason', 'telephone')
        thematic_domain = self.form_fields['thematic_domain']
        thematic_domain.custom_widget = MultiCheckBoxVocabularyWidget
        institutional_domain = self.form_fields['institutional_domain']
        institutional_domain.custom_widget = MultiCheckBoxVocabularyWidget

    def validate(self, action, data):
        errors = super(UserDataPanel, self).validate(action, data)
        return errors


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    first_name = schema.TextLine(title=_('label_first_name', default='First Name'), description=_('help_first_name', default='Enter your first name.'), required=True)
    last_name = schema.TextLine(title=_('label_last_name', default='Last Name'), description=_('help_last_name', default='Enter your last name.'), required=True)
    thematic_domain = schema.List(title=_('label_thematic_domain', default='Professional thematic domain'), value_type=schema.Choice(vocabulary=professional_thematic_domain_options))
    institutional_domain = schema.List(title=_('label_institutional_domain', default='Institutional domain'), value_type=schema.Choice(vocabulary=institutional_domain_options))
    reason = schema.TextLine(title=_('label_reason', default='Reason to create the account'), description=_('help_reason', default='Fill in the reason for account creation'), required=False)
    job_title = schema.TextLine(title=_('label_job_title', default='Job title'), description=_('help_job_title', default='Fill in the job title'), required=False)
    postal_address = schema.Text(title=_('label_postal_address', default='Postal address'), description=_('help_postal_address', default='Fill in the postal address'), required=False)
    telephone = schema.ASCIILine(title=_('label_telephone', default='Telephone number'), description=_('help_telephone', default='Fill in the telephone number'), required=False, constraint=validate_phone)
    mobile = schema.ASCIILine(title=_('label_mobile', default='Mobile telephone number'), description=_('help_mobile', default='Fill in the mobile telephone number'), required=False, constraint=validate_phone)
    fax = schema.ASCIILine(title=_('label_fax', default='Fax number'), description=_('help_fax', default='Fill in the fax number'), required=False, constraint=validate_phone)
    organisation = schema.TextLine(title=_('label_organisation', default='Organisation'), description=_('help_organisation', default='Fill in the organisation'), required=False)
    disclaimer = schema.Bool(title=_('label_disclaimer', default='Accept terms of use'), description=_('help_disclaimer', default='Tick this box to indicate that you have found, read and accepted the terms of use for this site. Your email will not be further distributed to third parties. The registration is only used for reporting purposes to the EP and Council.'), required=True, constraint=validateAccept)