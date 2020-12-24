# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteDeploy-1.5.0-py2.6.egg/paste/deploy/paster_templates.py
# Compiled at: 2012-02-27 07:41:55
import os
from paste.script.templates import Template
from paste.deploy.compat import print_

class PasteDeploy(Template):
    _template_dir = 'paster_templates/paste_deploy'
    summary = 'A web application deployed through paste.deploy'
    egg_plugins = [
     'PasteDeploy']
    required_templates = [
     'PasteScript#basic_package']

    def post(self, command, output_dir, vars):
        for prereq in ['PasteDeploy']:
            command.insert_into_file(os.path.join(output_dir, 'setup.py'), 'Extra requirements', '%r,\n' % prereq, indent=True)

        command.insert_into_file(os.path.join(output_dir, 'setup.py'), 'Entry points', '      [paste.app_factory]\n      main = %(package)s.wsgiapp:make_app\n' % vars, indent=False)
        if command.verbose:
            print_('*' * 72)
            print_('* Run "paster serve docs/devel_config.ini" to run the sample application')
            print_('* on http://localhost:8080')
            print_('*' * 72)