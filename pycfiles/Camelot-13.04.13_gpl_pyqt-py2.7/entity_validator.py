# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/entity_validator.py
# Compiled at: 2013-04-11 17:47:52
from camelot.admin.validator.entity_validator import EntityValidator
from camelot.admin.entity_admin import EntityAdmin

class PersonValidator(EntityValidator):

    def objectValidity(self, entity_instance):
        messages = super(PersonValidator, self).objectValidity(entity_instance)
        if not entity_instance.first_name or len(entity_instance.first_name) < 3:
            messages.append("A person's first name should be at least 2 characters long")
        return messages


class Admin(EntityAdmin):
    verbose_name = 'Person'
    list_display = ['first_name', 'last_name']
    validator = PersonValidator