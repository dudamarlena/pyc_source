# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/etl/repackage.py
# Compiled at: 2014-06-27 00:38:18
import sys, os, getopt
from etllib import cleanseImage, cleanseBody, unravelStructs, formatDate, prepareDocs, writeDoc
_verbose = False
_helpMessage = '\nUsage: repackage [-v] [-j json file] [-o object type]\n\nOptions:\n-j json file, --json=file\n    The origin JSON object file to repackage and extract out \n    individual object types from.\n-o object type --object=type\n    The object type from the JSON (e.g., "journal_entries", "teams", "partners")\n    to unravel from the aggregate JSON doc.\n-v, --verbose\n    Work verbosely rather than silently.\n'

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
            opts, args = getopt.getopt(argv[1:], 'hvj:o:', ['help', 'verbose', 'json=', 'object='])
        except getopt.error as msg:
            raise _Usage(msg)

        if len(opts) == 0:
            raise _Usage(_helpMessage)
        jsonFile = None
        objectType = None
        for option, value in opts:
            if option in ('-h', '--help'):
                raise _Usage(_helpMessage)
            elif option in ('-v', '--verbose'):
                _verbose = True
            elif option in ('-j', '--json'):
                jsonFile = value
            elif option in ('-o', '--object'):
                objectType = value

        if not os.path.exists(jsonFile):
            print >> sys.stderr, 'Path: [' + jsonFile + '] does not exist!\n'
            return 2
        if objectType == None:
            raise _Usage(_helpMessage)
        f = open(jsonFile, 'r')
        jsonContents = f.read()
        jsonObjects = prepareDocs(jsonContents, objectType)
        for obj in jsonObjects:
            cleanseImage(obj)
            cleanseBody(obj)
            formatDate(obj)
            unravelStructs(obj)
            filePath = os.getcwd() + '/' + str(obj['id']) + '.json'
            verboseLog('Writing json file: [' + filePath + ']')
            writeDoc(obj, filePath)

    except _Usage as err:
        print >> sys.stderr, sys.argv[0].split('/')[(-1)] + ': ' + str(err.msg)
        return 2

    return


if __name__ == '__main__':
    sys.exit(main())