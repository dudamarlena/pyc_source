# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alfanousDesktop/Templates.py
# Compiled at: 2015-06-30 06:52:37
"""
This module contains the html templates used in the GUI results. The reason 
that we don't separate them in independent files, is to avoid the headache of 
including separated files in packaging.
"""
import os, codecs
from jinja2 import Template, Environment
from PySide import QtCore
from gettext import gettext, ngettext
env = Environment(extensions=['jinja2.ext.i18n'])
env.install_gettext_callables(gettext, ngettext)
base_path = os.path.dirname(__file__)
AYA_RESULTS_TEMPLATE = env.from_string(codecs.open(base_path + '/templates/aya_results.html', 'r', 'utf-8').read())
TRANSLATION_RESULTS_TEMPLATE = env.from_string(codecs.open(base_path + '/templates/translation_results.html', 'r', 'utf-8').read())