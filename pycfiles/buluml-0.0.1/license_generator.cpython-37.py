# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bulrush/license_generator.py
# Compiled at: 2019-06-14 12:05:42
# Size of source mod 2**32: 1456 bytes
from collections import Mapping
import re
_HTML = '\n<ul class="menu-list">\n  <li>\n    <a rel="license" href="{url}">\n      <span class="icon is-small">\n        <i class="fa fa-{icon} fa-fw"></i>\n      </span>\n      <span>{content}</span>\n    </a>\n  </li>\n</ul>\n'
_DEFAULT_ICON = 'file-text-o'
_CC_LICENSE = re.compile('CC([-\\s])(?P<type>[A-Z-]+)\\1(?P<version>[\\d.]+)',
  flags=(re.VERBOSE | re.IGNORECASE))

def generate_license(license_):
    if isinstance(license_, Mapping):
        try:
            return _format_license(**license_)
        except TypeError:
            return ''

    return _generate_named_license(str(license_))


def _generate_named_license(license_name):
    if _CC_LICENSE.match(license_name):
        return _format_license(**_generate_cc_license(license_name))
    return _format_license(**_generate_generic_license(license_name))


def _format_license(*, name, icon=_DEFAULT_ICON, url):
    return _HTML.format(url=url, icon=icon, content=name)


def _generate_generic_license(license_name):
    return dict(name=license_name, icon=_DEFAULT_ICON, url='#')


def _generate_cc_license(license_name):
    match = _CC_LICENSE.match(license_name)
    type_ = match.group('type').lower()
    version = match.group('version')
    url = 'http://creativecommons.org/licenses/{}/{}/'.format(type_, version)
    name = 'CC {} {}'.format(type_.upper(), version)
    return dict(name=name, icon='creative-commons', url=url)