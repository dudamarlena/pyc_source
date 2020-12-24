# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/subtract.py
# Compiled at: 2014-09-13 23:24:19
"""
This module is the subtract command of bowl.

Created on 1 September 2014
@author: Charlie Lewis
"""
import fileinput, os, shutil

class subtract(object):
    """
    This class is responsible for the subtract command of the cli.
    """

    @classmethod
    def main(self, args):
        args.metadata_path = os.path.expanduser(args.metadata_path)
        if os.path.exists(os.path.join(args.metadata_path, 'services', args.OS, args.VERSION, args.TYPE, 'dockerfiles', args.NAME)):
            shutil.rmtree(os.path.join(args.metadata_path, 'services', args.OS, args.VERSION, args.TYPE, 'dockerfiles', args.NAME))
            try:
                found = 0
                for line in fileinput.input(os.path.join(args.metadata_path, 'services', args.OS, args.VERSION, args.TYPE, args.TYPE), inplace=True):
                    if args.NAME in line:
                        found = 1
                    elif found == 1:
                        if line == ' }\n' or line == ' },\n':
                            found = 0
                    else:
                        print '%s' % line,

                empty = 1
                with open(os.path.join(args.metadata_path, 'services', args.OS, args.VERSION, 'databases/databases'), 'r') as (f):
                    fl = f.readline()
                    if fl != '{\n':
                        empty = 0
                    else:
                        sl = f.readline()
                        if sl != '}' and sl != '}\n':
                            empty = 0
                with open(os.path.join(args.metadata_path, 'services', args.OS, args.VERSION, 'environment/environment'), 'r') as (f):
                    fl = f.readline()
                    if fl != '{\n':
                        empty = 0
                    else:
                        sl = f.readline()
                        if sl != '}' and sl != '}\n':
                            empty = 0
                with open(os.path.join(args.metadata_path, 'services', args.OS, args.VERSION, 'services/services'), 'r') as (f):
                    fl = f.readline()
                    if fl != '{\n':
                        empty = 0
                    else:
                        sl = f.readline()
                        if sl != '}' and sl != '}\n':
                            empty = 0
                with open(os.path.join(args.metadata_path, 'services', args.OS, args.VERSION, 'tools/tools'), 'r') as (f):
                    fl = f.readline()
                    if fl != '{\n':
                        empty = 0
                    else:
                        sl = f.readline()
                        if sl != '}' and sl != '}\n':
                            empty = 0
                if empty == 1:
                    shutil.rmtree(os.path.join(args.metadata_path, 'services', args.OS, args.VERSION))
                    found = 0
                    for line in fileinput.input(os.path.join(args.metadata_path, 'services', args.OS, 'versions'), inplace=True):
                        if args.VERSION in line:
                            found = 1
                        elif found == 1:
                            if line == ' }\n' or line == ' },\n':
                                found = 0
                        else:
                            print '%s' % line,

                    empty = 1
                    with open(os.path.join(args.metadata_path, 'services', args.OS, 'versions'), 'r') as (f):
                        fl = f.readline()
                        if fl != '{\n':
                            empty = 0
                        else:
                            sl = f.readline()
                            if sl != '}' and sl != '}\n':
                                empty = 0
                    if empty == 1:
                        shutil.rmtree(os.path.join(args.metadata_path, 'services', args.OS))
                        found = 0
                        for line in fileinput.input(os.path.join(args.metadata_path, 'services', 'oses'), inplace=True):
                            if args.OS in line:
                                found = 1
                            elif found == 1:
                                if line == ' }\n' or line == ' },\n':
                                    found = 0
                            else:
                                print '%s' % line,

                        empty = 1
                        with open(os.path.join(args.metadata_path, 'services', 'oses'), 'r') as (f):
                            fl = f.readline()
                            if fl != '{\n':
                                empty = 0
                            else:
                                sl = f.readline()
                                if sl != '}' and sl != '}\n':
                                    empty = 0
                        if empty == 1:
                            shutil.rmtree(os.path.join(args.metadata_path, 'services'))
            except:
                print 'Failed to remove service'

        else:
            print "Service doesn't exist."