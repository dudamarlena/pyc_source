# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ocfl/validation_logger.py
# Compiled at: 2020-04-07 15:26:24
# Size of source mod 2**32: 2984 bytes
"""OCFL Validation Logger.

Handle logging of validation errors and warnings.
"""
import json, os, os.path, re, logging

class ValidationLogger(object):
    __doc__ = 'Class for OCFL ValidationLogger.'
    validation_codes = None

    def __init__(self, warnings=False, lang='en'):
        """Initialize OCFL validation logger."""
        self.warnings = warnings
        self.lang = lang
        self.codes = {}
        self.messages = []
        self.num_errors = 0
        self.num_warnings = 0
        self.info = 0
        self.spec = 'https://ocfl.io/draft/spec/'
        if self.validation_codes is None:
            with open(os.path.join(os.path.dirname(__file__), 'data/validation-errors.json'), 'r') as (fh):
                self.validation_codes = json.load(fh)

    def error_or_warning(self, code, severity='error', **args):
        """Add error or warning to self.codes."""
        if code in self.validation_codes and 'description' in self.validation_codes[code]:
            desc = self.validation_codes[code]['description']
            lang_desc = None
            if self.lang in desc:
                lang_desc = desc[self.lang]
            else:
                if 'en' in desc:
                    lang_desc = desc['en']
                else:
                    if len(desc) > 0:
                        lang_desc = desc[sorted(list(desc.keys()))[0]]
                    else:
                        lang_desc = 'Unknown ' + severity + ': %s - no description, params (%s)'
        else:
            if 'params' in self.validation_codes[code]:
                params = []
                for param in self.validation_codes[code]['params']:
                    params.append(str(args[param]) if param in args else '???')

                try:
                    lang_desc = lang_desc % tuple(params)
                except TypeError:
                    lang_desc += str(args)

                message = '[' + code + '] ' + lang_desc
            else:
                message = 'Unknown ' + severity + ': %s - params (%s)' % (code, str(args))
            m = re.match('([EW](\\d\\d\\d))', code)
            if m:
                if int(m.group(2)) < 200:
                    message += ' (see ' + self.spec + '#' + m.group(1) + ')'
            self.codes[code] = message
            if severity == 'error' or self.warnings:
                self.messages.append(message)

    def error(self, code, **args):
        """Add error code to self.codes."""
        (self.error_or_warning)(code, severity='error', **args)
        self.num_errors += 1

    def warn(self, code, **args):
        """Add warning code to self.codes."""
        (self.error_or_warning)(code, severity='warning', **args)
        self.num_warnings += 1

    def __str__(self):
        """String of validator status."""
        s = ''
        for message in sorted(self.messages):
            s += message + '\n'

        return s