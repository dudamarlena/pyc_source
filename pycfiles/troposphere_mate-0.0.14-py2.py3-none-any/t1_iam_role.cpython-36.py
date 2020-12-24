# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/orch_example/web_app/app1_micro_service/t1_iam_role.py
# Compiled at: 2019-08-08 16:17:45
# Size of source mod 2**32: 446 bytes
try:
    from typing import List
except:
    pass

from troposphere_mate import ec2
from troposphere_mate import Select, GetAZs, Ref, Tags, Template, Parameter, Output
from troposphere_mate.orch_example.web_app.config import Config

class PrereqTier(Config):
    rel_path = '02-sg.json'

    def do_create_template(self, **kwargs):
        template = Template()
        template.add_parameter(Parameter(Type='string'))