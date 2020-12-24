# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/com/dtmilano/android/concertina.py
# Compiled at: 2019-10-11 02:14:01
"""
Copyright (C) 2012-2018  Diego Torres Milano
Created on Jul 6, 2015

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: Diego Torres Milano

"""
import json, random
__author__ = 'diego'
__version__ = '15.8.1'
DEBUG = True

class Concertina:
    PHRASES = {'generic': [
                 'Chicken Wings grow on trees',
                 'Carrot sticks help the mind think',
                 'Farts cause neurological damage',
                 'Jennifer Lopez is a Man (only on Tuesday)',
                 'That... Is what she said',
                 'Make me a sandwich',
                 "King Kong's brother was a Rabbit... Hmmm",
                 "Tuesday, that's when it will all begin",
                 'Rulers, do they rule the world?',
                 'Can a pen write without writing it down.',
                 'The iPod is a gigantic hummer',
                 'A calculator can save the world. Just press "On"',
                 'Cell phones... Do they have cells in them?',
                 'A battery can produce random flashes and generate helium. Doubtful',
                 'A flash drive produces no flash what so ever',
                 'A card can be a type of a pickle, if its a pickle card',
                 'just a minute',
                 'wait for me',
                 'it was silent',
                 'chaos reigned',
                 'be on time',
                 'get away from me',
                 'Hold that thought',
                 'settle down',
                 'by the light of the street lamp',
                 'slippers soaked from the heavy dew',
                 'haunted by the oddly familiar musid',
                 "The 'poke' button on facebook is awesome...\\\nBut I think there should be a 'stab' button..."], 
       'alexa': [
               'Alexa, E.T. phone home',
               'Alexa, tell me a wizard joke',
               "Alexa, what's up?",
               'Alexa, what can you do?',
               'Alexa, show me restaurants in Montreal',
               'Alexa, what’s the news?',
               'Alexa, why is Pluto not a planet?',
               'Alexa, translate ’good morning’ in Japanese.',
               'Alexa, open TuneIn Live.',
               'Alexa, what’s your favorite word?',
               'Alexa, who’s leading the Masters?',
               "Alexa, play 'Your Song' by Lady Gaga.",
               'Alexa, set a sleep timer for ten minutes.',
               'Alexa, who is your favorite poet?',
               'Alexa, tell me a baseball joke.',
               'Alexa, read my audiobook.',
               'Alexa, teach me something.',
               'Alexa, why is water wet?',
               'Alexa, how do I set up calling and messaging?',
               'Alexa, give me a tongue twister.']}
    EMAILS = [
     'user@example.com',
     'user@gmail.com',
     'user@yahoo.com',
     'user@outlook.com',
     'user@mail.com',
     'user@outlook.co.uk']
    PASSWORDS = [
     '123456',
     'password',
     '12345678',
     'qwerty',
     'abc123']
    PLACES = [
     'los angeles',
     'seattle',
     'ushuaia',
     'white horse',
     'berlin']

    def __init__(self):
        pass

    @staticmethod
    def getRandomText(target=None):
        if target is None:
            target = 'generic'
        return random.choice(Concertina.PHRASES[target])

    @staticmethod
    def sayRandomText(target=None):
        return Concertina.getRandomText(target)

    @staticmethod
    def getRandomEmail():
        return random.choice(Concertina.EMAILS)

    @staticmethod
    def getRandomPassword():
        return random.choice(Concertina.PASSWORDS)

    @staticmethod
    def getRandomPlace():
        return random.choice(Concertina.PLACES)

    @staticmethod
    def readConcertinaConfig(concertinaConfigFile):
        if concertinaConfigFile:
            config = json.load(open(concertinaConfigFile))
        else:
            config = dict()
        if 'limits' not in config:
            config['limits'] = dict()
            config['limits']['iterations'] = 100
            config['limits']['maxNoTargetViewsIterations'] = 25
        if 'probabilities' not in config:
            config['probabilities'] = dict()
            config['probabilities']['systemKeys'] = 1 / 6.0
            config['probabilities']['views'] = 5 / 6.0
        if 'systemKeys' not in config:
            config['systemKeys'] = dict()
            config['systemKeys']['keys'] = ['ENTER', 'BACK', 'HOME', 'MENU']
            n = float(len(config['systemKeys']['keys']))
            config['systemKeys']['probabilities'] = [ 1 / n for _ in config['systemKeys']['keys'] ]
        if 'views' not in config:
            config['views'] = dict()
            config['views']['selector'] = ['classes', 'contentDescriptions']
            config['views']['probabilities'] = [0.5, 0.5]
            config['views']['classes'] = dict()
            config['views']['classes']['regexs'] = ['android.widget.Button', 'android.widget.EditText',
             'android.widget.Scrollable', '.*']
            n = float(len(config['views']['classes']['regexs']))
            config['views']['classes']['probabilities'] = [ 1 / n for _ in config['views']['classes']['regexs'] ]
            config['views']['contentDescriptions'] = dict()
            config['views']['contentDescriptions']['regexs'] = ['.*']
            n = float(len(config['views']['contentDescriptions']['regexs']))
            config['views']['contentDescriptions']['probabilities'] = [ 1 / n for _ in config['views']['contentDescriptions']['regexs']
                                                                      ]
        return config

    @staticmethod
    def getConcertinaConfigDefault():
        return json.dumps(Concertina.readConcertinaConfig(None), indent=4, sort_keys=True)