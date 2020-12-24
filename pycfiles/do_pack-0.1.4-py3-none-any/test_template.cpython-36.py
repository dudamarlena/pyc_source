# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dropbox\dropbox\projects\python\do-pack\do\test_template.py
# Compiled at: 2018-02-21 17:14:20
# Size of source mod 2**32: 2336 bytes
from datetime import datetime
from string import Template
import json, os, click, sys
apache2 = 'Apache License 2.0'
bsd = 'BSD License'
gnuAgpl = 'GNU Affero General Public License v3'
mit = 'MIT License'
gnuGpl = 'GNU General Public License v3'
template_path = license_path = os.path.join(os.path.dirname(__file__), 'templates\\licenses\\')
year = str(datetime.now().year)
try:
    with open(template_path + 'index.json', 'r') as (i):
        license_list = json.load(i)
except FileNotFoundError:
    click.echo('LicenseNotFoundError: {} Not Found. Aborted!'.format(template_path + 'index.json'))
    sys.exit(1)

def show(index_json=license_list):
    """
    Prints a the list of licenses in the index.json for the user to choose
    """
    index = 1
    for licenses in index_json.keys():
        click.echo('{} - {}'.format(str(index), licenses))
        index += 1


def choose(license_name, author_name=None, project=None):
    """
    Allows to Choose one license, but only in assistant mode.
    """
    with open(template_path + license_list[license_name], 'r') as (f):
        license_content = Template(f.read())
    if license_name == apache2 or license_name == bsd or license_name == gnuAgpl or license_name == mit:
        return license_content.substitute(year=year,
          fullname=author_name)
    else:
        if license_name == gnuGpl:
            return license_content.substitute(year=year,
              fullname=author_name,
              project=project)
        return license_content.substitute()


if __name__ == '__main__':
    show()