# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/update.py
# Compiled at: 2014-07-25 01:39:08
__doc__ = '\nThis module is the update command of bowl.\n\nCreated on 17 July 2014\n@author: Charlie Lewis\n'
import os, requests, sys, bowl.api
from bowl.cli_opts import repositories
from bowl.cli_opts import start
from bowl.cli_opts import stop

class update(object):
    """
    This class is responsible for the update command of the cli.
    """

    @classmethod
    def main(self, args):
        repos = repositories.repositories.main(args)
        for repo in repos:
            if repo == 'localhost':
                path = os.path.dirname(bowl.api.__file__)
                child_pid = os.fork()
                if child_pid == 0:
                    os.chdir(path)
                    start.start.main(args)
                    sys.exit(0)
                with open('services.tar.gz', 'wb') as (handle):
                    response = requests.get('http://localhost:8080/repo/services', stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)

                pid, status = os.waitpid(child_pid, 0)
                stop.stop.main(args)
            else:
                with open('services.tar.gz', 'wb') as (handle):
                    response = requests.get('http://' + repo + ':8080/repo/services', stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)