# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/todd/github/slack-to-trello/slack_to_trello/model.py
# Compiled at: 2015-08-15 00:00:02
import os, json, httplib2
from trello import Board, List, TrelloClient
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_MESSAGE_URL = os.environ['SLACK_MESSAGE_URL']
TRELLO_API_KEY = os.environ['TRELLO_API_KEY']
TRELLO_TOKEN = os.environ['TRELLO_TOKEN']
TRELLO_BOARD_ID = os.environ['TRELLO_BOARD_ID']
TRELLO_LIST_ID = os.environ['TRELLO_LIST_ID']
trello_client = TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)

def make_trello_card(*args, **kwargs):
    """Generate a new Trello card"""
    board = Board(client=trello_client, board_id=TRELLO_BOARD_ID)
    card_list = List(board=board, list_id=TRELLO_LIST_ID)
    return card_list.add_card(*args, **kwargs)


def send_slack_message(channel, text):
    """Send a message to Slack"""
    http = httplib2.Http()
    return http.request(SLACK_MESSAGE_URL, 'POST', body=json.dumps({'channel': channel, 
       'text': text}))