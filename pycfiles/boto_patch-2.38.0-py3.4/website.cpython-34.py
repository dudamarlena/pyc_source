# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/website.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 10607 bytes


def tag(key, value):
    start = '<%s>' % key
    end = '</%s>' % key
    return '%s%s%s' % (start, value, end)


class WebsiteConfiguration(object):
    __doc__ = '\n    Website configuration for a bucket.\n\n    :ivar suffix: Suffix that is appended to a request that is for a\n        "directory" on the website endpoint (e.g. if the suffix is\n        index.html and you make a request to samplebucket/images/\n        the data that is returned will be for the object with the\n        key name images/index.html).  The suffix must not be empty\n        and must not include a slash character.\n\n    :ivar error_key: The object key name to use when a 4xx class error\n        occurs.  This key identifies the page that is returned when\n        such an error occurs.\n\n    :ivar redirect_all_requests_to: Describes the redirect behavior for every\n        request to this bucket\'s website endpoint. If this value is non None,\n        no other values are considered when configuring the website\n        configuration for the bucket. This is an instance of\n        ``RedirectLocation``.\n\n    :ivar routing_rules: ``RoutingRules`` object which specifies conditions\n        and redirects that apply when the conditions are met.\n\n    '

    def __init__(self, suffix=None, error_key=None, redirect_all_requests_to=None, routing_rules=None):
        self.suffix = suffix
        self.error_key = error_key
        self.redirect_all_requests_to = redirect_all_requests_to
        if routing_rules is not None:
            self.routing_rules = routing_rules
        else:
            self.routing_rules = RoutingRules()

    def startElement(self, name, attrs, connection):
        if name == 'RoutingRules':
            self.routing_rules = RoutingRules()
            return self.routing_rules
        if name == 'IndexDocument':
            return _XMLKeyValue([('Suffix', 'suffix')], container=self)
        if name == 'ErrorDocument':
            return _XMLKeyValue([('Key', 'error_key')], container=self)

    def endElement(self, name, value, connection):
        pass

    def to_xml(self):
        parts = [
         '<?xml version="1.0" encoding="UTF-8"?>',
         '<WebsiteConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">']
        if self.suffix is not None:
            parts.append(tag('IndexDocument', tag('Suffix', self.suffix)))
        if self.error_key is not None:
            parts.append(tag('ErrorDocument', tag('Key', self.error_key)))
        if self.redirect_all_requests_to is not None:
            parts.append(self.redirect_all_requests_to.to_xml())
        if self.routing_rules:
            parts.append(self.routing_rules.to_xml())
        parts.append('</WebsiteConfiguration>')
        return ''.join(parts)


class _XMLKeyValue(object):

    def __init__(self, translator, container=None):
        self.translator = translator
        if container:
            self.container = container
        else:
            self.container = self

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        for xml_key, attr_name in self.translator:
            if name == xml_key:
                setattr(self.container, attr_name, value)
                continue

    def to_xml(self):
        parts = []
        for xml_key, attr_name in self.translator:
            content = getattr(self.container, attr_name)
            if content is not None:
                parts.append(tag(xml_key, content))
                continue

        return ''.join(parts)


class RedirectLocation(_XMLKeyValue):
    __doc__ = "Specify redirect behavior for every request to a bucket's endpoint.\n\n    :ivar hostname: Name of the host where requests will be redirected.\n\n    :ivar protocol: Protocol to use (http, https) when redirecting requests.\n        The default is the protocol that is used in the original request.\n\n    "
    TRANSLATOR = [('HostName', 'hostname'),
     ('Protocol', 'protocol')]

    def __init__(self, hostname=None, protocol=None):
        self.hostname = hostname
        self.protocol = protocol
        super(RedirectLocation, self).__init__(self.TRANSLATOR)

    def to_xml(self):
        return tag('RedirectAllRequestsTo', super(RedirectLocation, self).to_xml())


class RoutingRules(list):

    def add_rule(self, rule):
        """

        :type rule: :class:`boto.s3.website.RoutingRule`
        :param rule: A routing rule.

        :return: This ``RoutingRules`` object is returned,
            so that it can chain subsequent calls.

        """
        self.append(rule)
        return self

    def startElement(self, name, attrs, connection):
        if name == 'RoutingRule':
            rule = RoutingRule(Condition(), Redirect())
            self.add_rule(rule)
            return rule

    def endElement(self, name, value, connection):
        pass

    def __repr__(self):
        return 'RoutingRules(%s)' % super(RoutingRules, self).__repr__()

    def to_xml(self):
        inner_text = []
        for rule in self:
            inner_text.append(rule.to_xml())

        return tag('RoutingRules', '\n'.join(inner_text))


