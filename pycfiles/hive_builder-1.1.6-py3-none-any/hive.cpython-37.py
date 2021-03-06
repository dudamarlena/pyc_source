# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mitsuru/Projects/hive-builder/hive/hive.py
# Compiled at: 2019-09-26 09:30:10
# Size of source mod 2**32: 22269 bytes
"""
hive: support tool to build docker site
"""
import argparse, configparser, subprocess, os, yaml
from logging import getLogger, StreamHandler, DEBUG, INFO
import backtrace, sys, re, select, termios, tty, pty, signal, time, pathlib

def get_python_path():
    for path in os.getenv('PATH').split(os.path.pathsep):
        full_path = os.path.join(path, 'python')
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path


class Error(Exception):
    pass


def directory_cast(directory):
    if directory.endswith('/'):
        directory = directory[:-1]
    if not os.path.isdir(directory):
        raise Error(f"{directory} is not a directory")
    return os.path.abspath(directory)


def int_cast(int_string):
    try:
        return int(int_string)
    except ValueError:
        raise Error(f"cannot parse as integer {int_string}")


def enum_cast(value, options):
    if value not in options:
        raise Error(f"value {value} not in {options}")
    return value


def bool_cast(s):
    if s.lower() in ('true', 'yes', '1'):
        return True
    if s.lower() in ('false', 'no', '0'):
        return False
    raise Error(f'boolean value {s} not in ["true", "yes", "1", "false", "no", "0"]')


class commandHandlerBase:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.logger = getLogger('hive')

    def setup_parser(self, subparsers, variables_metainf):
        self.subparser = subparsers.add_parser((self.name),
          description=(self.description), help=('see `{0} -h`'.format(self.name)))
        self.subparser.set_defaults(handler=self)


class initializeEnvironment(commandHandlerBase):

    def __init__(self):
        super().__init__('init', 'initialize hive environment')

    def do(self, context):
        if context.initialize():
            self.logger.info('Success to initialize hive context on {0}'.format(f"{context.vars['root_dir']}/.hive"))
        else:
            self.logger.info('hive context on {0} is already initialized'.format(f"{context.vars['root_dir']}/.hive"))


class setPersistent(commandHandlerBase):

    def __init__(self):
        super().__init__('set', 'set hive variable persistently')

    def do(self, context):
        name = context.args.variable_name
        casted_value = context.get_cast(name)(context.args.value)
        scope = context.set_persistent(name, casted_value)
        context.save_persistent()
        context.logger.info(f"set persistently {casted_value} to {name} on {scope}")

    def setup_parser(self, subparsers, variables_metainf):
        super().setup_parser(subparsers, variables_metainf)
        self.subparser.add_argument('variable_name', help='variable name')
        self.subparser.add_argument('value', help='variable value')


