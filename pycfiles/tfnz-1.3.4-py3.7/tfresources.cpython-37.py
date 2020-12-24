# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/cli/tfresources.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 1417 bytes
import json
from base64 import b64encode
from tfnz.cli import generic_cli, base_argparse

def main():
    parser = base_argparse('tfresources')
    generic_cli(parser, {None: list_resources})


def list_resources(location, args):
    resources = {'location':location.location, 
     'nodes':{b64encode(node.pk).decode():node.stats for node in location.nodes.values()}, 
     'volumes':[vol.display_name() for vol in location.volumes.values()], 
     'externals':[xtn.display_name() for xtn in location.externals.values()], 
     'endpoints':[ep.domain for ep in location.endpoints.values()]}
    print(json.dumps(resources, indent=2))


if __name__ == '__main__':
    main()