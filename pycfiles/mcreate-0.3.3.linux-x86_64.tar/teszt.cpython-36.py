# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.3/lib/python3.6/site-packages/create/teszt.py
# Compiled at: 2019-06-02 12:21:47
# Size of source mod 2**32: 167 bytes
import click

@click.command()
@click.argument('project')
def create(project):
    print(f"Succesfully created {project}")


if __name__ == '__main__':
    create()