class hiveContext:

    def __init__(self):
        self.init_logger()

    def setup(self, subcommand_handlers):
        self.load_variables_metainf()
        self.args = self.get_parser(subcommand_handlers).parse_args()
        self.reset_logger()
        self.vars = {'root_dir':self.args.root_dir,  'install_dir':os.path.abspath(os.path.dirname(__file__)), 
         'local_python_path':get_python_path()}
        self.load_persistents()
        self.load_command_line_options()
        self.overwritables = []
        self.load_defaults()
        self.overwritables = []
        self.logger.debug(f"varaiables initialized as {self.vars}")

    def load_variables_metainf(self):
        variables_metainf_path = os.path.dirname(__file__) + '/variables_metainf.yml'
        if os.path.exists(variables_metainf_path):
            with open(variables_metainf_path, 'r+') as (envf):
                self.variables_metainf = yaml.load(envf, Loader=(yaml.SafeLoader))
            self.logger.debug('variables meta information {0} is loaded from {1}'.format(self.variables_metainf, variables_metainf_path))

    def load_persistents(self):
        persistent_values_path = f"{self.vars['root_dir']}/.hive/persistents.yml"
        if os.path.exists(persistent_values_path):
            with open(persistent_values_path, 'r+') as (envf):
                self.persistent_values = yaml.load(envf, Loader=(yaml.SafeLoader))
            self.logger.debug('persistent values {0} is loaded from {1}'.format(self.persistent_values, persistent_values_path))
        else:
            self.persistent_values = {}
        self.vars.update(dict(((k, v['global']) for k, v in self.persistent_values.items() if 'global' in v)))
        if 'stage' not in self.vars:
            self.vars['stage'] = self.variables_metainf['stage']['default']
        self.vars.update(dict(((k, v[self.vars['stage']]) for k, v in self.persistent_values.items() if self.vars['stage'] in v)))

    def save_persistent(self):
        persistent_values_path = f"{self.vars['root_dir']}/.hive/persistents.yml"
        with open(persistent_values_path, 'w') as (envf):
            yaml.dump((self.persistent_values), envf, default_flow_style=False)

    def set_persistent(self, name, value):
        self.initialize()
        if name not in self.variables_metainf:
            raise Error(f"unknown variable {name}")
        metainf = self.variables_metainf[name]
        if 'persistent_scope' in metainf:
            if metainf['persistent_scope'] == 'none':
                raise Error(f"variable {name} can not be saved persistently")
        persistent_scope = metainf['persistent_scope'] if 'persistent_scope' in metainf else 'global'
        key = self.vars['stage'] if persistent_scope == 'stage' else 'global'
        if name not in self.persistent_values:
            self.persistent_values[name] = {}
        self.persistent_values[name][key] = value
        return key

    def load_defaults(self):
        vars_defaults = [(k, v['default']) for k, v in self.variables_metainf.items() if 'default' in v]
        dirty = True
        while dirty:
            dirty = False
            for k, v in vars_defaults:
                new_value = v
                try:
                    if type(v) == str:
                        new_value = (v.format)(**self.vars)
                except Exception:
                    pass
                else:
                    if (k not in self.vars or k) in self.overwritables:
                        if self.vars[k] != new_value:
                            self.vars[k] = new_value
                            if k not in self.overwritables:
                                self.overwritables.append(k)
                        dirty = True

    def initialize(self):
        path = f"{self.vars['root_dir']}/.hive"
        if not os.path.exists(path):
            os.mkdir(path)
            return True
        return False

    def get_cast(self, name):
        if name not in self.variables_metainf:
            raise Error(f"unknown variable {name}")
        else:
            metainf = self.variables_metainf[name]
            if 'type' in metainf:
                if metainf['type'] == 'boolean':
                    return bool_cast
            if 'type' in metainf:
                if metainf['type'] == 'enum':
                    return lambda x: enum_cast(x, metainf['options'])
            if 'type' in metainf:
                if metainf['type'] == 'integer':
                    return int_cast
            if 'type' in metainf and metainf['type'] == 'directory':
                return directory_cast
        return str

    @staticmethod
    def add_argument(parser, name, metainf, mutually_exclusive_group_map, help_format_dict):
        long_option = f"--{name.replace('-', '_')}"
        kwargs = {'help': (metainf['description'].format)(**help_format_dict)}
        if 'type' in metainf:
            if metainf['type'] == 'boolean':
                kwargs['action'] = 'store_true'
        if 'type' in metainf:
            if metainf['type'] == 'enum':
                kwargs['choices'] = metainf['options']
        if 'type' in metainf:
            if metainf['type'] == 'integer':
                kwargs['type'] = int_cast
        if 'type' in metainf:
            if metainf['type'] == 'directory':
                kwargs['type'] = directory_cast
        target = parser
        if 'command_line_mutually_exclusive_group' in metainf:
            group_name = metainf['command_line_mutually_exclusive_group']
            if group_name not in mutually_exclusive_group_map:
                mutually_exclusive_group_map[group_name] = parser.add_mutually_exclusive_group()
            target = mutually_exclusive_group_map[group_name]
        (target.add_argument)((metainf['command_line_option']), long_option, **kwargs)

    def get_parser(self, subcommand_handlers):
        parser = argparse.ArgumentParser(description='support tool to build docker site')
        mutually_exclusive_group_map = {}
        for metainf in [(k, v) for k, v in self.variables_metainf.items() if 'command_line_option' in v and ('command_line_option_level' not in v or v['command_line_option_level'] == 'global')]:
            hiveContext.add_argument(parser, metainf[0], metainf[1], mutually_exclusive_group_map, {})

        parser.set_defaults(root_dir=(os.getcwd()))
        subparsers = parser.add_subparsers(title='subcommands')
        for handler in subcommand_handlers:
            handler.setup_parser(subparsers, self.variables_metainf)

        return parser

    def load_command_line_options(self):
        self.vars.update(dict(((k, getattr(self.args, k)) for k, v in self.variables_metainf.items() if k != 'root_dir' if 'command_line_option' in v if hasattr(self.args, k) if getattr(self.args, k))))

    def do_subcommand(self):
        self.args.handler.do(self)

    def init_logger(self):
        self.logger = getLogger('hive')
        self.standard_handler = StreamHandler()
        self.logger.addHandler(self.standard_handler)
        self.logger.propagate = False
        self.standard_handler.setLevel(INFO)
        self.logger.setLevel(INFO)

    def reset_logger(self):
        if self.args.verbose:
            self.standard_handler.setLevel(DEBUG)
            self.logger.setLevel(DEBUG)


