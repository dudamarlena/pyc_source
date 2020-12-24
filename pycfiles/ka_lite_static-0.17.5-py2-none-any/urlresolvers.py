# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/urlresolvers.py
# Compiled at: 2018-07-11 18:15:30
"""
This module converts requested URLs to callback view functions.

RegexURLResolver is the main class here. Its resolve() method takes a URL (as
a string) and returns a tuple in this format:

    (view_function, function_args, function_kwargs)
"""
from __future__ import unicode_literals
import functools, re
from threading import local
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured, ViewDoesNotExist
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_str, force_text, iri_to_uri
from django.utils.functional import memoize, lazy
from django.utils.http import urlquote
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.utils.regex_helper import normalize
from django.utils import six
from django.utils.translation import get_language
_resolver_cache = {}
_ns_resolver_cache = {}
_callable_cache = {}
_prefixes = local()
_urlconfs = local()

class ResolverMatch(object):

    def __init__(self, func, args, kwargs, url_name=None, app_name=None, namespaces=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.app_name = app_name
        if namespaces:
            self.namespaces = [ x for x in namespaces if x ]
        else:
            self.namespaces = []
        if not url_name:
            if not hasattr(func, b'__name__'):
                url_name = (b'.').join([func.__class__.__module__, func.__class__.__name__])
            else:
                url_name = (b'.').join([func.__module__, func.__name__])
        self.url_name = url_name

    @property
    def namespace(self):
        return (b':').join(self.namespaces)

    @property
    def view_name(self):
        return (b':').join([ x for x in [self.namespace, self.url_name] if x ])

    def __getitem__(self, index):
        return (
         self.func, self.args, self.kwargs)[index]

    def __repr__(self):
        return b"ResolverMatch(func=%s, args=%s, kwargs=%s, url_name='%s', app_name='%s', namespace='%s')" % (
         self.func, self.args, self.kwargs, self.url_name, self.app_name, self.namespace)


class Resolver404(Http404):
    pass


class NoReverseMatch(Exception):
    silent_variable_failure = True


def get_callable(lookup_view, can_fail=False):
    """
    Convert a string version of a function name to the callable object.

    If the lookup_view is not an import path, it is assumed to be a URL pattern
    label and the original string is returned.

    If can_fail is True, lookup_view might be a URL pattern label, so errors
    during the import fail and the string is returned.
    """
    if not callable(lookup_view):
        mod_name, func_name = get_mod_func(lookup_view)
        if func_name == b'':
            return lookup_view
        try:
            mod = import_module(mod_name)
        except ImportError:
            parentmod, submod = get_mod_func(mod_name)
            if not can_fail and submod != b'' and not module_has_submodule(import_module(parentmod), submod):
                raise ViewDoesNotExist(b'Could not import %s. Parent module %s does not exist.' % (
                 lookup_view, mod_name))
            if not can_fail:
                raise
        else:
            try:
                lookup_view = getattr(mod, func_name)
                if not callable(lookup_view):
                    raise ViewDoesNotExist(b'Could not import %s.%s. View is not callable.' % (
                     mod_name, func_name))
            except AttributeError:
                if not can_fail:
                    raise ViewDoesNotExist(b'Could not import %s. View does not exist in module %s.' % (
                     lookup_view, mod_name))

    return lookup_view


get_callable = memoize(get_callable, _callable_cache, 1)

def get_resolver(urlconf):
    if urlconf is None:
        from django.conf import settings
        urlconf = settings.ROOT_URLCONF
    return RegexURLResolver(b'^/', urlconf)


get_resolver = memoize(get_resolver, _resolver_cache, 1)

def get_ns_resolver(ns_pattern, resolver):
    ns_resolver = RegexURLResolver(ns_pattern, resolver.url_patterns)
    return RegexURLResolver(b'^/', [ns_resolver])


get_ns_resolver = memoize(get_ns_resolver, _ns_resolver_cache, 2)

def get_mod_func(callback):
    try:
        dot = callback.rindex(b'.')
    except ValueError:
        return (
         callback, b'')

    return (
     callback[:dot], callback[dot + 1:])


class LocaleRegexProvider(object):
    """
    A mixin to provide a default regex property which can vary by active
    language.

    """

    def __init__(self, regex):
        self._regex = regex
        self._regex_dict = {}

    @property
    def regex(self):
        """
        Returns a compiled regular expression, depending upon the activated
        language-code.
        """
        language_code = get_language()
        if language_code not in self._regex_dict:
            if isinstance(self._regex, six.string_types):
                regex = self._regex
            else:
                regex = force_text(self._regex)
            try:
                compiled_regex = re.compile(regex, re.UNICODE)
            except re.error as e:
                raise ImproperlyConfigured(b'"%s" is not a valid regular expression: %s' % (
                 regex, six.text_type(e)))

            self._regex_dict[language_code] = compiled_regex
        return self._regex_dict[language_code]


class RegexURLPattern(LocaleRegexProvider):

    def __init__(self, regex, callback, default_args=None, name=None):
        LocaleRegexProvider.__init__(self, regex)
        if callable(callback):
            self._callback = callback
        else:
            self._callback = None
            self._callback_str = callback
        self.default_args = default_args or {}
        self.name = name
        return

    def __repr__(self):
        return force_str(b'<%s %s %s>' % (self.__class__.__name__, self.name, self.regex.pattern))

    def add_prefix(self, prefix):
        """
        Adds the prefix string to a string-based callback.
        """
        if not prefix or not hasattr(self, b'_callback_str'):
            return
        self._callback_str = prefix + b'.' + self._callback_str

    def resolve(self, path):
        match = self.regex.search(path)
        if match:
            kwargs = match.groupdict()
            if kwargs:
                args = ()
            else:
                args = match.groups()
            kwargs.update(self.default_args)
            return ResolverMatch(self.callback, args, kwargs, self.name)

    @property
    def callback(self):
        if self._callback is not None:
            return self._callback
        else:
            self._callback = get_callable(self._callback_str)
            return self._callback


class RegexURLResolver(LocaleRegexProvider):

    def __init__(self, regex, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        LocaleRegexProvider.__init__(self, regex)
        self.urlconf_name = urlconf_name
        if not isinstance(urlconf_name, six.string_types):
            self._urlconf_module = self.urlconf_name
        self.callback = None
        self.default_kwargs = default_kwargs or {}
        self.namespace = namespace
        self.app_name = app_name
        self._reverse_dict = {}
        self._namespace_dict = {}
        self._app_dict = {}
        self._callback_strs = set()
        self._populated = False
        return

    def __repr__(self):
        if isinstance(self.urlconf_name, list) and len(self.urlconf_name):
            urlconf_repr = b'<%s list>' % self.urlconf_name[0].__class__.__name__
        else:
            urlconf_repr = repr(self.urlconf_name)
        return str(b'<%s %s (%s:%s) %s>') % (
         self.__class__.__name__, urlconf_repr, self.app_name,
         self.namespace, self.regex.pattern)

    def _populate(self):
        lookups = MultiValueDict()
        namespaces = {}
        apps = {}
        language_code = get_language()
        for pattern in reversed(self.url_patterns):
            if hasattr(pattern, b'_callback_str'):
                self._callback_strs.add(pattern._callback_str)
            elif hasattr(pattern, b'_callback'):
                callback = pattern._callback
                if isinstance(callback, functools.partial):
                    callback = callback.func
                if not hasattr(callback, b'__name__'):
                    lookup_str = callback.__module__ + b'.' + callback.__class__.__name__
                else:
                    lookup_str = callback.__module__ + b'.' + callback.__name__
                self._callback_strs.add(lookup_str)
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
                    parent = normalize(pattern.regex.pattern)
                    for name in pattern.reverse_dict:
                        for matches, pat, defaults in pattern.reverse_dict.getlist(name):
                            new_matches = []
                            for piece, p_args in parent:
                                new_matches.extend([ (piece + suffix, p_args + args) for suffix, args in matches ])

                            lookups.appendlist(name, (new_matches, p_pattern + pat, dict(defaults, **pattern.default_kwargs)))

                    for namespace, (prefix, sub_pattern) in pattern.namespace_dict.items():
                        namespaces[namespace] = (
                         p_pattern + prefix, sub_pattern)

                    for app_name, namespace_list in pattern.app_dict.items():
                        apps.setdefault(app_name, []).extend(namespace_list)

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

    def resolve(self, path):
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
                        tried.extend([ [pattern] + t for t in sub_tried ])
                    else:
                        tried.append([pattern])
                else:
                    if sub_match:
                        sub_match_dict = dict(match.groupdict(), **self.default_kwargs)
                        sub_match_dict.update(sub_match.kwargs)
                        return ResolverMatch(sub_match.func, sub_match.args, sub_match_dict, sub_match.url_name, self.app_name or sub_match.app_name, [self.namespace] + sub_match.namespaces)
                    tried.append([pattern])

            raise Resolver404({b'tried': tried, b'path': new_path})
        raise Resolver404({b'path': path})
        return

    @property
    def urlconf_module(self):
        try:
            return self._urlconf_module
        except AttributeError:
            self._urlconf_module = import_module(self.urlconf_name)
            return self._urlconf_module

    @property
    def url_patterns(self):
        patterns = getattr(self.urlconf_module, b'urlpatterns', self.urlconf_module)
        try:
            iter(patterns)
        except TypeError:
            raise ImproperlyConfigured(b"The included urlconf %s doesn't have any patterns in it" % self.urlconf_name)

        return patterns

    def _resolve_special(self, view_type):
        callback = getattr(self.urlconf_module, b'handler%s' % view_type, None)
        if not callback:
            from django.conf import urls
            callback = getattr(urls, b'handler%s' % view_type)
        return (
         get_callable(callback), {})

    def resolve403(self):
        return self._resolve_special(b'403')

    def resolve404(self):
        return self._resolve_special(b'404')

    def resolve500(self):
        return self._resolve_special(b'500')

    def reverse(self, lookup_view, *args, **kwargs):
        return self._reverse_with_prefix(lookup_view, b'', *args, **kwargs)

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        if args and kwargs:
            raise ValueError(b"Don't mix *args and **kwargs in call to reverse()!")
        if not self._populated:
            self._populate()
        try:
            if lookup_view in self._callback_strs:
                lookup_view = get_callable(lookup_view, True)
        except (ImportError, AttributeError) as e:
            raise NoReverseMatch(b"Error importing '%s': %s." % (lookup_view, e))

        possibilities = self.reverse_dict.getlist(lookup_view)
        prefix_norm, prefix_args = normalize(urlquote(_prefix))[0]
        for possibility, pattern, defaults in possibilities:
            for result, params in possibility:
                if args:
                    if len(args) != len(params) + len(prefix_args):
                        continue
                    unicode_args = [ force_text(val) for val in args ]
                    candidate = (prefix_norm + result) % dict(zip(prefix_args + params, unicode_args))
                else:
                    if set(kwargs.keys()) | set(defaults.keys()) != set(params) | set(defaults.keys()) | set(prefix_args):
                        continue
                    matches = True
                    for k, v in defaults.items():
                        if kwargs.get(k, v) != v:
                            matches = False
                            break

                    if not matches:
                        continue
                    unicode_kwargs = dict([ (k, force_text(v)) for k, v in kwargs.items() ])
                    candidate = (prefix_norm.replace(b'%', b'%%') + result) % unicode_kwargs
                if re.search(b'^%s%s' % (prefix_norm, pattern), candidate, re.UNICODE):
                    if candidate.startswith(b'//'):
                        candidate = b'/%%2F%s' % candidate[2:]
                    return candidate

        m = getattr(lookup_view, b'__module__', None)
        n = getattr(lookup_view, b'__name__', None)
        if m is not None and n is not None:
            lookup_view_s = b'%s.%s' % (m, n)
        else:
            lookup_view_s = lookup_view
        raise NoReverseMatch(b"Reverse for '%s' with arguments '%s' and keyword arguments '%s' not found." % (
         lookup_view_s, args, kwargs))
        return


class LocaleRegexURLResolver(RegexURLResolver):
    """
    A URL resolver that always matches the active language code as URL prefix.

    Rather than taking a regex argument, we just override the ``regex``
    function to always return the active language-code as regex.
    """

    def __init__(self, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        super(LocaleRegexURLResolver, self).__init__(None, urlconf_name, default_kwargs, app_name, namespace)
        return

    @property
    def regex(self):
        language_code = get_language()
        if language_code not in self._regex_dict:
            regex_compiled = re.compile(b'^%s/' % language_code, re.UNICODE)
            self._regex_dict[language_code] = regex_compiled
        return self._regex_dict[language_code]


def resolve(path, urlconf=None):
    if urlconf is None:
        urlconf = get_urlconf()
    return get_resolver(urlconf).resolve(path)


def reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
    if urlconf is None:
        urlconf = get_urlconf()
    resolver = get_resolver(urlconf)
    args = args or []
    kwargs = kwargs or {}
    if prefix is None:
        prefix = get_script_prefix()
    if not isinstance(viewname, six.string_types):
        view = viewname
    else:
        parts = viewname.split(b':')
        parts.reverse()
        view = parts[0]
        path = parts[1:]
        resolved_path = []
        ns_pattern = b''
        while path:
            ns = path.pop()
            try:
                app_list = resolver.app_dict[ns]
                if current_app and current_app in app_list:
                    ns = current_app
                elif ns not in app_list:
                    ns = app_list[0]
            except KeyError:
                pass

            try:
                extra, resolver = resolver.namespace_dict[ns]
                resolved_path.append(ns)
                ns_pattern = ns_pattern + extra
            except KeyError as key:
                if resolved_path:
                    raise NoReverseMatch(b"%s is not a registered namespace inside '%s'" % (
                     key, (b':').join(resolved_path)))
                else:
                    raise NoReverseMatch(b'%s is not a registered namespace' % key)

    if ns_pattern:
        resolver = get_ns_resolver(ns_pattern, resolver)
    return iri_to_uri(resolver._reverse_with_prefix(view, prefix, *args, **kwargs))


reverse_lazy = lazy(reverse, str)

def clear_url_caches():
    global _callable_cache
    global _ns_resolver_cache
    global _resolver_cache
    _resolver_cache.clear()
    _ns_resolver_cache.clear()
    _callable_cache.clear()


def set_script_prefix(prefix):
    """
    Sets the script prefix for the current thread.
    """
    if not prefix.endswith(b'/'):
        prefix += b'/'
    _prefixes.value = prefix


def get_script_prefix():
    """
    Returns the currently active script prefix. Useful for client code that
    wishes to construct their own URLs manually (although accessing the request
    instance is normally going to be a lot cleaner).
    """
    return getattr(_prefixes, b'value', b'/')


def set_urlconf(urlconf_name):
    """
    Sets the URLconf for the current thread (overriding the default one in
    settings). Set to None to revert back to the default.
    """
    if urlconf_name:
        _urlconfs.value = urlconf_name
    elif hasattr(_urlconfs, b'value'):
        del _urlconfs.value


def get_urlconf(default=None):
    """
    Returns the root URLconf to use for the current thread if it has been
    changed from the default one.
    """
    return getattr(_urlconfs, b'value', default)


def is_valid_path(path, urlconf=None):
    """
    Returns True if the given path resolves against the default URL resolver,
    False otherwise.

    This is a convenience method to make working with "is this a match?" cases
    easier, avoiding unnecessarily indented try...except blocks.
    """
    try:
        resolve(path, urlconf)
        return True
    except Resolver404:
        return False