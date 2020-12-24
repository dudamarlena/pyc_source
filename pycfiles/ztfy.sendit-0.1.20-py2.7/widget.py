# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/skin/packet/widget.py
# Compiled at: 2013-05-31 13:02:11
from ztfy.security.browser.widget.interfaces import IPrincipalListWidget
from ztfy.sendit.app.interfaces import ISenditApplication
from ztfy.sendit.profile.interfaces import IProfile
from z3c.form.widget import FieldWidget
from ztfy.security.browser.widget.principal import PrincipalListWidget
from ztfy.utils.traversing import getParent

class IPacketRecipientsWidget(IPrincipalListWidget):
    """Packet recipients widget interface"""

    def canRegisterUser(self):
        """Check if user can register new external users"""
        pass


class PacketRecipientsWidget(PrincipalListWidget):
    """Packet recipients widget"""
    query_name = 'findFilteredPrincipals'
    registration_view_name = 'register_user.html'

    def canRegisterUser(self):
        profile = IProfile(self.request.principal)
        name, _plugin, _info = profile.getAuthenticatorPlugin()
        if name is None:
            return False
        else:
            app = getParent(self.context, ISenditApplication)
            return app is not None and name in app.internal_auth_plugins


def PacketRecipientsWidgetFactory(field, request):
    return FieldWidget(field, PacketRecipientsWidget(request))