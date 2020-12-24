# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/roster/new_roster.py
# Compiled at: 2018-07-20 07:07:39
# Size of source mod 2**32: 2411 bytes
import redis, argparse, subprocess, os

class Perform_Task:

    def __init__(self, roster='tasks_list', url='localhost', port='6379'):
        self.db = redis.StrictRedis(url, port, decode_responses=True)
        self.roster = roster

    def perform_all_tasks(self):
        HEADER = '\x1b[95m'
        OKBLUE = '\x1b[94m'
        OKGREEN = '\x1b[92m'
        WARNING = '\x1b[93m'
        while self.db.llen(self.roster) > 0:
            task = self.db.lpop(self.roster)
            task = task.split()
            out = subprocess.run(task, shell=False, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
            print(HEADER + out.stdout.decode('utf-8'))
            print(OKBLUE + out.stderr.decode('utf-8'))


class NewRoster:

    def __init__(self, tasks, roster='tasks_list', url='localhost', port='6379'):
        self.db = redis.StrictRedis(url, port, decode_responses=True)
        self.roster = roster
        for task in tasks:
            print(f"Pushing {task}")
            self.db.lpush(self.roster, task)

    def add_task(self, tasks, position=0):
        try:
            if position < 1:
                raise ValueError
        except:
            pass

        for task in tasks:
            print(f"Pushing {task}")
            self.db.lpush(self.roster, task)

    def del_task(self):
        raise NotImplementedError


def main(args):
    new_roster = NewRoster(tasks=(str(args.yo)))


parser = argparse.ArgumentParser(description='Commandline utility for adding tasks to roster')
parser.add_argument('-s', '--serve_rest', action='store_true', dest='serve', help='Run the bot with a REST endpoint')
parser.add_argument('-b', '--bind', action='store', default='0.0.0.0:8080', dest='bind', help="The socket to bind to ['0.0.0.0:8080']")
parser.add_argument('-u', '--url', action='store', dest='url', default='/', help="url for the bot ['/']")
parser.add_argument('-t', '--target', action='store', dest='yo', help='The python file with the build_bot() function')
parser.add_argument('-w', '--workers', default=1, dest='workers', help='no of gunicorn workers')
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)