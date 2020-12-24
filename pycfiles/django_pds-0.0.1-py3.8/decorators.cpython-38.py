# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/rest/decorators.py
# Compiled at: 2020-04-29 11:29:15
# Size of source mod 2**32: 477 bytes
from django_pds.core.controllers.base import RequiredController

def required(*fields):

    def required_wrapper(func):

        def checking_required(*args, **kwargs):
            required_ctrl = RequiredController()
            request = args[1]
            error, response = (required_ctrl.required)(request, *fields)
            if error:
                return response
            return func(*args, **kwargs)

        return checking_required

    return required_wrapper