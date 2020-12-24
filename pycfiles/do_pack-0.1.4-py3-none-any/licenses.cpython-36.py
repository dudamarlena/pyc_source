# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dropbox\dropbox\projects\python\do-pack\do\licenses.py
# Compiled at: 2018-03-05 16:14:20
# Size of source mod 2**32: 2975 bytes
"""
How to template the licenses:
----------------------------------------
GNU_GPLv3   = $year, $fullname, $project
apache2     = $year, $fullname
BSD         = $year, $fullname
GNU_AGPLv3  = $year, $fullname
mit         = $year, $fullname
GNU_LGPLv3  = None
Mozilla     = None
Unlicensed  = None
"""
from datetime import datetime
from string import Template
import json, click, sys, os
apache2 = 'Apache License 2.0'
gnuAgpl = 'GNU Affero General Public License v3'
gnuGpl = 'GNU General Public License v3'
bsd = 'BSD License'
mit = 'MIT License'
template_path = os.path.join(os.path.dirname(__file__), 'templates', 'licenses')

def load_index_json(path=template_path):
    """
    Open the index.json that contains the licenses and filenames.
    """
    try:
        with open(os.path.join(path, 'index.json'), 'r') as (i):
            return json.load(i)
    except FileNotFoundError:
        click.echo('LicenseNotFoundError: {} Not Found. Aborted!'.format(template_path + 'index.json'))
        sys.exit(1)


def load_license_content(license_name):
    """
    Load the content of a license
    """
    index_json = load_index_json()
    try:
        with open(os.path.join(template_path, index_json[license_name]), 'r') as (f):
            return Template(f.read())
    except FileNotFoundError:
        click.echo('LicenseNotFoundError: {} Not Found. Aborted!'.format(template_path + index_json[license_name]))
        sys.exit(1)


def show(index_json=load_index_json()):
    """
    Prints the list of licenses in the index.json for the user to choose
    """
    for index, licenses in enumerate(index_json.keys()):
        index += 1
        click.echo('{} - {}'.format(index, licenses))


def choose(license_name, author_name=None, project=None):
    """
    Allows to Choose a license in assistant mode.

    """
    year = str(datetime.now().year)
    lic_name = load_license_content(license_name)
    if license_name == apache2 or license_name == bsd or license_name == gnuAgpl or license_name == mit:
        return lic_name.substitute(year=year, fullname=author_name)
    else:
        if license_name == gnuGpl:
            return lic_name.substitute(year=year, fullname=author_name,
              project=project)
        return lic_name.substitute()


if __name__ == '__main__':
    pass