# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\i18n\tests\test_tg_gettext.py
# Compiled at: 2011-07-14 06:03:33
from turbogears.i18n.tg_gettext import *

def test_gettext():
    assert unicode(gettext('Welcome')) == 'Welcome'
    assert unicode(gettext('Welcome', 'en')) == 'Welcome'
    assert unicode(gettext('Welcome', 'fi')) == 'Tervetuloa'
    assert unicode(gettext('Welcome', 'fi_FI')) == 'Tervetuloa'


def test_invalid_domain():
    assert gettext('Welcome', 'fi', 'fubar') != 'Tervetuloa'


def test_is_unsupported_locale():
    assert is_locale_supported('en') == True
    assert is_locale_supported('en-gb') == False
    assert is_locale_supported('de') == False
    assert is_locale_supported('en', 'fubar') == False


def test_gettext_unsupported_locale():
    assert unicode(gettext('Welcome', 'en-gb')) == 'Welcome'
    assert unicode(gettext('Welcome', 'de')) == 'Welcome'


def test_ngettext():
    assert ngettext('You have %i apple', 'You have %i apples', 1) % 1 == 'You have 1 apple'
    assert ngettext('You have %i apple', 'You have %i apples', 1, 'fi') % 1 == 'Sinulla on 1 omena'
    assert ngettext('You have %i apple', 'You have %i apples', 3) % 3 == 'You have 3 apples'
    assert ngettext('You have %i apple', 'You have %i apples', 3, 'fi') % 3 == 'Sinulla on 3 omenaa'


def test_lazystring():
    s1 = lazystring(('simple').upper)
    assert s1 == 'SIMPLE'
    assert s1 != 'HARD'
    assert s1 > 'HARD' or s1 < 'HARD'