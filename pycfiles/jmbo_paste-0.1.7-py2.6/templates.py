# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_paste/templates.py
# Compiled at: 2011-09-22 10:48:12
from os import path
from paste.script import command
from paste.script.templates import Template, var
from random import choice
SCRIPT_PATH = path.abspath(path.dirname(__file__))
from jmbo_paste.config import APP_CONFIG

class JmboProjectTemplate(Template):
    _template_dir = 'templates/jmbo_project'
    summary = 'Creates a Buildout providing a Django instance and Django project with selected Jmbo apps installed.'
    use_cheetah = True
    vars = [
     var('secret_key', 'The secret key for hashing algorithms', default=('').join([ choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)
                                                                             ])),
     var('hostname_prd', 'Production instance hostname', default='localhost'),
     var('hostname_staging', 'Staging instance hostname', default='localhost'),
     var('hostname_qa', 'Quality Assurance instance hostname', default='localhost'),
     var('hostname_dev', 'Development instance hostname', default='localhost')]

    def pre(self, command, output_dir, vars):
        app_keys = APP_CONFIG.keys()
        app_keys.sort()
        prompts = {}
        for key in app_keys:
            app = APP_CONFIG[key]
            if app.has_key('confirm'):
                if not app['confirm']:
                    continue
            prompts[key] = command.challenge('Install %s?: y/n' % key, 'y', True)

        required_apps_set = set()
        for (key, value) in prompts.items():
            if value == 'y':
                required_apps_set.add(key)
                if APP_CONFIG[key].has_key('installed_app_dependencies'):
                    for app in APP_CONFIG[key]['installed_app_dependencies']:
                        required_apps_set.add(app)

        required_apps = {}
        for app in required_apps_set:
            required_apps[app] = APP_CONFIG[app]

        vars['required_apps'] = required_apps
        for key in required_apps.keys():
            if key == 'django-recaptcha':
                public_key = command.challenge('Enter your Recaptcha Public Key: ', '', True)
                private_key = command.challenge('Enter your Recaptcha Private Key: ', '', True)
                vars['required_apps']['django-recaptcha']['settings'] = ("# Your ReCaptcha provided public key.\nRECAPTCHA_PUBLIC_KEY = '%s'\n\n# Your ReCaptcha provided private key.\nRECAPTCHA_PRIVATE_KEY = '%s'" % (public_key, private_key),)