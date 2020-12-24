# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/circle_asset/cli.py
# Compiled at: 2015-02-28 14:02:08
# Size of source mod 2**32: 2011 bytes
from .version import *
from .project import Project
from .circle_api import get_latest_build, get_artifact_list
import argparse, sys
from fnmatch import fnmatch
from urllib.request import urlretrieve
API_ROOT = 'https://circleci.com/api/v1'

def main():
    arguments = argparse.ArgumentParser(description=SHORT_DESCRIPTION)
    arguments.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
    arguments.add_argument('--api-root', type=str, help='API root for CircleCI', default=API_ROOT)
    arguments.add_argument('--token', type=str, help='API key', nargs='?')
    arguments.add_argument('username', type=str, help='GitHub username')
    arguments.add_argument('project', type=str, help='GitHub project')
    arguments.add_argument('artifact', type=str, help='Artifact name (or pattern) to get', nargs='*', default=['*'])
    arguments.add_argument('--branch', type=str, help='Project branch', default='master')
    arguments.add_argument('--accept-failed', action='store_true', help='Accepts artifacts from the latest build')
    arguments.add_argument('--build', type=int, default=None, help='Go to a specific build')
    args = arguments.parse_args()
    project = Project(username=args.username, project=args.project, api_root=args.api_root, token=args.token)
    build = args.build
    if build is None:
        build = get_latest_build(project, args.branch, args.accept_failed)
    artifacts = get_artifact_list(project, build)
    for name, url in artifacts.items():
        if any(fnmatch(name, pattern) for pattern in args.artifact):
            print('Downloading {}...'.format(name), end='')
            sys.stdout.flush()
            urlretrieve(url, filename=name)
            print('{}[DONE]'.format(' ' * (60 - len(name))))
            continue