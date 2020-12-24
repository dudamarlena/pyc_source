# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adambogdal/git/freepacktbook/freepacktbook/pushover.py
# Compiled at: 2018-06-19 10:57:44
import json, requests

class PushoverNotification(object):

    def __init__(self, pushover_user, pushover_token):
        self.pushover_api = 'https://api.pushover.net/1/messages.json'
        self.pushover_user = pushover_user
        self.pushover_token = pushover_token

    def get_image_content(self, image_url):
        return requests.get(image_url, stream=True).content

    def notify(self, data):
        if not all([self.pushover_user, self.pushover_token]):
            return
        else:
            payload = {'user': self.pushover_user, 
               'token': self.pushover_token, 
               'title': data['title'], 
               'url': data['book_url'], 
               'url_title': data['title'], 
               'message': "Today's Free eBook\n%s\n%s" % (
                         data['title'], data['description'])}
            try:
                image_content = self.get_image_content(data['image_url'].replace(' ', '%20'))
            except Exception:
                files = None
            else:
                files = {'attachment': ('cover.jpg', image_content)}

            requests.post(self.pushover_api, data=payload, files=files)
            return