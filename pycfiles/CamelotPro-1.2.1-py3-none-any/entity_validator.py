# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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