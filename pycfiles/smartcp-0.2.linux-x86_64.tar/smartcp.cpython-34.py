# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/smartcp.py
# Compiled at: 2015-01-15 10:30:21
# Size of source mod 2**32: 9516 bytes
from __future__ import print_function
from __version__ import version
import yaml, itertools, os, filecmp, sys, getopt, shutil
from subprocess import call

def usage():
    print('Usage: {0} [OPTION]... [FILE]...\nRead FILE(s) and do smart copies accordingly.\n\n-q, --quiet      do not print the stdout of the command executed with -x\n                 with -qq, it does not print stderr neither\n-n, --no-copy    do not do the copy but execute the command given by -x\n-s, --set        with the syntax arg=value,\n                 set the argument with lablel arg to value instead of\n                 iterating over all different possible values\n-v               increment verbose level, -vv gives the most verbose output\n-x  command      execute command in the parent directory of the input\n                 before comparting the input and the output\n-h, --help       display this help and exit\n    --version    output version information and exit\n\nWith no FILE, or when FILE is -, read standard input.\n\nExamples:\n{0} config.yml - */config.yml  Do smart copies for config.yml,\n                               then standard input,\n                               then all config.yml in a subdirectory.\n{0}                            Do smart copies for standard output.'.format(program_name))


def show_version():
    print('{} {}\nCopyright (C) 2013 Benoît Legat.\nLicense GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Benoît Legat.'.format(program_name, version))


def ask_yes_or_no(prompt):
    while True:
        s = input(prompt)
        if len(s) == 0 or s in ('y', 'Y', 'yes', 'Yes'):
            return True
        if s in ('n', 'N', 'no', 'No'):
            return False
        print("Please answer 'y' or 'n'.")


def parent_dir_exists(path):
    folder = os.path.dirname(os.path.abspath(path))
    last = None
    current = folder
    while not os.path.exists(current):
        last = current
        current = os.path.dirname(current)

    if current != folder:
        if ask_yes_or_no('Create {} in {} ? [Y/n]: '.format(os.path.basename(last), current)):
            os.makedirs(last)
            return parent_dir_exists(path)
        print_err('There is no {} in {}'.format(os.path.basename(last), current))
        return False
    return True


def up_to_date(input_path, output_path):
    return os.path.exists(output_path) and filecmp.cmp(input_path, output_path)


def get(hash_map, key, raise_err=True):
    if key in hash_map:
        return hash_map[key]
    if raise_err:
        print_err("Missing key `{}' in `{}'".format(key, hash_map))
        sys.exit(1)
    else:
        return


def build_path(path_desc, arguments):
    if 'path_format' in path_desc:
        if 'parameters' in path_desc:
            params = [build_path(param, arguments) for param in path_desc['parameters']]
            return path_desc['path_format'].format(*params)
        else:
            return path_desc['path_format']
    else:
        if 'mapping' in path_desc:
            mapping = path_desc['mapping']
            key = build_path(get(path_desc, 'key'), arguments)
            if key in mapping:
                return mapping[key]
            else:
                return key
        else:
            if 'arg' in path_desc:
                if arguments:
                    label = path_desc['arg']
                    if label in arguments:
                        return arguments[label]
                    print_err("unknown label `{}', it should be in {}".format(label, arguments.keys()))
                    sys.exit(1)
                else:
                    print_err("didn't expect `arg' since there is no argument for this client")
                    sys.exit(1)
            else:
                print_err("{} should have `arg', `mapping' or `parameters'".format(path_desc))
                sys.exit(1)


def smart_copy(config_file, arg_set, command, quiet, do_copy):
    global indent_level
    if config_file:
        stream = open(config_file, 'r')
        print_verbose('Using {}'.format(config_file))
    else:
        stream = sys.stdin
        print_verbose('Using stdin')
    indent_level += 1
    config = yaml.load(stream)
    if not config:
        print_err('Empty config file')
        sys.exit(1)
    input_base = os.path.abspath(get(config, 'input_base'))
    for client in get(config, 'clients'):
        print_verbose('Updating {}'.format(get(client, 'name')))
        indent_level += 1
        arguments = get(client, 'arguments', False)
        if arguments:
            if type(arguments) != dict:
                print_err("arguments which is `{}' should be a hash".format(arguments))
                sys.exit(1)
            for key, value in arguments.items():
                if key in arg_set:
                    value = [str(arg) for arg in value]
                    setting = arg_set[key]
                    if setting in value:
                        arguments[key] = [
                         setting]
                    else:
                        arguments[key] = []
                        break

        for args_items in itertools.product(*arguments.values()) if arguments else [None]:
            if args_items:
                args = dict(zip(arguments.keys(), args_items))
            else:
                args = None
            input_path = os.path.join(input_base, build_path(get(client, 'input'), args))
            if os.path.exists(input_path):
                if command:
                    os.chdir(os.path.dirname(input_path))
                    if quiet >= 1:
                        dev_null = open(os.devnull, 'wb')
                    exit_value = call(command, shell=True, stdout=dev_null if quiet >= 1 else None, stderr=dev_null if quiet >= 2 else None)
                    if exit_value != 0:
                        print_err("`{}' exited with {}. aborting".format(command, exit_value))
                        sys.exit(1)
                    output_path = os.path.join(get(config, 'output_base'), build_path(get(client, 'output'), args))
                    if parent_dir_exists(output_path):
                        if up_to_date(input_path, output_path):
                            print_verbose("`{}' == `{}'".format(input_path, output_path), 2)
                        else:
                            if do_copy:
                                print_verbose("`{}' -> `{}'".format(input_path, output_path))
                                shutil.copyfile(input_path, output_path)
                            else:
                                print_verbose("`{}' != `{}'".format(input_path, output_path))
                    else:
                        print_verbose("`{}' /\\ `{}'".format(input_path, output_path))
                        sys.exit(1)
                        continue

        indent_level -= 1

    indent_level -= 1


program_name = 'smartcp'

def print_err(message):
    print('{0}: {1}'.format(program_name, message), file=sys.stderr)


verbose = 0
indent_level = 0

def print_verbose(message, level=1):
    global verbose
    if level <= verbose:
        print('{}{}'.format('  ' * indent_level, message))


def main():
    global verbose
    arg_set = {}
    do_copy = True
    command = None
    quiet = 0
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'nqs:vx:h', [
         'no-copy', 'quiet', 'set', 'help', 'version'])
    except getopt.GetoptError as err:
        print_err(str(err))
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-n', '--no-copy'):
            do_copy = False
        elif o in ('-q', '--quiet'):
            quiet += 1
        elif o in ('-s', '--set'):
            try:
                arg, value = a.split('=')
            except ValueError as e:
                print_err("{} should have the format `arg=value'".format(a))
                sys.exit(2)

            arg_set[arg] = value
        elif o == '-v':
            verbose += 1
        elif o == '-x':
            command = a
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o == '--version':
            show_version()
            sys.exit()
        elif not False:
            raise AssertionError('unhandled option')

    if not args:
        smart_copy(None, arg_set, command, quiet, do_copy)
    else:
        for config_file in args:
            if config_file == '-':
                smart_copy(None, arg_set, command, quiet, do_copy)
            elif os.path.exists(config_file):
                smart_copy(config_file, arg_set, command, quiet, do_copy)
            else:
                print_err('{}: No such file or directory'.format(config_file))
                sys.exit(1)


if __name__ == '__main__':
    main()