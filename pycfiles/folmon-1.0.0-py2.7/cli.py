# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/folmond/cli.py
# Compiled at: 2018-05-05 07:26:48
import click
from presentation import Presentation
presentation_obj = Presentation('/home/arun/Projects/bingoarun/folmon/sample-data')

@click.group()
def main():
    pass


@click.command()
def status():
    presentation_obj.getRecentStatus()


main.add_command(status)
if __name__ == '__main__':
    main()