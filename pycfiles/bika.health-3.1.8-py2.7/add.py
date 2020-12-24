# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/analysisrequest/add.py
# Compiled at: 2015-11-03 03:53:39
from bika.lims.browser.analysisrequest.add import AnalysisRequestAddView as AnalysisRequestAddViewLIMS
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import json
from Products.CMFCore.utils import getToolByName
from bika.lims.browser.widgets import AddressWidget

class AnalysisRequestAddView(AnalysisRequestAddViewLIMS):
    """
    The main AR Add form adapted for health usage
    """
    health_template = ViewPageTemplateFile('templates/ar_add_health_standard.pt')
    patient_template = ViewPageTemplateFile('templates/ar_addpatient.pt')
    doctor_referrer_template = ViewPageTemplateFile('templates/ar_add_doctor_referrer.pt')
    insurance_template = ViewPageTemplateFile('templates/ar_insurance.pt')
    analyses_template = ViewPageTemplateFile('templates/ar_analyses.pt')
    prices_template = ViewPageTemplateFile('templates/ar_prices.pt')

    def __init__(self, context, request):
        AnalysisRequestAddViewLIMS.__init__(self, context, request)
        self.templatename = self.request.get('tpl', '')
        self.w = AddressWidget()

    def __call__(self):
        self.templatename = 'classic'
        if self.templatename == 'classic':
            return AnalysisRequestAddViewLIMS.__call__(self)
        else:
            enable_bika_request_field = self.context.bika_setup.Schema().getField('EnableBikaAnalysisRequestRequestForm')
            enable_bika_request = enable_bika_request_field.get(self.context.bika_setup)
            if enable_bika_request:
                return AnalysisRequestAddViewLIMS.__call__(self)
            self.col_count = 1
            self.request.set('disable_border', 1)
            return self.health_template()

    def get_json_format(self, d):
        """
        Given some data, it gets its json format.
        :param d: Data to be formatted.
        :return: The formatted data in JSON.
        """
        return json.dumps(d)

    def getDepartments(self):
        """
        It obtains the different departments
        :return: A list with the department names and UID's [(UID,Name),....]
        """
        dep = getToolByName(self.context, 'bika_setup_catalog')(portal_type='Department')
        l = []
        for i in dep:
            l.append((i.UID, i.Title))

        return l

    def categoryInDepartment(self, category, department):
        """
        It checks if the category belongs to the department
        :param category: The category UID
        :param department: The department UID
        :return: True or False
        """
        obj = getToolByName(self.context, 'bika_setup_catalog')(UID=category)
        if obj:
            return obj[0].getObject().getDepartment().UID() == department
        else:
            return False

    def getAvailableServices(self, categoryuid):
        """ Return a list of services brains
        """
        bsc = getToolByName(self.context, 'bika_setup_catalog')
        services = bsc(portal_type='AnalysisService', sort_on='sortable_title', inactive_state='active', getCategoryUID=categoryuid)
        return services