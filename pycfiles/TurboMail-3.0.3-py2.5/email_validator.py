# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/email_validator.py
# Compiled at: 2009-08-26 20:45:28
"""A method of validating e-mail addresses and mail domains.

This module aims to provide the ultimate functions for:
* domain validation, and
* e-mail validation.

Why not just use a regular expression?
======================================
http://haacked.com/archive/2007/08/21/i-knew-how-to-validate-an-email-address-until-i.aspx

There are many regular expressions out there for this. The "perfect one" is
several KB long and therefore unmaintainable (Perl people wrote it...).

This is 2009 and domain rules are changing too. Impossible domain names have
become possible, international domain names are real...

So validating an e-mail address is more complex than you might think. Take a
look at some of the rules:
http://en.wikipedia.org/wiki/E-mail_address#RFC_specification

How to do it then?
==================
I believe the solution should combine simple regular expressions with
imperative programming.

E-mail validation is also dependent on the robustness principle:
"Be conservative in what you do, be liberal in what you accept from others."
http://en.wikipedia.org/wiki/Postel%27s_law

This module recognizes that e-mail validation can be done in several different
ways, according to purpose:

1) Most of the time you just want validation according to the standard rules.
So just say:  v = EmailValidator()

2) If you are creating e-mail addresses for your server or your organization,
you might need to satisfy a stricter policy such as "dash is not allowed in
email addresses". The EmailValidator constructor accepts a *local_part_chars*
argument to help build the right regular expression for you.
Example:  v = EmailValidator(local_part_chars='.-+_')

3) What about typos? An erroneous dot at the end of a typed email is typical.
Other common errors with the dots revolve around the @: user@.domain.com.
These typing mistakes can be automatically corrected, saving you from doing
it manually. For this you use the *fix* flag when instantiating a validator:

    d = DomainValidator(fix=True)
    domain, error_message = d.validate('.supercalifragilistic.com.br')
    if error_message:
        print 'Invalid domain: ' + domain
    else:
        print 'Valid domain: ' + domain

4) TODO: Squash the bugs in this feature!
Paranoid people may wish to verify that the informed domain actually exists.
For that you can pass a *lookup_dns='a'* argument to the constructor, or even
*lookup_dns='mx'* to verify that the domain actually has e-mail servers.
To use this feature, you need to install the *pydns* library:

     easy_install -UZ pydns

How to use
==========

The validating methods return a tuple (email, error_msg).
*email* is the trimmed and perhaps fixed email.
*error_msg* is an empty string when the e-mail is valid.

Typical usage is:

    v = EmailValidator() # or EmailValidator(fix=True)
    email = raw_input('Type an email: ')
    email, err = v.validate(email)
    if err:
        print 'Error: ' + err
    else:
        print 'E-mail is valid: ' + email  # the email, corrected

There is also an EmailHarvester class to collect e-mail addresses from any text.

Authors: Nando Florestan, Marco Ferreira
Code written in 2009 and donated to the public domain.
"""
import re
__all__ = [
 'BaseValidator', 'ValidationException', 'EmailValidator']

class ValidationException(ValueError):
    pass


class BaseValidator(object):

    def validate_or_raise(self, *a, **k):
        """Some people would condemn this whole module screaming:
        "Don't return success codes, use exceptions!"
        This method allows them to be happy, too.
        """
        (validatee, err) = self.validate(*a, **k)
        if err:
            raise ValidationException(err)
        else:
            return validatee


class DomainValidator(BaseValidator):
    """A domain name validator that is ready for internationalized domains.
    
    http://en.wikipedia.org/wiki/Internationalized_domain_name
    http://en.wikipedia.org/wiki/Top-level_domain
    """
    domain_pattern = '[\\w]+([\\w\\.\\-]+\\w)?'
    domain_regex = re.compile('^' + domain_pattern + '$', re.IGNORECASE | re.UNICODE)
    false_positive_ips = [
     '208.67.217.132']

    def __init__(self, fix=False, lookup_dns=None):
        self.fix = fix
        if lookup_dns:
            lookup_dns = lookup_dns.lower()
            if not lookup_dns == 'a' and not lookup_dns == 'mx':
                raise RuntimeError('Not a valid *lookup_dns* value: ' + lookup_dns)
        self._lookup_dns = lookup_dns

    def _apply_common_rules(self, part, maxlength):
        """This method contains the rules that must be applied to both the
        domain and the local part of the e-mail address.
        """
        part = part.strip()
        if self.fix:
            part = part.strip('.')
        if not part:
            return (
             part, 'It cannot be empty.')
        if len(part) > maxlength:
            return (
             part, 'It cannot be longer than %i chars.' % maxlength)
        if part[0] == '.':
            return (
             part, 'It cannot start with a dot.')
        if part[(-1)] == '.':
            return (
             part, 'It cannot end with a dot.')
        if '..' in part:
            return (
             part, 'It cannot contain consecutive dots.')
        return (
         part, '')

    def validate_domain(self, part):
        (part, err) = self._apply_common_rules(part, maxlength=255)
        if err:
            return (
             part, 'Invalid domain: %s' % err)
        if not self.domain_regex.search(part):
            return (
             part, 'Invalid domain.')
        if self._lookup_dns and not self.lookup_domain(part):
            return (
             part, 'Domain does not seem to exist.')
        else:
            return (
             part.lower(), '')

    validate = validate_domain

    def lookup_domain(self, domain, lookup_record=None):
        """Looks up the DNS record for *domain* and returns:
        
        * None if it does not exist,
        * The IP address if looking up the "A" record, or
        * The list of hosts in the "MX" record.
        
        The return value, if treated as a boolean, says whether a domain exists.
        
        You can pass "a" or "mx" as the *lookup_record* parameter. Otherwise,
        the *lookup_dns* parameter from the constructor is used.
        "a" means verify that the domain exists.
        "mx" means verify that the domain exists and specifies mail servers.
        """
        if lookup_record:
            lookup_record = lookup_record.lower()
        else:
            lookup_record = self._lookup_dns
        result = None
        if lookup_record == 'a':
            request = DNS.Request(domain)
            try:
                answers = request.req().answers
            except DNS.Lib.PackError, err:
                return False
            else:
                if answers:
                    result = answers[0]['data']
                    if result in self.false_positive_ips:
                        result = None
        elif lookup_record == 'mx':
            result = DNS.mxlookup(domain)
        else:
            raise RuntimeError('Not a valid lookup_record value: ' + lookup_record)
        return result


