# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dropbox\dropbox\projects\python\do-pack\do\setup_config.py
# Compiled at: 2018-02-21 22:28:47
# Size of source mod 2**32: 845 bytes
from string import Template
import click, sys, os
path_setup = os.path.join(os.path.dirname(__file__), 'templates\\template_setup.txt')

def setup_template(setup_name, setup_version, setup_description, setup_author, setup_author_email, setup_url):
    try:
        with open(path_setup, 'r') as (f):
            setup_content = Template(f.read())
    except FileNotFoundError:
        click.echo('setupNotFoundError: {} Not Found. Aborted!'.format(path_setup))
        sys.exit(1)

    return setup_content.substitute(setup_name=setup_name,
      setup_version=setup_version,
      setup_description=setup_description,
      setup_author=setup_author,
      setup_author_email=setup_author_email,
      setup_url=setup_url)