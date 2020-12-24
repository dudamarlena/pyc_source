# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/dprofiling/signals.py
# Compiled at: 2013-05-14 13:31:52
from logging import getLogger
from django.db.models.signals import pre_delete
from dprofiling.models import Profile
log = getLogger('dprofiling.signals')

def remove_dumps(sender, instance, **kwargs):
    if instance.dump:
        try:
            log.debug('Removing profile dump at %s' % (instance.dump.path,))
            instance.dump.delete(save=False)
        except:
            log.exception('Error removing a profile dump')


pre_delete.connect(remove_dumps, sender=Profile)