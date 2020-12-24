# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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