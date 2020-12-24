# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/wlogger/test.py
# Compiled at: 2015-12-23 13:52:03
import argparse, argcomplete, requests, pprint

def github_org_members(prefix, parsed_args, **kwargs):
    resource = ('https://api.github.com/orgs/{org}/members').format(org=parsed_args.organization)
    return (member['login'] for member in request.get(resource).json() if member['login'].startswith(prefix))


parser = argparse.ArgumentParser()
parser.add_argument('--organization', help='Github organization')
parser.add_argument('--member', help='Github member').completer = github_org_members
argcomplete.autcomplete(parser)
args = parser.parsed_args()
pprint.pprint(requests.get(('https://api.github.com/users/{m}').format(m=args.member)).json())