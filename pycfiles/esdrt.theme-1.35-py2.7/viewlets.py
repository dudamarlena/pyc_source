# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/theme/browser/viewlets.py
# Compiled at: 2019-05-21 05:08:56
from plone import api
from plone.app.layout.viewlets import common
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class LogoViewlet(common.LogoViewlet):
    index = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet, self).update()


class FooterViewlet(common.FooterViewlet):
    index = ViewPageTemplateFile('templates/footer.pt')

    def update(self):
        super(FooterViewlet, self).update()


class PersonalBarViewlet(common.PersonalBarViewlet):
    index = ViewPageTemplateFile('templates/personal_bar.pt')

    def update(self):
        super(PersonalBarViewlet, self).update()
        self.about = ('/').join([self.portal_state.navigation_root_url(), 'info'])
        self.help = ('/').join([self.portal_state.navigation_root_url(), 'help'])
        self.logout = ('/').join([self.portal_state.navigation_root_url(), 'logout'])
        if hasattr(self, 'user_name'):
            self.user_roles = self.get_groupnames()

    def get_groupnames(self):
        groupnames = {}
        user = api.user.get_current()
        groups = user.getGroups()
        sector_review_roles = []
        quality_expert_roles = []
        review_expert_roles = []
        lead_review_roles = []
        ms_coordinator_roles = []
        ms_expert_roles = []
        for group in groups:
            if group.startswith('extranet-esd-ghginv-sr-'):
                new_name = group.replace('extranet-esd-ghginv-sr-', '')
                splitted_name = new_name.split('-')
                if len(splitted_name) == 2:
                    sector_review_roles.append('%s - %s' % (
                     self.get_country_name(splitted_name[1]), splitted_name[0]))
            elif group.startswith('extranet-esd-ghginv-qualityexpert-'):
                new_name = group.replace('extranet-esd-ghginv-qualityexpert-', '')
                if new_name.strip():
                    quality_expert_roles.append('%s' % new_name)
            elif group.startswith('extranet-esd-esdreview-reviewexp-'):
                new_name = group.replace('extranet-esd-esdreview-reviewexp-', '')
                splitted_name = new_name.split('-')
                if len(splitted_name) == 2:
                    review_expert_roles.append('%s - %s' % (
                     splitted_name[0], self.get_country_name(splitted_name[1])))
            elif group.startswith('extranet-esd-esdreview-leadreview-'):
                new_name = group.replace('extranet-esd-esdreview-leadreview-', '')
                if new_name.strip():
                    lead_review_roles.append('%s' % self.get_country_name(new_name))
            elif group.startswith('extranet-esd-countries-msa-'):
                new_name = group.replace('extranet-esd-countries-msa-', '')
                if new_name.strip():
                    ms_coordinator_roles.append('%s' % self.get_country_name(new_name))
            elif group.startswith('extranet-esd-countries-msexpert-'):
                new_name = group.replace('extranet-esd-countries-msexpert-', '')
                if new_name.strip():
                    ms_expert_roles.append('%s' % self.get_country_name(new_name))

        sector_review_roles.sort()
        groupnames['sector_review_roles'] = sector_review_roles
        quality_expert_roles.sort()
        groupnames['quality_expert_roles'] = quality_expert_roles
        review_expert_roles.sort()
        groupnames['review_expert_roles'] = review_expert_roles
        lead_review_roles.sort()
        groupnames['lead_review_roles'] = lead_review_roles
        ms_coordinator_roles.sort()
        groupnames['ms_coordinator_roles'] = ms_coordinator_roles
        ms_expert_roles.sort()
        groupnames['ms_expert_roles'] = ms_expert_roles
        return groupnames

    def get_country_name(self, countryCode):
        if countryCode == 'at':
            return 'Austria'
        else:
            if countryCode == 'be':
                return 'Belgium'
            if countryCode == 'bg':
                return 'Bulgaria'
            if countryCode == 'hr':
                return 'Croatia'
            if countryCode == 'cy':
                return 'Cyprus'
            if countryCode == 'cz':
                return 'Czech Republic'
            if countryCode == 'dk':
                return 'Denmark'
            if countryCode == 'ee':
                return 'Estonia'
            if countryCode == 'fi':
                return 'Finland'
            if countryCode == 'fr':
                return 'France'
            if countryCode == 'de':
                return 'Germany'
            if countryCode == 'gr':
                return 'Greece'
            if countryCode == 'hu':
                return 'Hungary'
            if countryCode == 'is':
                return 'Iceland'
            if countryCode == 'ie':
                return 'Ireland'
            if countryCode == 'it':
                return 'Italy'
            if countryCode == 'lv':
                return 'Latvia'
            if countryCode == 'lt':
                return 'Lithuania'
            if countryCode == 'lu':
                return 'Luxembourg'
            if countryCode == 'mt':
                return 'Malta'
            if countryCode == 'nl':
                return 'Netherlands'
            if countryCode == 'pl':
                return 'Poland'
            if countryCode == 'pt':
                return 'Portugal'
            if countryCode == 'ro':
                return 'Romania'
            if countryCode == 'sk':
                return 'Slovakia'
            if countryCode == 'sl':
                return 'Slovania'
            if countryCode == 'es':
                return 'Spain'
            if countryCode == 'se':
                return 'Sweden'
            if countryCode == 'gb':
                return 'United Kingdom'
            return countryCode