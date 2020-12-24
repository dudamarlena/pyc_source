# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/subtract.py
# Compiled at: 2014-09-13 23:24:19
__doc__ = '\nThis module is the subtract command of bowl.\n\nCreated on 1 September 2014\n@author: Charlie Lewis\n'
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