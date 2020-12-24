# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/urls/resolvers.py
# Compiled at: 2019-02-14 00:35:17
"""
This module converts requested URLs to callback view functions.

RegexURLResolver is the main class here. Its resolve() method takes a URL (as
a string) and returns a ResolverMatch object which provides access to all
attributes of the resolved URL match.
"""
from __future__ import unicode_literals
import functools, re, threading
from importlib import import_module
from django.conf import settings
from django.core.checks import Warning
from django.core.checks.urls import check_resolver
from django.core.exceptions import ImproperlyConfigured
from django.utils import lru_cache, six
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_str, force_text
from django.utils.functional import cached_property
from django.utils.http import RFC3986_SUBDELIMS, escape_leading_slashes, urlquote
from django.utils.regex_helper import normalize
from django.utils.translation import get_language
from .exceptions import NoReverseMatch, Resolver404
from .utils import get_callable

class ResolverMatch(object):

    def __init__(self, func, args, kwargs, url_name=None, app_names=None, namespaces=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.url_name = url_name
        self.app_names = [ x for x in app_names if x ] if app_names else []
        self.app_name = (b':').join(self.app_names)
        self.namespaces = [ x for x in namespaces if x ] if namespaces else []
        self.namespace = (b':').join(self.namespaces)
        if not hasattr(func, b'__name__'):
            self._func_path = (b'.').join([func.__class__.__module__, func.__class__.__name__])
        else:
            self._func_path = (b'.').join([func.__module__, func.__name__])
        view_path = url_name or self._func_path
        self.view_name = (b':').join(self.namespaces + [view_path])

    def __getitem__(self, index):
        return (
         self.func, self.args, self.kwargs)[index]

    def __repr__(self):
        return b'ResolverMatch(func=%s, args=%s, kwargs=%s, url_name=%s, app_names=%s, namespaces=%s)' % (
         self._func_path, self.args, self.kwargs, self.url_name,
         self.app_names, self.namespaces)


@lru_cache.lru_cache(maxsize=None)
def get_resolver(urlconf=None):
    if urlconf is None:
        from django.conf import settings
        urlconf = settings.ROOT_URLCONF
    return RegexURLResolver(b'^/', urlconf)


@lru_cache.lru_cache(maxsize=None)
def get_ns_resolver(ns_pattern, resolver):
    ns_resolver = RegexURLResolver(ns_pattern, resolver.url_patterns)
    return RegexURLResolver(b'^/', [ns_resolver])


class LocaleRegexDescriptor(object):

    def __get__(self, instance, cls=None):
        """
        Return a compiled regular expression based on the active language.
        """
        if instance is None:
            return self
        else:
            if isinstance(instance._regex, six.string_types):
                instance.__dict__[b'regex'] = self._compile(instance._regex)
                return instance.__dict__[b'regex']
            language_code = get_language()
            if language_code not in instance._regex_dict:
                instance._regex_dict[language_code] = self._compile(force_text(instance._regex))
            return instance._regex_dict[language_code]

    def _compile(self, regex):
        """
        Compile and return the given regular expression.
        """
        try:
            return re.compile(regex, re.UNICODE)
        except re.error as e:
            raise ImproperlyConfigured(b'"%s" is not a valid regular expression: %s' % (
             regex, six.text_type(e)))


class LocaleRegexProvider(object):
    """
    A mixin to provide a default regex property which can vary by active
    language.
    """

    def __init__(self, regex):
        self._regex = regex
        self._regex_dict = {}

    regex = LocaleRegexDescriptor()

    def describe(self):
        """
        Format the URL pattern for display in warning messages.
        """
        description = (b"'{}'").format(self.regex.pattern)
        if getattr(self, b'name', False):
            description += (b" [name='{}']").format(self.name)
        return description

    def _check_pattern_startswith_slash(self):
        """
        Check that the pattern does not begin with a forward slash.
        """
        regex_pattern = self.regex.pattern
        if not settings.APPEND_SLASH:
            return []
        else:
            if (regex_pattern.startswith(b'/') or regex_pattern.startswith(b'^/')) and not regex_pattern.endswith(b'/'):
                warning = Warning((b"Your URL pattern {} has a regex beginning with a '/'. Remove this slash as it is unnecessary. If this pattern is targeted in an include(), ensure the include() pattern has a trailing '/'.").format(self.describe()), id=b'urls.W002')
                return [
                 warning]
            return []


class RegexURLPattern(LocaleRegexProvider):

    def __init__(self, regex, callback, default_args=None, name=None):
        LocaleRegexProvider.__init__(self, regex)
        self.callback = callback
        self.default_args = default_args or {}
        self.name = name

    def __repr__(self):
        return force_str(b'<%s %s %s>' % (self.__class__.__name__, self.name, self.regex.pattern))

    def check(self):
        warnings = self._check_pattern_name()
        if not warnings:
            warnings = self._check_pattern_startswith_slash()
        return warnings

    def _check_pattern_name(self):
        """
        Check that the pattern name does not contain a colon.
        """
        if self.name is not None and b':' in self.name:
            warning = Warning((b"Your URL pattern {} has a name including a ':'. Remove the colon, to avoid ambiguous namespace references.").format(self.describe()), id=b'urls.W003')
            return [
             warning]
        else:
            return []
            return

    def resolve(self, path):
        match = self.regex.search(path)
        if match:
            kwargs = match.groupdict()
            args = () if kwargs else match.groups()
            kwargs.update(self.default_args)
            return ResolverMatch(self.callback, args, kwargs, self.name)

    @cached_property
    def lookup_str(self):
        """
        A string that identifies the view (e.g. 'path.to.view_function' or
        'path.to.ClassBasedView').
        """
        callback = self.callback
        while isinstance(callback, functools.partial):
            callback = callback.func

        if not hasattr(callback, b'__name__'):
            return callback.__module__ + b'.' + callback.__class__.__name__
        else:
            if six.PY3:
                return callback.__module__ + b'.' + callback.__qualname__
            return callback.__module__ + b'.' + callback.__name__


class RegexURLResolver(LocaleRegexProvider):

    def __init__(self, regex, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        LocaleRegexProvider.__init__(self, regex)
        self.urlconf_name = urlconf_name
        self.callback = None
        self.default_kwargs = default_kwargs or {}
        self.namespace = namespace
        self.app_name = app_name
        self._reverse_dict = {}
        self._namespace_dict = {}
        self._app_dict = {}
        self._callback_strs = set()
        self._populated = False
        self._local = threading.local()
        return

    def __repr__(self):
        if isinstance(self.urlconf_name, list) and len(self.urlconf_name):
            urlconf_repr = b'<%s list>' % self.urlconf_name[0].__class__.__name__
        else:
            urlconf_repr = repr(self.urlconf_name)
        return str(b'<%s %s (%s:%s) %s>') % (
         self.__class__.__name__, urlconf_repr, self.app_name,
         self.namespace, self.regex.pattern)

    def check(self):
        warnings = self._check_include_trailing_dollar()
        for pattern in self.url_patterns:
            warnings.extend(check_resolver(pattern))

        if not warnings:
            warnings = self._check_pattern_startswith_slash()
        return warnings

    def _check_include_trailing_dollar(self):
        """
        Check that include is not used with a regex ending with a dollar.
        """
        regex_pattern = self.regex.pattern
        if regex_pattern.endswith(b'$') and not regex_pattern.endswith(b'\\$'):
            warning = Warning((b"Your URL pattern {} uses include with a regex ending with a '$'. Remove the dollar from the regex to avoid problems including URLs.").format(self.describe()), id=b'urls.W001')
            return [
             warning]
        else:
            return []

    def _populate(self):
        if getattr(self._local, b'populating', False):
            return
        self._local.populating = True
        lookups = MultiValueDict()
        namespaces = {}
        apps = {}
        language_code = get_language()
        for pattern in reversed(self.url_patterns):
            if isinstance(pattern, RegexURLPattern):
                self._callback_strs.add(pattern.lookup_str)
            p_pattern = pattern.regex.pattern
            if p_pattern.startswith(b'^'):
                p_pattern = p_pattern[1:]
            if isinstance(pattern, RegexURLResolver):
                if pattern.namespace:
                    namespaces[pattern.namespace] = (
                     p_pattern, pattern)
                    if pattern.app_name:
                        apps.setdefault(pattern.app_name, []).append(pattern.namespace)
                else:
                    parent_pat = pattern.regex.pattern
                    for name in pattern.reverse_dict:
                        for matches, pat, defaults in pattern.reverse_dict.getlist(name):
                            new_matches = normalize(parent_pat + pat)
                            lookups.appendlist(name, (
                             new_matches,
                             p_pattern + pat,
                             dict(defaults, **pattern.default_kwargs)))

                    for namespace, (prefix, sub_pattern) in pattern.namespace_dict.items():
                        namespaces[namespace] = (
                         p_pattern + prefix, sub_pattern)

                    for app_name, namespace_list in pattern.app_dict.items():
                        apps.setdefault(app_name, []).extend(namespace_list)

                if not getattr(pattern._local, b'populating', False):
                    pattern._populate()
                self._callback_strs.update(pattern._callback_strs)
            else:
                bits = normalize(p_pattern)
                lookups.appendlist(pattern.callback, (bits, p_pattern, pattern.default_args))
                if pattern.name is not None:
                    lookups.appendlist(pattern.name, (bits, p_pattern, pattern.default_args))

        self._reverse_dict[language_code] = lookups
        self._namespace_dict[language_code] = namespaces
        self._app_dict[language_code] = apps
        self._populated = True
        self._local.populating = False
        return

    @property
    def reverse_dict(self):
        language_code = get_language()
        if language_code not in self._reverse_dict:
            self._populate()
        return self._reverse_dict[language_code]

    @property
    def namespace_dict(self):
        language_code = get_language()
        if language_code not in self._namespace_dict:
            self._populate()
        return self._namespace_dict[language_code]

    @property
    def app_dict(self):
        language_code = get_language()
        if language_code not in self._app_dict:
            self._populate()
        return self._app_dict[language_code]

    def _is_callback(self, name):
        if not self._populated:
            self._populate()
        return name in self._callback_strs

    def resolve(self, path):
        path = force_text(path)
        tried = []
        match = self.regex.search(path)
        if match:
            new_path = path[match.end():]
            for pattern in self.url_patterns:
                try:
                    sub_match = pattern.resolve(new_path)
                except Resolver404 as e:
                    sub_tried = e.args[0].get(b'tried')
                    if sub_tried is not None:
                        tried.extend([pattern] + t for t in sub_tried)
                    else:
                        tried.append([pattern])
                else:
                    if sub_match:
                        sub_match_dict = dict(match.groupdict(), **self.default_kwargs)
                        sub_match_dict.update(sub_match.kwargs)
                        sub_match_args = sub_match.args
                        if not sub_match_dict:
                            sub_match_args = match.groups() + sub_match.args
                        return ResolverMatch(sub_match.func, sub_match_args, sub_match_dict, sub_match.url_name, [
                         self.app_name] + sub_match.app_names, [
                         self.namespace] + sub_match.namespaces)
                    tried.append([pattern])

            raise Resolver404({b'tried': tried, b'path': new_path})
        raise Resolver404({b'path': path})
        return

    @cached_property
    def urlconf_module(self):
        if isinstance(self.urlconf_name, six.string_types):
            return import_module(self.urlconf_name)
        else:
            return self.urlconf_name

    @cached_property
    def url_patterns(self):
        patterns = getattr(self.urlconf_module, b'urlpatterns', self.urlconf_module)
        try:
            iter(patterns)
        except TypeError:
            msg = b"The included URLconf '{name}' does not appear to have any patterns in it. If you see valid patterns in the file then the issue is probably caused by a circular import."
            raise ImproperlyConfigured(msg.format(name=self.urlconf_name))

        return patterns

    def resolve_error_handler(self, view_type):
        callback = getattr(self.urlconf_module, b'handler%s' % view_type, None)
        if not callback:
            from django.conf import urls
            callback = getattr(urls, b'handler%s' % view_type)
        return (
         get_callable(callback), {})

    def reverse(self, lookup_view, *args, **kwargs):
        return self._reverse_with_prefix(lookup_view, b'', *args, **kwargs)

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        if args and kwargs:
            raise ValueError(b"Don't mix *args and **kwargs in call to reverse()!")
        text_args = [ force_text(v) for v in args ]
        text_kwargs = {k:force_text(v) for k, v in kwargs.items()}
        if not self._populated:
            self._populate()
        possibilities = self.reverse_dict.getlist(lookup_view)
        for possibility, pattern, defaults in possibilities:
            for result, params in possibility:
                if args:
                    if len(args) != len(params):
                        continue
                    candidate_subs = dict(zip(params, text_args))
                else:
                    if set(kwargs.keys()) | set(defaults.keys()) != set(params) | set(defaults.keys()):
                        continue
                    matches = True
                    for k, v in defaults.items():
                        if kwargs.get(k, v) != v:
                            matches = False
                            break

                    if not matches:
                        continue
                    candidate_subs = text_kwargs
                candidate_pat = _prefix.replace(b'%', b'%%') + result
                if re.search(b'^%s%s' % (re.escape(_prefix), pattern), candidate_pat % candidate_subs, re.UNICODE):
                    url = urlquote(candidate_pat % candidate_subs, safe=RFC3986_SUBDELIMS + str(b'/~:@'))
                    return escape_leading_slashes(url)

        m = getattr(lookup_view, b'__module__', None)
        n = getattr(lookup_view, b'__name__', None)
        if m is not None and n is not None:
            lookup_view_s = b'%s.%s' % (m, n)
        else:
            lookup_view_s = lookup_view
        patterns = [ pattern for possibility, pattern, defaults in possibilities ]
        if patterns:
            if args:
                arg_msg = b"arguments '%s'" % (args,)
            elif kwargs:
                arg_msg = b"keyword arguments '%s'" % (kwargs,)
            else:
                arg_msg = b'no arguments'
            msg = b"Reverse for '%s' with %s not found. %d pattern(s) tried: %s" % (
             lookup_view_s, arg_msg, len(patterns), patterns)
        else:
            msg = b"Reverse for '%(view)s' not found. '%(view)s' is not a valid view function or pattern name." % {b'view': lookup_view_s}
        raise NoReverseMatch(msg)
        return


class LocaleRegexURLResolver(RegexURLResolver):
    """
    A URL resolver that always matches the active language code as URL prefix.

    Rather than taking a regex argument, we just override the ``regex``
    function to always return the active language-code as regex.
    """

    def __init__(self, urlconf_name, default_kwargs=None, app_name=None, namespace=None, prefix_default_language=True):
        super(LocaleRegexURLResolver, self).__init__(None, urlconf_name, default_kwargs, app_name, namespace)
        self.prefix_default_language = prefix_default_language
        return

    @property
    def regex(self):
        language_code = get_language() or settings.LANGUAGE_CODE
        if language_code not in self._regex_dict:
            if language_code == settings.LANGUAGE_CODE and not self.prefix_default_language:
                regex_string = b''
            else:
                regex_string = b'^%s/' % language_code
            self._regex_dict[language_code] = re.compile(regex_string, re.UNICODE)
        return self._regex_dict[language_code]