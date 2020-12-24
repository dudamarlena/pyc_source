# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/add.py
# Compiled at: 2014-09-20 15:47:46
"""
This module is the add command of bowl.

Created on 26 May 2014
@author: Charlie Lewis
"""
import ast, distutils.core, fileinput, json, os, sys
from bowl.cli_opts import link

class Object(object):
    pass


class add(object):
    """
    This class is responsible for the add command of the cli.
    """

    @classmethod
    def main(self, args):
        if os.path.exists(os.path.join(args.metadata_path, args.OS, args.VERSION, args.TYPE, 'dockerfiles', args.NAME)):
            print 'Service already exists.'
            sys.exit(0)
        j_args = {}
        try:
            j_string = ''
            if args.JSON[0] != '{':
                try:
                    with open(args.JSON, 'r') as (f):
                        for line in f:
                            j_string += line

                    j_string = j_string.replace('\n', '')
                    j_string = j_string.replace('\r', '')
                    j_string = j_string.replace('\t', '')
                    j_string = j_string.replace(' ', '')
                except:
                    print 'Unable to open the JSON file.'
                    sys.exit(0)

            else:
                j_string = args.JSON
            try:
                j_args = json.loads(j_string)
            except:
                if j_string[1] == "'":
                    junk = 1
                else:
                    junk = 1

        except:
            print 'Malformed JSON object.'
            sys.exit(0)

        if 'cluster' in j_args:
            if j_args['cluster'] != 'yes' and j_args['cluster'] != 'no':
                print "'cluster' key must be either 'yes' or 'no'."
                sys.exit(0)
        else:
            print "Missing 'cluster' key in JSON object."
            sys.exit(0)
        if 'combine_cmd' in j_args:
            if j_args['combine_cmd'] != 'yes' and j_args['combine_cmd'] != 'no':
                print "'combine_cmd' key must be either 'yes' or 'no'."
                sys.exit(0)
            if 'background_cmd' in j_args:
                check = 1
            else:
                print "Missing 'background_cmd' key in JSON object."
                sys.exit(0)
        else:
            print "Missing 'combine_cmd' key in JSON object."
            sys.exit(0)
        if 'tty' in j_args:
            if j_args['tty'] != 'yes' and j_args['tty'] != 'no':
                print "'tty' key must be either 'yes' or 'no'."
                sys.exit(0)
        else:
            print "Missing 'tty' key in JSON object."
            sys.exit(0)
        if 'interactive' in j_args:
            if j_args['interactive'] != 'yes' and j_args['interactive'] != 'no':
                print "'interactive' key must be either 'yes' or 'no'."
                sys.exit(0)
        else:
            print "Missing 'interactive' key in JSON object."
            sys.exit(0)
        if not os.path.exists(os.path.join(args.PATH, 'Dockerfile')):
            print 'Dockerfile not found.'
            sys.exit(0)
        if args.repository:
            print args.repository
            print 'TODO'
        else:
            link_args = Object()
            link_args.z = True
            link_args.metadata_path = args.metadata_path
            link_args.path = os.path.expanduser(args.metadata_path)
            link_args.SERVICE_HOST = 'localhost'
            link_args.NAME = 'local'
            if link.link.main(link_args):
                directory = os.path.join(args.metadata_path, 'services')
                directory = os.path.expanduser(directory)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                directory_os = os.path.join(directory, args.OS)
                if not os.path.exists(directory_os):
                    os.makedirs(directory_os)
                directory_version = os.path.join(directory_os, args.VERSION)
                if not os.path.exists(directory_version):
                    os.makedirs(directory_version)
                directory_databases = os.path.join(directory_version, 'databases')
                if not os.path.exists(directory_databases):
                    os.makedirs(directory_databases)
                directory_docker = os.path.join(directory_databases, 'dockerfiles')
                if not os.path.exists(directory_docker):
                    os.makedirs(directory_docker)
                directory_environment = os.path.join(directory_version, 'environment')
                if not os.path.exists(directory_environment):
                    os.makedirs(directory_environment)
                directory_docker = os.path.join(directory_environment, 'dockerfiles')
                if not os.path.exists(directory_docker):
                    os.makedirs(directory_docker)
                directory_services = os.path.join(directory_version, 'services')
                if not os.path.exists(directory_services):
                    os.makedirs(directory_services)
                directory_docker = os.path.join(directory_services, 'dockerfiles')
                if not os.path.exists(directory_docker):
                    os.makedirs(directory_docker)
                directory_tools = os.path.join(directory_version, 'tools')
                if not os.path.exists(directory_tools):
                    os.makedirs(directory_tools)
                directory_docker = os.path.join(directory_tools, 'dockerfiles')
                if not os.path.exists(directory_docker):
                    os.makedirs(directory_docker)
                directory_name = os.path.join(directory_docker, args.NAME)
                if not os.path.exists(directory_name):
                    os.makedirs(directory_name)
                try:
                    if os.path.exists(os.path.join(directory, 'oses')):
                        os_name = '"' + args.OS + '":'
                        if os_name not in open(os.path.join(directory, 'oses')).read():
                            num_lines = sum(1 for line in open(os.path.join(directory, 'oses')))
                            for line_number, line in enumerate(fileinput.input(os.path.join(directory, 'oses'), inplace=1)):
                                try:
                                    if line_number == num_lines - 2:
                                        sys.stdout.write(line.rstrip('\n') + ',\n')
                                    elif line_number == num_lines - 1:
                                        sys.stdout.write('\n')
                                    else:
                                        sys.stdout.write(line)
                                except:
                                    print 'Malformed oses file, not enough lines'

                            with open(os.path.join(directory, 'oses'), 'a') as (f):
                                f.write(' "' + args.OS + '":\n' + ' {\n' + '  "title": "' + args.OS.capitalize() + '",\n' + '  "type": "menu",\n' + '  "subtitle": "Please select a version...",\n' + '  "object": "os",\n' + '  "options": []\n' + ' }\n' + '}')
                    else:
                        with open(os.path.join(directory, 'oses'), 'a') as (f):
                            f.write('{\n "' + args.OS + '":\n' + ' {\n' + '  "title": "' + args.OS.capitalize() + '",\n' + '  "type": "menu",\n' + '  "subtitle": "Please select a version...",\n' + '  "object": "os",\n' + '  "options": []\n' + ' }\n' + '}')
                except:
                    print 'unable to add operating systems'

                try:
                    directory = os.path.join(directory, args.OS)
                    if os.path.exists(os.path.join(directory, 'versions')):
                        version_name = '"' + args.VERSION + '":'
                        if version_name not in open(os.path.join(directory, 'versions')).read():
                            num_lines = sum(1 for line in open(os.path.join(directory, 'versions')))
                            for line_number, line in enumerate(fileinput.input(os.path.join(directory, 'versions'), inplace=1)):
                                try:
                                    if line_number == num_lines - 2:
                                        sys.stdout.write(line.rstrip('\n') + ',\n')
                                    elif line_number == num_lines - 1:
                                        sys.stdout.write('\n')
                                    else:
                                        sys.stdout.write(line)
                                except:
                                    print 'Malformed version file, not enough lines'

                            with open(os.path.join(directory, 'versions'), 'a') as (f):
                                f.write(' "' + args.VERSION + '":\n' + ' {\n' + '  "title": "' + args.VERSION.capitalize() + '",\n' + '  "type": "menu",\n' + '  "subtitle": "Please select services...",\n' + '  "object": "version",\n' + '  "options": []\n' + ' }\n' + '}')
                    else:
                        with open(os.path.join(directory, 'versions'), 'a') as (f):
                            f.write('{\n "' + args.VERSION + '":\n' + ' {\n' + '  "title": "' + args.VERSION.capitalize() + '",\n' + '  "type": "menu",\n' + '  "subtitle": "Please select services...",\n' + '  "object": "version",\n' + '  "options": []\n' + ' }\n' + '}')
                except:
                    print 'unable to add versions'

                if args.TYPE == 'databases':
                    try:
                        if os.path.exists(os.path.join(directory_databases, 'databases')):
                            db_name = '"' + args.NAME + '":'
                            if db_name not in open(os.path.join(directory_databases, 'databases')).read():
                                num_lines = sum(1 for line in open(os.path.join(directory_databases, 'databases')))
                                for line_number, line in enumerate(fileinput.input(os.path.join(directory_databases, 'databases'), inplace=1)):
                                    try:
                                        if line_number == num_lines - 2:
                                            sys.stdout.write(line.rstrip('\n') + ',\n')
                                        elif line_number == num_lines - 1:
                                            sys.stdout.write('\n')
                                        else:
                                            sys.stdout.write(line)
                                    except:
                                        print 'Malformed databases file, not enough lines'

                                with open(os.path.join(directory_databases, 'databases'), 'a') as (f):
                                    f.write(' "' + args.NAME + '":\n' + ' {\n' + '  "title": "' + args.NAME + '",\n' + '  "type": "choice_menu",\n' + '  "command": "' + args.OS + ':' + args.VERSION + ':' + args.TYPE + ':' + args.NAME + '",\n' + '  "object": "database",\n' + '  "cluster": "' + j_args['cluster'] + '",\n' + '  "combine_cmd": "' + j_args['combine_cmd'] + '",\n' + '  "background_cmd": "' + j_args['background_cmd'] + '",\n' + '  "tty": "' + j_args['tty'] + '",\n' + '  "interactive": "' + j_args['interactive'] + '"\n' + ' }\n' + '}')
                        else:
                            with open(os.path.join(directory_databases, 'databases'), 'a') as (f):
                                f.write('{\n "' + args.NAME + '":\n' + ' {\n' + '  "title": "' + args.NAME + '",\n' + '  "type": "choice_menu",\n' + '  "command": "' + args.OS + ':' + args.VERSION + ':' + args.TYPE + ':' + args.NAME + '",\n' + '  "object": "database",\n' + '  "cluster": "' + j_args['cluster'] + '",\n' + '  "combine_cmd": "' + j_args['combine_cmd'] + '",\n' + '  "background_cmd": "' + j_args['background_cmd'] + '",\n' + '  "tty": "' + j_args['tty'] + '",\n' + '  "interactive": "' + j_args['interactive'] + '"\n' + ' }\n' + '}')
                    except:
                        print 'unable to add databases'

                else:
                    try:
                        if not os.path.exists(os.path.join(directory_databases, 'databases')):
                            with open(os.path.join(directory_databases, 'databases'), 'w') as (f):
                                f.write('{\n}')
                    except:
                        pass

                    if args.TYPE == 'environment':
                        try:
                            if os.path.exists(os.path.join(directory_environment, 'environment')):
                                env_name = '"' + args.NAME + '":'
                                if env_name not in open(os.path.join(directory_environment, 'environment')).read():
                                    num_lines = sum(1 for line in open(os.path.join(directory_environemnt, 'environemnt')))
                                    for line_number, line in enumerate(fileinput.input(os.path.join(directory_environment, 'environment'), inplace=1)):
                                        try:
                                            if line_number == num_lines - 2:
                                                sys.stdout.write(line.rstrip('\n') + ',\n')
                                            elif line_number == num_lines - 1:
                                                sys.stdout.write('\n')
                                            else:
                                                sys.stdout.write(line)
                                        except:
                                            print 'Malformed environment file, not enough lines'

                                    with open(os.path.join(directory_environment, 'environment'), 'a') as (f):
                                        f.write(' "' + args.NAME + '":\n' + ' {\n' + '  "title": "' + args.NAME + '",\n' + '  "type": "choice_menu",\n' + '  "command": "' + args.OS + ':' + args.VERSION + ':' + args.TYPE + ':' + args.NAME + '",\n' + '  "object": "environment",\n' + '  "cluster": "' + j_args['cluster'] + '",\n' + '  "combine_cmd": "' + j_args['combine_cmd'] + '",\n' + '  "background_cmd": "' + j_args['background_cmd'] + '",\n' + '  "tty": "' + j_args['tty'] + '",\n' + '  "interactive": "' + j_args['interactive'] + '"\n' + ' }\n' + '}')
                            else:
                                with open(os.path.join(directory_environment, 'environment'), 'a') as (f):
                                    f.write('{\n "' + args.NAME + '":\n' + ' {\n' + '  "title": "' + args.NAME + '",\n' + '  "type": "choice_menu",\n' + '  "command": "' + args.OS + ':' + args.VERSION + ':' + args.TYPE + ':' + args.NAME + '",\n' + '  "object": "environment",\n' + '  "cluster": "' + j_args['cluster'] + '",\n' + '  "combine_cmd": "' + j_args['combine_cmd'] + '",\n' + '  "background_cmd": "' + j_args['background_cmd'] + '",\n' + '  "tty": "' + j_args['tty'] + '",\n' + '  "interactive": "' + j_args['interactive'] + '"\n' + ' }\n' + '}')
                        except:
                            print 'unable to add environment'

                    else:
                        try:
                            if not os.path.exists(os.path.join(directory_environment, 'environment')):
                                with open(os.path.join(directory_environment, 'environment'), 'w') as (f):
                                    f.write('{\n}')
                        except:
                            pass

                        if args.TYPE == 'services':
                            try:
                                if os.path.exists(os.path.join(directory_services, 'services')):
                                    service_name = '"' + args.NAME + '":'
                                    if service_name not in open(os.path.join(directory_services, 'services')).read():
                                        num_lines = sum(1 for line in open(os.path.join(directory_services, 'services')))
                                        for line_number, line in enumerate(fileinput.input(os.path.join(directory_services, 'services'), inplace=1)):
                                            try:
                                                if line_number == num_lines - 2:
                                                    sys.stdout.write(line.rstrip('\n') + ',\n')
                                                elif line_number == num_lines - 1:
                                                    sys.stdout.write('\n')
                                                else:
                                                    sys.stdout.write(line)
                                            except:
                                                print 'Malformed services file, not enough lines'

                                        with open(os.path.join(directory_services, 'services'), 'a') as (f):
                                            f.write(' "' + args.NAME + '":\n' + ' {\n' + '  "title": "' + args.NAME + '",\n' + '  "type": "choice_menu",\n' + '  "command": "' + args.OS + ':' + args.VERSION + ':' + args.TYPE + ':' + args.NAME + '",\n' + '  "object": "services",\n' + '  "cluster": "' + j_args['cluster'] + '",\n' + '  "combine_cmd": "' + j_args['combine_cmd'] + '",\n' + '  "background_cmd": "' + j_args['background_cmd'] + '",\n' + '  "tty": "' + j_args['tty'] + '",\n' + '  "interactive": "' + j_args['interactive'] + '"\n' + ' }\n' + '}')
                                else:
                                    with open(os.path.join(directory_services, 'services'), 'a') as (f):
                                        f.write('{\n "' + args.NAME + '":\n' + ' {\n' + '  "title": "' + args.NAME + '",\n' + '  "type": "choice_menu",\n' + '  "command": "' + args.OS + ':' + args.VERSION + ':' + args.TYPE + ':' + args.NAME + '",\n' + '  "object": "services",\n' + '  "cluster": "' + j_args['cluster'] + '",\n' + '  "combine_cmd": "' + j_args['combine_cmd'] + '",\n' + '  "background_cmd": "' + j_args['background_cmd'] + '",\n' + '  "tty": "' + j_args['tty'] + '",\n' + '  "interactive": "' + j_args['interactive'] + '"\n' + ' }\n' + '}')
                            except:
                                print 'unable to add services'

                        else:
                            try:
                                if not os.path.exists(os.path.join(directory_services, 'services')):
                                    with open(os.path.join(directory_services, 'services'), 'w') as (f):
                                        f.write('{\n}')
                            except:
                                pass

                        if args.TYPE == 'tools':
                            try:
                                if os.path.exists(os.path.join(directory_tools, 'tools')):
                                    tool_name = '"' + args.NAME + '":'
                                    if tool_name not in open(os.path.join(directory_tools, 'tools')).read():
                                        num_lines = sum(1 for line in open(os.path.join(directory_tools, 'tools')))
                                        for line_number, line in enumerate(fileinput.input(os.path.join(directory_tools, 'tools'), inplace=1)):
                                            try:
                                                if line_number == num_lines - 2:
                                                    sys.stdout.write(line.rstrip('\n') + ',\n')
                                                elif line_number == num_lines - 1:
                                                    sys.stdout.write('\n')
                                                else:
                                                    sys.stdout.write(line)
                                            except:
                                                print 'Malformed tools file, not enough lines'

                                        with open(os.path.join(directory_tools, 'tools'), 'a') as (f):
                                            f.write(' "' + args.NAME + '":\n' + ' {\n' + '  "title": "' + args.NAME + '",\n' + '  "type": "choice_menu",\n' + '  "command": "' + args.OS + ':' + args.VERSION + ':' + args.TYPE + ':' + args.NAME + '",\n' + '  "object": "tools",\n' + '  "cluster": "' + j_args['cluster'] + '",\n' + '  "combine_cmd": "' + j_args['combine_cmd'] + '",\n' + '  "background_cmd": "' + j_args['background_cmd'] + '",\n' + '  "tty": "' + j_args['tty'] + '",\n' + '  "interactive": "' + j_args['interactive'] + '"\n' + ' }\n' + '}')
                                else:
                                    with open(os.path.join(directory_tools, 'tools'), 'a') as (f):
                                        f.write('{\n "' + args.NAME + '":\n' + ' {\n' + '  "title": "' + args.NAME + '",\n' + '  "type": "choice_menu",\n' + '  "command": "' + args.OS + ':' + args.VERSION + ':' + args.TYPE + ':' + args.NAME + '",\n' + '  "object": "tools",\n' + '  "cluster": "' + j_args['cluster'] + '",\n' + '  "combine_cmd": "' + j_args['combine_cmd'] + '",\n' + '  "background_cmd": "' + j_args['background_cmd'] + '",\n' + '  "tty": "' + j_args['tty'] + '",\n' + '  "interactive": "' + j_args['interactive'] + '"\n' + ' }\n' + '}')
                            except:
                                print 'unable to add tools'

                        else:
                            try:
                                if not os.path.exists(os.path.join(directory_tools, 'tools')):
                                    with open(os.path.join(directory_tools, 'tools'), 'w') as (f):
                                        f.write('{\n}')
                            except:
                                pass

                    try:
                        distutils.dir_util.copy_tree(args.PATH, os.path.join(directory_version, args.TYPE, 'dockerfiles', args.NAME))
                    except:
                        print 'failed to copy Dockerfile directory.'

            else:
                print 'unable to link localhost as a repository'
        print args