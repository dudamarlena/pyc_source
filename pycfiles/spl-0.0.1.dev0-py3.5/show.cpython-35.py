# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spl/commands/show.py
# Compiled at: 2016-12-14 10:04:15
# Size of source mod 2**32: 1462 bytes
from spl.errors import NonSingletonResultException, ExitCode
from spl.state import State

def add_parser_args(parser):
    parser.add_argument('package_name')


def run(spiget, args):
    try:
        print(formatResource(spiget.resource_details(args.package_name), spiget))
        return ExitCode.OK
    except NonSingletonResultException:
        print("'{}' matches more than one resource. Please use the resource ID to show details.".format(args.package_name))
        return ExitCode.NON_SINGLETON_RESULT


def formatResource(resource, spiget):
    with State.load(spiget) as (state):
        installed_version = state.installed_resources[str(resource.id)]['resource'].current_version if state.resource_is_installed(resource) else 'N/A'
        strings = [
         'Package:           {}'.format(resource.name),
         'ID:                {}'.format(resource.id),
         'Author:            {}'.format(resource.author.name),
         'Tag:               {}'.format(resource.tag),
         'Category:          {}'.format(resource.category.name),
         'Latest version:    {}'.format(resource.current_version),
         'Installed version: {}'.format(installed_version),
         'Versions:          {}'.format(resource.versions),
         'Updated:           {}'.format(resource.update_date),
         'Tested against:    [{}]'.format(', '.join(resource.tested_versions))]
        return '\n'.join(strings)