# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/new.py
# Compiled at: 2014-09-28 15:41:59
"""
This module is the new command of bowl.

Created on 15 March 2014
@author: Charlie Lewis
"""
import ast, curses, docker, importlib, inspect, os, shutil, sys, time, uuid
from bowl.cli_opts import link
from bowl.cli_opts import repositories
from bowl.cli_opts import services
from bowl.cli_opts import unlink

class Object(object):
    pass


class new(object):
    """
    This class is responsible for the new command of the cli.
    """

    @staticmethod
    def build_dockerfile(self, dockerfile, uuid_dir, main_arg):
        with open('/tmp/' + uuid_dir + '/Dockerfile', 'w') as (f):
            for line in dockerfile:
                f.write(line + '\n')

        image_tag = 'bowl-' + uuid_dir
        if len(self.hosts) == 0:
            print 'WARNING: No hosts were selected to run these services.'
        for index, host in enumerate(self.hosts):
            c = docker.Client(base_url='tcp://' + host['title'] + ':2375', version='1.12', timeout=2)
            d_tag = None
            d_quiet = False
            d_nocache = False
            d_rm = False
            d_stream = False
            d_fileobj = None
            d_timeout = None
            d_custom_context = False
            d_encoding = None
            d_tag = 'bowl-' + uuid_dir
            d_path = '/tmp/' + uuid_dir
            d_command = None
            d_hostname = None
            d_user = None
            d_detach = False
            d_stdin_open = False
            d_tty = False
            d_mem_limit = 0
            d_ports = None
            d_environment = None
            d_volumes = None
            d_network_disabled = False
            d_name = None
            d_entrypoint = None
            d_cpu_shares = None
            d_working_dir = None
            d_memswap_limit = 0
            d_image = image_tag
            d_binds = None
            d_port_bindings = None
            d_lxc_conf = None
            d_publish_all_ports = False
            d_links = None
            d_privileged = False
            d_dns = None
            d_dns_search = None
            d_volumes_from = None
            d_network_mode = None
            d_restart_policy = None
            d_cap_add = None
            d_cap_drop = None
            d_container = container
            d_links = self.link_names
            output = c.build(tag='bowl-' + uuid_dir, quiet=False, path='/tmp/' + uuid_dir, nocache=False, rm=False, stream=False)
            print list(output)
            if len(self.names) != 0:
                if self.unique:
                    container = c.create_container(image_tag, tty=True, stdin_open=True, name=self.names[index], hostname=self.names[index])
                else:
                    container = c.create_container(image_tag, tty=True, stdin_open=True, name=self.names[0], hostname=self.names[0])
            else:
                container = c.create_container(image_tag, tty=True, stdin_open=True, name=image_tag, hostname=image_tag)
            if self.link_names:
                c.start(container, publish_all_ports=True, links=self.link_names)
            else:
                c.start(container, publish_all_ports=True)
            try:
                directory = main_arg.metadata_path
                directory = os.path.expanduser(directory)
                with open(os.path.join(directory, 'containers'), 'a') as (f):
                    if len(self.names) != 0:
                        if self.unique:
                            f.write("{'image_id': '" + image_tag + "'," + " 'container_name': '" + self.names[index] + "'," + " 'container_id': '" + container['Id'] + "'," + " 'host': '" + host['title'] + "'" + '}\n')
                        else:
                            f.write("{'image_id': '" + image_tag + "'," + " 'container_name': '" + self.names[0] + "'," + " 'container_id': '" + container['Id'] + "'," + " 'host': '" + host['title'] + "'" + '}\n')
                    else:
                        f.write("{'image_id': '" + image_tag + "'," + " 'container_name': '" + image_tag + "'," + " 'container_id': '" + container['Id'] + "'," + " 'host': '" + host['title'] + "'" + '}\n')
            except:
                pass

        shutil.rmtree('/tmp/' + uuid_dir)
        return

    @staticmethod
    def build_options(self, main_arg):
        menu_dict = {'title': 'Build your bowl', 
           'type': 'menu', 
           'subtitle': 'Please select a choice...', 
           'options': [
                     {'title': 'Build Container', 
                        'type': 'menu', 
                        'subtitle': 'Please select an Operating System...', 
                        'options': []},
                     {'title': 'Choose Image', 
                        'type': 'menu', 
                        'subtitle': 'Please select an Image...', 
                        'options': []}]}
        try:
            directory = main_arg.metadata_path
            directory = os.path.expanduser(directory)
            with open(os.path.join(directory, 'images'), 'r') as (f):
                for line in f:
                    menu_dict['options'][1]['options'].append(ast.literal_eval(line.rstrip('\n')))

        except:
            pass

        launch_dict = {'title': 'Launch Container', 
           'type': 'launch'}
        launch_image_dict = {'title': 'Launch Image(s)', 
           'type': 'launch'}
        args = Object()
        args.quiet = False
        args.json = True
        args.z = True
        args.metadata_path = main_arg.metadata_path
        all_dict = services.services.main(args)
        if 'oses' in all_dict:
            os_num = 0
            try:
                for os_key in all_dict['oses']:
                    version_num = 0
                    menu_dict['options'][0]['options'].append(all_dict['oses'][os_key])
                    for version_key in all_dict['oses'][os_key]['versions']:
                        menu_dict['options'][0]['options'][os_num]['options'].append(all_dict['oses'][os_key]['versions'][version_key])
                        database_dict = {'title': 'Databases', 
                           'type': 'menu', 
                           'subtitle': 'Please select databases...', 
                           'options': []}
                        for database_key in all_dict['oses'][os_key]['versions'][version_key]['databases']:
                            database_dict['options'].append(all_dict['oses'][os_key]['versions'][version_key]['databases'][database_key])
                            key = os_key + '.' + version_key + '.databases.' + database_key
                            try:
                                self.combine_cmd_dict[key] = all_dict['oses'][os_key]['versions'][version_key]['databases'][database_key]['combine_cmd']
                                if self.combine_cmd_dict[key] == 'yes':
                                    self.background_cmd_dict[key] = all_dict['oses'][os_key]['versions'][version_key]['databases'][database_key]['background_cmd']
                            except:
                                print 'key error'

                        environment_dict = {'title': 'Environment Tools', 'type': 'menu', 
                           'subtitle': 'Please select environment tools...', 
                           'options': []}
                        for environment_key in all_dict['oses'][os_key]['versions'][version_key]['environment']:
                            environment_dict['options'].append(all_dict['oses'][os_key]['versions'][version_key]['environment'][environment_key])
                            key = os_key + '.' + version_key + '.environment.' + environment_key
                            try:
                                self.combine_cmd_dict[key] = all_dict['oses'][os_key]['versions'][version_key]['environment'][environment_key]['combine_cmd']
                                if self.combine_cmd_dict[key] == 'yes':
                                    self.background_cmd_dict[key] = all_dict['oses'][os_key]['versions'][version_key]['environment'][environment_key]['background_cmd']
                            except:
                                print 'key error'

                        service_dict = {'title': 'Services', 'type': 'menu', 
                           'subtitle': 'Please select services...', 
                           'options': []}
                        for service_key in all_dict['oses'][os_key]['versions'][version_key]['services']:
                            service_dict['options'].append(all_dict['oses'][os_key]['versions'][version_key]['services'][service_key])
                            key = os_key + '.' + version_key + '.services.' + service_key
                            try:
                                self.combine_cmd_dict[key] = all_dict['oses'][os_key]['versions'][version_key]['services'][service_key]['combine_cmd']
                                if self.combine_cmd_dict[key] == 'yes':
                                    self.background_cmd_dict[key] = all_dict['oses'][os_key]['versions'][version_key]['services'][service_key]['background_cmd']
                            except:
                                print 'key error'

                        tool_dict = {'title': 'Tools', 'type': 'menu', 
                           'subtitle': 'Please select tools...', 
                           'options': []}
                        for tool_key in all_dict['oses'][os_key]['versions'][version_key]['tools']:
                            tool_dict['options'].append(all_dict['oses'][os_key]['versions'][version_key]['tools'][tool_key])
                            key = os_key + '.' + version_key + '.tools.' + tool_key
                            try:
                                self.combine_cmd_dict[key] = all_dict['oses'][os_key]['versions'][version_key]['tools'][tool_key]['combine_cmd']
                                if self.combine_cmd_dict[key] == 'yes':
                                    self.background_cmd_dict[key] = all_dict['oses'][os_key]['versions'][version_key]['tools'][tool_key]['background_cmd']
                            except:
                                print 'key error'

                        host_dict = {'title': 'Docker Hosts', 'type': 'menu', 
                           'subtitle': 'Please select which hosts are available to use for containers...', 
                           'options': []}
                        try:
                            directory = main_arg.metadata_path
                            directory = os.path.expanduser(directory)
                            with open(os.path.join(directory, 'hosts'), 'r') as (f):
                                for line in f:
                                    host_dict['options'].append(ast.literal_eval(line.rstrip('\n')))

                        except:
                            pass

                        menu_dict['options'][0]['options'][os_num]['options'][version_num]['options'].append(database_dict)
                        menu_dict['options'][0]['options'][os_num]['options'][version_num]['options'].append(environment_dict)
                        menu_dict['options'][0]['options'][os_num]['options'][version_num]['options'].append(service_dict)
                        menu_dict['options'][0]['options'][os_num]['options'][version_num]['options'].append(tool_dict)
                        menu_dict['options'][0]['options'][os_num]['options'][version_num]['options'].append(host_dict)
                        menu_dict['options'][0]['options'][os_num]['options'][version_num]['options'].append(launch_dict)
                        version_num += 1

                    os_num += 1

                menu_dict['options'][1]['options'].append(launch_image_dict)
            except:
                print 'failure'

        return menu_dict

    @staticmethod
    def query_yes_no(self, question, default='no'):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "no" (the default), "yes" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 
           'n': False}
        if default == None:
            prompt = ' [y/n] '
        else:
            if default == 'yes':
                prompt = ' [Y/n] '
            elif default == 'no':
                prompt = ' [y/N] '
            else:
                raise ValueError("invalid default answer: '%s'" % default)
            while True:
                sys.stdout.write(question + prompt)
                choice = raw_input().lower()
                if default is not None and choice == '':
                    return valid[default]
                if choice in valid:
                    return valid[choice]
                sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

        return

    @classmethod
    def main(self, args):
        if not os.path.exists(os.path.expanduser(args.metadata_path)):
            os.mkdir(os.path.expanduser(args.metadata_path))
        if args.toggle_default:
            if os.path.exists(os.path.join(os.path.expanduser(args.metadata_path), 'no_default')):
                os.remove(os.path.join(os.path.expanduser(args.metadata_path), 'no_default'))
            else:
                open(os.path.join(os.path.expanduser(args.metadata_path), 'no_default'), 'a').close()
        self.link_names = {}
        self.combine_cmd_dict = {}
        self.background_cmd_dict = {}
        this_dir, this_filename = os.path.split(__file__)
        link_path = os.path.join(os.path.dirname(this_dir), 'containers/.default/')
        link_args = Object()
        link_args.z = True
        link_args.metadata_path = os.path.expanduser(args.metadata_path)
        link_args.SERVICE_HOST = 'localhost'
        link_args.NAME = 'default'
        link_args.path = link_path
        link.link.main(link_args)
        if os.path.exists(os.path.join(os.path.expanduser(args.metadata_path), 'no_default')):
            unlink_args = Object()
            unlink_args.metadata_path = os.path.expanduser(args.metadata_path)
            unlink_args.NAME = 'default'
            unlink.unlink.main(unlink_args)
        menu_dict = self.build_options(self, args)
        if not args.no_curses:
            self.win = curses.initscr()
            self.win.keypad(1)
        self.build_dict = {}
        self.build_dict['services'] = []
        self.hosts = []
        self.launch = False
        self.exit = False
        self.image = False
        self.default = True
        self.user = False
        self.name = False
        self.names = []
        self.unique = False
        self.cmd = False
        self.entrypoint = False
        self.port = False
        self.link = False
        self.volume = False
        if not args.no_curses:
            curses.noecho()
            curses.cbreak()
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            self.menus_dict = {}
            build_dict = self.build_dict
            build_dict = self.process_menu(self, args, menu_dict, build_dict)
            self.build_dict = build_dict
            curses.endwin()
        else:
            if args.command:
                self.cmd = True
                self.default = False
            if args.entrypoint:
                self.entrypoint = True
                self.default = False
            if args.volume:
                self.volume = True
                self.default = False
            if args.port:
                self.port = True
                self.default = False
            if args.link:
                self.link = True
                self.default = False
            if args.name:
                self.name = True
                self.default = False
            if args.unique:
                self.unique = True
                self.default = False
            if args.user:
                self.user = True
                self.default = False
            if args.image:
                self.image = True
                self.launch = True
            if args.service:
                self.build_dict['services'] = args.service
                self.launch = True
            if args.host:
                for host in args.host:
                    h = {}
                    h['type'] = 'choice_menu'
                    h['title'] = host
                    self.hosts.append(h)

        if self.launch and not args.no_curses:
            self.default = self.query_yes_no(self, 'Use default runtime settings?', default='yes')
        if not self.default:
            if not args.no_curses:
                curses.noecho()
                curses.cbreak()
                curses.start_color()
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            options_dict = {'title': 'Runtime options', 
               'type': 'menu', 
               'subtitle': 'Please select the runtime options you would like to change...', 
               'options': [
                         {'title': 'Do you want to override the CMD of the container?', 
                            'type': 'choice_menu', 
                            'options': [
                                      {'config': 'cmd'}]},
                         {'title': 'Do you want to override the ENTRYPOINT of the container?', 
                            'type': 'choice_menu', 
                            'options': [
                                      {'config': 'entrypoint'}]},
                         {'title': 'Do you want to attach a volume to this container?', 
                            'type': 'choice_menu', 
                            'options': [
                                      {'config': 'volume'}]},
                         {'title': 'Do you want to specify how a port should be exposed?', 
                            'type': 'choice_menu', 
                            'options': [
                                      {'config': 'port'}]},
                         {'title': 'Do you want to link this container to another container?', 
                            'type': 'choice_menu', 
                            'options': [
                                      {'config': 'link'}]},
                         {'title': 'Do you want to name this container?', 
                            'type': 'choice_menu', 
                            'options': [
                                      {'config': 'name'}]},
                         {'title': 'Do you want an account on this container?', 
                            'type': 'choice_menu', 
                            'options': [
                                      {'config': 'user'}]}]}
            if len(self.hosts) > 1:
                options_dict['options'].append({'title': 'Should the containers use different parameters?', 
                   'type': 'choice_menu', 
                   'options': [
                             {'config': 'unique'}]})
            if not args.no_curses:
                self.config_dict = {}
                self.config_dict['services'] = []
                config_dict = self.config_dict
                config_dict = self.options_menu(self, args, options_dict, config_dict)
                self.config_dict = config_dict
                curses.endwin()
        if self.name:
            if self.unique:
                for host in self.hosts:
                    c = docker.Client(base_url='tcp://' + host['title'] + ':2375', version='1.12', timeout=2)
                    name = raw_input('Enter container name for container running on ' + host['title'] + ':')
                    self.names.append(name)

            else:
                name = raw_input('Enter container name: ')
                self.names.append(name)
            print self.names
        if self.link:
            containers = []
            if self.unique:
                for host in self.hosts:
                    c = docker.Client(base_url='tcp://' + host['title'] + ':2375', version='1.12', timeout=2)
                    containers = c.containers()
                    if len(containers) == 0:
                        print 'There are no running containers on the host ' + host['title'] + ' to link to.'
                        junk = raw_input('Press enter to continue...')
                    else:
                        if not args.no_curses:
                            curses.noecho()
                            curses.cbreak()
                            curses.start_color()
                            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
                        options_dict = {'title': 'Containers to Link', 
                           'type': 'menu', 
                           'subtitle': 'Please select the containers you would like to link on host ' + host['title'] + '...', 
                           'options': []}
                        for container in containers:
                            container_name = ''
                            names = container['Names']
                            for n in names:
                                container_name += n[1:] + ' - '

                            container_id = container['Id']
                            container_name += container_id
                            options_dict['options'].append({'title': '"' + container_name + '"', 
                               'type': 'link_choice_menu', 
                               'options': [
                                         {'link': container['Names'][0][1:]}]})

                        if not args.no_curses:
                            self.config_dict = {}
                            self.config_dict['services'] = []
                            config_dict = self.config_dict
                            config_dict = self.options_menu(self, args, options_dict, config_dict)
                            self.config_dict = config_dict
                            curses.endwin()

            else:
                for host in self.hosts:
                    c = docker.Client(base_url='tcp://' + host['title'] + ':2375', version='1.12', timeout=2)
                    containers.append(c.containers())
                    print containers

            if len(containers) == 0:
                print 'There are no running containers on the host to link to.'
                junk = raw_input('Press enter to continue...')
            else:
                if not args.no_curses:
                    curses.noecho()
                    curses.cbreak()
                    curses.start_color()
                    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
                options_dict = {'title': 'Containers to Link', 
                   'type': 'menu', 
                   'subtitle': 'Please select the containers you would like to link...', 
                   'options': []}
                for host in containers:
                    for container in host:
                        container_name = ''
                        names = container['Names']
                        for n in names:
                            container_name += n[1:] + ' - '

                        container_id = container['Id']
                        container_name += container_id
                        options_dict['options'].append({'title': '"' + container_name + '"', 
                           'type': 'link_choice_menu', 
                           'options': [
                                     {'link': container['Names'][0][1:]}]})

            if not args.no_curses:
                self.config_dict = {}
                self.config_dict['services'] = []
                config_dict = self.config_dict
                config_dict = self.options_menu(self, args, options_dict, config_dict)
                self.config_dict = config_dict
                curses.endwin()
            print self.link
        if self.port:
            print self.port
        if self.volume:
            volumes = []
            no = True
            while no:
                volume = raw_input('Enter a volume (path:path): ')
                volumes.append(volume)
                no = self.query_yes_no(self, 'Would you like to add another volume?', default='no')

            print self.volume
            print volumes
        if self.entrypoint:
            entrypoint = raw_input('Enter new runtime ENTRYPOINT: ')
            print entrypoint
        if self.cmd:
            cmd = raw_input('Enter new runtime CMD: ')
            print cmd
        if self.image:
            for index, image_info in enumerate(self.build_dict['services']):
                image_tag, image_host = image_info.split(',', 1)
                c = docker.Client(base_url='tcp://' + image_host + ':2375', version='1.12', timeout=2)
                cmd = raw_input('Enter command you wish to use for ' + image_tag + ': ')
                if len(self.names) != 0:
                    if self.unique:
                        container = c.create_container(image_tag, command=cmd, tty=True, stdin_open=True, name=self.names[index], hostname=self.names[index])
                    else:
                        container = c.create_container(image_tag, command=cmd, tty=True, stdin_open=True, name=self.names[0], hostname=self.names[0])
                else:
                    container = c.create_container(image_tag, command=cmd, tty=True, stdin_open=True)
                c.start(container, publish_all_ports=True)

        if self.launch and not self.image:
            if self.user:
                username = raw_input('Enter username: ')
                ssh_pubkey = raw_input('Enter path to ssh public key: ')
            this_dir, this_filename = os.path.split(__file__)
            services = self.build_dict['services']
            if len(services) == 0:
                print 'No services were selected.'
            else:
                print 'The following services have been selected and will be packaged up into a container: '
                print services
                dockerfile = []
                num_services = len(services)
                envs = {}
                workdirs = {}
                entrypoints = {}
                cmds = {}
                uuid_dir = str(uuid.uuid4())
                os.mkdir('/tmp/' + uuid_dir)
                for service in sorted(services):
                    service_orig = service
                    service = service.split(', ')[0]
                    envs[service] = []
                    workdirs[service] = []
                    entrypoints[service] = []
                    cmds[service] = []
                    entrypoint = '/bin/sh -c'
                    cmd = ''
                    service_name = service.split(':', 3)
                    key = ('.').join(service_name)
                    os_flavor = ('/').join(service_name[0:3])
                    repo_args = Object()
                    repo_args.z = True
                    repo_args.metadata_path = os.path.expanduser(args.metadata_path)
                    repos = repositories.repositories.main(repo_args)
                    try:
                        copied = 0
                        for repo in repos:
                            if repo.split(', ')[0].strip() == service_orig.split(', ')[1].strip() and copied == 0:
                                copied = 1
                                shutil.copytree(os.path.join(repo.split(', ')[2], os_flavor + '/dockerfiles/' + service_name[3]), '/tmp/' + uuid_dir + '/' + service_name[3])
                                path = os.path.join(repo.split(', ')[2], os_flavor + '/dockerfiles/' + service_name[3] + '/Dockerfile')

                        with open(path, 'r') as (f):
                            for line in f:
                                if line.rstrip('\n') not in dockerfile:
                                    if line.startswith('EXPOSE'):
                                        if any(cmd.startswith('EXPOSE') for cmd in dockerfile):
                                            line = (' ').join(line.rstrip('\n').split(' ', 1)[1:])
                                            matching = [ s for s in dockerfile if 'EXPOSE' in s ]
                                            matching.append(line)
                                            dockerfile.remove(matching[0])
                                            dockerfile.append((' ').join(matching))
                                        else:
                                            dockerfile.append(line.rstrip('\n'))
                                    elif line.startswith('ADD'):
                                        add_line = line.rstrip('\n').split()
                                        dockerfile.append(add_line[0] + ' ' + service_name[3] + '/' + add_line[1] + ' ' + add_line[2])
                                    elif line.startswith('COPY'):
                                        copy_line = line.rstrip('\n').split()
                                        dockerfile.append(copy_line[0] + ' ' + service_name[3] + '/' + copy_line[1] + ' ' + copy_line[2])
                                    elif line.startswith('USER'):
                                        if num_services == 1:
                                            dockerfile.append(line.rstrip('\n'))
                                        elif self.combine_cmd_dict[key] == 'yes':
                                            envs[service].append(line.rstrip('\n'))
                                    elif line.startswith('ENV'):
                                        if num_services == 1:
                                            dockerfile.append(line.rstrip('\n'))
                                        else:
                                            if self.combine_cmd_dict[key] == 'yes':
                                                envs[service].append(line.rstrip('\n'))
                                            dockerfile.append(line.rstrip('\n'))
                                    elif line.startswith('WORKDIR'):
                                        if num_services == 1:
                                            dockerfile.append(line.rstrip('\n'))
                                        else:
                                            if self.combine_cmd_dict[key] == 'yes':
                                                workdirs[service].append(line.rstrip('\n'))
                                            dockerfile.append(line.rstrip('\n'))
                                    elif line.startswith('ENTRYPOINT'):
                                        if num_services == 1:
                                            dockerfile.append(line.rstrip('\n'))
                                        elif self.combine_cmd_dict[key] == 'yes':
                                            entrypoints[service].append(line.rstrip('\n'))
                                        entrypoint = line.rstrip('\n').split(' ', 1)[1:][0]
                                    elif line.startswith('CMD'):
                                        if num_services == 1:
                                            dockerfile.append(line.rstrip('\n'))
                                        elif self.combine_cmd_dict[key] == 'yes':
                                            cmds[service].append(self.background_cmd_dict[key])
                                        cmd = line.rstrip('\n').split(' ', 1)[1:][0]
                                    else:
                                        dockerfile.append(line.rstrip('\n'))

                    except:
                        print 'Dockerfile not found'

                if len(cmds) > 1:
                    print '\nFound more than one service that runs a command, installing supervisord...'
                    dockerfile.append('RUN apt-get install -y supervisor')
                    for cmd in cmds:
                        cmd_a = cmd.split(':')
                        with open('/tmp/' + uuid_dir + '/' + cmd_a[(-1)] + '.conf', 'w') as (f):
                            f.write('[program:' + cmd_a[(-1)] + ']\n')
                            f.write('command=' + cmds[cmd][0])
                            dockerfile.append('ADD ' + cmd_a[(-1)] + '.conf /etc/supervisor/conf.d/' + cmd_a[(-1)] + '.conf')

                if self.user:
                    try:
                        with open(os.path.expanduser(ssh_pubkey), 'r') as (fi):
                            with open('/tmp/' + uuid_dir + '/authorized_keys', 'w') as (fo):
                                for line in fi:
                                    fo.write(line)

                        dockerfile.append('RUN useradd ' + username)
                        dockerfile.append('RUN mkdir -p /home/' + username + '/.ssh && chown ' + username + ' /home/' + username + '/.ssh && chmod 700 /home/' + username + '/.ssh')
                        dockerfile.append('ADD authorized_keys /home/' + username + '/.ssh/authorized_keys')
                        dockerfile.append('RUN apt-get install -y sudo')
                        dockerfile.append('RUN echo "' + username + ' ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers')
                    except:
                        print 'SSH Key file not found, failed to create user'

                print '\n### GENERATED DOCKERFILE ###'
                cmd = False
                for line in dockerfile:
                    if 'CMD' in line:
                        cmd = True

                if not cmd:
                    if len(cmds) > 1:
                        dockerfile.append('CMD /usr/bin/supervisord -n')
                    else:
                        dockerfile.append('CMD /bin/bash')
                for line in dockerfile:
                    print line

                print '### END GENERATED DOCKERFILE ###\n'
                self.build_dockerfile(self, dockerfile, uuid_dir, args)
                print self.link_names

    @staticmethod
    def display_menu(self, args, menu, parent, build_dict):
        option_size = len(menu['options'])
        hash_menu = hash(str(menu))
        choice = []
        if hash_menu in self.menus_dict:
            choice = self.menus_dict[hash_menu]
        else:
            choice = [
             ' '] * (option_size + 1)
            self.menus_dict[hash_menu] = choice
        if parent is None:
            back = 'Exit'
        else:
            back = 'Return to %s menu' % parent['title']
        position = 0
        key = None
        if not args.no_curses:
            highlighted = curses.color_pair(1)
            normal = curses.A_NORMAL
        else:
            highlighted = ''
            normal = ''
        while key != ord('\n'):
            if not args.no_curses:
                self.win.clear()
                self.win.border(0)
                self.win.addstr(2, 2, menu['title'], curses.A_STANDOUT)
                self.win.addstr(4, 2, menu['subtitle'], curses.A_BOLD)
            for index in range(option_size):
                textstyle = normal
                if position == index:
                    textstyle = highlighted
                if not args.no_curses:
                    if menu['options'][index]['title'] == 'Docker Hosts':
                        self.win.addstr(index + 6, 4, '%d - %s' % (index + 1, menu['options'][index]['title']), textstyle)
                    elif menu['options'][index]['type'] == 'choice_menu' or menu['options'][index]['type'] == 'link_choice_menu':
                        self.win.addstr(index + 5, 4, '%d - [%s] %s' % (index + 1, choice[index], menu['options'][index]['title']), textstyle)
                    elif menu['options'][index]['type'] == 'image_choice_menu':
                        self.win.addstr(index + 5, 4, '%d - [%s] %s | %s' % (index + 1, choice[index], menu['options'][index]['title'], menu['options'][index]['host']), textstyle)
                    elif menu['options'][index]['type'] == 'launch':
                        self.win.addstr(index + 6, 4, '%d - %s' % (index + 1, menu['options'][index]['title']), textstyle)
                    else:
                        self.win.addstr(index + 5, 4, '%d - %s' % (index + 1, menu['options'][index]['title']), textstyle)

            textstyle = normal
            if position == option_size:
                textstyle = highlighted
            if back != 'Exit':
                if 'object' in parent and parent['object'] == 'os':
                    if len(build_dict['services']) > 0:
                        back = 'Exit'
                else:
                    back = 'Return to %s menu' % parent['title']
            if not args.no_curses:
                self.win.addstr(option_size + 6, 4, '%d - %s' % (option_size + 1, back), textstyle)
                self.win.refresh()
                key = self.win.getch()
            try:
                if key >= ord('1') and key <= ord(str(option_size + 1)):
                    position = key - ord('0') - 1
                elif key == 258:
                    if position < option_size:
                        position += 1
                    else:
                        position = 0
                elif key == 259:
                    if position > 0:
                        position -= 1
                    else:
                        position = option_size
                elif key == 32 and menu['options'][position]['type'] == 'link_choice_menu':
                    if choice[position] == ' ':
                        choice[position] = 'x'
                        self.link_names[menu['options'][position]['options'][0]['link']] = menu['options'][position]['options'][0]['link']
                    else:
                        choice[position] = ' '
                elif key == 32 and (menu['options'][position]['type'] == 'choice_menu' or menu['options'][position]['type'] == 'image_choice_menu'):
                    if choice[position] == ' ':
                        choice[position] = 'x'
                        if 'command' in menu['options'][position]:
                            build_dict['services'].append(menu['options'][position]['command'] + ', ' + menu['options'][position]['repository'])
                        elif self.default:
                            self.hosts.append(menu['options'][position])
                        elif 'options' in menu['options'][position]:
                            if 'config' in menu['options'][position]['options'][0]:
                                if 'unique' == menu['options'][position]['options'][0]['config']:
                                    self.unique = True
                                if 'cmd' == menu['options'][position]['options'][0]['config']:
                                    self.cmd = True
                                if 'entrypoint' == menu['options'][position]['options'][0]['config']:
                                    self.entrypoint = True
                                if 'volume' == menu['options'][position]['options'][0]['config']:
                                    self.volume = True
                                if 'port' == menu['options'][position]['options'][0]['config']:
                                    self.port = True
                                if 'link' == menu['options'][position]['options'][0]['config']:
                                    self.link = True
                                if 'name' == menu['options'][position]['options'][0]['config']:
                                    self.name = True
                                if 'user' == menu['options'][position]['options'][0]['config']:
                                    self.user = True
                    else:
                        choice[position] = ' '
                        if 'command' in menu['options'][position]:
                            build_dict['services'].remove(menu['options'][position]['command'] + ', ' + menu['options'][position]['repository'])
                        elif self.default:
                            self.hosts.remove(menu['options'][position])
                        elif 'options' in menu['options'][position]:
                            if 'config' in menu['options'][position]['options'][0]:
                                if 'unique' == menu['options'][position]['options'][0]['config']:
                                    self.unique = False
                                if 'cmd' == menu['options'][position]['options'][0]['config']:
                                    self.cmd = False
                                if 'entrypoint' == menu['options'][position]['options'][0]['config']:
                                    self.entrypoint = False
                                if 'volume' == menu['options'][position]['options'][0]['config']:
                                    self.volume = False
                                if 'port' == menu['options'][position]['options'][0]['config']:
                                    self.port = False
                                if 'link' == menu['options'][position]['options'][0]['config']:
                                    self.link = False
                                if 'name' == menu['options'][position]['options'][0]['config']:
                                    self.name = False
                                if 'user' == menu['options'][position]['options'][0]['config']:
                                    self.user = False
                elif key != ord('\n'):
                    if not args.no_curses:
                        curses.flash()
            except:
                if not args.no_curses:
                    curses.flash()

            self.menus_dict[hash_menu] = choice

        return (
         position, back, build_dict)

    @staticmethod
    def options_menu(self, args, menu, config_dict, parent=None):
        option_size = len(menu['options'])
        exit_menu = False
        while not exit_menu:
            position, back, config_dict = self.display_menu(self, args, menu, parent, config_dict)
            if position == option_size:
                exit_menu = True

        return config_dict

    @staticmethod
    def process_menu(self, args, menu, build_dict, parent=None):
        option_size = len(menu['options'])
        exit_menu = False
        while not exit_menu and not self.launch and not self.exit:
            position, back, build_dict = self.display_menu(self, args, menu, parent, build_dict)
            if position == option_size:
                exit_menu = True
                if back == 'Exit':
                    self.exit = True
            elif menu['options'][position]['type'] == 'menu':
                build_dict = self.process_menu(self, args, menu['options'][position], build_dict, menu)
            elif menu['options'][position]['type'] == 'launch':
                if position == 1:
                    self.image = True
                self.launch = True

        return build_dict