# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mara_kim/Documents/code/autochthe/kismet-py/kismet/kernel/install.py
# Compiled at: 2019-01-25 20:14:33
# Size of source mod 2**32: 1830 bytes
import json, os, sys, argparse
from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory
kernel_json = {'argv':[
  sys.executable, '-m', 'kismet.kernel', '-f', '{connection_file}'], 
 'display_name':'Kismet', 
 'language':'kismet'}

def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as (td):
        os.chmod(td, 493)
        with open(os.path.join(td, 'kernel.json'), 'w') as (f):
            json.dump(kernel_json, f, sort_keys=True)
        print('Installing Kismet Jupyter kernel spec')
        KernelSpecManager().install_kernel_spec(td, 'kismet', user=user, prefix=prefix)


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False


def main(argv=None):
    parser = argparse.ArgumentParser(description='Install Kismet Jupyter kernel spec')
    prefix_locations = parser.add_mutually_exclusive_group()
    prefix_locations.add_argument('--user',
      help='Install KernelSpec in user home directory', action='store_true')
    prefix_locations.add_argument('--sys-prefix',
      help='Install KernelSpec in sys.prefix. Useful in conda / virtualenv',
      action='store_true',
      dest='sys_prefix')
    prefix_locations.add_argument('--prefix',
      help='Install KernelSpec in this prefix', default=None)
    args = parser.parse_args(argv)
    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    else:
        if args.prefix:
            prefix = args.prefix
        else:
            if args.user or not _is_root():
                user = True
    install_my_kernel_spec(user=user, prefix=prefix)


if __name__ == '__main__':
    main()