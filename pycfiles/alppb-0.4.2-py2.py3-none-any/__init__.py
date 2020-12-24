# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alpine_release_info/__init__.py
# Compiled at: 2017-12-03 07:52:36
import yaml, urllib2
from commandify import commandify, main_command
from os import path
defaults = {'mirror': 'nl.alpinelinux.org', 
   'arch': 'x86_64', 
   'flavor': 'alpine-vanilla', 
   'query': 'version', 
   'branch': 'latest-stable'}

def info(mirror, branch, arch, flavor, query):
    here = path.abspath(path.dirname(__file__))
    info = file(path.join(here, 'alpine.yml'))
    params = yaml.safe_load(info).get('alpine')
    if arch not in params.get('architectures'):
        raise ValueError('Invalid architeture, use one of: ' + (', ').join(params.get('architectures')))
    if flavor not in params.get('flavors'):
        raise ValueError('Invalid flavor, use one of: ' + (', ').join(params.get('flavors')))
    if query not in params.get('queries'):
        raise ValueError('Invalid query, use one of: ' + (', ').join(params.get('queries')))
    if branch not in params.get('branches'):
        raise ValueError('Invalid branch, use one of: ' + (', ').join(params.get('branches')))
    baseurl = 'https://' + mirror + '/alpine/' + branch + '/releases/' + arch
    try:
        f = urllib2.urlopen(baseurl + '/latest-releases.yaml')
    except urllib2.HTTPError as e:
        if e.code == 404:
            raise ValueError('No latest-releases.yaml for branch ' + branch)
        else:
            raise ValueError('Could not process, http error: ' + e.code)

    data = yaml.safe_load(f)
    for release in data:
        if release.get('flavor') == flavor and release.get('arch') == arch:
            release['url'] = baseurl + '/' + release.get('file')
            release['gpgsig'] = release.get('url') + '.asc'
            print release.get(query)
            return release.get(query)

    raise ValueError('Error: No release found. Check branch, flavor and architecture.')


@main_command(mirror={'flag': '-m'}, branch={'flag': '-b'}, arch={'flag': '-a'}, flavor={'flag': '-f'}, query={'flag': '-q'})
def info_cmd(mirror=defaults['mirror'], branch=defaults['branch'], arch=defaults['arch'], flavor=defaults['flavor'], query=defaults['query']):
    return info(mirror, branch, arch, flavor, query)


def main():
    try:
        commandify(suppress_warnings=['default_true'])
    except ValueError as error:
        print error.message
        exit(1)


if __name__ == '__main__':
    main()