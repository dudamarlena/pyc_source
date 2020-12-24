# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_gameplay_mechanics.py
# Compiled at: 2020-01-24 08:41:24
# Size of source mod 2**32: 1921 bytes
import io
from contextlib import redirect_stdout
from game_hero.gameplay_mechanics import Gameplay
from game_hero.game_characters import Orderus, WildBeast

def test_gameplay_instance():
    """
    Tests singleton implementation for the Gameplay instances.
    """
    first_instance = Gameplay()
    second_instance = Gameplay()
    assert first_instance is second_instance, 'Gameplay on different instances'


def test_simulate_round():
    """
    Tests round simulation and effects on health of the characters.
    """
    gameplay = Gameplay()
    orderus = Orderus()
    beast = WildBeast()
    pre_fight_orderus_health = orderus.health
    pre_fight_beast_health = beast.health
    gameplay.simulate_round(attacker=orderus, defender=beast)
    assert orderus.health == pre_fight_orderus_health, 'Attacker health change'
    assert beast.health != pre_fight_beast_health, 'Defender health unchanged!'


def test_simulate_fight():
    """
    Tests fight simulation
    Checks on health of the characters, win resolution and attack order.
    """
    gameplay = Gameplay()
    orderus = Orderus()
    beast = WildBeast()
    with io.StringIO() as (buffer):
        with redirect_stdout(buffer):
            gameplay.simulate_fight(game_hero=orderus, magical_beast=beast)
            fight_output = buffer.getvalue()
    if not 'wins' in fight_output:
        raise AssertionError('None of the characters won')
    elif f"{orderus.name} wins" in fight_output:
        assert orderus.health > beast.health, 'Incorrect win based on health!'
        if not gameplay._last_attacker == orderus:
            raise AssertionError('Incorrect attack order!')
    else:
        assert beast.health > orderus.health, 'Incorrect win based on health!'
        assert gameplay._last_attacker == beast, 'Incorrect attack order!'