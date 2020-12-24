# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/util/paste_templates.py
# Compiled at: 2007-09-30 15:56:52
from paste.script import templates

class OortAppTemplate(templates.Template):
    summary = 'A clean Oort web app package'
    _template_dir = 'paste_templates/oort_app'
    required_templates = ['basic_package']
    use_cheetah = False