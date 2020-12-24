# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/etl/poster.py
# Compiled at: 2014-11-13 06:49:01
import os, sys, getopt
from etllib import prepareDocForSolr, postJsonDocToSolr
_verbose = False
_helpMessage = '\nUsage: poster [-v] [-u url] [-d directory]\n\nOptions:\n-u url, --url=url\n    Post to Apache Solr at the given url.\n-v, --verbose\n    Work verbosely rather than silently.  \n-d, --directory\n    reads input json files from this directory\nInput: STDIN or -d\nSTDIN\n    Line by line absolute or relative paths to JSON docs to post to Apache Solr.\n'

def verboseLog(message):
    global _verbose
    if _verbose:
        print >> sys.stderr, message


class _Usage(Exception):
    """An error for problems with arguments on the command line."""

    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    global _verbose
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], 'hvu:d:', ['help', 'verbose', 'url=', 'directory='])
        except getopt.error as msg:
            raise _Usage(msg)

        if len(opts) == 0:
            raise _Usage(_helpMessage)
        solrUrl = None
        dirFile = ''
        for option, value in opts:
            if option in ('-h', '--help'):
                raise _Usage(_helpMessage)
            elif option in ('-u', '--url'):
                solrUrl = value
            elif option in ('-v', '--verbose'):
                _verbose = True
            elif option in ('-d', '--directory'):
                dirFile = value

        for filename in os.listdir(dirFile) if dirFile else sys.stdin:
            filename = dirFile + '\\' + filename.rstrip() if dirFile else filename.rstrip()
            if '.json' not in filename or not os.path.exists(filename):
                continue
            verboseLog('Processing: ' + filename)
            f = open(filename, 'r')
            jsonContents = f.read()
            postString = prepareDocForSolr(jsonContents)
            verboseLog(postString)
            postJsonDocToSolr(solrUrl, postString)

    except _Usage as err:
        print >> sys.stderr, sys.argv[0].split('/')[(-1)] + ': ' + str(err.msg)
        return 2

    return


if __name__ == '__main__':
    sys.exit(main())