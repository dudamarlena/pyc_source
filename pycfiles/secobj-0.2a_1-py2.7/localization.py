# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/localization.py
# Compiled at: 2012-08-03 03:52:40
import secobj, gettext, os.path
DOMAIN = 'secobj'
LOCALEDIR = os.path.join(os.path.dirname(secobj.__file__), 'languages')
TRANSLATION = gettext.translation(DOMAIN, LOCALEDIR, fallback=True)
_ = TRANSLATION.ugettext