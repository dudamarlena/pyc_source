# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/mlmmj_archiver/main.py
# Compiled at: 2013-01-22 07:33:08
import argparse, yaml, os

class Config(object):

    def __init__(self, args):
        self.configfile = open(args.config, 'r')
        self.lists = yaml.load(self.configfile)
        self.configfile.close()
        for list in self.lists.keys():
            self.lists[list]['options']['parsed_output'] = ''
            if self.lists[list].has_key('options'):
                if self.lists[list]['options'].has_key('output'):
                    for output in self.lists[list]['options']['output']:
                        if output == 'showreplies':
                            self.lists[list]['options']['parsed_output'] = self.lists[list]['options']['parsed_output'] + 'HM_SHOWREPLIES=1 '
                        else:
                            print "Unkown option '%s' in %s list!" % (output, list)
                            exit(1)

            else:
                self.lists[list]['options'] = {}
            if self.lists[list]['options'].has_key('index'):
                if self.lists[list]['options']['index'] == 'monthly':
                    self.lists[list]['options']['parsed_output'] = self.lists[list]['options']['parsed_output'] + 'HM_MONTHLY_INDEX=1'
                elif self.lists[list]['options']['index'] == 'yearly':
                    self.lists[list]['options']['parsed_output'] = self.lists[list]['options']['parsed_output'] + 'HM_YEARLY_INDEX=1'
                else:
                    print "Unkown index option '%s' in %s list!" % (self.lists[list]['options']['index'], list)
            if not self.lists[list]['options'].has_key('ordering'):
                self.lists[list]['options']['ordering'] = 'thread'
            if not self.lists[list]['options'].has_key('threadlevels'):
                self.lists[list]['options']['threadlevels'] = 100
            if not self.lists[list]['options'].has_key('lang'):
                self.lists[list]['options']['lang'] = 'en'
            if not os.path.exists(self.lists[list]['archive']):
                os.mkdir(self.lists[list]['archive'])
            if os.path.exists(self.lists[list]['archive'] + '/last'):
                indexfile = open(self.lists[list]['archive'] + '/last', 'r')
                self.lists[list]['lastindex'] = int(indexfile.read())
                if self.lists[list]['lastindex'] == 0:
                    self.lists[list]['lastindex'] = 1
                indexfile.close()
            else:
                self.lists[list]['lastindex'] = 1
            self.lists[list]['options']['hypermail_args'] = ''
            if args.overwrite == True:
                self.lists[list]['options']['hypermail_args'] = self.lists[list]['options']['hypermail_args'] + '-x '
                self.lists[list]['lastindex'] = 1
            if args.progress == True:
                self.lists[list]['options']['hypermail_args'] = self.lists[list]['options']['hypermail_args'] + '-p '
            indexfile = open(self.lists[list]['list'] + '/index', 'r')
            self.lists[list]['newindex'] = int(indexfile.read())
            indexfile.close()


def run(args):
    config = Config(args)
    for list in config.lists.keys():
        if config.lists[list]['lastindex'] == 1 and config.lists[list]['newindex'] == 1:
            loop_start = 1
            loop_end = 2
        else:
            loop_start = config.lists[list]['lastindex']
            loop_end = config.lists[list]['newindex'] + 1
        for id in range(loop_start, loop_end):
            os.system("env %s HM_DEFAULTINDEX=%s HM_THRDLEVELS=%i HM_FOLDER_BY_DATE='%%Y/%%m' hypermail -g -l %s -L %s -u -d %s %s < %s" % (
             config.lists[list]['options']['parsed_output'],
             config.lists[list]['options']['ordering'],
             config.lists[list]['options']['threadlevels'],
             list,
             config.lists[list]['options']['lang'],
             config.lists[list]['archive'],
             config.lists[list]['options']['hypermail_args'],
             config.lists[list]['list'] + '/archive/' + str(id)))

        indexfile = open(config.lists[list]['archive'] + '/last', 'w')
        indexfile.write(str(config.lists[list]['newindex']))
        indexfile.close()


def main():
    parser = argparse.ArgumentParser(description='mlmmj archive generator')
    parser.add_argument('-c', '--config', default='/etc/mlmmj-archiver/config.yml', help='use alternate config file (default: %(default)s)')
    parser.add_argument('-x', '--overwrite', action='store_const', const=True, help='overwrite archives')
    parser.add_argument('-p', '--progress', action='store_const', const=True, help='show progress')
    args = parser.parse_args()
    run(args)