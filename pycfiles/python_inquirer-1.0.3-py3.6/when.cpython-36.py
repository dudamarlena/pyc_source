# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/when.py
# Compiled at: 2019-08-16 00:21:06
# Size of source mod 2**32: 1112 bytes
"""
When example
"""
from __future__ import print_function, unicode_literals
from python_inquirer import style_from_dict, Token, prompt, print_json
from examples import custom_style_2

def dislikes_bacon(answers):
    return not answers['bacon']


questions = [
 {'type':'confirm', 
  'name':'bacon', 
  'message':'Do you like bacon?'},
 {'type':'input', 
  'name':'favorite', 
  'message':'Bacon lover, what is your favorite type of bacon?', 
  'when':lambda answers: answers['bacon']},
 {'type':'confirm', 
  'name':'pizza', 
  'message':'Ok... Do you like pizza?', 
  'default':False, 
  'when':dislikes_bacon},
 {'type':'input', 
  'name':'favorite', 
  'message':'Whew! What is your favorite type of pizza?', 
  'when':lambda answers: answers.get('pizza', False)}]
answers = prompt(questions, style=custom_style_2)
print_json(answers)