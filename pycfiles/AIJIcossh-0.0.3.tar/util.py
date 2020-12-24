# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiio/util.py
# Compiled at: 2016-09-28 20:22:12
import random
phrases = {'rephrase': [
              "so you're saying that",
              'in other words,',
              'so,'], 
   'inquire': [
             'please elaborate on',
             'tell me more regarding',
             "i'd like to know more about"], 
   'noted': [
           'noted',
           'thanks for the info',
           'cool',
           'ok, great'], 
   'what': [
          'what?',
          "i'm not sure what you mean",
          "i don't get it"], 
   'unsure': [
            "i'm not sure",
            "it's hard to say",
            'ummm..'], 
   'exhausted': [
               "i don't know anymore :(",
               'you tell me'], 
   'agree': [
           'exactly!',
           'i completely agree.',
           "you're preaching to the choir :)",
           "you've got my vote!"], 
   'disagree': [
              "i don't think you're right.",
              "you're wrong!",
              'not exactly...']}

def randphrase(ptype):
    return random.choice(phrases[ptype])