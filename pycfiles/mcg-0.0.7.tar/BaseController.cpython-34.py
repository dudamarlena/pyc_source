# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/cli/BaseController.py
# Compiled at: 2017-01-25 07:33:25
# Size of source mod 2**32: 1084 bytes
from cement.core.controller import CementBaseController, expose
from core.Manager import Manager
VERSION = '0.0.6'
BANNER = '\nMeteor Crud Generator v%s\nCopyright (c) 2017 Bizarro Solutions\n' % VERSION

class BaseController(CementBaseController):

    class Meta:
        label = 'base'
        description = 'MCG generates backend and unit tests for a Meteor Application'
        epilog = 'Suggestions or bugs must be reported to info@bizarro.solutions'
        arguments = [
         (
          [
           '-v', '--version'],
          dict(action='version', version=BANNER)),
         (
          [
           '-p', '--project'],
          dict(help='Option to create a Meteor Project')),
         (
          [
           '-a', '--api'],
          dict(help='Option to create a Meteor Api'))]

    @expose(hide=True, aliases=['run'])
    def default(self):
        self.app.log.info('Run command. [default] Function')

    @expose(help='Create command. [create] Function')
    def create(self):
        manager = Manager({'project': self.app.pargs.project,  'api': self.app.pargs.api})
        manager.begin()