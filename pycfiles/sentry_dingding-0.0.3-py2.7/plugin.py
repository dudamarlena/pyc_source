# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/sentry_dingding/plugin.py
# Compiled at: 2019-05-08 12:46:20
import json, requests
from sentry.plugins.bases.notify import NotificationPlugin
import sentry_dingding
from .forms import DingDingOptionsForm
DingTalk_API = 'https://oapi.dingtalk.com/robot/send?access_token={token}'

class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'ansheng'
    author_url = 'https://github.com/anshengme/sentry-dingding'
    version = sentry_dingding.VERSION
    description = 'Send error counts to DingDing.'
    resource_links = [
     ('Source', 'https://github.com/anshengme/sentry-dingding'),
     ('Bug Tracker', 'https://github.com/anshengme/sentry-dingding/issues'),
     ('README', 'https://github.com/anshengme/sentry-dingding/blob/master/README.md')]
    slug = 'DingDing'
    title = 'DingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return
        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(token=access_token)
        title = ('New alert from {}').format(event.project.slug)
        data = {'msgtype': 'markdown', 
           'markdown': {'title': title, 
                        'text': ('#### {title} \n > {message} [href]({url})').format(title=title, message=event.message, url=('{}events/{}/').format(group.get_absolute_url(), event.id))}}
        requests.post(url=send_url, headers={'Content-Type': 'application/json'}, data=json.dumps(data).encode('utf-8'))