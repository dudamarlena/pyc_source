# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mailman/interfaces.py
# Compiled at: 2008-10-06 10:31:17
""" iccommunity.mailman interfaces.
"""
from zope import schema
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty
from iccommunity.mailman.i18n import _

class IicCommunitySite(Interface):
    """
        """
    __module__ = __name__


class IicCommunityManagementMailman(Interface):
    """
        """
    __module__ = __name__
    host = schema.ASCIILine(title=_('URI'), required=False, description=_('Host of the LDAP server with mailman entry (ldap://ldap.host.com/),or files where mailman exists (file:///usr/lib/mailman).'))
    available_lists = schema.List(title=_('Available Lists'), required=False, default=[], description=_('Available Lists'), value_type=schema.Choice(vocabulary='iccommunity.mailman.lists'))


class IicCommunityMailmanUserLists(Interface):
    """
        """
    __module__ = __name__
    subscribed_lists = schema.List(title=_('Subscribed Lists'), required=False, default=[], description=_('Subscribed Lists'), value_type=schema.Choice(vocabulary='iccommunity.mailman.available_lists'))


class IicCommunityMailman(Interface):
    """
        """
    __module__ = __name__

    def get_lists(self):
        """
                Retorna las listas del mailman.

                        @rtype: list
                        @return: Listas del mailman.
                """
        pass

    def get_members(self, listname):
        """
                Retorna los miembros de una lista

                        @listname: List name
                        @return: List of members
                """
        pass

    def get_listbyGroups(self, groups):
        """
                Retorna las listas del mailman asociadas a cada grupo.

                        @type groups: list
                        @param groups: La lista de grupos.

                        @rtype: list
                        @return: Listas del mailman asociadas a cada grupo.
                """
        pass

    def set_listbyGroups(self, groups, lists):
        """
                Define las listas de un grupo.

                        @type groups: list
                        @param groups: La lista de grupos.
                        @type lists: list
                        @param lists: Las listas.

                        @rtype: None
                """
        pass

    def set_host(self, host):
        """
                Setea el origen del mailman. host puede ser None (Usar el mailman local) o un PloneLdap?.

                        @type host: object
                        @param host: Host del mailman.

                        @rtype: None
                """
        pass

    def subscribed_lists(self, member):
        """
                Return lists where member is subscribed

                        @member: Plone member
                        @return: List of mailman lists
                """
        pass

    def subscribe(self, member, listname, password=None, digest=False, ack=0, admin_notif=0, text=None, whence='icCommunity.mailman'):
        """
                Inscribe un miembro a una lista.

                        @member: Plone member
                        @listname: Mailman list name
                        @password: Password for mailman administration. None mean random password.
                        @digest: Accept digest mail
                        @ack: flag specifies user should get an acknowledgement of subscription.
                        @admin_notif: flag specifies admin notify.
                        @text: text to append to ack
                        @whence: from the modification was made.

                        @return: Listas del mailman.
                """
        pass

    def unsubscribe(self, member, listname, admin_notif=0, ack=0, whence='icCommunity.mailman'):
        """
                Desuscribe un miembro a una lista.

                        @member: Plone member
                        @listname: Mailman list name
                        @password: Password for mailman administration. None mean random password.
                        @digest: Accept digest mail
                        @ack: flag specifies user should get an acknowledgement of subscription.
                        @admin_notif: flag specifies admin notify.
                        @text: text to append to ack
                        @whence: from the modification was made.

                        @return: Listas del mailman.
                """
        pass