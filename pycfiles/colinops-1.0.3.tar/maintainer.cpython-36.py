# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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