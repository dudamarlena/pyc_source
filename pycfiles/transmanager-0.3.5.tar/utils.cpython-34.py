# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/utils.py
# Compiled at: 2016-06-01 06:08:22
# Size of source mod 2**32: 1568 bytes
import re
from django.contrib.contenttypes.models import ContentType
from hvad.models import TranslatableModel

def get_application_choices():
    """
    Get the select options for the application selector

    :return:
    """
    result = []
    keys = set()
    for ct in ContentType.objects.order_by('app_label', 'model'):
        try:
            if issubclass(ct.model_class(), TranslatableModel):
                if ct.app_label not in keys:
                    result.append(('{}'.format(ct.app_label), '{}'.format(ct.app_label.capitalize())))
                    keys.add(ct.app_label)
        except TypeError:
            continue

    return result


def get_model_choices():
    """
    Get the select options for the model selector

    :return:
    """
    result = []
    for ct in ContentType.objects.order_by('app_label', 'model'):
        try:
            if issubclass(ct.model_class(), TranslatableModel):
                result.append((
                 '{} - {}'.format(ct.app_label, ct.model.lower()),
                 '{} - {}'.format(ct.app_label.capitalize(), ct.model_class()._meta.verbose_name_plural)))
        except TypeError:
            continue

    return result


def get_num_words(text):
    """
    Counts and returns the number of words found in a given text

    :param text:
    :return:
    """
    try:
        word_regexp_pattern = re.compile('[a-zA-Záéíóúñ]+')
        num_words = re.findall(word_regexp_pattern, text)
        return len(num_words)
    except TypeError:
        return 0