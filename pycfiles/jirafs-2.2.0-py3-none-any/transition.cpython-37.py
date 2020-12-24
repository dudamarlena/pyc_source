# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/transition.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 3098 bytes
from collections import OrderedDict
from jirafs.plugin import CommandPlugin
from jirafs.utils import run_command_method_with_kwargs
from jirafs.exceptions import JiraInteractionFailed

class Command(CommandPlugin):
    __doc__ = ' Transition the current issue into a new state '
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def handle(self, args, folder, **kwargs):
        state = self.get_state_from_string(folder, args.state)
        if state is None:
            state = self.get_state_from_user(folder)
        return self.cmd(folder, state)

    def main(self, folder, state_id):
        folder.jira.transition_issue(folder.issue, state_id)
        starting_status = folder.get_fields()['status']
        pull_result = run_command_method_with_kwargs('pull', folder=folder)
        if starting_status == folder.get_fields()['status']:
            raise JiraInteractionFailed("JIRA was not able to successfully transition this issue into the requested state.  This type of failure usually occurs when one's JIRA configuration requires that certain fields be specified before transitioning into a given state.  Unfortunately, no details regarding what fields may be required are provided via JIRA's API.")
        return pull_result[1]

    def get_transition_dict(self, folder):
        if not hasattr(self, '_transition_dict'):
            value = folder.jira.transitions(folder.issue)
            self._transition_dict = OrderedDict(((v['id'], v) for v in value))
        return self._transition_dict

    def get_state_from_string(self, folder, value):
        options = self.get_transition_dict(folder)
        if value is None:
            return
        if value in options:
            return value
        for k, v in options.items():
            if value.upper() == v['name'].upper():
                return k

    def get_state_from_user(self, folder):
        options = self.get_transition_dict(folder)
        response = None
        while response is None:
            for option_id, option_data in options.items():
                print('%s: %s (%s)' % (
                 option_id,
                 option_data['name'],
                 option_data.get('to', {}).get('description', '')))

            print('')
            response = self.get_state_from_string(folder, input('Please select a state from the above options: '))

        return response

    def add_arguments(self, parser):
        parser.add_argument('state', default=None, nargs='?')