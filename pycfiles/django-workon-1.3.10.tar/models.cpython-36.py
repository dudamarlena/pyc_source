# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/LEPOLE/workon/utils/models.py
# Compiled at: 2018-01-19 22:56:12
# Size of source mod 2**32: 168 bytes
__all__ = [
 'm2m_auto_create']

def m2m_auto_create(instance, field_name, active=True):
    getattr(instance._meta.model, field_name).through._meta.auto_created = active