# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/vagrantplaybook/ansible.py
# Compiled at: 2017-11-02 18:07:24
from __future__ import absolute_import, division, print_function
__metaclass__ = type
from vagrantplaybook.compat import compat_text_type, to_str
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
ansible_tempar = Templar
ansible_loader = DataLoader

def ansible_unwrap(value):
    """ utility function for unwrapping values generated

    Keyword arguments:
    value           --  Generated value
    """
    if isinstance(value, compat_text_type):
        return to_str(value)
    else:
        if isinstance(value, list):
            return [ ansible_unwrap(i) for i in value ]
        if isinstance(value, dict):
            return {ansible_unwrap(k):ansible_unwrap(v) for k, v in value.iteritems()}
        return value