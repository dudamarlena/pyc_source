# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/lib/regex.py
# Compiled at: 2016-04-19 10:47:47
"""
.. module:: regex
    :synopsis: Regexes to be used around the app.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""
from flask import current_app
from eventum.config import eventum_config

class _LiveRegexCollection(object):
    SLUG_REGEX = '[0-9a-zA-Z-]+'
    FILENAME_REGEX = '[\\w\\-@\\|\\(\\)]+'

    @property
    def FULL_FILENAME_REGEX(self):
        return ('{fname}({ext})').format(fname=self.FILENAME_REGEX, ext=('|').join(eventum_config.EVENTUM_ALLOWED_UPLOAD_EXTENSIONS))

    @property
    def EXTENSION_REGEX(self):
        return ('|').join(eventum_config.EVENTUM_ALLOWED_UPLOAD_EXTENSIONS)

    @property
    def VALID_PATHS(self):
        return ('^({}|http://|https://).*$').format(current_app.config['EVENTUM_BASEDIR'])


Regex = _LiveRegexCollection()