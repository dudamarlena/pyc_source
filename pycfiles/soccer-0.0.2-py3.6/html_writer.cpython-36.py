# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\soccer\writers\html_writer.py
# Compiled at: 2018-01-08 04:59:40
# Size of source mod 2**32: 2808 bytes
""" HTML writer """
import logging
from soccer.writers import BasicWriter

class HTMLWriter(BasicWriter):
    __doc__ = '\n    HTML writer\n    '

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def league_table(self, table):
        html = '<table><thead><tr><th>#</th><th>Team</th><th>P</th><th>W</th><th>D</th><th>L</th><th>Goals</th><th>Pts</th></tr></thead><tbody>'
        for team in table['standings']:
            html = html + f"<tr><th>{team['position']}</th><th>{team['teamName']}</th><th>{team['playedGames']}</th><th>{team['wins']}</th><th>{team['draws']}</th><th>{team['losses']}</th><th>{team['goals']}:{team['goalsAgainst']}</th><th>{team['points']}</th></tr>"

        html = html + '</tbody></table>'
        return html

    def rank_table(self, table, position):
        html = '<table><thead><tr><th>#</th><th>Team</th><th>P</th><th>W</th><th>D</th><th>L</th><th>Goals</th><th>Diff</th><th>Pts</th></tr></thead><tbody>'
        if position == 'won':
            position = 1
        else:
            if position == 'last':
                position = len(table['standings'])
        for pos in range(max(0, position - 2), min(position + 3, len(table['standings']))):
            team = table['standings'][pos]
            if pos == position:
                html = html + f"<tr><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td>{team['wins']}</td><td>{team['draws']}</td><td>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td>{team['goals'] - team['goalsAgainst']}</td><td>{team['points']}</td></tr>"
            else:
                html = html + f"<tr><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td>{team['wins']}</td><td>{team['draws']}</td><td>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td>{team['goals'] - team['goalsAgainst']}</td><td>{team['points']}</td></tr>"

        html = html + '</tbody></table>'
        return html

    def title_table(self, title_table):
        html = '<table><thead><tr><th>Team</th><th># Wins</th><th>Seasons</th></tr></thead><tbody>'
        for team in title_table:
            html = html + f"<tr><td>{team['teamName']}</td><td>{team['numberOfTitles']}</td><td>{team['seasons']}</td></tr>"

        html = html + '</tbody></table>'
        return html

    def fixture_list(self, fixtures):
        html = "<table><thead><tr><th>Home</th><th colspan='3'>Result</th><th>Away</th></tr></thead><tbody>"
        for fixture in fixtures:
            html = html + f"<tr><td>{fixture['homeTeam']['name']}</td><td>{fixture['result']['goalsHomeTeam']}</td><td>:</td><td>{fixture['result']['goalsAwayTeam']}</td><td>{fixture['homeTeam']['name']}</td></tr>"

        html = html + '</tbody></table>'
        return html