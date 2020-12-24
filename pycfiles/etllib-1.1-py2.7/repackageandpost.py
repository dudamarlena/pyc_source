# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/etl/repackageandpost.py
# Compiled at: 2014-06-27 00:38:32
from etllib import prepareDocs, cleanseBody, cleanseImage, unravelStructs, formatDate, prepareDocForSolr, postJsonDocToSolr
import getopt, sys, os
_verbose = False
_helpMessage = '\nUsage: repackageandpost [-v] [-u url] [-o object type]\n\nOptions:\n-u url, --url=url\n    Post to Apache Solr at the given url.\n\n-o object type --object=type\n    The object type from the JSON file (e.g., "journal_entries", "teams", "partners")\n    to unravel from the aggregate JSON doc.\n    \n-v, --verbose\n    Work verbosely rather than silently.\n    \nInput:\nSTDIN\n    Line by line absolute or relative paths to JSON docs that it will transform and\n    post to Apache Solr.\n'

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
            opts, args = getopt.getopt(argv[1:], 'hvu:o:', ['help', 'verbose', 'url=', 'object='])
        except getopt.error as msg:
            raise _Usage(msg)

        if len(opts) == 0:
            raise _Usage(_helpMessage)
        solrUrl = None
        objectType = None
        for option, value in opts:
            if option in ('-h', '--help'):
                raise _Usage(_helpMessage)
            elif option in ('-v', '--verbose'):
                _verbose = True
            elif option in ('-u', '--url'):
                solrUrl = value
            elif option in ('-o', '--object'):
                objectType = value

        if solrUrl == None or objectType == None:
            raise _Usage(_helpMessage)
        for filename in sys.stdin:
            filename = filename.rstrip()
            if '.json' not in filename or not os.path.exists(filename):
                continue
            verboseLog('Processing: ' + filename)
            f = open(filename, 'r')
            jsonContents = f.read()
            jsonObjs = prepareDocs(jsonContents, objectType)
            for obj in jsonObjs:
                cleanseImage(obj)
                cleanseBody(obj)
                formatDate(obj)
                unravelStructs(obj)
                postString = prepareDocForSolr(obj, False)
                verboseLog(postString)
                postJsonDocToSolr(solrUrl, postString)

    except _Usage as err:
        print >> sys.stderr, sys.argv[0].split('/')[(-1)] + ': ' + str(err.msg)
        return 2

    return


if __name__ == '__main__':
    sys.exit(main())