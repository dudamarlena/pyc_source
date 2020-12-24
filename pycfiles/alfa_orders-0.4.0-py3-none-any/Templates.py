# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanousDesktop/Templates.py
# Compiled at: 2015-06-30 06:52:37
__doc__ = "\nThis module contains the html templates used in the GUI results. The reason \nthat we don't separate them in independent files, is to avoid the headache of \nincluding separated files in packaging.\n"
import os, codecs
from jinja2 import Template, Environment
from PySide import QtCore
from gettext import gettext, ngettext
env = Environment(extensions=['jinja2.ext.i18n'])
env.install_gettext_callables(gettext, ngettext)
base_path = os.path.dirname(__file__)
AYA_RESULTS_TEMPLATE = env.from_string(codecs.open(base_path + '/templates/aya_results.html', 'r', 'utf-8').read())
TRANSLATION_RESULTS_TEMPLATE = env.from_string(codecs.open(base_path + '/templates/translation_results.html', 'r', 'utf-8').read())