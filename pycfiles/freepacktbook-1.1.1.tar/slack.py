# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adambogdal/git/freepacktbook/freepacktbook/slack.py
# Compiled at: 2016-09-25 04:21:53
import json, requests

class SlackNotification(object):
    icon_url = 'https://github-bogdal.s3.amazonaws.com/freepacktbook/icon.png'

    def __init__(self, slack_url, channel):
        self.slack_url = slack_url
        self.channel = channel
        if not self.channel.startswith('#'):
            self.channel = '#%s' % (self.channel,)

    def notify(self, data):
        if not all([self.slack_url, self.channel]):
            return
        payload = {'channel': self.channel, 'username': 'PacktPub Free Learning', 
           'icon_url': self.icon_url, 
           'attachments': [
                         {'fallback': "Today's Free eBook: %s" % data['title'], 
                            'pretext': "Today's Free eBook:", 
                            'title': data['title'], 
                            'title_link': data['book_url'], 
                            'color': '#ff7f00', 
                            'text': '%s\n%s' % (data['description'], data.get('url', '')), 
                            'thumb_url': data['image_url'].replace(' ', '%20')}]}
        requests.post(self.slack_url, data={'payload': json.dumps(payload)})