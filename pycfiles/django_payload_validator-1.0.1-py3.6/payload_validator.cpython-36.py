# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_payload_validator/payload_validator.py
# Compiled at: 2018-02-05 10:47:32
# Size of source mod 2**32: 576 bytes
from base_payload_validator import BasePayloadValidator

class CreateTeamValidator(BasePayloadValidator):
    validation_rule = {'fields':{'name':{'type':str, 
       'required':True}, 
      'description':{'type':str, 
       'required':True}, 
      'team_type':{'type':str, 
       'required':True,  'allowed_values':['tech', 'management', 'business', 'marketing']}, 
      'members':{'type': list}}, 
     'auto_populate_fields':{'created_by':'request.user', 
      'last_updated_by':'request.user'}, 
     'excluded_fields':[
      'members']}