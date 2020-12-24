# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/hierarchical.py
# Compiled at: 2019-08-16 00:21:06
# Size of source mod 2**32: 2374 bytes
"""
hierarchical prompt usage example
"""
from __future__ import print_function, unicode_literals
from python_inquirer import style_from_dict, Token, prompt
from examples import custom_style_2

def ask_direction():
    directions_prompt = {'type':'list', 
     'name':'direction', 
     'message':'Which direction would you like to go?', 
     'choices':[
      'Forward', 'Right', 'Left', 'Back']}
    answers = prompt(directions_prompt)
    return answers['direction']


def main():
    print('You find yourself in a small room, there is a door in front of you.')
    exit_house()


def exit_house():
    direction = ask_direction()
    if direction == 'Forward':
        print('You find yourself in a forest')
        print('There is a wolf in front of you; a friendly looking dwarf to the right and an impasse to the left.')
        encounter1()
    else:
        print('You cannot go that way. Try again')
        exit_house()


def encounter1():
    direction = ask_direction()
    if direction == 'Forward':
        print('You attempt to fight the wolf')
        print('Theres a stick and some stones lying around you could use as a weapon')
        encounter2b()
    else:
        if direction == 'Right':
            print('You befriend the dwarf')
            print('He helps you kill the wolf. You can now move forward')
            encounter2a()
        else:
            print('You cannot go that way')
            encounter1()


def encounter2a():
    direction = ask_direction()
    if direction == 'Forward':
        output = 'You find a painted wooden sign that says:'
        output += ' \n'
        output += ' ____  _____  ____  _____ \n'
        output += '(_  _)(  _  )(  _ \\(  _  ) \n'
        output += '  )(   )(_)(  )(_) ))(_)(  \n'
        output += ' (__) (_____)(____/(_____) \n'
        print(output)
    else:
        print('You cannot go that way')
        encounter2a()


def encounter2b():
    prompt({'type':'list', 
     'name':'weapon', 
     'message':'Pick one', 
     'choices':[
      'Use the stick',
      'Grab a large rock',
      'Try and make a run for it',
      'Attack the wolf unarmed']},
      style=custom_style_2)
    print('The wolf mauls you. You die. The end.')


if __name__ == '__main__':
    main()