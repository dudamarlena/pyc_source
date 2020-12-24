# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/sites.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
from .interface import AttributeExposer
from .compat import iteritems, implements_to_string, text_type
from .settings import SettingsContainer
from .context.expression import Expression
from babel import Locale
import gettext, locale, re
from collections import namedtuple
import logging
from operator import attrgetter
log = logging.getLogger(b'moya.runtime')
startup_log = logging.getLogger(b'moya.startup')
SiteMatch = namedtuple(b'SiteMatch', [b'site', b'site_data', b'custom_data'])

@implements_to_string
class LocaleProxy(AttributeExposer):
    __moya_exposed_attributes__ = [
     b'language',
     b'territory',
     b'language_name',
     b'display_name',
     b'territory_name',
     b'territories',
     b'languages',
     b'months']

    def __init__(self, locale_name=b'en_US.UTF-8'):
        self._locale_name = locale_name
        self._locale = Locale.parse(locale_name)
        self._territories = None
        self._languages = None
        self._months = None
        super(LocaleProxy, self).__init__()
        return

    def __moyapy__(self):
        return self._locale

    def __repr__(self):
        return (b"<locale '{}'>").format(self._locale_name)

    def __str__(self):
        return self._locale_name

    @property
    def language(self):
        return self._locale.language

    @property
    def languages(self):
        if self._languages is None:
            self._languages = dict(self._locale.languages)
        return self._languages

    @property
    def territory(self):
        return self._locale.territory

    @property
    def language_name(self):
        return self._locale.get_language_name()

    @property
    def display_name(self):
        return self._locale.get_display_name()

    @property
    def territory_name(self):
        return self._locale.get_territory_name()

    @property
    def territories(self):
        if self._territories is None:
            self._territories = dict(self._locale.territories)
        return self._territories

    @property
    def months(self):
        if self._months is None:
            self._months = dict(self._locale.months)
        return self._months


@implements_to_string
class SiteInstance(AttributeExposer):
    __moya_exposed_attributes__ = [
     b'base_content',
     b'timezone',
     b'user_timezone',
     b'append_slash',
     b'head_as_get',
     b'language',
     b'locale',
     b'datetime_format',
     b'time_format',
     b'date_format',
     b'timespan_format',
     b'translations',
     b'host',
     b'theme']

    def __init__(self, site, site_data, custom_data, _as_bool=lambda t: t.strip().lower() in ('yes', 'true')):
        self._site = site
        self._data = SettingsContainer.from_dict(custom_data)
        get = site_data.get
        self.base_content = get(b'base_content')
        self.timezone = get(b'timezone')
        self.user_timezone = _as_bool(get(b'user_timezone', b'no'))
        self.append_slash = _as_bool(get(b'append_slash', b'no'))
        self.head_as_get = _as_bool(get(b'head_as_get', b'yes'))
        self.language = get(b'language')
        _locale = get(b'locale', b'en')
        if _locale == b'auto':
            _locale, _ = locale.getdefaultlocale()
        try:
            self.locale = LocaleProxy(_locale)
        except:
            log.error(b"unable to get locale '%s', defaulting to 'en'", _locale)
            self.locale = LocaleProxy(b'en')

        self.datetime_format = get(b'datetime_format')
        self.time_format = get(b'time_format')
        self.date_format = get(b'date_format')
        self.timespan_format = get(b'timespan_format')
        self.translations = gettext.NullTranslations()
        self.host = get(b'host')
        self.theme = get(b'theme')

    def __str__(self):
        return (b'<site "{}">').format(self._site.domain)

    def __repr__(self):
        return (b"Site('{}')").format(self._site.domain)

    def __moyarepr__(self, context):
        return (b"<site '{}'>").format(self._site.domain)

    def __moyaconsole__(self, console):
        console.text(text_type(self), fg=b'green', bold=True)
        table = sorted([ (k, getattr(self, k)) for k in self.__moya_exposed_attributes__ ])
        console.table(table, header_row=[b'key', b'value'])