def sigchld_handler(sig, frame):
    raise InterruptedError()


def get_popen_lines(proc, master_fd, slave_fd):
    o = ''
    while proc.poll() is None:
        r = []
        w = []
        e = []
        try:
            try:
                signal.signal(signal.SIGCHLD, sigchld_handler)
                r, w, e = select.select([sys.stdin, master_fd], [], [])
            except InterruptedError:
                pass

        finally:
            signal.signal(signal.SIGCHLD, signal.SIG_IGN)

        if sys.stdin in r:
            d = os.read(sys.stdin.fileno(), 40960)
            if d.find(b'\x03') >= 0:
                proc.send_signal(signal.SIGINT)
                raise Error('Keyboard Interrupt')
            os.write(master_fd, d)
        elif master_fd in r:
            o += os.read(master_fd, 40960)
            while o.find(b'\n') > 0:
                bline = o[:o.find(b'\n') + 1]
                o = o[o.find(b'\n') + 1:]
                os.write(sys.stdout.fileno(), bline)
                yield bline.decode('utf-8')

    if len(o) > 0:
        yield o.decode('utf-8')


RECAP_PATTERN = re.compile('[^ :]*[ :]*ok=(\\d*)\\s*changed=(\\d*)\\s*unreachable=(\\d*)\\s*failed=(\\d*)\\s*skipped=(\\d*)\\s*rescued=(\\d*)\\s*ignored=(\\d*)\\s*')
ANSI_ESCAPE = re.compile('\\x1b[^m]*m')

def run_and_check_ansible_playbook(args):
    old_tty = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    master_fd, slave_fd = pty.openpty()
    try:
        proc = subprocess.Popen(args, stdin=slave_fd, stdout=slave_fd,
          stderr=slave_fd,
          start_new_session=True,
          universal_newlines=True)
        wait_recap = True
        error_count = 0
        for line in get_popen_lines(proc, master_fd, slave_fd):
            line = ANSI_ESCAPE.sub('', line)
            if wait_recap:
                if line.startswith('PLAY RECAP'):
                    wait_recap = False
                else:
                    m = RECAP_PATTERN.match(line)
                    if m:
                        error_count += int(m.group(3)) + int(m.group(4))

        if proc.returncode != 0:
            raise Error(f"ansible-playbook command failed: exit code = {proc.returncode}")
        if error_count > 0:
            raise Error(f"{error_count} tasks failed or unreachable")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


HOST_DEF_PATTERN = re.compile('^Host *(.*)$')

