# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mara_kim/Documents/code/github/kismet-py/kismet/chatbot/slack.py
# Compiled at: 2019-07-19 22:50:59
# Size of source mod 2**32: 825 bytes
from os import getenv
from slack import RTMClient
from kismet.core import process_markdown
token = getenv('SLACK_TOKEN', '')

@RTMClient.run_on(event='message')
def on_message(**payload):
    rtm_client = payload['web_client']
    data = payload['data']
    if 'user' not in data:
        return
    user = data['user']
    self_id = rtm_client.auth_test().data['user_id']
    channel_id = data['channel']
    thread_ts = data.get('thread_ts', None)
    text = data['text']
    text = text.replace('<@' + str(self_id) + '>', 'kismet')
    response = process_markdown(text, '<@{}>'.format(user))
    if response:
        rtm_client.chat_postMessage(channel=channel_id,
          thread_ts=thread_ts,
          text=response)


print('Starting Slack client')
client = RTMClient(token=token)
client.start()