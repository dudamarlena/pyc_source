# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sgiraud/WDIR/dev/plone/install/zinstance/src/plonerules.slack/plonerules/slack/actions/interfaces.py
# Compiled at: 2015-03-25 04:42:06
from zope.interface import Interface
from zope import schema

class ISlackAction(Interface):
    """Definition of the configuration available for a Slack action"""
    chanel = schema.TextLine(title='Channel', description='The channel to post (ex: #general)', required=True)
    username = schema.TextLine(title='Username', description='The username to use for post', required=True)
    token = schema.TextLine(title='Webhook Token', description='The token (available in API settings on slack)', required=True)
    emoji = schema.TextLine(title='emoji to use', description="An emoji picked in http://www.emoji-cheat-sheet.com/ (ex: ':dash:')", required=True)
    message = schema.Text(title='Message', description='Type in here the message that you want to post. Some defined content can be replaced: ${title} will be replaced by the title of the newly created item.  ${url} will be replaced by the URL of the newly created item, ${username} by the who made the action and ${description} by the description', required=True)