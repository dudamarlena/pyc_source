# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/tests/formfactoryapp/actions.py
# Compiled at: 2017-09-07 07:30:48
from formfactory import actions

@actions.register
def dummy_action(form_instance):
    return True


@actions.register
def dummy_wizard_action(form_dict, **kwargs):
    return True