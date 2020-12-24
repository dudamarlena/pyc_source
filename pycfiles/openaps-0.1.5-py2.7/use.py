# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/uses/use.py
# Compiled at: 2015-12-15 13:09:24
"""
use - module for openaps devices to re-use

"""
from openaps.cli.subcommand import Subcommand

class Use(Subcommand):
    """A no-op base use.
    A Use is a mini well-behaved linux application.
    openaps framework will initialize your Use with a `method` and
    `parent` objects, which are contextual objects within openaps.
  """

    def __init__(self, method=None, parent=None):
        self.method = method
        self.name = self.__class__.__name__.split('.').pop()
        self.parent = parent
        self.device = parent.device

    def main(self, args, app):
        """
    Put main app logic here.
    print "HAHA", args, app
    """
        pass

    def to_ini(self, args):
        return self.get_params(args)

    def from_ini(self, fields):
        return fields

    def get_params(self, args):
        """
    Return dictionary of all parameters collected from args.
    """
        return dict()

    def before_main(self, args, app):
        pass

    def after_main(self, args, app):
        pass

    def __call__(self, args, app):
        """
      openaps will use this to interface with your app.
    """
        self.before_main(args, app)
        output = self.main(args, app)
        self.after_main(args, app)
        return output