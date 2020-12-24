# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mailman/mailman.py
# Compiled at: 2008-10-06 10:31:17
import sys
from urlparse import urlparse
from zope.interface import implements
from zope.component import getAllUtilitiesRegisteredFor
from Products.CMFCore.utils import getToolByName
from interfaces import IicCommunityMailman
from i18n import _

class icCommunityMailmanBase(object):
    """
        """
    __module__ = __name__
    implements(IicCommunityMailman)

    def __init__(self, url_prefixes):
        self.url_prefixes = url_prefixes

    def get_lists(self):
        """
                Retorna las listas del mailman.

                        @rtype: list
                        @return: Listas del mailman.
                """
        return []

    def get_members(self, listname):
        """
                Retorna los miembros de una lista

                        @listname: List name
                        @return: List of members
                """
        return []

    def get_listsbyGroups(self, groups):
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
        url_parts = urlparse(host)
        if url_parts[0] not in self.url_prefixes:
            raise RuntimeError(_('Protocolo no soportado'))
        self.url_parts = url_parts

    def subscribed_lists(self, member):
        """
                Return lists where member is subscribed

                        @member: Plone member
                        @return: List of mailman lists
                """
        email = member.getProperty('email')
        lists = []
        for listname in self.get_lists():
            if email in self.get_members(listname):
                lists.append(listname)

        return lists

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


class icCommunityMailmanLocal(icCommunityMailmanBase):
    """
        """
    __module__ = __name__

    def set_host(self, host):
        super(icCommunityMailmanLocal, self).set_host(host)
        self.mailman_path = self.url_parts[2]
        try:
            sys.path.extend([self.mailman_path])
            import Mailman
        except:
            raise RuntimeError(_('Path no valido'))

    def get_lists(self):
        """
                Retorna las listas del mailman.

                        @rtype: list
                        @return: Listas del mailman.
                """
        try:
            from Mailman.Utils import list_names
            lists = list_names()
        except:
            raise RuntimeError(_('Path no valido'))

        return lists

    def get_members(self, listname):
        """
                Retorna los miembros de una lista

                        @listname: List name
                        @return: List of members
                """
        import pdb
        pdb.set_trace()
        try:
            from Mailman.MailList import MailList
        except:
            raise RuntimeError(_('Path no valido'))

        return MailList(listname).getMembers()

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
        try:
            from Mailman.MailList import MailList
            from Mailman.UserDesc import UserDesc
            from Mailman import Errors
        except:
            raise RuntimeError(_('Path no valido'))

        userdesc = UserDesc(email=member.getProperty('email'), fullname=member.getProperty('fullname'), password=password, digest=digest, lang=member.getProperty('language'))
        mlist = MailList(listname)
        try:
            mlist.ApprovedAddMember(userdesc, ack=ack, admin_notif=admin_notif, text=text, whence=whence)
        except Errors.MMAlreadyAMember:
            msg = _('Already a member: %(member)s')
        except Errors.MMBadEmailError:
            if userdesc.address == '':
                msg = _('Bad/Invalid email address: blank line')
            else:
                msg = _('Bad/Invalid email address: %(member)s')
        except Errors.MMHostileAddress:
            msg = _('Hostile address (illegal characters): %(member)s')
        else:
            msg = _('Subscribed: %(member)s')

        mlist.Save()

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
        try:
            from Mailman.MailList import MailList
            from Mailman import Errors
        except:
            raise RuntimeError(_('Path no valido'))

        mlist = MailList(listname)
        email = member.getProperty('email')
        mlist.ApprovedDeleteMember(email, whence=whence, admin_notif=admin_notif, ack=ack)
        mlist.Save()


class icCommunityMailmanLDAP(icCommunityMailmanBase):
    """
        """
    __module__ = __name__


class icCommunityMailmanTest(icCommunityMailmanBase):
    """
        """
    __module__ = __name__

    def get_lists(self):
        """
                Retorna las listas falsas.

                        @rtype: list
                        @return: Listas falsas.
                """
        return [
         'fake list', 'black hole list']


class icCommunityMailmanUtility(icCommunityMailmanBase):
    """
        """
    __module__ = __name__
    utility = None
    url_prefixes = []

    def __init__(self):
        pass

    def get_lists(self):
        """
                Retorna las listas del mailman.

                        @rtype: list
                        @return: Listas del mailman.
                """
        return self.utility.get_lists()

    def set_host(self, host):
        url_parts = urlparse(host)
        self.scheme = url_parts[0]
        utilities = getAllUtilitiesRegisteredFor(IicCommunityMailman)
        self.utility = None
        for utility in utilities:
            if self.scheme in utility.url_prefixes:
                self.utility = utility
                break

        if not self.utility:
            raise RuntimeError(_("Protocolo '%s' no soportado" % self.scheme))
        self.utility.set_host(host)
        return


local = icCommunityMailmanLocal(['local', 'file', ''])
ldap = icCommunityMailmanLDAP(['ldap', 'ldaps'])
test = icCommunityMailmanTest(['test'])