# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/z3cform/kss/form.py
# Compiled at: 2008-06-17 13:02:24
"""
collective.z3cform.kss

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: form.py 66814 2008-06-17 16:42:27Z jfroche $
"""
import os
from z3c.form.form import FormTemplateFactory
from z3c.form.interfaces import IForm
import collective.z3cform.kss
path = lambda p: os.path.join(os.path.dirname(collective.z3cform.kss.__file__), p)
form_factory = FormTemplateFactory(path('form.pt'), form=IForm)