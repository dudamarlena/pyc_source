# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/devlab/new/t1/application/commander.py
# Compiled at: 2019-08-24 20:46:43
"""
Commander.py
Place all your command line functionalities in here.
Execute your commands in as `flasik $command-name`

=== Example ===

# 1
@command
def hello():
  print("Hello world!")

# run > flasik hello

# 2
@command('do-something')
@argument(name)
def do_something(name):
  print("Hello %s" % name)

# run > flasik do-something Mardix

# 3
run > 'flasik' to view all of your commands

"""
from flasik.commander import command, option, argument, click
from flasik import db

@command()
def setup():
    """ Application initial setup """
    click.echo('This is a setup!')