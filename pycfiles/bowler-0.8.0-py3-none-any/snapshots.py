# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/snapshots.py
# Compiled at: 2014-08-01 00:01:56
__doc__ = '\nThis module is the snapshots command of bowl.\n\nCreated on 17 July 2014\n@author: Charlie Lewis\n'
import ast, os

class snapshots(object):
    """
    This class is responsible for the snapshots command of the cli.
    """

    @classmethod
    def main(self, args):
        snapshots = []
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            with open(os.path.join(directory, 'snapshots'), 'r') as (f):
                for line in f:
                    snapshot = ast.literal_eval(line.rstrip('\n'))
                    snapshots.append(snapshot['snapshot_id'])

        except:
            pass

        if not args.z:
            for snapshot in snapshots:
                print snapshot

        return snapshots