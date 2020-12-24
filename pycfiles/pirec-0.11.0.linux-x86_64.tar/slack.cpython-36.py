# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jstutters/.virtualenvs/pirec/lib/python3.6/site-packages/pirec/recorders/slack.py
# Compiled at: 2017-02-10 11:03:57
# Size of source mod 2**32: 1118 bytes
"""Exposes the Slack result recorder."""
try:
    import requests
except ImportError:
    pass

class Slack(object):
    __doc__ = 'Send a Slack notification when a pipeline completes.\n\n    Args:\n        url (str): Slack Webhook URL\n        channel (str): The channel name to post to\n        values: (dict): A mapping of result keys to report\n\n    Note:\n        Use of this class requires the installation of the `slackclient module\n        <https://slackapi.github.io/python-slackclient/>`_.\n    '

    def __init__(self, url, channel, values):
        """Initialize the recorder."""
        self.url = url
        self.channel = channel
        self.values = values

    def write(self, results):
        """Send a message to Slack.

        Args:
            results (dict): A dictionary of results to record
        """
        msg = [
         'Pirec task complete']
        for field in self.values:
            msg.append('{0}: {1}'.format(field, self.values[field](results)))

        payload = {'text':'\n'.join(msg),  'channel':self.channel}
        requests.post((self.url), json=payload)