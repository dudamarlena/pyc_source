# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/website.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 10607 bytes


def tag(key, value):
    start = '<%s>' % key
    end = '</%s>' % key
    return '%s%s%s' % (start, value, end)


class WebsiteConfiguration(object):
    """WebsiteConfiguration"""

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
    """RedirectLocation"""
    TRANSLATOR = [
     ('HostName', 'hostname'),
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
    """RoutingRule"""

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
    """Condition"""
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
    """Redirect"""
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