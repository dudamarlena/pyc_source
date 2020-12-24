# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/kssh/kssh.py
# Compiled at: 2017-04-23 18:13:09
import sys, re, os, rlcompleter, readline
from subprocess import call
default_key_name = 'id_rsa'
version = '1.2.0'
show_errors = False
description = '\n\x1b[1mkssh [Kris SSH]\x1b[0m V%s\n\nAuthor: Kris Nova <kris@nivenly.com>\n\n    Quick Start : kssh <new_ssh_alias>\n\n    \x1b[1mkssh\x1b[0m is a simple utility for managing SSH hosts and tracking aliases in an SSH config file.\n    This tool is catered to work on OSX. Any other operating systems are currently not supported.\n\n[ACTIONS]\n\n    \x1b[95m[CONNECT]\x1b[0m Will connected to an alias. If no alias is found, will attempt to create one.\n        kssh <\x1b[91malias\x1b[0m>\n        kssh connect <\x1b[91malias\x1b[0m>\n\n    \x1b[95m[LIST]\x1b[0m Will list all known aliases.\n        kssh list\n\n    \x1b[95m[GENERATE]\x1b[0m Will generate a new RSA key named after the alias.\n        kssh GENERATE <\x1b[91malias\x1b[0m>\n\n    \x1b[95m[COPY]\x1b[0m Will attempt to copy an RSA key to a remote host.\n        kssh copy <\x1b[91muser\x1b[0m> <\x1b[91mhost\x1b[0m> <\x1b[91mpath_to_key\x1b[0m>\n\n    \x1b[95m[TEST]\x1b[0m Will test a connection no a known alias. If the alias is not found, the test will fail.\n        kssh test <\x1b[91malias\x1b[0m>\n\n    \x1b[95m[ADD]\x1b[0m Will add a new alias. If the alias already exists, it will be updated.\n        kssh add <\x1b[91malias\x1b[0m>\n\n    \x1b[95m[DELETE]\x1b[0m Will delete an existing alias if it exists.\n        kssh delete <\x1b[91malias\x1b[0m>\n\n    \x1b[95m[PURGE]\x1b[0m Will purge the existing SSH config data (This cannot be undone!)\n        kssh purge\n' % version
actions = [
 'connect', 'list', 'generate', 'copy', 'test', 'add', 'delete', 'purge']
if 'libedit' in readline.__doc__:
    readline.parse_and_bind('bind ^I rl_complete')
else:
    readline.parse_and_bind('tab: complete')

def main():
    try:
        firstarg = sys.argv[1]
        if firstarg == '-h' or firstarg == '--help':
            sys.exit(1)
    except:
        print description
        sys.exit(1)

    init_datastore()
    try:
        action_function = 'action_' + firstarg
        if firstarg == 'list':
            action_list()
        if firstarg == 'copy':
            action_copy(sys.argv[2], sys.argv[3], sys.argv[4])
        if firstarg == 'purge':
            i = raw_input("Purge all SSH config data?\n(This action cannot be undone)\n\tOnly 'yes' will be accepted : ")
            if i == 'yes':
                out('Purging all SSH config data')
                write_data('')
            else:
                out('Retaining SSH config data')
        else:
            f = getattr(sys.modules[__name__], action_function)
            f(sys.argv[2])
    except SystemExit:
        out('Exiting..')
        sys.exit(1)
    except KeyboardInterrupt:
        out('\nSIGTERM detected. Exiting gracefully')
    except IndexError:
        print description
        sys.exit(1)
    except AttributeError:
        if show_errors:
            print sys.exc_info()
        action_connect(firstarg)
    except:
        if show_errors:
            print sys.exc_info()

    out('Bye!')


def action_add(name):
    if exists(name):
        out('Record exists, updating')
    else:
        out('Adding new record')
    readline.set_completer(complete_hosts)
    host = raw_input('HostName: ')
    readline.set_completer(complete_users)
    user = raw_input('User: ')
    readline.set_completer(complete_keys)
    key = raw_input('Key: ').rstrip()
    if key == '':
        key = default_key_name
    if '.ssh' not in key:
        key = os.path.expanduser('~') + '/.ssh/' + key
        out('Key absolute path %s' % key)
    if not os.path.exists(key):
        out('Unable to locate key %s' % key)
        key = action_generate(key)
    start = '##<---' + name + '---\n'
    stop = '\n##---' + name + '--->'
    block = 'Host %s\n    HostName %s\n    User %s\n    IdentityFile %s' % (name, host, user, key)
    block = start + block + stop
    existing_config = get_data()
    if exists(name):
        config = re.sub(start + '.*?' + stop, block, existing_config, flags=re.DOTALL)
        write_data(config)
        out('Updating SSH config with new record')
    else:
        write_data(existing_config + '\n' + block)
        out('Adding new record to SSH config')
    if not action_test(name):
        action_copy(user, host, key)
        if not action_test(name):
            out('Major error, unable to contact host')
            sys.exit(1)
    out("You can now access this host using 'kssh %s'" % name)


