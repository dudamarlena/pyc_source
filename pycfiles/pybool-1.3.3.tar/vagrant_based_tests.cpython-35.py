# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/tests/api_v2/vagrant_based_tests.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 3197 bytes
import re
from fabric.api import local
from fabric.context_managers import settings, show, hide, quiet

def with_ephemeral_vagrant_box(images=None, verbose=False):
    """
    A decorator that creates ephemeral vagrant instances, executes the
    wrapped function and destroys the vagrant instance.

    takes a list of vagrants images, and executes the wrapped function for each
    one of those images.

    params:
        list images: array containing a list of vagrant images
        bool verbose: print out debug information
    """
    if not images:
        images = []

    def decorator(func):

        def wrapper(*args, **kwargs):
            for image in images:
                vagrant_up(image=image)
                user, ip, port, pkey = vagrant_ssh_config()
                hs = build_host_string(user, ip, port)
                if verbose:
                    fabric_flags = show('debug')
                else:
                    fabric_flags = hide('everything')
                with settings(fabric_flags, host_string=hs, key_filename=pkey, disable_known_hosts=True):
                    try:
                        print('In method: %s for vagrant image %s' % (
                         func.func_name, image))
                        func(*args, **kwargs)
                        vagrant_destroy()
                    except:
                        vagrant_destroy()
                        raise

        return wrapper

    return decorator


def vagrant_up(image):
    """
        runs a vagrant instance

        params:
            string image: name of the docker image
    """
    with quiet():
        vagrant_destroy()
    with settings(hide('stdout')):
        local('vagrant init %s' % image)
        local('vagrant box update')
        local('vagrant up')


def vagrant_destroy():
    """
        cleans the vagrant instance
    """
    local('vagrant destroy -f')
    local('rm -f Vagrantfile')


def build_host_string(user, ip, port):
    """
        builds a fabric ssh host string for a vagrant instance

        params:
            user: user to connect to the vagrant instance
            ip: ip address of the vagrant instance
            port: port for the ssh daemon

        returns:
            string: < root@vagrant_ip_address:port_number >
    """
    host_string = '%s@%s:%s' % (user, ip, port)
    return host_string


def vagrant_ssh_config():
    """
        returns the vagrant ssh config for a running instance
    """
    ssh_config = local('vagrant ssh-config', capture=True)
    user = re.search('\\s{3}User\\s(.*)', ssh_config).group(1)
    port = re.search('\\s{3}Port\\s(\\d+)', ssh_config).group(1)
    ip = re.search('\\s{3}HostName\\s(.*)', ssh_config).group(1)
    pkey = re.search('\\s{3}IdentityFile\\s(.*)', ssh_config).group(1)
    return (
     user, ip, port, pkey)