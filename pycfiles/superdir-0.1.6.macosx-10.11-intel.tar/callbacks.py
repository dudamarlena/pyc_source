# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/superdir/callbacks.py
# Compiled at: 2016-08-25 12:21:11
import os, sys, utils

def create_file(node):
    """ Create a regular file if node has NoneType for children.  Otherwise, creates a directory. """
    if node['path'] == os.path.abspath(os.curdir):
        return
    else:
        if os.path.exists(node['path']):
            print ('Error, the directory {} already exists').format(node['path'])
            sys.exit(1)
        if node['children'] is None:
            try:
                open(node['path'], 'w').close()
            except IOError as E:
                print ('Error: could not create regular file: {}.').format(node['path'])
                print E

        else:
            try:
                os.mkdir(node['path'])
            except IOError as E:
                print ('Error: could not create directory: {}.').format(node['path'])
                print E

        return


def make_config_processor(config_path=None):
    """ Takes relative name of config file in ~/home directory """
    full_path = os.path.abspath(os.path.join(os.path.expanduser('~'), config_path))
    try:
        with open(full_path) as (config_file):
            hooks = dict([ map(str.strip, line.split('=')) for line in config_file if line.strip()
                         ])
    except IOError as E:
        print 'Could not open config file.'
        print E
        sys.exit(1)

    def process_config_hooks(node):
        """ on each node, if there's a match in the config settings, that file is created. """
        filename = node['value']
        if filename in hooks:
            try:
                with open(hooks[filename], 'r') as (src_file):
                    with open(node['path'], 'w') as (dst_file):
                        dst_file.write(src_file.read())
            except IOError as E:
                print 'Could not write config hook to new file.'
                print E
                sys.exit(1)

    return process_config_hooks