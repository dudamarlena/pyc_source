# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/individuals/templatetags/get_genotype.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 629 bytes
from django import template
register = template.Library()

@register.filter
def get_genotype(variant):
    """Removes all values of arg from the given string"""
    genotype = variant.genotype
    if genotype == '0/0':
        return '(%s;%s)' % (variant.ref, variant.ref)
    if genotype == '0/1':
        return '(%s;%s)' % (variant.ref, variant.alt)
    if genotype == '1/0':
        return '(%s;%s)' % (variant.alt, variant.ref)
    if genotype == '1/1':
        return '(%s;%s)' % (variant.alt, variant.alt)
    return 'ref:%s, alt:%s, genotype:%s' % (variant.ref, variant.alt, variant.genotype)