# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/slack.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 1334 bytes
import os
from slack import WebClient

class SlackIntegration:
    token = os.environ.get('SLACK_TOKEN')

    def __init__(self, manager):
        self.manager = manager
        self.channel = manager.config.get('slack_channel', 'agile')
        self.cli = WebClient(token=(self.token))

    @classmethod
    def add(cls, manager):
        if cls.token:
            manager.message_brokers.append(cls(manager))

    def __call__(self, message):
        info = self.manager.info
        repo = self.manager.github_repo().repo_path
        sha = info['head']['id']
        commit = 'https://github.com/%s/commit/%s' % (repo, sha)
        message = '*%s* - %s\nby %s <%s>\n%s' % (
         repo,
         info['branch'],
         info['head']['committer_name'],
         info['head']['committer_email'],
         message)
        attachments = [
         dict(fallback=('Git commit %s' % commit),
           actions=[
          dict(type='button',
            text='Git commit',
            url=commit)])]
        self.cli.api_call('chat.postMessage',
          channel=(self.channel),
          text=message,
          attachments=attachments)