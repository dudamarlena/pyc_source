# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/variant/utils.py
# Compiled at: 2015-09-15 01:59:29
from __future__ import unicode_literals
import logging
from django.conf import settings
from django.utils.text import slugify
from .models import Experiment
logger = logging.getLogger(__name__)

def get_experiment_variant(request, experiment_name, make_decision=True):
    try:
        if experiment_name in request.variant_experiments:
            return request.variant_experiments[experiment_name]
    except AttributeError:
        logger.warn(b'VariantMiddleware must be enabled for Variant experiments to be persistent.')
        request.variant_experiments = {}

    if not make_decision:
        return
    else:
        try:
            experiment = Experiment.objects.get(name=experiment_name, active=True)
        except Experiment.DoesNotExist:
            experiment = None
            variant = None

        if experiment:
            cookie_name = get_experiment_cookie_name(experiment_name)
            variant = request.COOKIES.get(cookie_name, None)
            if not variant or variant not in experiment.get_variants():
                variant = experiment.choose_variant()
        request.variant_experiments[experiment_name] = variant
        return variant


def get_experiment_cookie_name(experiment_name):
    cookie_pattern = getattr(settings, b'VARIANT_EXPERIMENT_COOKIE', b'dvc_{}')
    return slugify(cookie_pattern.format(experiment_name))