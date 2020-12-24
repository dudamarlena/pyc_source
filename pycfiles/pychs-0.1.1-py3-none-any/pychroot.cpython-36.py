# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/pkgcore/pychroot/build/lib/pychroot/scripts/pychroot.py
# Compiled at: 2019-12-01 01:06:22
# Size of source mod 2**32: 5026 bytes
__doc__ = "an extended chroot equivalent\n\npychroot is an extended **chroot(1)** equivalent that also provides support for\nautomatically handling bind mounts. By default, the proc and sysfs filesystems\nare mounted to their respective /proc and /sys locations inside the chroot as\nwell as bind mounting /dev and /etc/resolv.conf from the host system.\n\nIn addition to the defaults, the user is able to specify custom bind mounts.\nFor example, the following command will recursively bind mount the user's home\ndirectory at the same location inside the chroot directory::\n\n    pychroot -R /home/user ~/chroot\n\nThis allows a user to easily set up a custom chroot environment without having\nto resort to scripted mount handling or other methods.\n"
import argparse, errno
from functools import partial
import os, sys
from snakeoil.cli import arghparse
from ..base import Chroot
from ..exceptions import ChrootError

def bindmount(s, recursive=False, readonly=False):
    """Argparse argument type for bind mount variants."""
    opts = {'recursive':recursive, 
     'readonly':readonly}
    return {s: opts}


class mountpoints(argparse.Action):
    """mountpoints"""

    def __call__(self, parser, namespace, values, option_string=None):
        if not getattr(namespace, 'mountpoints', False):
            namespace.mountpoints = {}
        namespace.mountpoints.update(values)


argparser = arghparse.ArgumentParser(color=False,
  debug=False,
  quiet=False,
  verbose=False,
  description=__doc__,
  script=(__file__, __name__))
argparser.add_argument('path', help='path to newroot')
argparser.add_argument('command',
  nargs=(argparse.REMAINDER), help='optional command to run', docs="\n        Optional command to run.\n\n        Similar to chroot(1), if unspecified this defaults to $SHELL from the\n        host environment and if that's unset it executes /bin/sh.\n    ")
chroot_options = argparser.add_argument_group('chroot options')
chroot_options.add_argument('--no-mounts',
  action='store_true', help='disable the default bind mounts',
  docs="\n        Disable the default bind mounts which can be used to obtain a standard\n        chroot environment that you'd expect when using chroot(1).\n    ")
chroot_options.add_argument('--hostname',
  type=str, help='specify the chroot hostname', docs='\n        Specify the chroot hostname. In order to set the domain name as well,\n        pass an FQDN instead of a singular hostname.\n    ')
chroot_options.add_argument('--skip-chdir',
  action='store_true', help="do not change working directory to '/'",
  docs="\n        Do not change the current working directory to '/'.\n\n        Unlike chroot(1), this currently doesn't limit you to only using it\n        when the new root isn't '/'. In other words, you can use a new chroot\n        environment on the current host system rootfs with one caveat: any\n        absolute paths will use the new rootfs.\n    ")
chroot_options.add_argument('-B',
  '--bind', type=bindmount, action=mountpoints, metavar='SRC[:DEST]',
  help='specify custom bind mount',
  docs="\n        Specify a custom bind mount.\n\n        In order to mount the same source to multiple destinations, use the\n        SRC:DEST syntax. For example, the following will bind mount '/srv/data'\n        to /srv/data and /home/user/data in the chroot::\n\n            pychroot -B /srv/data -B /srv/data:/home/user/data /path/to/chroot\n    ")
chroot_options.add_argument('-R',
  '--rbind', type=partial(bindmount, recursive=True), action=mountpoints,
  metavar='SRC[:DEST]',
  help='specify custom recursive bind mount')
chroot_options.add_argument('--ro',
  '--readonly', type=partial(bindmount, readonly=True), action=mountpoints,
  metavar='SRC[:DEST]',
  help='specify custom readonly bind mount',
  docs="\n        Specify a custom readonly bind mount.\n\n        Readonly, recursive bind mounts aren't currently supported on Linux so\n        this has to be a standalone option for now. Once they are, support for\n        them and other mount attributes will be added as an extension to the\n        mount point argument syntax.\n    ")

@argparser.bind_final_check
def _validate_args(parser, namespace):
    if not namespace.command:
        namespace.command = [
         os.getenv('SHELL', '/bin/sh'), '-i']
    else:
        if not hasattr(namespace, 'mountpoints'):
            namespace.mountpoints = None
        if namespace.no_mounts:
            Chroot.default_mounts = {}


@argparser.bind_main_func
def main(options, out, err):
    cmd = options.command[0]
    try:
        with Chroot((options.path), mountpoints=(options.mountpoints), hostname=(options.hostname),
          skip_chdir=(options.skip_chdir)) as (c):
            os.execvp(cmd, options.command)
    except FileNotFoundError as e:
        argparser.error(f"failed to run command {cmd!r}: {e}", status=1)
    except ChrootError as e:
        argparser.error((str(e)), status=1)

    return c.exit_status