def action_copy(user, host, path_to_key):
    out('Copying id for %s@%s with key %s' % (user, host, path_to_key))
    if '.pub' not in path_to_key:
        path_to_key = path_to_key + '.pub'
    if '.ssh' not in path_to_key:
        path_to_key = os.path.expanduser('~') + '/.ssh/' + path_to_key
    with open(path_to_key) as (f):
        content = f.read()
    copy_cmd = "mkdir -p -m 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo '%s' >> ~/.ssh/authorized_keys" % content
    out(copy_cmd)
    call(['ssh', user + '@' + host, copy_cmd])


def action_generate(name):
    out('Generating new RSA key')
    if '.ssh' not in name:
        name = os.path.expanduser('~') + '/.ssh/' + name
    call(['ssh-keygen', '-f', name, '-N', ''])
    return name


def action_test(name):
    out('Testing the alias')
    response = call(['ssh', '-oBatchMode=yes', name, '#'])
    if response == 0:
        out('Success')
        return True
    out('Failure')
    return False


def action_delete(name):
    start = '##<---' + name + '---\n'
    stop = '\n##---' + name + '--->'
    new_config = re.sub(start + '.*?' + stop, '', get_data(), flags=re.DOTALL)
    if not new_config:
        out('SSH config record %s not found' % name)
    else:
        out('Removing %s SSH config record' % name)
        write_data(new_config.strip())


def action_list():
    data = get_data()
    if data == '':
        out('No hosts found')
        sys.exit(1)
    list = data.split('##<---')
    for k in list:
        for i in k.split('\n'):
            i = i.strip()
            if not i or '---' in i:
                continue
            if 'Host ' in i:
                alias = i.split(' ')[1]
                continue
            if 'User ' in i:
                user = i.split(' ')[1]
            if 'HostName' in i:
                host = i.split(' ')[1]
            if 'Identity' in i:
                id = i.split(' ')[1]
                msg = '     %s@%s (%s)' % (user, host, id)
                out('[%s]' % alias)
                out(msg)
                out('')

    sys.exit(1)


def action_connect(name):
    if not exists(name):
        out('Unable to find alias %s' % name)
        action_add(name)
    out('Connecting to %s' % name)
    call(['ssh', name])
    out('Connection closed')


def init_datastore():
    if not os.path.exists(os.path.expanduser('~') + '/.ssh'):
        print 'Setting up kssh datastore..'
        os.makedirs(os.path.expanduser('~') + '/.ssh')
    if not os.path.exists(os.path.expanduser('~') + '/.ssh/config'):
        f = open(os.path.expanduser('~') + '/.ssh/config', 'w')
        f.write('')
        f.close()


def exists(name):
    start = '##<---' + name + '---\n'
    if start not in get_data():
        return False
    return True


def write_data(data):
    f = open(os.path.expanduser('~') + '/.ssh/config', 'w')
    f.write(data)
    f.close()


def get_data():
    with open(os.path.expanduser('~') + '/.ssh/config') as (f):
        return f.read()


def out(message):
    print '\x1b[1mkSSH : \x1b[0m \x1b[95m%s\x1b[0m' % message


def get_data_key(key):
    vals = []
    lines = get_data().split('\n')
    for k in lines:
        k = k.strip()
        if k.startswith(key + ' '):
            vals.append(k.split(' ')[1])

    return vals


def complete_hosts(text, state):
    for a in get_data_key('HostName'):
        if text in a:
            if not state:
                return a
            state -= 1


def complete_users(text, state):
    for a in get_data_key('User'):
        if text in a:
            if not state:
                return a
            state -= 1


def complete_keys(text, state):
    files = os.listdir(os.path.expanduser('~') + '/.ssh/')
    for a in files:
        if text in a:
            if not state:
                return a
            state -= 1


def complete_aliases(text, state):
    for a in get_data_key('Host'):
        if text in a:
            if not state:
                return a
            state -= 1


def complete_launcher(text, state):
    for a in actions:
        if text in a:
            if not state:
                return a
            state -= 1


if __name__ == '__main__':
    main()