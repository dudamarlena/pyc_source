# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/donn/Projects/pythoning/fui/trunk/fuimodules/i18n.py
# Compiled at: 2008-01-25 06:45:35
import locale, gettext, sys, os
root = __file__
if os.path.islink(root):
    root = os.path.realpath(root)
moduleroot = os.path.dirname(os.path.abspath(root))
localedir = os.path.join(moduleroot, 'locale')
try:
    loc = locale.setlocale(locale.LC_ALL, '')
except:
    print 'And now for something completely different...'
    print 'setlocale failed. Please report this to us.'
    raise SystemExit

domain = 'all'
gettext.install(domain, localedir, unicode=True)
try:
    lang = gettext.translation(domain, localedir, languages=[loc])
    lang.install(unicode=True)
except IOError:
    pass