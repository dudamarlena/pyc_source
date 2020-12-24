# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/p10userdata/adapter.py
# Compiled at: 2011-10-06 05:46:39
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """

    def get_firstname(self):
        return self.context.getProperty('firstname', '')

    def set_firstname(self, value):
        return self.context.setMemberProperties({'firstname': value})

    firstname = property(get_firstname, set_firstname)

    def get_lastname(self):
        return self.context.getProperty('lastname', '')

    def set_lastname(self, value):
        return self.context.setMemberProperties({'lastname': value})

    lastname = property(get_lastname, set_lastname)

    def get_school(self):
        return self.context.getProperty('school', '')

    def set_school(self, value):
        return self.context.setMemberProperties({'school': value})

    school = property(get_school, set_school)

    def get_reference(self):
        return self.context.getProperty('reference', '')

    def set_reference(self, value):
        return self.context.setMemberProperties({'reference': value})

    reference = property(get_reference, set_reference)