# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_payload_validator/views.py
# Compiled at: 2018-02-05 10:47:32
# Size of source mod 2**32: 179 bytes
from validator_views import BaseValidatorView
from payload_validator import CreateTeamValidator

class CreateTeam(BaseValidatorView):
    payload_validator = CreateTeamValidator