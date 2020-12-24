# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\derek_2\google drive\nvda-addon-exploded\addontemplate\NVDAAddonTemplate\__init__.py
# Compiled at: 2016-08-07 02:29:30
from __future__ import print_function
import sys, os
from collections import OrderedDict
from cookiecutter.main import cookiecutter
if sys.version.startswith('2'):
    eval = input
    input = raw_input
promptDict = OrderedDict((
 (
  'authorName',
  [
   'Author Name',
   'John Doe']),
 (
  'authorEmail',
  [
   'Author Email',
   'John.Doe225830@blacklist.com']),
 (
  'projectName',
  [
   'Project Name',
   'Simple Addon']),
 (
  'addonName',
  [
   'Addon Name',
   'simpleAddon']),
 (
  'addonSummary',
  [
   "Addon Summary\n\t\tThis text shows up in the add-ons manager for the add-ons name. Keep it short, it's the user facing name.",
   'Simple Addon']),
 (
  'addonDescription',
  [
   'Addon Description\n\t\tThe add-on description can be edited later from buildVars.py, because it may be longer than one line.',
   'This is my first add-on. It currently does nothing.']),
 (
  'version',
  [
   'Add-on Version\n\t\tEither something like 1.0.0, 1.0.0-dev, or a date based version (16.07, or 16.07.1).',
   '0.1.0-dev']),
 (
  'addonURL',
  [
   'If you have an add-on URL, type it here. Otherwise, press enter.',
   'None']),
 (
  'createGlobalPlugin',
  [
   'Do you want a globalPlugin skeleton generated for you, (y/n)',
   'y']),
 (
  'createAppModule',
  [
   'Do you want an appModule skeleton generated for you? (Y/N).',
   'y']),
 (
  'useContinuousIntegrationWithTravisCI',
  [
   'Use continuous integration with Travis CI?\n\t\tPlease see the readme to learn more.',
   'n'])))

def getInput(prompt, default=''):
    answer = ''
    while answer == '':
        print(prompt)
        answer = input(default)
        if answer == '':
            answer = default
        if default in ('y', 'n'):
            if answer.lower() not in ('y', 'n', 'yes', 'no'):
                print('Please answer yes or no.')
                continue

    return answer


def run():
    context = {}
    for item in promptDict:
        context[item] = getInput(*promptDict[item])

    context['project_slug'] = ('_').join(context['projectName'].split()) if ' ' in context['projectName'] else context['projectName']
    curFileDir = os.path.join(os.path.dirname(__file__), 'data')
    cookiecutter(curFileDir, no_input=True, extra_context=context)