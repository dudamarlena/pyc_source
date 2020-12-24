# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parang/evolve.py
# Compiled at: 2009-08-22 22:50:09
""" Genetic evolver for PyDip bots
    Copyright (C) 2004-2008  Eric Wald
    
    This software may be reused for non-commercial purposes without charge,
    and without notifying the authors.  Use of any part of this software for
    commercial purposes without permission from the authors is prohibited.
"""
from main import ThreadManager
from network import ServerSocket
from player import Observer
from server import Server
game_number = 0

def evolve(player_class, file_name):
    if not hasattr(player_class, 'get_values'):
        print '%s cannot be evolved.' % player_class.__name__
    log_file = open(file_name, 'a', 1)
    try:
        evolve_logged(player_class, log_file)
    finally:
        log_file.close()


def evolve_logged(player_class, stream):
    """ Runs a server and a bunch of bots, attempting to optimize them."""
    global game_number
    name = player_class.__name__
    next_values = None

    def output(line, *args):
        text = str(line) % args + '\n'
        print text,
        stream.write(text)

    manager = ThreadManager()
    manager.pass_exceptions = True
    sock = ServerSocket(Server, manager)
    if sock.open():
        manager.add_polled(sock)
        server = sock.server
    else:
        output('Failed to open the server.')
        return
    while not server.closed:
        game = server.default_game()
        game_number += 1
        client = manager.add_client(GeneSplicer, output=output)
        if client:
            manager.process()
        if client and client.player:
            splicer = client.player
        else:
            output('Failed to start the gene splicer.')
            return
        players = []
        for dummy in range(game.players_needed()):
            if next_values:
                vals = next_values.pop()
                output('Starting %s with %s', name, vals)
                client = manager.add_client(player_class, values=vals)
            else:
                output('Starting %s with default values', name)
                client = manager.add_client(player_class)
            if client:
                manager.process()
            if client and client.player:
                players.append(client.player)
            else:
                output('Failed to start.')
                return

        while not game.closed:
            manager.process(30)

        next_values = splicer.get_next_values(players)

    manager.close()
    return


class GeneSplicer(Observer):
    """ An observer to collect winner information for the evolver."""

    def __init__(self, output, **kwargs):
        self.__super.__init__(**kwargs)
        self.use_map = True
        self.winners = []
        self.output = output

    def handle_DRW(self, message):
        self.output(message)
        if len(message) > 3:
            self.winners = message[2:-1]
        else:
            self.winners = self.map.current_powers()

    def handle_SLO(self, message):
        self.output(message)
        self.winners = [message[2]]

    def handle_SCO(self, message):
        self.output('Game #%d, %s: %s', game_number, self.map.current_turn.year or 'start', message)

    def get_next_values(self, players):
        win_values = []
        self.output('Players in %s, ended in %s:', self.map.name, self.map.current_turn)
        for player in players:
            values = player.get_values()
            token = player.power.key
            if token in self.winners:
                status = 'Winner'
                win_values.append(values)
            else:
                status = 'Loser'
            self.output('- %s: %s as %s', status, values, token)

        if win_values:
            cycles = len(players) // len(win_values)
        else:
            cycles = 0
        result = win_values[:]
        cycles -= 1
        if cycles > 1:
            result += [ val_set.mutate(0.4) for val_set in win_values ]
            cycles -= 1
        while cycles > 0:
            result += [ val_set.mutate(0.05) for val_set in win_values ]
            cycles -= 1

        return result


if __name__ == '__main__':
    from dumbbot import DumbBot
    evolve(DumbBot, 'log/stats/evolution')