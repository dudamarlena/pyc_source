# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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