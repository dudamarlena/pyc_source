# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/todd/github/slack-to-trello/slack_to_trello/__init__.py
# Compiled at: 2015-08-15 00:00:02
import os
from flask import Flask, request
from slack_to_trello.model import SLACK_TOKEN, make_trello_card, send_slack_message
app = Flask(__name__)

@app.route('/')
def root():
    """Reply to curious persons"""
    return 'slack-to-trello made by Underdog.io with love <3'


@app.route('/slack/message', methods=['POST'])
def slack_message():
    """When we receive a message from Slack, generate a Trello card and reply"""
    if request.form['token'] != SLACK_TOKEN:
        return ("Provided Slack token from message didn't match our server's Slack token. Please double check they are aligned",
                403)
    text = request.form['text']
    user_name = request.form['user_name']
    channel_name = request.form['channel_name']
    card = make_trello_card(name=('{text} ({user_name})').format(text=text, user_name=user_name))
    send_slack_message(channel=('#{channel_name}').format(channel_name=channel_name), text=('Trello card "<{url}|{text}>" created by "{user_name}"').format(url=card.url, text=text, user_name=user_name))
    return ''


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    env = os.environ.get('ENV', 'development')
    app.debug = env != 'production'
    app.run(port=port)