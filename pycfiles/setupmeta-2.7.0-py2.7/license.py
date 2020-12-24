# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setupmeta/license.py
# Compiled at: 2020-04-29 13:54:52
"""
Auto-fill license info (best-effort to cover the 5 top licenses...)

It's one of those annoying things, you're supposed to have:
- a LICENSE* file (copy-pasted legalese)
- a 'license' attribute in your metadata (short word(s), like "MIT")
- 'License :: OSI Approved :: ...' in your classifiers

Like the Shadoks say: why do simple when one can do complicated?
"""
import re
RE_VERSION = re.compile('version (\\d+(.\\d+)?)', re.IGNORECASE)

class License:

    def __init__(self, short, match=None):
        self.short = short
        self._match = match or short
        if not isinstance(self._match, list):
            self._match = [
             self._match]

    def match(self, contents):
        if not contents or any(m not in contents for m in self._match):
            return
        short = self.short
        version = None
        m = RE_VERSION.search(contents)
        if m:
            version = m.group(1)
        if self.short == 'GNU':
            pre = ''
            post = ''
            if 'LESSER' in contents:
                pre = 'Lesser '
            elif 'AFFERO' in contents:
                pre = 'Affero '
            if version:
                post = 'v%s' % version[0]
            short = '%sGPL%s' % (pre and pre[0], post)
        if short == 'Apache' and version:
            short = '%s %s' % (self.short, version)
        return short


BSD_CHATTER = [
 'Redistribution and use in source and binary forms', 'permitted provided that the following conditions']
KNOWN_LICENSES = [
 License('MIT', 'MIT License'),
 License('Apache', 'apache.org/licenses'),
 License('GNU'),
 License('MPL', 'Mozilla Public License'),
 License('BSD', BSD_CHATTER)]

def determined_license(contents):
    """
    :param str|None contents: Contents to determine license from
    :return tuple(str, str): Short name and classifier name
    """
    for license in KNOWN_LICENSES:
        short = license.match(contents)
        if short:
            return short