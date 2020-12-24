# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/recognize.py
# Compiled at: 2015-01-30 14:03:55
import getopt, os, pickle, pprint, sys

def usage():
    print 'Usage: recognize [OPTION]... [word] ...\n    \nIf a "word" argument is given, it check if its a valid word,\nand if not, it gives suggestions.\n\nIf the iadfa file is not given it will generate one with the\ndata/test.dico.\n\nMandatory arguments to long options are mandatory for short options too.\n-d, --dico-file=FILE            this is the dictionnary file that will\n                                be used to generate the IADFA. \n-e, --export=FILE               export the IADFA to a graphviz file.\n-i, --iadfa=FILE                Use this file for the IADFA. If you\n                                specify the \'-d\' or \'--dico\' option,\n                                this is where the IADFA will be stored.\n-n, --distance=n                this is the levenshtein distance. [default=1]\n-o, --oflazer                   use the [oflazer96errortolerant] algorithm,\n                                instead of the [schulz02fast] faster algorithm.\n-t, --transitions-file=FILE     the file that contain/will contain the OFlazer\n                                transitions. (only works if you specified that\n                                you want to use OFlazer algorithm.\n-v, --verbose                   verbose mode. It causes the program to print\n                                debugging messages about its progress.\n'


def generateIADFA(dictFilename, iadfaFilename):
    debug('loading IADFA code')
    from iadfa import IncrementalAdfa
    debug('Reading the dico file.')
    f = open(dictFilename, 'r')
    debug('Starting the FSA construction.')
    a = IncrementalAdfa(f, sorted=True)
    pickle.dump(a, open(iadfaFilename, 'w'))
    debug('FSA saved.')
    return a


def exportFileToPS(fsa, filename):
    debug('Exporting the fsa in a graphviz format.')
    fsa.graphVizExport(filename)


def debug(output):
    if verbose is True:
        print output


verbose = False
config = {'transitionsFile': 'levenshtein.dat', 'iadfaFile': 'iadfa.dat', 
   'dicoFile': None}

def getTransitionStates(filename, distance):
    from possibleStates import genTransitions
    transitions = {}
    try:
        debug('Checking for existing transitions file')
        transitions = pickle.load(open(filename, 'r'))
        debug('Transitions file loaded')
    except:
        pass

    distanceStr = str(distance)
    if transitions.has_key(distanceStr) is False:
        debug('Creating the dynamic levenshtein transitions')
        transitions[distanceStr] = genTransitions(distance)
        try:
            pickle.dump(transitions, open(filename, 'w'))
            debug('The transitions are dumped.')
        except IOError as e:
            debug('Was unable to save the generated transitions: ' + str(e))

    return transitions[distanceStr]


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:e:i:n:ot:vh', ['dico-file=', 'export=', 'iadfa=', 'distance=', 'oflazer', 'transitions-file=', 'verbose', 'help'])
    except getopt.GetoptError as e:
        print e
        usage()
        sys.exit(2)

    gen = False
    export = False
    useFastAlgo = True
    distance = None
    transitionsFile = config['transitionsFile']
    iadfaFile = config['iadfaFile']
    dicoFile = config['dicoFile']
    for o, a in opts:
        if o in ('-d', '--dico-file'):
            dicoFile = a
        if o in ('-e', '--export'):
            export = True
            exportFilename = a
        if o in ('-i', '--iadfa'):
            iadfaFile = a
        if o in ('-n', '--distance'):
            try:
                distance = int(a)
            except:
                print 'The distance given in argument is not a number'
                usage()
                sys.exit(2)

        if o in ('-o', '--oflazer'):
            useFastAlgo = False
        if o in ('-h', '--help'):
            usage()
            sys.exit(2)
        if o in ('-t', '--transitions-file'):
            transitionsFile = a
        if o in ('-v', '--verbose'):
            verbose = True

    if os.path.exists(iadfaFile):
        try:
            debug('Loading the FSA from IADFA file')
            a = pickle.load(open(iadfaFile, 'r'))
        except:
            print "There's no valid IADFA file. You should Specify one, or " + "you should generate config's 'iadfaFile' file."
            sys.exit(2)

    else:
        if dicoFile is None:
            print 'No dico file specified!'
            usage()
            sys.exit(2)
        a = generateIADFA(dicoFile, iadfaFile)
    if distance is not None:
        if distance <= 0:
            print 'The distance cannot be negative.'
            usage()
            sys.exit(2)
        if distance > 3:
            print 'You cannot specify a distance greater than 3.'
            usage()
            sys.exit(2)
    else:
        distance = 1
    if export is True:
        exportFileToPS(a, exportFilename)
    transitionStates = None
    if len(args) > 0:
        if useFastAlgo is True:
            debug("Using Schulz's algoritm")
            from fsc import ErrorTolerantRecognizer
            transitionStates = getTransitionStates(transitionsFile, distance)
        else:
            debug("Using Flazer's algorithm")
            from et import ErrorTolerantRecognizer
        print transitionStates
        etr = ErrorTolerantRecognizer(distance, transitionStates)
        for word in args:
            print 'Starting the recognizer for ' + word
            suggestions = etr.recognize(word, a)
            print 'Suggestions for ' + word
            for suggestion in suggestions:
                print '  ' + suggestion

    else:
        debug('No words to be checked.')