# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/etl/imagesimilarity.py
# Compiled at: 2015-05-20 00:05:35
import json, getopt, sys, os
from etllib import compareKeySimilarity, compareValueSimilarity, convertKeyUnicode, generateCirclePacking, generateCluster, generateLevelCluster
_verbose = False
_helpMessage = '\n\nUsage: imagesimilarity [-v --verbose] [-h --help] <operation> [--threshold <threshold>] [--maxnode <maxNumberOfNode>] [-f --directory <directory of images>] [-c --file <file1 file2>] \n\nOperation:\nDEFAULT IS --key\n--key\n    compare similarity by using file metadata key \n\n--value\n    compare similarity by using file metadata value\n\nOptions:  \n--threshold [value of threshold] <default threshold = 0.01>\n    set threshold for cluster similarity   \n--maxnode [value of number of nodes] <default num = 10>\n    set max num of node for each cluster node\n-o, --output\n    the directory of output files\n-f, --directory [path to directory]\n    read similarity-scores.txt file from this directory\n-c, --file [file1 file2]\n    compare given files\n-v, --verbose\n    Work verbosely rather than silently.\n-h --help\n    show help on the screen\n\nExample:\nimagesimilarity.py -f [directory of images]\nimagesimilarity.py -o [directory of output files] -f [directory of images]\nimagesimilarity.py --key  --threshold [threshold] -f [directory of images]\nimagesimilarity.py --threshold [threshold] --maxnode [maxNumberOfNode] -f [directory of images]\nimagesimilarity.py -c [file1 file2]\nimagesimilarity.py -o [directory of output files] -c [file1 file2]\nimagesimilarity.py --key  --threshold [threshold] -c [file1 file2]\nimagesimilarity.py --threshold [threshold] --maxnode [maxNumberOfNode] -c [file1 file2]\n\n'

def verboseLog(message):
    global _verbose
    if _verbose:
        print >> sys.stderr, message


class _Usage(Exception):
    """ an error for arguments """

    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    global _verbose
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], 'f:c:t:o:vhkrm:', ['directory=', 'file=', 'threshold=', 'output=', 'verbose', 'help', 'key', 'value', 'maxnode='])
        except getopt.error as msg:
            raise _Usage(msg)

        if len(opts) == 0:
            raise _Usage(_helpMessage)
        threshold = 0.01
        output_dir = ''
        filenames = []
        filename_list = []
        dirFile = ''
        flag = 1
        maxNumberOfNode = 10
        for option in argv[1:]:
            if option in '--key':
                flag = 1
            elif option in '--value':
                flag = 2

        if '-v' in argv or '--verbose' in argv:
            _verbose = True
        else:
            if '-h' in argv or '--help' in argv:
                raise _Usage(_helpMessage)
            else:
                if '--threshold' in argv:
                    index = argv.index('--threshold')
                    threshold = float(argv[(index + 1)])
                if '--maxnode' in argv:
                    index = argv.index('--maxnode')
                    maxNumberOfNode = argv[(index + 1)]
                if '-o' in argv or '--output' in argv:
                    if '-o' in argv:
                        index = argv.index('-o')
                    elif '--output' in argv:
                        index = argv.index('--output')
                    output_dir = argv[(1 + index)]
                if '-c' in argv or '--file' in argv:
                    if '-c' in argv:
                        index = argv.index('-c')
                    elif '--file' in argv:
                        index = argv.index('--file')
                    filenames = argv[1 + index:]
                if '-f' in argv or '--directory' in argv:
                    if '-f' in argv:
                        index = argv.index('-f')
                    elif '--directory' in argv:
                        index = argv.index('--directory')
                    dirFile = argv[(index + 1)]
                    filenames = [ filename for filename in os.listdir(dirFile) if not filename.startswith('.') ]
            filenames = [ x.strip() for x in filenames ]
            filenames = [ filenames[k].strip("'\n") for k in range(len(filenames)) ]
            for filename in filenames:
                if not os.path.isfile(os.path.join(dirFile, filename)):
                    continue
                filename = os.path.join(dirFile, filename) if dirFile else filename
                filename_list.append(filename)

        if len(filename_list) < 2:
            raise _Usage('you need to type in at least two valid files')
        similarity_score = []
        if flag == 1:
            sorted_resemblance_scores, file_parsed_data = compareKeySimilarity(filename_list)
        else:
            if flag == 2:
                sorted_resemblance_scores, file_parsed_data = compareValueSimilarity(filename_list)
            for tuple in sorted_resemblance_scores:
                similarity_score.append(os.path.basename(tuple[0].rstrip(os.sep)) + ',' + str(tuple[1]) + ',' + tuple[0] + ',' + convertKeyUnicode(file_parsed_data[tuple[0]]) + '\n')

        clusterStruct = generateCluster(similarity_score, threshold)
        clusterStruct = json.dumps(clusterStruct, sort_keys=True, indent=4, separators=(',',
                                                                                        ': '))
        circlePackingStruct = generateCirclePacking(similarity_score, threshold)
        levelClusterStruct = generateLevelCluster(clusterStruct)
        with open(os.path.join(output_dir, 'clusters.json'), 'w') as (f):
            f.write(clusterStruct)
        with open(os.path.join(output_dir, 'levelCluster.json'), 'w') as (f):
            f.write(json.dumps(levelClusterStruct, sort_keys=True, indent=4, separators=(',',
                                                                                         ': ')))
        with open(os.path.join(output_dir, 'circle.json'), 'w') as (f):
            f.write(json.dumps(circlePackingStruct, sort_keys=True, indent=4, separators=(',',
                                                                                          ': ')))
    except _Usage as err:
        print >> sys.stderr, sys.argv[0].split('/')[(-1)] + ': ' + str(err.msg)
        return 2

    return


if __name__ == '__main__':
    sys.exit(main())