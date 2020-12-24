# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/etl/translatejson.py
# Compiled at: 2016-06-28 18:34:06
import json, sys, getopt
from tika import translate
import hirlite
_verbose = False
_helpMessage = '\nUsage: translate [-v] [-c column headers file] [-i input json file] [-j output json file] [-p cred file] [-r translation cache file] [-f from] [-t to]\n\nOptions:\n-i input json file --injson=file\n    The input named JSON file.\n-j json file --json=file\n    Output the named JSON file.\n-c column headers file --cols=file\n    Use the provided column headers to parse the TSV and to name fields in the JSON.\n-f from language --from=2 letter language code\n    The 2 letter code of the language to translate from.\n-t to language --to=2 letter language code\n    The 2 letter code of the language to translate to.\n-r path  --rlite=path to rlite file\n    The path to the rlite-py translation cache for efficiency and to avoid lookups. \n-v, --verbose\n    Work verbosely rather than silently.\n'
_rlite = None

def initRLite(the_path='./translation.rdb'):
    global _rlite
    _rlite = hirlite.Rlite(encoding='utf8', path=the_path)


def verboseLog(message):
    global _verbose
    if _verbose:
        print >> sys.stderr, message


def cacheTranslation(original, translated):
    _rlite.command('set', original.encode('utf-8', 'ignore'), translated.encode('utf-8', 'ignore'))


def translateFromCache(original):
    return _rlite.command('get', original.encode('utf-8', 'ignore'))


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
            opts, args = getopt.getopt(argv[1:], 'hvj:c:f:t:i:r:', ['help', 'verbose', 'json=', 'cols=', 'from=', 'to=', 'injson=', 'rlite='])
        except getopt.error as msg:
            raise _Usage(msg)

        if len(opts) == 0:
            raise _Usage(_helpMessage)
        cols = []
        colHeaderFilePath = None
        outputJsonFilePath = None
        fromLang = None
        toLang = None
        inputJsonFilePath = None
        rlitePath = None
        for option, value in opts:
            if option in ('-h', '--help'):
                raise _Usage(_helpMessage)
            elif option in ('-i', '--injson'):
                inputJsonFilePath = value
            elif option in ('-j', '--json'):
                outputJsonFilePath = value
            elif option in ('-r', '--rlite'):
                rlitePath = value
            elif option in ('-c', '--cols'):
                colHeaderFilePath = value
            elif option in ('-f', '--from'):
                fromLang = value
            elif option in ('-t', '--to'):
                toLang = value
            elif option in ('-v', '--verbose'):
                _verbose = True

        if inputJsonFilePath == None or outputJsonFilePath == None or colHeaderFilePath == None or fromLang == None or toLang == None or rlitePath == None:
            raise _Usage(_helpMessage)
        initRLite(rlitePath)
        with open(colHeaderFilePath) as (headers):
            cols = headers.read().splitlines()
            verboseLog(cols)
        with open(inputJsonFilePath) as (jsonFile):
            jsonData = jsonFile.read()
            jsonStruct = json.loads(jsonData)
        for col in cols:
            if col in jsonStruct:
                translated = translateFromCache(jsonStruct[col])
                if translated == None:
                    translated = translate.from_buffer(jsonStruct[col], fromLang, toLang)
                    verboseLog('translating: file: [' + inputJsonFilePath + ']: field: [' + col + ']: orig: [' + jsonStruct[col] + ']: to translated: [' + translated + ']')
                    cacheTranslation(jsonStruct[col], translated)
                jsonStruct[col] = translated
            else:
                print 'column [' + col + '] not present in json file: [' + inputJsonFilePath + ']'

        outFile = open(outputJsonFilePath, 'wb')
        verboseLog('Writing output file: [' + outputJsonFilePath + ']')
        json.dump(jsonStruct, outFile, encoding='utf-8')
    except _Usage as err:
        print >> sys.stderr, sys.argv[0].split('/')[(-1)] + ': ' + str(err.msg)
        return 2

    return


if __name__ == '__main__':
    sys.exit(main())