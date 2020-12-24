# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/repoexternals/tag.py
# Compiled at: 2007-09-27 04:21:40
import sys, re, optparse, pysvn
usage = 'usage: %prog [options] externals'
parser = optparse.OptionParser(usage=usage)
external = re.compile('^(\\s*#?\\s*)([^#\\s]+)(\\s*)(.*?)(\\s*)(\\S+)(\\s*)$')

def run(externals):
    client = pysvn.Client()
    external_match = external.match
    for line in externals:
        match = external_match(line)
        if match is not None and client.is_url(match.group(6)):
            try:
                info = client.info(match.group(2))
            except pysvn.ClientError:
                info = None
            else:
                if info is not None:
                    yield match.expand('\\1\\2\\3-r %s%s\\6\\7' % (info.revision.number, match.group(5) or ' '))
                else:
                    yield line
        else:
            yield line

    return


def main():
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('requires externals')
    (externals,) = args
    if externals == '-':
        externals = sys.stdin
    else:
        externals = file(externals)
    for line in run(externals):
        print line,


if __name__ == '__main__':
    main()