class EmailValidator(DomainValidator):

    def __init__(self, local_part_chars=".-+_!#$%&'/=`|~?^{}*", **k):
        super(EmailValidator, self).__init__(**k)
        self.local_part_pattern = '[a-z0-9' + local_part_chars.replace('-', '\\-') + ']+'
        self.local_part_regex = re.compile('^' + self.local_part_pattern + '$', re.IGNORECASE)

    def validate_local_part(self, part):
        (part, err) = self._apply_common_rules(part, maxlength=64)
        if err:
            return (
             part, 'Invalid local part: %s' % err)
        if not self.local_part_regex.search(part):
            return (
             part, 'Invalid local part.')
        return (
         part, '')

    def validate_email(self, email):
        if not email:
            return (
             email, 'The e-mail is empty.')
        parts = email.split('@')
        if len(parts) != 2:
            return (
             email, 'An email address must contain a single @')
        (local, domain) = parts
        (domain, err) = self.validate_domain(domain)
        if err:
            return (
             email,
             'The e-mail has a problem to the right of the @: %s' % err)
        (local, err) = self.validate_local_part(local)
        if err:
            return (
             email,
             'The email has a problem to the left of the @: %s' % err)
        return (local + '@' + domain, '')

    validate = validate_email


class EmailHarvester(EmailValidator):

    def __init__(self, *a, **k):
        super(EmailHarvester, self).__init__(*a, **k)
        self.harvest_regex = re.compile(self.local_part_pattern + '@' + self.domain_pattern, re.IGNORECASE | re.UNICODE)

    def harvest(self, text):
        """Iterator that yields the e-mail addresses contained in *text*."""
        for match in self.harvest_regex.finditer(text):
            yield match.group().replace('..', '.')


if __name__ == '__main__':
    d = DomainValidator()
    (domain, err) = d.validate('acentuaÃ§Ã£o.com')
    assert not err
    (domain, err) = d.validate('tld.Ã¡cÃ§Ãªnts')
    assert not err
    (domain, err) = d.validate('subdomain.subdomain.subdomain.sub.domain.tld')
    assert not err
    (domain, err) = d.validate('.com')
    assert err
    v = EmailValidator()
    (email, err) = v.validate('Dmitry.Shostakovich@great-music.com')
    assert not err
    (email, err) = v.validate('  ha@ha.ha  ')
    assert not err
    (email, err) = v.validate("a.a-a+a_a!a#a$a%a&a'a/a=a`a|a~a?a^a{a}a*a@special.chars")
    assert not err
    (email, err) = v.validate('user+mailbox@example.com')
    assert not err
    (email, err) = v.validate('customer/department=shipping@example.com')
    assert not err
    (email, err) = v.validate('$A12345@example.com')
    assert not err
    (email, err) = v.validate('!def!xyz%abc@example.com')
    assert not err
    (email, err) = v.validate('_somename@example.com')
    assert not err
    (email, err) = v.validate('Abc.example.com')
    assert err
    (email, err) = v.validate('A@b@example.com')
    assert err
    (email, err) = v.validate('Abc.@example.com')
    assert err
    (email, err) = v.validate('Abc..123@example.com')
    assert err
    (email, err) = v.validate('Ã£@example.com')
    assert err
    (email, err) = v.validate('\\@example.com')
    assert err
    v = EmailValidator(lookup_dns='a')
    while True:
        email = raw_input('Type an email or CTRL-C to quit: ').decode('utf8')
        (email, err) = v.validate(email)
        if err:
            print 'Error: ' + err
        else:
            print 'E-mail is valid: ' + email