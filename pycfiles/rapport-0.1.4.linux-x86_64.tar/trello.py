# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/plugins/trello.py
# Compiled at: 2013-05-14 04:37:04
"""
Trello plugin.
"""
import trolly.client, trolly.member, rapport.plugin, rapport.util
_RAPPORT_API_KEY = 'e8b72b9823082ad89dd7dfb40e8373bd'

class TrelloPlugin(rapport.plugin.Plugin):

    def __init__(self, api_key=_RAPPORT_API_KEY, user_auth_token=None, *args, **kwargs):
        super(TrelloPlugin, self).__init__(*args, **kwargs)
        self._c = trolly.client.Client(api_key=_RAPPORT_API_KEY, user_auth_token=user_auth_token)

    def collect(self, timeframe):
        card_fields = 'name,desc,closed,dateLastActivity,due'
        json = self._c.fetchJson(('/members/{0}').format(self.login), query_params={'boards': 'all', 'cards': 'all', 
           'organizations': 'all', 
           'card_fields': card_fields})
        open_cards, closed_cards, due_cards = [], [], []
        for card in json['cards']:
            last_activity = rapport.util.datetime_from_iso8601(card['dateLastActivity'])
            if timeframe.contains(last_activity):
                if card['closed']:
                    closed_cards.append(card)
                else:
                    open_cards.append(card)
                if card['due']:
                    due_cards.append(card)

        open_boards, closed_boards = [], []
        for board in json['boards']:
            if board['closed']:
                closed_boards.append(board)
            else:
                open_boards.append(board)

        return self._results({'boards': json['boards'], 'open_boards': open_boards, 
           'closed_boards': closed_boards, 
           'cards': json['cards'], 
           'open_cards': open_cards, 
           'closed_cards': closed_cards, 
           'due_cards': due_cards, 
           'organizations': json['organizations']})


rapport.plugin.register('trello', TrelloPlugin)