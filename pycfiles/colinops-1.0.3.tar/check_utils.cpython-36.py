# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/colin/core/checks/check_utils.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 1005 bytes
import re

def check_label(labels, required, value_regex, target_labels):
    """
    Check if the label is required and match the regex

    :param labels: [str]
    :param required: bool (if the presence means pass or not)
    :param value_regex: str
    :param target_labels: [str]
    :return: bool (required==True: True if the label is present and match the regex if specified)
                    (required==False: True if the label is not present)
    """
    present = target_labels is not None and not set(labels).isdisjoint(set(target_labels))
    if present:
        if required:
            if not value_regex:
                return True
        if value_regex:
            pattern = re.compile(value_regex)
            present_labels = set(labels) & set(target_labels)
            for l in present_labels:
                if not bool(pattern.match(target_labels[l])):
                    return False

            return True
        else:
            return False
    else:
        return not required