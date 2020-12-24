# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/repoze/what/plugins/x509/predicates.py
# Compiled at: 2012-03-22 17:57:39
"""
This module contains all the predicates related to x.509 authorization.
"""
from repoze.what.predicates import Predicate
from repoze.who.plugins.x509.utils import *
import re
__all__ = [
 'is_subject', 'is_issuer', 'X509Predicate', 'X509DNPredicate']

class X509Predicate(Predicate):
    """
    Represents a predicate based on the X.509 protocol. It can be evaluated,
    although it can only check that is a valid client certificate.

    Users must use a subclass or inherit from it.
    """

    def __init__(self, **kwargs):
        """

        :param verify_key: The WSGI environment key that specify if the client
            certificate is valid or not. A value of 'SUCCESS' will make it
            valid. If you don't specify a key, then the value that it will take
            is by default ``SSL_CLIENT_VERIFY``
        :param validity_start_key: The WSGI environment key that specifies the
            encoded datetime that indicates the start of the validity range.
            If the timezone is not UTC (or GMT), it will fail.
        :param validity_end_key: The WSGI environment key that specifies the
            encoded datetime that indicates the end of the validity range.
            If the timezone is not UTC (or GMT), it will fail.
        """
        self.verify_key = kwargs.pop('verify_key', None) or VERIFY_KEY
        self.validity_start_key = kwargs.pop('validity_start_key', None) or VALIDITY_START_KEY
        self.validity_end_key = kwargs.pop('validity_end_key', None) or VALIDITY_END_KEY
        super(X509Predicate, self).__init__(msg=kwargs.get('msg'))
        return

    def evaluate(self, environ, credentials):
        """
        Evaluates the predicate. A subclass should override this method however
        call it before doing its custom code.

        :param environ: The WSGI environment.
        :param credentials: The user credentials. These will not be used

        :raise NotAuthorizedError: If the predicate is not met.
        """
        if not verify_certificate(environ, self.verify_key, self.validity_start_key, self.validity_end_key):
            self.unmet()


class X509DNPredicate(X509Predicate):
    """
    Represents a predicate that evaluates a distinguished name encoded in a
    OpenSSL X.509 DN string. It evaluates according to the properties
    specified.
    """

    def __init__(self, common_name=None, organization=None, organizational_unit=None, country=None, state=None, locality=None, environ_key=None, **kwargs):
        """
        :param common_name: The common name of the distinguished name.
        :param organization: The organization of the distinguished name.
        :param organizational_unit: The organization unit of the distinguished
            name.
        :param country: ISO-3166-1 alpha-2 encoding of the country of the
            distinguished name.
        :param state: The state within the country of the distinguished name.
        :param locality: The locality or city of the distinguished name.
        :param environ_key: The WSGI environment key of where the distinguished
            name is located.
        :param kwargs: You can specify a custom attribute type. The name of the
            key will count as the type, and the value is what is going to be
            checked against.

        :raise ValueError: When you don't specify at least one value for the
            parameters, including any custom one; or, when you don't specify an
            ``environ_key``.
        """
        if common_name is None and organizational_unit is None and organization is None and country is None and state is None and locality is None and len(kwargs) == 0:
            raise ValueError('At least one of common_name, organizational_unit, organization, country, state, locality, or one custom parameter must have a value')
        super(X509DNPredicate, self).__init__(**kwargs)
        field_and_values = (
         (
          'O', organization, 'organization'),
         (
          'CN', common_name, 'common_name'),
         (
          'OU', organizational_unit, 'organizational_unit'),
         (
          'C', country, 'country'),
         (
          'ST', state, 'state'),
         (
          'L', locality, 'locality'))
        self.log = kwargs.get('log')
        self._prepare_dn_params_with_consistency(field_and_values, kwargs)
        if environ_key is None or len(environ_key) == 0:
            raise ValueError('This predicate requires a WSGI environ key')
        self.environ_key = environ_key
        return

    def _prepare_dn_params_with_consistency(self, check_params, kwargs):
        self.dn_params = []
        for param in check_params:
            if param[0] in kwargs and param[1] is not None:
                self.log and self.log.warn('Choosing %s over "%s"' % (param[0], param[1]))
                del kwargs[param[0]]
            if param[1] is not None:
                self.dn_params.append((param[0], param[1]))

        for param in ('validity_start_key', 'validity_end_key', 'verify_key'):
            try:
                del kwargs[param]
            except:
                pass

        self.dn_params.extend(kwargs.iteritems())
        return

    def evaluate(self, environ, credentials):
        """
        Evaluates a distinguished name or the server variables that represents
        it, already parsed. First it checks for the server variables, and then
        it tries to parse the distinguished name. See the documentation for
        more information.
        
        :param environ: The WSGI environment.
        :param credentials: The user credentials. This parameter is not used.

        :raise NotAuthorizedError: When the evaluation fails.
        """
        super(X509DNPredicate, self).evaluate(environ, credentials)
        try:
            for (suffix, value) in self.dn_params:
                self._check_server_variable(environ, '_' + suffix, value)

        except KeyError:
            pass
        else:
            return

        dn = environ.get(self.environ_key)
        if dn is None:
            self.unmet()
        try:
            parsed_dn = parse_dn(dn)
        except:
            self.unmet()

        try:
            for (key, value) in self.dn_params:
                self._check_parsed_dict(parsed_dn, key, value)

        except KeyError:
            self.unmet()

        return

    def _check_parsed_dict(self, parsed, key, value):
        parsed_value = parsed[key]
        if isinstance(value, list) or isinstance(value, tuple):
            for v in value:
                if v not in parsed_value:
                    self.unmet()

        if value not in parsed_value:
            self.unmet()

    def _check_server_variable(self, environ, suffix, value):
        key = self.environ_key + suffix
        if isinstance(value, list) or isinstance(value, tuple):
            environ_values = []
            for n in range(len(value)):
                environ_values.append(environ[(key + '_' + str(n))])

            for v in value:
                if v not in environ_values:
                    self.unmet()

        if environ[key] != value:
            self.unmet()


class is_issuer(X509DNPredicate):
    """
    Represents a predicate that evaluates the issuer distinguished name.
    """
    ISSUER_KEY_DN = 'SSL_CLIENT_I_DN'
    message = 'Invalid SSL client issuer.'

    def __init__(self, common_name=None, organization=None, organizational_unit=None, country=None, state=None, locality=None, issuer_key=None, **kwargs):
        super(is_issuer, self).__init__(common_name, organization, organizational_unit, country, state, locality, (issuer_key or self.ISSUER_KEY_DN), **kwargs)


class is_subject(X509DNPredicate):
    """
    Represents a predicate that evalutes the subject distinguished name.
    """
    SUBJECT_KEY_DN = 'SSL_CLIENT_S_DN'
    message = 'Invalid SSL client subject.'

    def __init__(self, common_name=None, organization=None, organizational_unit=None, country=None, state=None, locality=None, subject_key=None, **kwargs):
        super(is_subject, self).__init__(common_name, organization, organizational_unit, country, state, locality, (subject_key or self.SUBJECT_KEY_DN), **kwargs)