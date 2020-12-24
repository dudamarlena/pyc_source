# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/emr/bootstrap_action.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1830 bytes
from boto.compat import six

class BootstrapAction(object):

    def __init__(self, name, path, bootstrap_action_args):
        self.name = name
        self.path = path
        if isinstance(bootstrap_action_args, six.string_types):
            bootstrap_action_args = [
             bootstrap_action_args]
        self.bootstrap_action_args = bootstrap_action_args

    def args(self):
        args = []
        if self.bootstrap_action_args:
            args.extend(self.bootstrap_action_args)
        return args

    def __repr__(self):
        return '%s.%s(name=%r, path=%r, bootstrap_action_args=%r)' % (
         self.__class__.__module__, self.__class__.__name__,
         self.name, self.path, self.bootstrap_action_args)