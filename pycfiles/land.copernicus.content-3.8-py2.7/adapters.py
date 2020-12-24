# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/rules/download/adapters.py
# Compiled at: 2017-11-01 05:34:47
from datetime import datetime
from operator import methodcaller
from itertools import imap as map
from plone.stringinterp.adapters import BaseSubstitution
import plone.api as api
from land.copernicus.content.config import EEAMessageFactory as _
from land.copernicus.content.browser.download import _friendly_date

def _starlist(filenames):
    joiner = '\n* '
    return joiner + joiner.join(filenames)


class UserName(BaseSubstitution):
    category = _('Async download')
    description = _('User full name')

    def safe_call(self):
        user = api.user.get(userid=self.wrapper.userid)
        return user.getProperty('fullname') or ''


class UserEmail(BaseSubstitution):
    category = _('Async download')
    description = _('User email')

    def safe_call(self):
        user = api.user.get(self.wrapper.userid)
        return user.getProperty('email')


class ExpDate(BaseSubstitution):
    category = _('Async download')
    description = _('Download expiration date')

    def safe_call(self):
        expires = datetime.fromtimestamp(self.wrapper.exp_time)
        return _friendly_date(expires)


class FilesComma(BaseSubstitution):
    category = _('Async download')
    description = _('List of files, comma separated')

    def safe_call(self):
        return (', ').join(self.wrapper.filenames)


class FilesStar(BaseSubstitution):
    category = _('Async download')
    description = _('List of files, newline and leading *')

    def safe_call(self):
        return _starlist(self.wrapper.filenames)


class NumFiles(BaseSubstitution):
    category = _('Async download')
    description = _('Number of files')

    def safe_call(self):
        return len(self.wrapper.filenames)


def _missing_list(filenames):
    if filenames:
        return ('\nThe following {} files are missing and are not included in the archive: \n {}.\n').format(len(filenames), _starlist(filenames))
    return ''


class MissingFiles(BaseSubstitution):
    category = _('Async download')
    description = _('Missing files block')

    def safe_call(self):
        return _missing_list(self.wrapper.missing_files) or ''


class URL(BaseSubstitution):
    category = _('Async download')
    description = _('Download URL')

    def safe_call(self):
        return self.wrapper.done_url