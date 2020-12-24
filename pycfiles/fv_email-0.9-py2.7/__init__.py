# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/fv_email/__init__.py
# Compiled at: 2013-09-25 23:04:46
import formencode, formencode.validators, socket, re
from encodings import idna
_ = lambda s: s
try:
    import dns.resolver, dns.exception
    have_dns = True
except ImportError:
    have_dns = False

class Email(formencode.validators.Email):
    usernameRE = re.compile('^[^\'";:,\\t\\n\\r@<>()\\[\\]]+$', re.I)
    predomainRE = re.compile('^\\.|\\.\\.|\\.$|\\w{64,}', re.I)
    messages = {'multipleAt': _('The email address may not contain more than one @')}

    def __init__(self, *args, **kw):
        global have_dns
        formencode.FancyValidator.__init__(self, *args, **kw)
        if self.resolve_domain:
            if not have_dns:
                import warnings
                warnings.warn('dnspython <http://www.dnspython.org/> is not installed on your system (or the dns.resolver package cannot be found). I cannot resolve domain names in addresses.  The resolve_domain setting has been set to False.')
                self.resolve_domain = False

    def validate_python(self, value, state):
        if not value:
            raise formencode.Invalid(self.message('empty', state), value, state)
        split = value.split('@')
        if len(split) > 2:
            raise formencode.Invalid(self.message('multipleAt', state), value, state)
        if len(split) < 2:
            raise formencode.Invalid(self.message('noAt', state), value, state)
        username, domain = split
        if not self.usernameRE.search(username):
            raise formencode.Invalid(self.message('badUsername', state, username=username), value, state)
        if self.predomainRE.search(domain) or not domain.strip():
            raise formencode.Invalid(self.message('badDomain', state, domain=domain), value, state)
        idna_domain = ('.').join([ idna.ToASCII(l) for l in domain.split('.') ])
        if not self.domainRE.search(idna_domain):
            raise formencode.Invalid(self.message('badDomain', state, domain=domain), value, state)
        if self.resolve_domain:
            assert have_dns, 'dnspython should be available'
            try:
                try:
                    a = dns.resolver.query(domain, 'MX')
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as e:
                    try:
                        a = dns.resolver.query(domain, 'A')
                    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as e:
                        raise formencode.Invalid(self.message('domainDoesNotExist', state, domain=domain), value, state)

            except (socket.error, dns.exception.DNSException) as e:
                raise formencode.Invalid(self.message('socketError', state, error=e), value, state)

    def _to_python(self, value, state):
        return re.sub(re.compile('\\s', re.UNICODE), '', value)