class RoutingRule(object):
    __doc__ = "Represents a single routing rule.\n\n    There are convenience methods to making creating rules\n    more concise::\n\n        rule = RoutingRule.when(key_prefix='foo/').then_redirect('example.com')\n\n    :ivar condition: Describes condition that must be met for the\n        specified redirect to apply.\n\n    :ivar redirect: Specifies redirect behavior.  You can redirect requests to\n        another host, to another page, or with another protocol. In the event\n        of an error, you can can specify a different error code to return.\n\n    "

    def __init__(self, condition=None, redirect=None):
        self.condition = condition
        self.redirect = redirect

    def startElement(self, name, attrs, connection):
        if name == 'Condition':
            return self.condition
        if name == 'Redirect':
            return self.redirect

    def endElement(self, name, value, connection):
        pass

    def to_xml(self):
        parts = []
        if self.condition:
            parts.append(self.condition.to_xml())
        if self.redirect:
            parts.append(self.redirect.to_xml())
        return tag('RoutingRule', '\n'.join(parts))

    @classmethod
    def when(cls, key_prefix=None, http_error_code=None):
        return cls(Condition(key_prefix=key_prefix, http_error_code=http_error_code), None)

    def then_redirect(self, hostname=None, protocol=None, replace_key=None, replace_key_prefix=None, http_redirect_code=None):
        self.redirect = Redirect(hostname=hostname, protocol=protocol, replace_key=replace_key, replace_key_prefix=replace_key_prefix, http_redirect_code=http_redirect_code)
        return self


class Condition(_XMLKeyValue):
    __doc__ = '\n    :ivar key_prefix: The object key name prefix when the redirect is applied.\n        For example, to redirect requests for ExamplePage.html, the key prefix\n        will be ExamplePage.html. To redirect request for all pages with the\n        prefix docs/, the key prefix will be /docs, which identifies all\n        objects in the docs/ folder.\n\n    :ivar http_error_code: The HTTP error code when the redirect is applied. In\n        the event of an error, if the error code equals this value, then the\n        specified redirect is applied.\n\n    '
    TRANSLATOR = [
     ('KeyPrefixEquals', 'key_prefix'),
     ('HttpErrorCodeReturnedEquals', 'http_error_code')]

    def __init__(self, key_prefix=None, http_error_code=None):
        self.key_prefix = key_prefix
        self.http_error_code = http_error_code
        super(Condition, self).__init__(self.TRANSLATOR)

    def to_xml(self):
        return tag('Condition', super(Condition, self).to_xml())


class Redirect(_XMLKeyValue):
    __doc__ = "\n    :ivar hostname: The host name to use in the redirect request.\n\n    :ivar protocol: The protocol to use in the redirect request.  Can be either\n    'http' or 'https'.\n\n    :ivar replace_key: The specific object key to use in the redirect request.\n        For example, redirect request to error.html.\n\n    :ivar replace_key_prefix: The object key prefix to use in the redirect\n        request. For example, to redirect requests for all pages with prefix\n        docs/ (objects in the docs/ folder) to documents/, you can set a\n        condition block with KeyPrefixEquals set to docs/ and in the Redirect\n        set ReplaceKeyPrefixWith to /documents.\n\n    :ivar http_redirect_code: The HTTP redirect code to use on the response.\n\n    "
    TRANSLATOR = [
     ('Protocol', 'protocol'),
     ('HostName', 'hostname'),
     ('ReplaceKeyWith', 'replace_key'),
     ('ReplaceKeyPrefixWith', 'replace_key_prefix'),
     ('HttpRedirectCode', 'http_redirect_code')]

    def __init__(self, hostname=None, protocol=None, replace_key=None, replace_key_prefix=None, http_redirect_code=None):
        self.hostname = hostname
        self.protocol = protocol
        self.replace_key = replace_key
        self.replace_key_prefix = replace_key_prefix
        self.http_redirect_code = http_redirect_code
        super(Redirect, self).__init__(self.TRANSLATOR)

    def to_xml(self):
        return tag('Redirect', super(Redirect, self).to_xml())