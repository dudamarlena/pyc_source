# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/checks/labels/maintainer.py
# Compiled at: 2018-04-05 06:15:36
# Size of source mod 2**32: 647 bytes
from colin.checks.abstract.labels import LabelCheck

class MaintainerCheck(LabelCheck):

    def __init__(self):
        super().__init__(name='maintainer_label_required', message="Label 'maintainer' has to be specified.",
          description='The name and email of the maintainer (usually the submitter).',
          reference_url='https://fedoraproject.org/wiki/Container:Guidelines#LABELS',
          tags=[
         'maintainer', 'label', 'required'],
          label='maintainer',
          required=True,
          value_regex=None)