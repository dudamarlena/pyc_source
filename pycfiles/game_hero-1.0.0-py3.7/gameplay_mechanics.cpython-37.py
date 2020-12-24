# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\game_hero\gameplay_mechanics.py
# Compiled at: 2020-01-24 07:34:21
# Size of source mod 2**32: 8401 bytes
"""
Mechanics of the HeroGame gameplay.

The playable character, called Orderus, has some strengths and weaknesses,
as all heroes have.
After battling all kinds of monsters for more than a hundred years,
Orderus now has the following stats:

- Health: 70 - 100
- Strength: 70 - 80
- Defence: 45 – 55
- Speed: 40 – 50
- Luck: 10% - 30% (0% means no luck, 100% lucky all the time).
Also, he possesses 2 skills:

- Rapid strike: Strike twice while it’s his turn to attack;
(there’s a 10% chance he’ll use this skill every time he attacks)
- Magic shield: Takes only half of the usual damage when an enemy attacks;
(there’s a 20% change he’ll use this skill every time he defends.)

Gameplay

Orderus encounters a wild beast, with the following properties:

- Health: 60 - 90
- Strength: 60 - 90
- Defence: 40 – 60
- Speed: 40 – 60
- Luck: 25% - 40%

The game simulates a battle between Orderus and a wild beast,
taking into consideration that, in every battle,
Orderus and the beast must be initialized with random properties (within range)

The first attack is done by the player with the higher speed.
If both players have the same speed,
then the attack is carried on by the player with the highest luck.
After an attack, the players switch roles:
the attacker now defends and the defender now attacks.

The damage done by the attacker is calculated with the following formula:
Damage = Attacker strength – Defender defence

The damage is subtracted from the defender’s health.
An attacker can miss their hit and do no damage if the defender gets lucky.
Orderus’ skills occur randomly, based on their chances on each turn

Game over

The game ends when one of the players remain without health
or the number of turns reaches 20.
The application outputs the results for each turn: what happened,
which skills were used (if any), the damage done, defender’s health left.
Additionally, if there's a winner before the maximum number of rounds,
it'll be declared.

"""
from typing import Union
from game_hero import game_characters
from game_hero import game_constants
CHARACTER_TYPE = Union[(game_characters.Orderus, game_characters.WildBeast)]

class Singleton(type):
    __doc__ = 'Singleton metaclass-based design pattern'
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = (super(Singleton, cls).__call__)(*args, **kwargs)
        return cls._instances[cls]


class Gameplay(metaclass=Singleton):

    def __init__(self):
        """
        The game simulates a battle between Orderus and a wild beast,
        taking into consideration that, in every battle,
        Orderus and the Beast are initialized with random properties
        (within character range)

        The instance has a `_last_attacker` field which holds info
        on who was the last attacker in the previous turn of the fight,
        knowing which player's turn is in the current one.
        """
        self._last_attacker = None

    def simulate_round(self, attacker: CHARACTER_TYPE, defender: CHARACTER_TYPE):
        """
        Simulates one fight round in the HeroGame.

        Sets the `_last_attacker` field, and checks if the defender is lucky,
        therefore ending the fight (the defender dodges the attack).

        Otherwise, calculates the damage which is about to be dealt,
        and if the attacker is Orderus, check for his Rapid Strike skill,
        and if he's the defender, check for his Magic Shield skill, which
        both influence the value of the damage being dealt.

        After damage computation, subtracts said value from defender's health,
        outputing the actions from within the round.

        :param attacker: Character attacking this turn
        :param defender: Character defending this turn
        :return: None, plays the fight round
        """
        self._last_attacker = attacker
        if defender.is_lucky:
            print(f"{defender.name} dodged the hit!\nHe remains with {defender.health} health points")
            return
        else:
            damage_dealt = attacker.strength - defender.defence
            if isinstance(attacker, game_characters.Orderus):
                damage_dealt = attacker.rapid_strike_damage(damage_dealt)
            else:
                damage_dealt = defender.magic_shield_mitigation(damage_dealt)
        defender.health -= damage_dealt
        print(f"{attacker.name} hits {defender.name} with {damage_dealt} damage\n{defender.name} is left with {defender.health} health points\n")

    def simulate_fight(self, game_hero: game_characters.Orderus, magical_beast: game_characters.WildBeast):
        """
        Simulates the fight between the Game's Hero and the Wild Beast.

        Takes into account the maximum number of rounds in the turn-based fight

        In the first round, if both players have the same speed, then the one
        that is luckier gets to have the first attack, with rounds switching
        the characters between attacker and defender,
        based on who attacker previously.

        The game ends whenever one of the character's health reaches zero
        or below, or the maximum number of rounds is reached.

        :param game_hero: Hero of the Game (orderus)
        :param magical_beast: The beast confronting him (WildBeast)
        :return: None, simulates the fight
        """
        if game_hero.speed == magical_beast.speed:
            if game_hero.luck >= magical_beast.luck:
                print(f"{game_hero.name} hits first (gets lucky)")
                self.simulate_round(attacker=game_hero, defender=magical_beast)
            else:
                print(f"{magical_beast.name} hits first (gets lucky)")
                self.simulate_round(attacker=magical_beast, defender=game_hero)
        elif game_hero.speed > magical_beast.speed:
            print(f"{game_hero.name} hits first (faster than the opponent)")
            self.simulate_round(attacker=game_hero, defender=magical_beast)
        else:
            print(f"{magical_beast.name} hits first (faster than the opponent)")
            self.simulate_round(attacker=magical_beast, defender=game_hero)
        for fight_round in range(1, game_constants.TOTAL_FIGHT_ROUNDS):
            if isinstance(self._last_attacker, game_characters.WildBeast):
                self.simulate_round(attacker=game_hero, defender=magical_beast)
                if magical_beast.health <= 0:
                    print(f"The fight has ended, {game_hero.name} wins")
                    return
                else:
                    self.simulate_round(attacker=magical_beast, defender=game_hero)
                    if game_hero.health <= 0:
                        print(f"The fight has ended, {magical_beast.name} wins")
                        return

        if game_hero.health >= magical_beast.health:
            print(f"The fight has ended, {game_hero.name} wins")
        else:
            print(f"The fight has ended, {magical_beast.name} wins")