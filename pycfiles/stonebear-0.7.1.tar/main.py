# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cb/Projekter/stonebear/stonebear/main.py
# Compiled at: 2011-09-06 17:57:43
import os, sys, argparse, imp, stonebear
from build import build
from push import push
from clean import clean
from deploy import deploy

def main():
    """
    Main interface function of stonebear
    """
    config_filename = 'stonebeard.py'
    config = {'compilers': [], 'input': [], 'output': [], 'remove_from_output_dirs': [], 'prebuild': '', 
       'postbuild': '', 
       'prepush': '', 
       'postpush': '', 
       'preclean': '', 
       'postclean': '', 
       'env': {}}
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--version', '-v', action='version', version='stonebear ' + stonebear.__version__ + '')
    subparser = parser.add_subparsers()
    sub_build = subparser.add_parser('build', help='run build process')
    sub_build.set_defaults(func=build)
    sub_push = subparser.add_parser('push', help='run env push command')
    sub_push.add_argument('env', nargs=1, help='name of environment to use')
    sub_push.set_defaults(func=push)
    sub_clean = subparser.add_parser('clean', help='clean build directory')
    sub_clean.set_defaults(func=clean)
    sub_deploy = subparser.add_parser('deploy', help='run clean, build and                                      push processes')
    sub_deploy.add_argument('env', nargs=1, help='name of environment to use')
    sub_deploy.set_defaults(func=deploy)
    try:
        args = parser.parse_args()
    except IOError as e:
        print e
        sys.exit(1)

    config_path = os.getcwd() + '/' + config_filename
    try:
        user_config = imp.load_source('stonebeard.config', config_path)
        user_config = user_config.config
    except IOError:
        print 'no config file %s found' % config_path
        sys.exit(1)

    config = dict(config.items() + user_config.items())
    args.func(args, config)
    sys.exit(0)


if __name__ in ('__main__', 'stonebear.main'):
    main()