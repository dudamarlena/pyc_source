# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\admin\appdata\local\temp\pip-install-vivcrm\py-cake\pycake\pycake_template\{{cookiecutter.project_short_name}}\src\{{cookiecutter.project_short_name}}\cli.py
# Compiled at: 2018-11-11 20:47:23
"""Console script for {{cookiecutter.project_short_name}}."""
import sys, click

@click.command()
def main(args=None):
    click.echo('Replace this message by putting your code into {{cookiecutter.project_short_name}}.cli.main')
    click.echo('See click documentation at http://click.pocoo.org/')
    return 0


if __name__ == '__main__':
    sys.exit(main())