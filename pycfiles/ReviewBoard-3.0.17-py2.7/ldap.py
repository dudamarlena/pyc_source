# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/backends/ldap.py
# Compiled at: 2020-02-11 04:03:56
"""LDAP authentication backend."""
from __future__ import absolute_import, unicode_literals
import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import six
from django.utils.translation import ugettext_lazy as _
try:
    import ldap
except ImportError:
    ldap = None

from reviewboard.accounts.backends.base import BaseAuthBackend
from reviewboard.accounts.forms.auth import LDAPSettingsForm

class LDAPBackend(BaseAuthBackend):
    """Authentication backend for LDAP servers.

    This allows the use of LDAP servers for authenticating users in Review
    Board, and for importing individual users on-demand. It allows for a lot of
    customization in terms of how the LDAP server is queried, providing
    compatibility with most open source and commercial LDAP servers.

    The following Django settings are supported:

    ``LDAP_ANON_BIND_UID``:
        The full DN (distinguished name) of a user account with
        sufficient access to perform lookups of users and groups in the LDAP
        server. This is treated as a general or "anonymous" user for servers
        requiring authentication, and will not be otherwise imported into the
        Review Board server (unless attempting to log in with the same name).

        This can be unset if the LDAP server supports actual anonymous binds
        without a DN.

    ``LDAP_ANON_BIND_PASSWD``:
        The password used for the account specified in ``LDAP_ANON_BIND_UID``.

    ``LDAP_ANON_BIND_UID``:
        The full distinguished name of a user account with sufficient access
        to perform lookups of users and groups in the LDAP server. This can
        be unset if the LDAP server supports anonymous binds.

    ``LDAP_BASE_DN``:
        The base DN (distinguished name) used to perform LDAP searches.

    ``LDAP_EMAIL_ATTRIBUTE``:
        The attribute designating the e-mail address of a user in the
        directory. E-mail attributes are only used if this is set and if
        ``LDAP_EMAIL_DOMAIN`` is not set.

    ``LDAP_EMAIL_DOMAIN``:
        The domain name to use for e-mail addresses. If set, users imported
        from LDAP will have an e-mail address in the form of
        :samp:`{username}@{LDAP_EMAIL_DOMAIN}`. This takes priority over
        ``LDAP_EMAIL_ATTRIBUTE``.

    ``LDAP_GIVEN_NAME_ATTRIBUTE``:
        The attribute designating the given name (or first name) of a user
        in the directory. This defaults to ``givenName`` if not provided.

    ``LDAP_SURNAME_ATTRIBUTE``:
        The attribute designating the surname (or last name) of a user in the
        directory. This defaults to ``sn`` if not provided.

    ``LDAP_TLS``:
        Whether to use TLS to communicate with the LDAP server.

    ``LDAP_UID``:
        The attribute indicating a user's unique ID in the directory. This
        is used to compute a user lookup filter in the format of
        :samp:`({LDAP_UID}={username})`.

    ``LDAP_UID_MASK``:
        A mask defining a filter for looking up users. This must contain
        ``%s`` somewhere in the string, representing the username.
        For example: ``(something_special=%s)``.

    ``LDAP_URI``:
        The URI to the LDAP server to connect to for all communication.
    """
    backend_id = b'ldap'
    name = _(b'LDAP')
    settings_form = LDAPSettingsForm
    login_instructions = _(b'Use your standard LDAP username and password.')

    def authenticate(self, username, password, **kwargs):
        """Authenticate a user.

        This will attempt to authenticate the user against the LDAP server.
        If the username and password are valid, a
        :py:class:`~django.contrib.auth.models.User` will be returned, and
        added to the database if it doesn't already exist.

        Args:
            username (unicode):
                The username used to authenticate.

            password (unicode):
                The password used to authenticate.

        Returns:
            django.contrib.auth.models.User:
            The resulting user, if authentication was successful. If
            unsuccessful, ``None`` is returned.
        """
        username = username.strip()
        if not password:
            logging.warning(b'Attempted to authenticate "%s" with an empty password against LDAP.', username)
            return
        else:
            ldapo = self._connect()
            if ldapo is None:
                return
            if isinstance(username, six.text_type):
                username_bytes = username.encode(b'utf-8')
            else:
                username_bytes = username
            if isinstance(password, six.text_type):
                password = password.encode(b'utf-8')
            userdn = self._get_user_dn(ldapo, username)
            try:
                logging.debug(b'Attempting to authenticate user DN "%s" (username %s) in LDAP', userdn.decode(b'utf-8'), username)
                ldapo.bind_s(userdn, password)
                return self.get_or_create_user(username=username_bytes, ldapo=ldapo, userdn=userdn)
            except ldap.INVALID_CREDENTIALS:
                logging.warning(b'Error authenticating user "%s" in LDAP: The credentials provided were invalid', username)
            except ldap.LDAPError as e:
                logging.warning(b'Error authenticating user "%s" in LDAP: %s', username, e)
            except Exception as e:
                logging.exception(b'Unexpected error authenticating user "%s" in LDAP: %s', username, e)

            return

    def get_or_create_user(self, username, request=None, ldapo=None, userdn=None):
        """Return a user account, importing from LDAP if necessary.

        If the user already exists in the database, it will be returned
        directly. Otherwise, this will attempt to look up the user in LDAP
        and create a local user account representing that user.

        Args:
            username (unicode):
                The username to look up.

            request (django.http.HttpRequest, optional):
                The optional HTTP request for this operation.

            ldapo (ldap.LDAPObject, optional):
                The existing LDAP connection, if the caller has one. If not
                provided, a new connection will be created.

            userdn (unicode, optional):
                The DN for the user being looked up, if the caller knows it.
                If not provided, the DN will be looked up.

        Returns:
            django.contrib.auth.models.User:
            The resulting user, if it could be found either locally or in
            LDAP. If the user does not exist, ``None`` is returned.
        """
        username = self.INVALID_USERNAME_CHAR_REGEX.sub(b'', username).lower()
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            pass

        if ldap is None:
            logging.error(b'Attempted to look up user "%s" in LDAP, but the python-ldap package is not installed!', username)
            return
        else:
            try:
                if ldapo is None:
                    ldapo = self._connect(request=request)
                    if ldapo is None:
                        return
                if userdn is None:
                    userdn = self._get_user_dn(ldapo=ldapo, username=username, request=request)
                    if userdn is None:
                        return
                search_result = ldapo.search_s(userdn, ldap.SCOPE_BASE)
                user_info = search_result[0][1]
                given_name_attr = getattr(settings, b'LDAP_GIVEN_NAME_ATTRIBUTE', b'givenName')
                first_name = user_info.get(given_name_attr, [username])[0]
                surname_attr = getattr(settings, b'LDAP_SURNAME_ATTRIBUTE', b'sn')
                last_name = user_info.get(surname_attr, [b''])[0]
                try:
                    if settings.LDAP_FULL_NAME_ATTRIBUTE:
                        full_name = user_info[settings.LDAP_FULL_NAME_ATTRIBUTE][0]
                        full_name = full_name.decode(b'utf-8')
                        try:
                            first_name, last_name = full_name.split(b' ', 1)
                        except ValueError:
                            first_name = full_name
                            last_name = b''

                except AttributeError:
                    pass

                if settings.LDAP_EMAIL_DOMAIN:
                    email = b'%s@%s' % (username, settings.LDAP_EMAIL_DOMAIN)
                elif settings.LDAP_EMAIL_ATTRIBUTE:
                    try:
                        email = user_info[settings.LDAP_EMAIL_ATTRIBUTE][0]
                    except KeyError:
                        logging.error(b'LDAP: could not get e-mail address for user %s using attribute %s', username, settings.LDAP_EMAIL_ATTRIBUTE)
                        email = b''

                else:
                    logging.warning(b'LDAP: e-mail for user %s is not specified', username)
                    email = b''
                user = User(username=username, password=b'', first_name=first_name, last_name=last_name, email=email)
                user.set_unusable_password()
                user.save()
                return user
            except ldap.NO_SUCH_OBJECT as e:
                logging.warning(b'LDAP error: %s settings.LDAP_BASE_DN: %s User DN: %s', e, settings.LDAP_BASE_DN, userdn, exc_info=1)
            except ldap.LDAPError as e:
                logging.warning(b'LDAP error: %s', e, exc_info=1)

            return

    def _connect(self, request=None):
        """Connect to LDAP.

        This will attempt to connect and authenticate (if needed) to the
        configured LDAP server.

        Args:
            request (django.http.HttpRequest, optional):
                The optional HTTP request used for logging context.

        Returns:
            ldap.LDAPObject:
            The resulting LDAP connection, if it could connect. If LDAP
            support isn't available, or there was an error, this will return
            ``None``.
        """
        if ldap is None:
            return
        else:
            try:
                ldapo = ldap.initialize(settings.LDAP_URI)
                ldapo.set_option(ldap.OPT_REFERRALS, 0)
                ldapo.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                if settings.LDAP_TLS:
                    ldapo.start_tls_s()
                if settings.LDAP_ANON_BIND_UID:
                    ldapo.simple_bind_s(settings.LDAP_ANON_BIND_UID, settings.LDAP_ANON_BIND_PASSWD)
                else:
                    ldapo.simple_bind_s()
                return ldapo
            except ldap.INVALID_CREDENTIALS:
                if settings.LDAP_ANON_BIND_UID:
                    logging.warning(b'Error authenticating with LDAP: The credentials provided for "%s" were invalid.', settings.LDAP_ANON_BIND_UID, request=request)
                else:
                    logging.warning(b'Error authenticating with LDAP: Anonymous access to this server is not permitted.', request=request)
            except ldap.LDAPError as e:
                logging.warning(b'Error authenticating with LDAP: %s', e, request=request)
            except Exception as e:
                logging.exception(b'Unexpected error occurred while authenticating with LDAP: %s', e, request=request)

            return

    def _get_user_dn(self, ldapo, username, request=None):
        """Return the DN for a given username.

        This will perform a lookup in LDAP to try to find a DN for a given
        username, which can be used in subsequent lookups and for
        authentication.

        Args:
            ldapo (ldap.LDAPObject):
                The LDAP connection.

            username (unicode):
                The username to look up in the directory.

            request (django.http.HttpRequest, optional):
                The optional HTTP request used for logging context.

        Returns:
            unicode:
            The DN for the username, if found. If not found, this will return
            ``None``.
        """
        assert ldapo is not None
        try:
            if settings.LDAP_UID_MASK:
                uidfilter = settings.LDAP_UID_MASK % username
            else:
                uidfilter = b'(%(userattr)s=%(username)s)' % {b'userattr': settings.LDAP_UID, 
                   b'username': username}
            search = ldapo.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, uidfilter)
            if search:
                return search[0][0]
            logging.warning(b'LDAP error: The specified object does not exist in the Directory: %s', username, request=request)
        except ldap.LDAPError as e:
            logging.warning(b'Error authenticating user "%s" in LDAP: %s', username, e, request=request)
        except Exception as e:
            logging.exception(b'Unexpected error authenticating user "%s" in LDAP: %s', username, e, request=request)

        return