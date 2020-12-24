# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/views/i18n.py
# Compiled at: 2019-02-14 00:35:17
import importlib, itertools, json, os, warnings
from django import http
from django.apps import apps
from django.conf import settings
from django.template import Context, Engine
from django.urls import translate_url
from django.utils import six
from django.utils._os import upath
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.formats import get_format
from django.utils.http import is_safe_url, urlunquote
from django.utils.translation import LANGUAGE_SESSION_KEY, check_for_language, get_language, to_locale
from django.utils.translation.trans_real import DjangoTranslation
from django.views.generic import View
DEFAULT_PACKAGES = [
 'django.conf']
LANGUAGE_QUERY_PARAMETER = 'language'

def set_language(request):
    """
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.POST.get('next', request.GET.get('next'))
    if (next or not request.is_ajax()) and not is_safe_url(url=next, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next = request.META.get('HTTP_REFERER')
        if next:
            next = urlunquote(next)
        if not is_safe_url(url=next, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next = '/'
    response = http.HttpResponseRedirect(next) if next else http.HttpResponse(status=204)
    if request.method == 'POST':
        lang_code = request.POST.get(LANGUAGE_QUERY_PARAMETER)
        if lang_code and check_for_language(lang_code):
            if next:
                next_trans = translate_url(next, lang_code)
                if next_trans != next:
                    response = http.HttpResponseRedirect(next_trans)
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code, max_age=settings.LANGUAGE_COOKIE_AGE, path=settings.LANGUAGE_COOKIE_PATH, domain=settings.LANGUAGE_COOKIE_DOMAIN)
    return response


def get_formats():
    """
    Returns all formats strings required for i18n to work
    """
    FORMAT_SETTINGS = ('DATE_FORMAT', 'DATETIME_FORMAT', 'TIME_FORMAT', 'YEAR_MONTH_FORMAT',
                       'MONTH_DAY_FORMAT', 'SHORT_DATE_FORMAT', 'SHORT_DATETIME_FORMAT',
                       'FIRST_DAY_OF_WEEK', 'DECIMAL_SEPARATOR', 'THOUSAND_SEPARATOR',
                       'NUMBER_GROUPING', 'DATE_INPUT_FORMATS', 'TIME_INPUT_FORMATS',
                       'DATETIME_INPUT_FORMATS')
    result = {}
    for attr in FORMAT_SETTINGS:
        result[attr] = get_format(attr)

    formats = {}
    for k, v in result.items():
        if isinstance(v, (six.string_types, int)):
            formats[k] = force_text(v)
        elif isinstance(v, (tuple, list)):
            formats[k] = [ force_text(value) for value in v ]

    return formats


js_catalog_template = "\n{% autoescape off %}\n(function(globals) {\n\n  var django = globals.django || (globals.django = {});\n\n  {% if plural %}\n  django.pluralidx = function(n) {\n    var v={{ plural }};\n    if (typeof(v) == 'boolean') {\n      return v ? 1 : 0;\n    } else {\n      return v;\n    }\n  };\n  {% else %}\n  django.pluralidx = function(count) { return (count == 1) ? 0 : 1; };\n  {% endif %}\n\n  /* gettext library */\n\n  django.catalog = django.catalog || {};\n  {% if catalog_str %}\n  var newcatalog = {{ catalog_str }};\n  for (var key in newcatalog) {\n    django.catalog[key] = newcatalog[key];\n  }\n  {% endif %}\n\n  if (!django.jsi18n_initialized) {\n    django.gettext = function(msgid) {\n      var value = django.catalog[msgid];\n      if (typeof(value) == 'undefined') {\n        return msgid;\n      } else {\n        return (typeof(value) == 'string') ? value : value[0];\n      }\n    };\n\n    django.ngettext = function(singular, plural, count) {\n      var value = django.catalog[singular];\n      if (typeof(value) == 'undefined') {\n        return (count == 1) ? singular : plural;\n      } else {\n        return value[django.pluralidx(count)];\n      }\n    };\n\n    django.gettext_noop = function(msgid) { return msgid; };\n\n    django.pgettext = function(context, msgid) {\n      var value = django.gettext(context + '\\x04' + msgid);\n      if (value.indexOf('\\x04') != -1) {\n        value = msgid;\n      }\n      return value;\n    };\n\n    django.npgettext = function(context, singular, plural, count) {\n      var value = django.ngettext(context + '\\x04' + singular, context + '\\x04' + plural, count);\n      if (value.indexOf('\\x04') != -1) {\n        value = django.ngettext(singular, plural, count);\n      }\n      return value;\n    };\n\n    django.interpolate = function(fmt, obj, named) {\n      if (named) {\n        return fmt.replace(/%\\(\\w+\\)s/g, function(match){return String(obj[match.slice(2,-2)])});\n      } else {\n        return fmt.replace(/%s/g, function(match){return String(obj.shift())});\n      }\n    };\n\n\n    /* formatting library */\n\n    django.formats = {{ formats_str }};\n\n    django.get_format = function(format_type) {\n      var value = django.formats[format_type];\n      if (typeof(value) == 'undefined') {\n        return format_type;\n      } else {\n        return value;\n      }\n    };\n\n    /* add to global namespace */\n    globals.pluralidx = django.pluralidx;\n    globals.gettext = django.gettext;\n    globals.ngettext = django.ngettext;\n    globals.gettext_noop = django.gettext_noop;\n    globals.pgettext = django.pgettext;\n    globals.npgettext = django.npgettext;\n    globals.interpolate = django.interpolate;\n    globals.get_format = django.get_format;\n\n    django.jsi18n_initialized = true;\n  }\n\n}(this));\n{% endautoescape %}\n"

def render_javascript_catalog(catalog=None, plural=None):
    template = Engine().from_string(js_catalog_template)

    def indent(s):
        return s.replace('\n', '\n  ')

    context = Context({'catalog_str': indent(json.dumps(catalog, sort_keys=True, indent=2)) if catalog else None, 
       'formats_str': indent(json.dumps(get_formats(), sort_keys=True, indent=2)), 
       'plural': plural})
    return http.HttpResponse(template.render(context), 'text/javascript')


def get_javascript_catalog(locale, domain, packages):
    app_configs = apps.get_app_configs()
    allowable_packages = set(app_config.name for app_config in app_configs)
    allowable_packages.update(DEFAULT_PACKAGES)
    packages = [ p for p in packages if p in allowable_packages ]
    paths = []
    for package in packages:
        p = importlib.import_module(package)
        path = os.path.join(os.path.dirname(upath(p.__file__)), 'locale')
        paths.append(path)

    trans = DjangoTranslation(locale, domain=domain, localedirs=paths)
    trans_cat = trans._catalog
    plural = None
    if '' in trans_cat:
        for line in trans_cat[''].split('\n'):
            if line.startswith('Plural-Forms:'):
                plural = line.split(':', 1)[1].strip()

    if plural is not None:
        plural = [ el.strip() for el in plural.split(';') if el.strip().startswith('plural=') ][0].split('=', 1)[1]
    pdict = {}
    maxcnts = {}
    catalog = {}
    trans_fallback_cat = trans._fallback._catalog if trans._fallback else {}
    for key, value in itertools.chain(six.iteritems(trans_cat), six.iteritems(trans_fallback_cat)):
        if key == '' or key in catalog:
            continue
        if isinstance(key, six.string_types):
            catalog[key] = value
        elif isinstance(key, tuple):
            msgid = key[0]
            cnt = key[1]
            maxcnts[msgid] = max(cnt, maxcnts.get(msgid, 0))
            pdict.setdefault(msgid, {})[cnt] = value
        else:
            raise TypeError(key)

    for k, v in pdict.items():
        catalog[k] = [ v.get(i, '') for i in range(maxcnts[k] + 1) ]

    return (
     catalog, plural)


def _get_locale(request):
    language = request.GET.get(LANGUAGE_QUERY_PARAMETER)
    if not (language and check_for_language(language)):
        language = get_language()
    return to_locale(language)


def _parse_packages(packages):
    if packages is None:
        packages = list(DEFAULT_PACKAGES)
    elif isinstance(packages, six.string_types):
        packages = packages.split('+')
    return packages


def null_javascript_catalog(request, domain=None, packages=None):
    """
    Returns "identity" versions of the JavaScript i18n functions -- i.e.,
    versions that don't actually do anything.
    """
    return render_javascript_catalog()


def javascript_catalog(request, domain='djangojs', packages=None):
    """
    Returns the selected language catalog as a javascript library.

    Receives the list of packages to check for translations in the
    packages parameter either from an infodict or as a +-delimited
    string from the request. Default is 'django.conf'.

    Additionally you can override the gettext domain for this view,
    but usually you don't want to do that, as JavaScript messages
    go to the djangojs domain. But this might be needed if you
    deliver your JavaScript source from Django templates.
    """
    warnings.warn('The javascript_catalog() view is deprecated in favor of the JavaScriptCatalog view.', RemovedInDjango20Warning, stacklevel=2)
    locale = _get_locale(request)
    packages = _parse_packages(packages)
    catalog, plural = get_javascript_catalog(locale, domain, packages)
    return render_javascript_catalog(catalog, plural)


def json_catalog(request, domain='djangojs', packages=None):
    """
    Return the selected language catalog as a JSON object.

    Receives the same parameters as javascript_catalog(), but returns
    a response with a JSON object of the following format:

        {
            "catalog": {
                # Translations catalog
            },
            "formats": {
                # Language formats for date, time, etc.
            },
            "plural": '...'  # Expression for plural forms, or null.
        }
    """
    warnings.warn('The json_catalog() view is deprecated in favor of the JSONCatalog view.', RemovedInDjango20Warning, stacklevel=2)
    locale = _get_locale(request)
    packages = _parse_packages(packages)
    catalog, plural = get_javascript_catalog(locale, domain, packages)
    data = {'catalog': catalog, 
       'formats': get_formats(), 
       'plural': plural}
    return http.JsonResponse(data)


class JavaScriptCatalog(View):
    """
    Return the selected language catalog as a JavaScript library.

    Receives the list of packages to check for translations in the `packages`
    kwarg either from the extra dictionary passed to the url() function or as a
    plus-sign delimited string from the request. Default is 'django.conf'.

    You can override the gettext domain for this view, but usually you don't
    want to do that as JavaScript messages go to the djangojs domain. This
    might be needed if you deliver your JavaScript source from Django templates.
    """
    domain = 'djangojs'
    packages = None

    def get(self, request, *args, **kwargs):
        locale = get_language()
        domain = kwargs.get('domain', self.domain)
        packages = kwargs.get('packages', '')
        packages = packages.split('+') if packages else self.packages
        paths = self.get_paths(packages) if packages else None
        self.translation = DjangoTranslation(locale, domain=domain, localedirs=paths)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_paths(self, packages):
        allowable_packages = dict((app_config.name, app_config) for app_config in apps.get_app_configs())
        app_configs = [ allowable_packages[p] for p in packages if p in allowable_packages ]
        return [ os.path.join(app.path, 'locale') for app in app_configs ]

    def get_plural(self):
        plural = None
        if '' in self.translation._catalog:
            for line in self.translation._catalog[''].split('\n'):
                if line.startswith('Plural-Forms:'):
                    plural = line.split(':', 1)[1].strip()

        if plural is not None:
            plural = [ el.strip() for el in plural.split(';') if el.strip().startswith('plural=') ][0].split('=', 1)[1]
        return plural

    def get_catalog(self):
        pdict = {}
        maxcnts = {}
        catalog = {}
        trans_cat = self.translation._catalog
        trans_fallback_cat = self.translation._fallback._catalog if self.translation._fallback else {}
        for key, value in itertools.chain(six.iteritems(trans_cat), six.iteritems(trans_fallback_cat)):
            if key == '' or key in catalog:
                continue
            if isinstance(key, six.string_types):
                catalog[key] = value
            elif isinstance(key, tuple):
                msgid = key[0]
                cnt = key[1]
                maxcnts[msgid] = max(cnt, maxcnts.get(msgid, 0))
                pdict.setdefault(msgid, {})[cnt] = value
            else:
                raise TypeError(key)

        for k, v in pdict.items():
            catalog[k] = [ v.get(i, '') for i in range(maxcnts[k] + 1) ]

        return catalog

    def get_context_data(self, **kwargs):
        return {'catalog': self.get_catalog(), 
           'formats': get_formats(), 
           'plural': self.get_plural()}

    def render_to_response(self, context, **response_kwargs):

        def indent(s):
            return s.replace('\n', '\n  ')

        template = Engine().from_string(js_catalog_template)
        context['catalog_str'] = indent(json.dumps(context['catalog'], sort_keys=True, indent=2)) if context['catalog'] else None
        context['formats_str'] = indent(json.dumps(context['formats'], sort_keys=True, indent=2))
        return http.HttpResponse(template.render(Context(context)), 'text/javascript')


class JSONCatalog(JavaScriptCatalog):
    """
    Return the selected language catalog as a JSON object.

    Receives the same parameters as JavaScriptCatalog and returns a response
    with a JSON object of the following format:

        {
            "catalog": {
                # Translations catalog
            },
            "formats": {
                # Language formats for date, time, etc.
            },
            "plural": '...'  # Expression for plural forms, or null.
        }
    """

    def render_to_response(self, context, **response_kwargs):
        return http.JsonResponse(context)