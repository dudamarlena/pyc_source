# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/core/checks/labels.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 2739 bytes
from ..result import CheckResult
from .check_utils import check_label
from .containers import ContainerAbstractCheck
from .dockerfile import DockerfileAbstractCheck
from .images import ImageAbstractCheck

class LabelAbstractCheck(ContainerAbstractCheck, ImageAbstractCheck, DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, labels, required, value_regex=None):
        super(LabelAbstractCheck, self).__init__(message, description, reference_url, tags)
        self.labels = labels
        self.required = required
        self.value_regex = value_regex

    def check(self, target):
        passed = check_label(labels=(self.labels), required=(self.required),
          value_regex=(self.value_regex),
          target_labels=(target.labels))
        return CheckResult(ok=passed, description=(self.description),
          message=(self.message),
          reference_url=(self.reference_url),
          check_name=(self.name),
          logs=[])


class DeprecatedLabelAbstractCheck(ContainerAbstractCheck, ImageAbstractCheck, DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, old_label, new_label):
        super(DeprecatedLabelAbstractCheck, self).__init__(message, description, reference_url, tags)
        self.old_label = old_label
        self.new_label = new_label

    def check(self, target):
        labels = target.labels
        old_present = labels is not None and self.old_label in labels
        passed = not old_present or self.new_label in labels
        return CheckResult(ok=passed, description=(self.description),
          message=(self.message),
          reference_url=(self.reference_url),
          check_name=(self.name),
          logs=[])