# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/multi_agents_subprocess.py
# Compiled at: 2009-12-22 03:50:08
import re, sys, os, getpass, sys, logging
from optparse import OptionParser
import subprocess
from eventlet import api
from pyogp.lib.client.agentmanager import AgentManager
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings

def login():
    """ login an to a login endpoint """
    parser = OptionParser(usage='usage: %prog --file filename [options]')
    logger = logging.getLogger('client.example')
    parser.add_option('-l', '--loginuri', dest='loginuri', default='https://login.aditi.lindenlab.com/cgi-bin/login.cgi', help='specified the target loginuri')
    parser.add_option('-r', '--region', dest='region', default=None, help='specifies the region (regionname/x/y/z) to connect to')
    parser.add_option('-q', '--quiet', dest='verbose', default=True, action='store_false', help='enable verbose mode')
    parser.add_option('-f', '--file', dest='file', default=None, help='csv formatted file containing first,last,pass for multi agent login (required)')
    parser.add_option('-c', '--count', dest='count', default=0, help='number of agents to login')
    parser.add_option('-e', '--executable', dest='executable', default=None, help='what program to run')
    (options, args) = parser.parse_args()
    options.count = int(options.count)
    if len(args) > 0:
        parser.error('Unsupported arguments specified: ' + str(args))
    if options.file == None:
        parser.error('Missing required -f argument for logging in multiple agents')
    if options.executable == None:
        parser.error('Missing required executable to run')
    try:
        f = open(options.file, 'r')
        data = f.readlines()
        f.close()
    except IOError, error:
        print 'Data File not found. Stopping. Error: %s' % error
        return
    else:
        try:
            f = open(options.executable, 'r')
            executable = options.executable
        except IOError, error:
            try:
                local_executable = os.path.join(os.path.dirname(__file__), options.executable)
                f = open(local_executable, 'r')
                executable = local_executable
            except IOError, error:
                print 'Executable not found. Stopping. Error: %s' % error
                return

        print 'Using the %s executable' % executable
        clients = []
        line_count = 0
        for line in data:
            line_count += 1

        if options.count > 0:
            if options.count > line_count:
                print 'The count parameter requests more agents (%s) than you have in your data file (%s). Logging in max available.' % (options.count, line_count)
        counter = 0
        for line in data:
            counter += 1
            if len(line.strip().split(',')) != 3:
                print 'We expect a line with 3 comma separated parameters, we got %s' % line.strip().split(',')
                print 'Stopping.'
            clients.append(line.strip().split(','))
            if counter >= options.count:
                break

        if options.verbose:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)-30s%(name)-30s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
            logging.getLogger('').setLevel(logging.DEBUG)
        else:
            print 'Attention: This script will print nothing if you use -q. So it might be boring to use it like that ;-)'
        for client in clients:
            py = sys.executable
            cmd = '%s %s --password=%s %s %s' % (py, executable, client[2], client[0], client[1])
            print "running '%s'" % cmd
            subprocess.Popen(cmd, shell=True)

    return


def main():
    return login()


if __name__ == '__main__':
    main()