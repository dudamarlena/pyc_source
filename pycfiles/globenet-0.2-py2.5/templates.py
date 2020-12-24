# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globenet/paste/templates.py
# Compiled at: 2008-08-26 14:23:46
from __future__ import with_statement
from paste.script import templates, command
import subprocess, os, yaml

class GlobenetTemplate(templates.Template):
    egg_plugins = [
     'globenet']
    summary = 'Template for creating a basic globenet package'
    _template_dir = 'project'
    use_cheetah = True

    def post(self, command, output_dir, vars):
        subprocess.Popen(['python', 'bootstrap.py', '--no-site-packages', 'env'], cwd=output_dir)


class ControllerTemplate(templates.Template):
    egg_plugins = [
     'globenet']
    summary = 'Template for creating globenet controllers'
    _template_dir = 'controller'
    use_cheeta = True


class GlobenetGenerate(command.Command):
    usage = 'CONTROLLER_NAME'
    summary = 'generate parts of your project'
    group_name = 'globenet'
    parser = command.Command.standard_parser(simulate=True, quiet=True, overwrite=True, interactive=True)

    def command(self):
        template = ControllerTemplate('controller')
        if not self.args:
            if self.interactive:
                controllername = self.challenge('Enter controller name')
            else:
                raise command.BadCommand('You must provider a CONTROLLER_NAME')
        else:
            controllername = self.args[0]
        vars = {'controller': controllername}
        vars.update(self.parse_vars(self.args[1:]))
        template.run(self, 'controllers', vars)
        if os.path.exists('config.ini'):
            with open('config.ini', 'r') as (f):
                c = f.read()
                config = yaml.load(c)
        else:
            config = {}
        if 'controllers' not in config:
            config['controllers'] = []
        config['controllers'].append({'class': 'controllers.%s.%s' % (controllername, controllername.capitalize()), 
           'url': controllername})
        with open('config.ini', 'w+') as (f):
            f.write(yaml.dump(config))