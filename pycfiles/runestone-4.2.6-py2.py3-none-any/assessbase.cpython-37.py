# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/mchoice/assessbase.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 1948 bytes
__author__ = 'bmiller'
from runestone.common.runestonedirective import RunestoneIdDirective
_base_js_escapes = (('\\', '\\u005C'), ("'", '\\u0027'), ('"', '\\u0022'), ("'", '\\u0027'),
                    ('>', '\\u003E'), ('<', '\\u003C'), ('&', '\\u0026'), ('=', '\\u003D'),
                    ('-', '\\u002D'), (';', '\\u003B'), ('\u2028', '\\u2028'), ('\u2029', '\\u2029'))
_js_escapes = _base_js_escapes + tuple([('%c' % z, '\\u%04X' % z) for z in range(32)])

def escapejs(value):
    """Hex encodes characters for use in JavaScript strings."""
    if not isinstance(value, str):
        value = str(value)
    for bad, good in _js_escapes:
        value = value.replace(bad, good)

    return value


class Assessment(RunestoneIdDirective):
    __doc__ = 'Base Class for assessments'

    def run(self):
        super(Assessment, self).run()
        if self.content:
            if 'iscode' in self.options:
                self.options['bodytext'] = '<pre>' + '\n'.join(self.content) + '</pre>'
            else:
                self.options['bodytext'] = '\n'.join(self.content)
        else:
            self.options['bodytext'] = '\n'