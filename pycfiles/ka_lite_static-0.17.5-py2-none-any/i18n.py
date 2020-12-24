# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/views/i18n.py
# Compiled at: 2018-07-11 18:15:30
import os, gettext as gettext_module
from django import http
from django.conf import settings
from django.utils import importlib
from django.utils.translation import check_for_language, activate, to_locale, get_language
from django.utils.text import javascript_quote
from django.utils.encoding import smart_text
from django.utils.formats import get_format_modules, get_format
from django.utils._os import upath
from django.utils.http import is_safe_url
from django.utils import six

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
    next = request.REQUEST.get('next')
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
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
    for module in [settings] + get_format_modules(reverse=True):
        for attr in FORMAT_SETTINGS:
            result[attr] = get_format(attr)

    src = []
    for k, v in result.items():
        if isinstance(v, (six.string_types, int)):
            src.append("formats['%s'] = '%s';\n" % (javascript_quote(k), javascript_quote(smart_text(v))))
        elif isinstance(v, (tuple, list)):
            v = [ javascript_quote(smart_text(value)) for value in v ]
            src.append("formats['%s'] = ['%s'];\n" % (javascript_quote(k), ("', '").join(v)))

    return ('').join(src)


NullSource = '\n/* gettext identity library */\n\nfunction gettext(msgid) { return msgid; }\nfunction ngettext(singular, plural, count) { return (count == 1) ? singular : plural; }\nfunction gettext_noop(msgid) { return msgid; }\nfunction pgettext(context, msgid) { return msgid; }\nfunction npgettext(context, singular, plural, count) { return (count == 1) ? singular : plural; }\n'
LibHead = '\n/* gettext library */\n\nvar catalog = new Array();\n'
LibFoot = "\n\nfunction gettext(msgid) {\n  var value = catalog[msgid];\n  if (typeof(value) == 'undefined') {\n    return msgid;\n  } else {\n    return (typeof(value) == 'string') ? value : value[0];\n  }\n}\n\nfunction ngettext(singular, plural, count) {\n  value = catalog[singular];\n  if (typeof(value) == 'undefined') {\n    return (count == 1) ? singular : plural;\n  } else {\n    return value[pluralidx(count)];\n  }\n}\n\nfunction gettext_noop(msgid) { return msgid; }\n\nfunction pgettext(context, msgid) {\n  var value = gettext(context + '\\x04' + msgid);\n  if (value.indexOf('\\x04') != -1) {\n    value = msgid;\n  }\n  return value;\n}\n\nfunction npgettext(context, singular, plural, count) {\n  var value = ngettext(context + '\\x04' + singular, context + '\\x04' + plural, count);\n  if (value.indexOf('\\x04') != -1) {\n    value = ngettext(singular, plural, count);\n  }\n  return value;\n}\n"
LibFormatHead = '\n/* formatting library */\n\nvar formats = new Array();\n\n'
LibFormatFoot = "\nfunction get_format(format_type) {\n    var value = formats[format_type];\n    if (typeof(value) == 'undefined') {\n      return format_type;\n    } else {\n      return value;\n    }\n}\n"
SimplePlural = '\nfunction pluralidx(count) { return (count == 1) ? 0 : 1; }\n'
InterPolate = '\nfunction interpolate(fmt, obj, named) {\n  if (named) {\n    return fmt.replace(/%\\(\\w+\\)s/g, function(match){return String(obj[match.slice(2,-2)])});\n  } else {\n    return fmt.replace(/%s/g, function(match){return String(obj.shift())});\n  }\n}\n'
PluralIdx = "\nfunction pluralidx(n) {\n  var v=%s;\n  if (typeof(v) == 'boolean') {\n    return v ? 1 : 0;\n  } else {\n    return v;\n  }\n}\n"

def null_javascript_catalog(request, domain=None, packages=None):
    """
    Returns "identity" versions of the JavaScript i18n functions -- i.e.,
    versions that don't actually do anything.
    """
    src = [
     NullSource, InterPolate, LibFormatHead, get_formats(), LibFormatFoot]
    return http.HttpResponse(('').join(src), 'text/javascript')


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
    if request.GET:
        if 'language' in request.GET:
            if check_for_language(request.GET['language']):
                activate(request.GET['language'])
    if packages is None:
        packages = [
         'django.conf']
    if isinstance(packages, six.string_types):
        packages = packages.split('+')
    packages = [ p for p in packages if p == 'django.conf' or p in settings.INSTALLED_APPS ]
    default_locale = to_locale(settings.LANGUAGE_CODE)
    locale = to_locale(get_language())
    t = {}
    paths = []
    en_selected = locale.startswith('en')
    en_catalog_missing = True
    for package in packages:
        p = importlib.import_module(package)
        path = os.path.join(os.path.dirname(upath(p.__file__)), 'locale')
        paths.append(path)

    paths.extend(list(reversed(settings.LOCALE_PATHS)))
    for path in paths:
        try:
            catalog = gettext_module.translation(domain, path, ['en'])
            t.update(catalog._catalog)
        except IOError:
            pass
        else:
            if en_selected:
                en_catalog_missing = False

    if default_locale != 'en':
        for path in paths:
            try:
                catalog = gettext_module.translation(domain, path, [default_locale])
            except IOError:
                catalog = None

            if catalog is not None:
                t.update(catalog._catalog)

    if locale != default_locale:
        if en_selected and en_catalog_missing:
            t = {}
        else:
            locale_t = {}
            for path in paths:
                try:
                    catalog = gettext_module.translation(domain, path, [locale])
                except IOError:
                    catalog = None

                if catalog is not None:
                    locale_t.update(catalog._catalog)

            if locale_t:
                t = locale_t
    src = [
     LibHead]
    plural = None
    if '' in t:
        for l in t[''].split('\n'):
            if l.startswith('Plural-Forms:'):
                plural = l.split(':', 1)[1].strip()

    if plural is not None:
        plural = [ el.strip() for el in plural.split(';') if el.strip().startswith('plural=') ][0].split('=', 1)[1]
        src.append(PluralIdx % plural)
    else:
        src.append(SimplePlural)
    csrc = []
    pdict = {}
    for k, v in t.items():
        if k == '':
            continue
        if isinstance(k, six.string_types):
            csrc.append("catalog['%s'] = '%s';\n" % (javascript_quote(k), javascript_quote(v)))
        elif isinstance(k, tuple):
            if k[0] not in pdict:
                pdict[k[0]] = k[1]
            else:
                pdict[k[0]] = max(k[1], pdict[k[0]])
            csrc.append("catalog['%s'][%d] = '%s';\n" % (javascript_quote(k[0]), k[1], javascript_quote(v)))
        else:
            raise TypeError(k)

    csrc.sort()
    for k, v in pdict.items():
        src.append("catalog['%s'] = [%s];\n" % (javascript_quote(k), (',').join(["''"] * (v + 1))))

    src.extend(csrc)
    src.append(LibFoot)
    src.append(InterPolate)
    src.append(LibFormatHead)
    src.append(get_formats())
    src.append(LibFormatFoot)
    src = ('').join(src)
    return http.HttpResponse(src, 'text/javascript')