@implements_to_string
class Site(object):
    """Site data associated with a domain"""
    _re_domain = re.compile(b'(\\*)|(\\{.*?\\})|(.*?)')
    _re_named_match = re.compile(b'{.*?}').match

    def __init__(self, domain, insert_order=0, site_data=None, custom_data=None):
        self.domain = domain
        if site_data is None:
            site_data = {}
        if custom_data is None:
            custom_data = None
        if b'priority' in site_data:
            _priority = site_data[b'priority']
            try:
                priority = int(_priority)
            except ValueError:
                startup_log.error((b"priority in site section should should be an integer (not '{}')").format(_priority))

        else:
            priority = 0
        self.order = (
         priority, insert_order)
        self.site_data = site_data
        self.custom_data = custom_data
        with Expression._lock:
            if site_data:
                for v in site_data.values():
                    Expression.extract(v)

            if custom_data:
                for v in custom_data.values():
                    Expression.extract(v)

        tokens = []
        for token in self._re_domain.split(domain):
            if token:
                if self._re_named_match(token):
                    name = token[1:-1]
                    if name.startswith(b'*'):
                        name = name[1:]
                        if name:
                            tokens.append((b'(?P<{}>.*?)').format(re.escape(name)))
                        else:
                            tokens.append((b'(?:.*?)').format(re.escape(name)))
                    elif name:
                        tokens.append((b'(?P<{}>[\\w-]*?)').format(re.escape(name)))
                    else:
                        tokens.append((b'(?:[\\w-]*?)').format(re.escape(name)))
                elif token == b'*':
                    tokens.append(b'.*?')
                else:
                    tokens.append(re.escape(token))

        re_domain = (b'^{}$').format((b'').join(tokens))
        self._match = re.compile(re_domain).match
        return

    def __str__(self):
        return (b'<site "{}">').format(self.domain)

    def __repr__(self):
        return (b"Site('{}', {!r})").format(self.domain, self.site_data)

    def __moyarepr__(self, context):
        return (b"<site '{}', {}>").format(self.domain, context.to_expr(self.site_data))

    def match(self, domain):
        match = self._match(domain)
        if match is None:
            return (None, None)
        else:
            match_dict = match.groupdict()
            site_data = self.site_data.copy()
            custom_data = self.custom_data.copy()
            site_data.update(match_dict)
            custom_data.update(match_dict)
            return (site_data, custom_data)


class Sites(object):
    """A container that maps site wild-cards on to a dictionary"""
    _site_keys = [
     ('base_content', 'site#content.base'),
     ('timezone', 'UTC'),
     ('user_timezone', 'yes'),
     ('append_slash', 'no'),
     ('locale', 'en_us.UTF-8'),
     ('language', 'en-US'),
     ('datetime_format', 'medium'),
     ('date_format', 'medium'),
     ('time_format', 'medium'),
     ('timespan_format', 'medium'),
     ('host', '${.request.host_url}'),
     ('theme', 'default')]

    def __init__(self):
        self._defaults = {}
        self._sites = []
        self._order = 0

    def __repr__(self):
        return repr(self._sites)

    def clear(self):
        """Clear all site information"""
        del self._sites[:]

    def set_defaults(self, section):
        self._defaults = {k:section.get(k, default) for k, default in self._site_keys}

    def add_from_section(self, domains, section):
        """Add a site from a named section in settings"""
        site_data = self._defaults.copy()
        custom_data = {}
        for k, v in iteritems(section):
            prefix, hyphen, key = k.partition(b'-')
            if hyphen and prefix in ('data', ''):
                custom_data[key] = v
            else:
                site_data[k] = v

        for domain in domains.split(b','):
            domain = domain.strip()
            site = Site(domain, self._order, site_data=site_data, custom_data=custom_data)
            self._order += 1
            self._sites.append(site)

    def add(self, domains, **data):
        if isinstance(domains, text_type):
            domains = domains.split(b',')
        for domain in domains:
            domain = domain.strip()
            site = Site(domain, self._order, custom_data=data)
            self._order += 1
            self._sites.append(site)

    def _match(self, domain, _order_key=attrgetter(b'order')):
        self._sites.sort(key=_order_key, reverse=True)
        for site in self._sites:
            site_data, custom_data = site.match(domain)
            if site_data is not None:
                return SiteMatch(site, site_data, custom_data)

        return

    def match(self, domain, context=None):
        site_match = self._match(domain)
        if site_match is None:
            return
        else:
            site, site_data, custom_data = site_match
            if context is None:
                return custom_data
            sub = context.sub
            with context.data_frame(site_data):
                new_site_data = {k:sub(v) for k, v in site_data.items()}
            with context.data_frame(custom_data):
                new_custom_data = {k:sub(v) for k, v in custom_data.items()}
            return SiteInstance(site, new_site_data, new_custom_data)

    def __contains__(self, domain):
        return self.match(domain) is not None


if __name__ == b'__main__':
    sites = Sites()
    sites.add(b'www.moyaproject.com', name=b'www')
    sites.add(b'moyaproject.com', name=b'nodomain')
    sites.add(b'{name}.moyaroject.com', subdomain=True)
    sites.add(b'127.*', local=True)
    print(1, sites.match(b'www.moyaroject.com'))
    print(2, sites.match(b'moyaroject.com'))
    print(3, sites.match(b'blog.moyaroject.com'))
    print(4, sites.match(b'127.0.0.1'))
    print(5, sites.match(b'google.com'))
    print(b'moyaroject.com' in sites)
    print(b'google.com' in sites)
    print(sites)
    print(Site(b'{*subdomain}.{domain}.{tld}').match(b'sub.sub-domain.moyaroject.com'))
    sites = Sites()
    sites.add(b'www.moyaroject.com,blog.moyaroject.com')
    sites = Sites()
    sites.add(b'*')
    print(sites.match(b'alternative.localhost'))
    sites = Sites()
    sites.add(b'{*domain}', name=b'test')
    print(sites.match(b'www.moyaproject.com'))