class ansbileCommandBase(commandHandlerBase):

    def get_playbook_path(self, vars):
        return f"{vars['playbooks_dir']}/{self.name}.yml"

    def collect_ansible_vars(self, vars, variables_metainf):
        ansible_vars = dict(((v['name_in_ansible'], vars[k]) for k, v in variables_metainf.items() if k in vars if 'name_in_ansible' in v))
        return ansible_vars

    def collect_ansible_cfg_vars(self, vars, variables_metainf):
        ansible_cfg_vars = [dict(name=(v['name_in_ansible_cfg']), value=(vars[k]), section=(v['section_in_ansible_cfg'] if 'section_in_ansible_cfg' in v else 'defaults')) for k, v in variables_metainf.items() if k in vars if 'name_in_ansible_cfg' in v]
        return ansible_cfg_vars

    def collect_environment_vars(self, vars, variables_metainf, ansible_cfg_file_path):
        environment_vars = dict(((v['name_in_environment'], vars[k]) for k, v in variables_metainf.items() if k in vars if 'name_in_environment' in v))
        environment_vars['ANSIBLE_CONFIG'] = ansible_cfg_file_path
        return environment_vars

    def build_context(self, context):
        context.load_defaults()
        context_dir = context.vars['context_dir']
        temp_dir = context.vars['temp_dir']
        os.makedirs(context_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        ansible_vars = self.collect_ansible_vars(context.vars, context.variables_metainf)
        self.vars_file_path = f"{temp_dir}/vars.yml"
        context.logger.debug(f"ansible extra variables: {ansible_vars}")
        with open(self.vars_file_path, 'w') as (varsf):
            yaml.dump(ansible_vars, varsf, default_flow_style=False)
            ansible_cfg_vars = self.collect_ansible_cfg_vars(context.vars, context.variables_metainf)
            context.logger.debug(f"ansible cfg setting {ansible_cfg_vars}")
            config = configparser.ConfigParser(interpolation=(configparser.ExtendedInterpolation()))
            for var in ansible_cfg_vars:
                if not config.has_section(var['section']):
                    config.add_section(var['section'])
                config.set(var['section'], var['name'], str(var['value']))

            ansible_cfg_file_path = f"{temp_dir}/ansible.cfg"
            with open(ansible_cfg_file_path, 'w') as (cfg_varsf):
                config.write(cfg_varsf)
            environment_vars = self.collect_environment_vars(context.vars, context.variables_metainf, ansible_cfg_file_path)
            for k, v in environment_vars.items():
                os.environ[k] = v

            context.logger.debug(f"environment variables: {os.environ}")

    def setup_parser(self, subparsers, variables_metainf):
        super().setup_parser(subparsers, variables_metainf)
        mutually_exclusive_group_map = {}
        for variable in [(k, v) for k, v in variables_metainf.items() if 'command_line_option' in v if 'command_line_option_level' in v if v['command_line_option_level'] == 'phase' if self.name in v['command_line_option_available']]:
            hiveContext.add_argument(self.subparser, variable[0], variable[1], mutually_exclusive_group_map, {'subject_name': self.subject_name})


class phaseBase(ansbileCommandBase):

    def do(self, context):
        context.vars['phase'] = self.name
        self.build_context(context)
        self.do_one(context)

    def get_limit_targets(self, context):
        return context.vars['stage']

    def do_one(self, context):
        context.logger.info(f"=== PHASE {self.name} START at {time.strftime('%Y-%m-%d %H:%M:%S %z')} ===")
        args = ['ansible-playbook', '--limit', self.get_limit_targets(context)]
        if 'verbose' in context.vars:
            if context.vars['verbose']:
                args.append('-vvv')
        if 'check_mode' in context.vars:
            if context.vars['check_mode']:
                args.append('-C')
        args += ['--extra-vars', f"@{self.vars_file_path}"]
        args.append(self.get_playbook_path(context.vars))
        context.logger.debug(f"commnad={args}")
        run_and_check_ansible_playbook(args)
        context.set_persistent('start_phase', self.name)
        if not context.vars.get('destroy'):
            next_idx = PHASE_LIST.index(self) + 1
            if next_idx < len(PHASE_LIST):
                context.set_persistent('start_phase', PHASE_NAME_LIST[next_idx])
        context.save_persistent()
        context.logger.info(f"=== PHASE {self.name} END at {time.strftime('%Y-%m-%d %H:%M:%S %z')} ===")


class buildInfra(phaseBase):

    def __init__(self):
        super().__init__('build-infra', 'build infrastructure, setup networks, global ip, firewall')
        self.subject_name = 'vpc/subnet/host'


class setupHosts(phaseBase):

    def __init__(self):
        super().__init__('setup-hosts', 'setup hosts, install software, configure services, configure cluster')
        self.subject_name = 'host'

    def get_limit_targets(self, context):
        target = context.vars['stage']
        if 'limit_target' in context.vars:
            target += ',' + context.vars['limit_target']
        return target


class buildImages(phaseBase):

    def __init__(self):
        super().__init__('build-images', 'build container images')
        self.subject_name = 'container'

    def do_one(self, context):
        socket_path = f"{context.vars['temp_dir']}/docker_repository.sock"
        if pathlib.Path(socket_path).is_socket():
            raise Error(f"fail to create socket {socket_path}, another hive process may doing build-image" + ' or the file has been left because previus hive process aborted suddenly')
        ssh_config_path = context.vars['context_dir'] + '/ssh_config'
        grep_proc = subprocess.run(['grep', '^Host ', ssh_config_path], stdout=(subprocess.PIPE))
        if grep_proc.returncode == 1:
            raise Error(f"no Host entry in {ssh_config_path}")
        if grep_proc.returncode != 0:
            raise Error(f"fail to read ssh_config {ssh_config_path} error, you may never done build-infra: {grep_proc.stderr}")
        *_, last_host = map(lambda x: x.decode(encoding='utf-8').split(' ')[1], grep_proc.stdout.splitlines())
        args = ['ssh', '-N', '-F', ssh_config_path, '-L', socket_path + ':/var/run/docker.sock', last_host]
        ssh_tunnel_proc = subprocess.Popen(args)
        try:
            super().do_one(context)
        finally:
            ssh_tunnel_proc.send_signal(signal.SIGTERM)
            ssh_tunnel_proc.wait()
            os.remove(socket_path)


class buildVolumes(phaseBase):

    def __init__(self):
        super().__init__('build-volumes', 'build volumes on hives')
        self.subject_name = 'volume'


class buildNetworks(phaseBase):

    def __init__(self):
        super().__init__('build-networks', 'build networks for swarm')
        self.subject_name = 'ingress network'


class deployServices(phaseBase):

    def __init__(self):
        super().__init__('deploy-services', 'deploy services')
        self.subject_name = 'service'


class initializeServices(phaseBase):

    def __init__(self):
        super().__init__('initialize-services', 'initialize services')
        self.subject_name = 'service'

    def get_playbook_path(self, vars):
        return f"{vars['root_dir']}/{self.name}.yml"


PHASE_LIST = [
 buildInfra(), setupHosts(), buildImages(),
 buildVolumes(), buildNetworks(), deployServices(), initializeServices()]
PHASE_NAME_LIST = list(map(lambda x: x.name, PHASE_LIST))

class allPhase(phaseBase):

    def __init__(self):
        super().__init__('all', 'do all phase')
        self.subject_name = 'all'

    def do(self, context):
        start_phase_idx = PHASE_NAME_LIST.index(context.vars['start_phase'])
        last_idx = len(PHASE_LIST)
        for idx in range(start_phase_idx, last_idx):
            PHASE_LIST[idx].build_context(context)
            PHASE_LIST[idx].do_one(context)


class inventoryList(ansbileCommandBase):

    def __init__(self):
        super().__init__('inventory', 'list ansible inventory')

    def do(self, context):
        self.build_context(context)
        args = ['ansible-inventory',
         '--playbook-dir=' + context.vars['playbooks_dir'], '--list']
        subprocess.run(args)


class execSsh(ansbileCommandBase):

    def __init__(self):
        super().__init__('ssh', 'ssh to hive server')
        self.subject_name = 'host'

    def do(self, context):
        self.build_context(context)
        ssh_config_path = context.vars['context_dir'] + '/ssh_config'
        grep_proc = subprocess.run(['grep', '^Host ', ssh_config_path], stdout=(subprocess.PIPE))
        if grep_proc.returncode == 1:
            raise Error(f"no Host entry in {ssh_config_path}")
        if grep_proc.returncode != 0:
            raise Error(f"fail to read ssh_config {ssh_config_path} error, you may never done build-infra: {grep_proc.stderr}")
        hosts = list(map(lambda x: x.decode(encoding='utf-8').split(' ')[1], grep_proc.stdout.splitlines()))
        ssh_host = context.vars.get('ssh_host')
        if ssh_host is None:
            ssh_host = hosts[(len(hosts) - 1)]
        else:
            if ssh_host not in hosts:
                raise Error(f"host {ssh_host} is not found in {ssh_config_path}")
            else:
                args = [
                 '/usr/bin/ssh', '-F', ssh_config_path]
                if context.vars['foward_zabbix']:
                    args += ['-L', f"localhost:{context.vars['foward_zabbix_port']}:{ssh_host}:10052"]
                args += [ssh_host]
                try:
                    ssh_proc = subprocess.Popen(args)
                    ssh_proc.wait()
                except KeyboardInterrupt:
                    ssh_proc.send_signal(signal.SIGTERM)
                    ssh_proc.wait()


SUBCOMMANDS = PHASE_LIST + [allPhase(), inventoryList(), initializeEnvironment(), setPersistent(), execSsh()]

def get_parser():
    context = hiveContext()
    context.load_variables_metainf()
    return context.get_parser(SUBCOMMANDS)


def main():
    context = hiveContext()
    try:
        context.setup(SUBCOMMANDS)
        context.do_subcommand()
    except Error as e:
        try:
            context.logger.error(f"HIVE ERROR: {str(e)}")
            sys.exit(1)
        finally:
            e = None
            del e

    except Exception:
        tpe, v, tb = sys.exc_info()
        backtrace.hook(reverse=True, strip_path=True, tb=tb, tpe=tpe, value=v)
        sys.exit(1)


if __name__ == '__main__':
    main()