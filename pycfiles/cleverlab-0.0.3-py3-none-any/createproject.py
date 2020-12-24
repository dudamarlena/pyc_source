# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/plugins/createproject.py
# Compiled at: 2006-08-02 05:57:50
from paste.script.command import Command
from paste.script.create_distro import CreateDistroCommand
from paste.script.templates import Template

class HaroldTemplate(Template):
    """ Creates a Clever Harold project via 'paste create -t harold'

    """
    __module__ = __name__
    summary = 'A Clever Harold project'
    _template_dir = '../project/'
    egg_plugins = ['CleverHarold']
    required_templates = ['basic_package']
    use_cheetah = True


class HaroldCreate(Command):
    """ Creates a Clever Harold project via 'paste init-harold'

    """
    __module__ = __name__
    min_args = 0
    max_args = 1
    usage = 'NAME'
    summary = 'Create a new Clever Harold project'
    parser = Command.standard_parser(verbose=True)
    parser.add_option('-o', '--orm-type', dest='orm_type', metavar='ORM', help='Add initial models using specified ORM package.')

    def command(self):
        """ create a Clever Harold project

        """
        if self.verbose:
            print 'Creating new Clever Harold project...'
        c = CreateDistroCommand('harold')
        args = self.args
        args.append('-t CleverHarold#harold')
        c.parse_args(args)
        c.run(args)
        if self.verbose:
            print 'Clever Harold project created.'