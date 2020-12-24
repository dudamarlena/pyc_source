# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/asyncbots/command.py
# Compiled at: 2018-01-10 15:35:36
# Size of source mod 2**32: 3771 bytes
"""Module for Commands which bots use to act in Slack"""
import abc
from collections import namedtuple
import os
from asyncbots.history import HistoryDoc

class Command(metaclass=abc.ABCMeta):
    __doc__ = 'Abstract class for Commands. Commands are used by bots to act in Slack.'

    @abc.abstractmethod
    async def execute(self, slack, event=None):
        """
        Slack will call this method to execute the command.
        If it returns another Command, that will be executed and so on.
        Execution order is depth first.
        """
        pass


class MessageCommand(Command):
    __doc__ = 'Most basic Command, sends a message.'

    def __init__(self, channel=None, user=None, text='', success_callback=None):
        self.channel = channel
        self.user = user
        self.text = text
        self.callback = success_callback

    async def execute(self, slack, event=None):
        """
        Sends the message to the specified channel,
        unless it is falsy, in which case sends it to the specified user."""
        channel = slack.ids.cid(self.channel) if self.channel else slack.ids.dmid(uid=(self.user)) if self.user else event['channel']
        max_index = (len(self.text) - 1) // 4000
        for index in range(max_index + 1):
            if index < max_index:
                await slack.send(self.text[4000 * index:4000 * (index + 1)], channel, None)
            else:
                await slack.send(self.text[4000 * index:4000 * (index + 1)], channel, self.callback)


class DeleteCommand(Command):
    __doc__ = "Deletes the response that this command was in response to. Possibly doesn't work."

    def __init__(self, channel=None, user=None, text=''):
        pass

    async def execute(self, slack, event=None):
        await slack.delete_message((event['channel']), (event['user']), (event['ts']), admin_key=True)


Record = namedtuple('Record', ['channel', 'uid', 'text', 'time'])

class HistoryCommand(Command):
    __doc__ = '\n    Pass a callback to slack with signature:\n        f(hist_list) where hist is a list of (channel, user, text, time) namedtuples.\n    The callback will be executed on a list of past messages which match the specified parameters.\n    Only works if Slack was constructed with db=True (requires MongoDB).\n    '

    def __init__(self, callback, channel=None, user=None):
        self.callback = callback
        self.channel = channel
        self.user = user

    async def execute(self, slack, event=None):
        kwargs = {}
        if self.channel:
            kwargs['channel'] = self.channel
        if self.user:
            kwargs['uid'] = self.user
        hist_objects = (HistoryDoc.objects)(**kwargs)
        hist_list = [Record(r.channel, r.uid, r.text, r.time) for r in hist_objects]
        return await self.callback(hist_list)


class ReactCommand(Command):
    __doc__ = 'Posts an emoji reaction on the message this command was created in response to.'

    def __init__(self, emoji):
        self._emoji = emoji

    async def execute(self, slack, event=None):
        await slack.react(self._emoji, event)


class UploadCommand(Command):
    __doc__ = '\n    Uploads a file in the specified channel.\n    Setting delete=True will causel the file to be deleted off the filesystem after upload.\n    '

    def __init__(self, user=None, channel=None, file_name=None, delete=False):
        self.user = user
        self.channel = channel
        self.file_name = file_name
        self.delete = delete

    async def execute(self, slack, event=None):
        await slack.upload_file(f_name=(self.file_name), channel=(self.channel), user=(self.user))
        if self.delete:
            os.remove(self.file_name)