# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyneuroml/analysis/ChannelHelper.py
# Compiled at: 2018-09-10 05:44:50
from math import exp
from pyneuroml.pynml import get_value_in_si, print_comment_v

def evaluate_HHExpLinearRate(rate, midpoint, scale, v):
    rate_si = get_value_in_si(rate)
    midpoint_si = get_value_in_si(midpoint)
    scale_si = get_value_in_si(scale)
    v_si = get_value_in_si(v)
    print_comment_v('Evaluating: rate * ((v - (midpoint))/scale) / ( 1 - exp(-1 * (v - (midpoint)) / scale)) ')
    print_comment_v('            %s * ((v - (%s))/%s) / ( 1 - exp(-1 * (v - (%s)) / %s))  for v = %s' % (rate, midpoint, scale, midpoint, scale, v))
    print_comment_v('            %s * ((%s - (%s))/%s) / ( 1 - exp(-1 * (%s - (%s)) / %s)) ' % (rate_si, v_si, midpoint_si, scale_si, v_si, midpoint_si, scale_si))
    print_comment_v('            <... type="HHExpLinearRate" rate="%s" midpoint="%s" scale="%s" />' % (rate, midpoint, scale))
    r = rate_si * ((v_si - midpoint_si) / scale_si) / (1 - exp(-(v_si - midpoint_si) / scale_si))
    print_comment_v('   = %s per_s' % r)
    print_comment_v('   = %s per_ms' % (r / 1000.0))


def evaluate_HHSigmoidRate(rate, midpoint, scale, v):
    rate_si = get_value_in_si(rate)
    midpoint_si = get_value_in_si(midpoint)
    scale_si = get_value_in_si(scale)
    v_si = get_value_in_si(v)
    print_comment_v('Evaluating: rate / (1 + exp(-1 * (v - midpoint)/scale))  ')
    print_comment_v('            %s / ( 1 + exp(-1 * (v - (%s)) / %s))  for v = %s' % (rate, midpoint, scale, v))
    print_comment_v('            %s / ( 1 + exp(-1 * (%s - (%s)) / %s)) ' % (rate_si, v_si, midpoint_si, scale_si))
    print_comment_v('            <... type="HHSigmoidRate" rate="%s" midpoint="%s" scale="%s" />' % (rate, midpoint, scale))
    r = rate_si / (1 + exp(-1 * (v_si - midpoint_si) / scale_si))
    print_comment_v('   = %s per_s' % r)
    print_comment_v('   = %s per_ms' % (r / 1000.0))


def evaluate_HHExpRate(rate, midpoint, scale, v):
    rate_si = get_value_in_si(rate)
    midpoint_si = get_value_in_si(midpoint)
    scale_si = get_value_in_si(scale)
    v_si = get_value_in_si(v)
    print_comment_v('Evaluating: rate * exp( (v - midpoint) / scale) ')
    print_comment_v('            %s * exp( (v - (%s)) / %s)  for v = %s' % (rate, midpoint, scale, v))
    print_comment_v('            %s * exp( (%s - (%s)) / %s) ' % (rate_si, v_si, midpoint_si, scale_si))
    print_comment_v('            <... type="HHExpRate" rate="%s" midpoint="%s" scale="%s" />' % (rate, midpoint, scale))
    r = rate_si * exp((v_si - midpoint_si) / scale_si)
    print_comment_v('   = %s per_s' % r)
    print_comment_v('   = %s per_ms' % (r / 1000.0))