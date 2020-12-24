# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/djangosampler/sampler.py
# Compiled at: 2015-11-17 05:08:04
from datetime import datetime
from time import time
import json, random, traceback
from django.conf import settings
from django.db.models import F
from django.db.utils import DatabaseError
from django.utils.encoding import force_unicode
from models import Query, Sample, Stack
USE_COST = getattr(settings, 'DJANGO_SAMPLER_USE_COST', False)
FREQ = float(getattr(settings, 'DJANGO_SAMPLER_FREQ', 0))
BASE_TIME = float(getattr(settings, 'DJANGO_SAMPLER_BASE_TIME', 0.005))

def _get_tidy_stacktrace():
    """Gets a tidy stacktrace. The tail of the stack is removed to exclude
    sampler internals. Will return a stack printed cleanly and without any
    trace of djangosampler.
    """
    stack = traceback.extract_stack()
    tidy_stack = []
    for trace in stack[:-3]:
        if 'djangosampler' in trace[0] and '/sampler.py' in trace[0]:
            continue
        else:
            tidy_stack.append('%s:%s (%s): %s' % trace)

    return ('\n').join(tidy_stack)


def _calculate_bias(time):
    bias = time / BASE_TIME
    if FREQ * bias > 1:
        bias = 1 / FREQ
    return bias


def _calculate_cost(time):
    if USE_COST:
        bias = _calculate_bias(time)
        cost = time / bias
        return cost
    else:
        return 0.0


def _json_params(params):
    try:
        return json.dumps([ force_unicode(x) for x in params ])
    except TypeError:
        return ''


def should_sample(time):
    """Determines if a sample should be taken. The probability of this will
    be multiplied by the time if cost-based sampling is enabled.
    """
    if not FREQ:
        return False
    else:
        if USE_COST:
            bias = _calculate_bias(time)
            return random.random() > 1 - FREQ * bias
        return random.random() < FREQ


def drop_exceptions(fn):
    """Decorator that makes the given method drop any exceptions that fall out of
    it. This is useful when doing sampling as it ensures that the sampler cannot
    cause a breakage.
    """

    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except:
            pass

    return wrapped


@drop_exceptions
def sample(query_type, query, time, params):
    """Main method that records the given query.

    The params argument will be
    recorded alongside individual samples as a JSON object. It is a suitable
    place to store things like SQL parameters.
    """
    if 'djangosampler' in query:
        return
    stack = _get_tidy_stacktrace()
    date_now = datetime.now().date()
    stack_hash = hash((date_now, tuple(stack), query))
    query_hash = hash((date_now, query_type, query))
    try:
        query_model, _ = Query.objects.get_or_create(hash=query_hash, defaults={'query_type': query_type, 
           'query': query})
    except DatabaseError:
        return

    try:
        stack_model, _ = Stack.objects.get_or_create(hash=stack_hash, defaults={'stack': stack, 'query': query_model})
    except DatabaseError:
        return

    cost = _calculate_cost(time)
    params = _json_params(params)
    try:
        Sample.objects.create(query=query, params=params, duration=time, cost=cost, stack=stack_model)
    except DatabaseError:
        return

    Stack.objects.filter(hash=stack_hash).update(total_duration=F('total_duration') + time, total_cost=F('total_cost') + cost, count=F('count') + 1)
    Query.objects.filter(hash=query_hash).update(total_duration=F('total_duration') + time, total_cost=F('total_cost') + cost, count=F('count') + 1)


class sampling:

    def __init__(self, sample_type, sample_key, params=()):
        self.sample_type = sample_type
        self.sample_key = sample_key
        self.params = params

    def __enter__(self):
        self.start_time = time()
        return self

    def __exit__(self, type, value, traceback):
        end_time = time()
        duration = end_time - self.start_time
        if should_sample(duration):
            sample(self.sample_type, self.sample_key, duration, self.params)
        return False