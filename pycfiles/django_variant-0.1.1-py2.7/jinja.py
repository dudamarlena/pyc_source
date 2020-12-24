# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/variant/jinja.py
# Compiled at: 2015-09-15 01:59:29
import jinja2
from .utils import get_experiment_variant

@jinja2.contextfunction
def experiment_variant(context, experiment):
    try:
        request = context['request']
    except KeyError:
        return jinja2.Undefined('request must be defined in Context')

    return get_experiment_variant(request, experiment, make_decision=False)