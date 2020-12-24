# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/z3cform/kss/form.py
# Compiled at: 2008-06-17 13:02:24
__doc__ = '\ncollective.z3cform.kss\n\nLicensed under the GPL license, see LICENCE.txt for more details.\nCopyright by Affinitic sprl\n\n$Id: form.py 66814 2008-06-17 16:42:27Z jfroche $\n'
import os
from z3c.form.form import FormTemplateFactory
from z3c.form.interfaces import IForm
import collective.z3cform.kss
path = lambda p: os.path.join(os.path.dirname(collective.z3cform.kss.__file__), p)
form_factory = FormTemplateFactory(path('form.pt'), form=IForm)