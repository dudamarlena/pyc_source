# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/create.py
# Compiled at: 2019-03-11 23:04:44
import six
from jirafs import utils
from jirafs.plugin import CommandPlugin
from jirafs.utils import run_command_method_with_kwargs

class Command(CommandPlugin):
    """Create a new JIRA issue"""
    MIN_VERSION = '1.15'
    MAX_VERSION = '1.99.99'
    AUTOMATICALLY_INSTANTIATE_FOLDER = False
    FIELDS = (
     {'name': 'project', 
        'prompt': 'Project', 
        'required': True, 
        'path': 'project.key'},
     {'name': 'issuetype', 
        'prompt': 'Issue Type', 
        'default': 'Task', 
        'path': 'issuetype.name'},
     {'name': 'summary', 
        'prompt': 'Summary', 
        'required': True},
     {'name': 'description', 
        'prompt': 'Description', 
        'required': False})

    def set_field_value(self, data, field, value):
        starting_reference = data
        path = field.get('path', field['name'])
        for part in path.split('.'):
            if part not in data:
                data[part] = {}
            last_reference = data
            data = data[part]

        last_reference[path.split('.')[(-1)]] = value
        return starting_reference

    def prompt_for_input(self, field):
        while True:
            if field.get('default'):
                value = raw_input('%s (%s): ' % (
                 field.get('prompt'),
                 field.get('default')))
            else:
                value = raw_input('%s: ' % field.get('prompt'))
            value = value.strip()
            if value:
                return value
            if not field.get('required') and field.get('default'):
                return field.get('default')
            if not field.get('required'):
                return value

    def main(self, args, jira, path, parser, **kwargs):
        server = args.server
        if not server:
            server = utils.get_default_jira_server()
        issue_data = {}
        for field in self.FIELDS:
            if getattr(args, field['name']) is not None:
                self.set_field_value(issue_data, field, getattr(args, field['name']))
            elif args.quiet:
                self.set_field_value(issue_data, field, field.get('default'))
            else:
                self.set_field_value(issue_data, field, self.prompt_for_input(field))

        jira_client = jira(server)
        issue = jira_client.create_issue(issue_data)
        return run_command_method_with_kwargs('clone', path=None, url=issue.permalink(), jira=jira)

    def add_arguments(self, parser):
        parser.add_argument('--server', default=None)
        parser.add_argument('--quiet', '-q', default=False, action='store_true')
        for argument in self.FIELDS:
            parser.add_argument('--%s' % argument['name'], default=None, type=six.text_type)

        return