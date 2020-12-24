# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuitepriors/birdseed/fixpriors.py
# Compiled at: 2010-07-13 12:32:46
min_var = 0.0001
min_mean = 0.0001
import sys, optparse, mpgutils.utils as utils, math, re
exprNA = re.compile('NA')

def convert_cluster(x):
    return [
     float(x[0]), float(x[1]), float(x[2]), float(x[3]), float(x[4]), int(x[5])]


def badvariances(cluster):
    if float(cluster[2]) * float(cluster[4]) < float(cluster[3]) * float(cluster[3]):
        return True
    else:
        return False


def fixvariances(cluster):
    fixedVar = round(0.9 * math.sqrt(float(cluster[2]) * float(cluster[4])), 4)
    result = [cluster[0], cluster[1], cluster[2], fixedVar, cluster[4], cluster[5]]
    return result


def fixpriors(inputFile, outputFile):
    f = open(inputFile)
    g = open(outputFile, 'w')
    for line in f:
        if exprNA.search(line) is not None:
            continue
        groups = line.split(';')
        line_out = groups[0]
        for k in range(1, len(groups)):
            cluster = groups[k].split()
            cluster = convert_cluster(cluster)
            if cluster[0] < min_mean:
                cluster[0] = min_mean
            if cluster[1] < min_mean:
                cluster[1] = min_mean
            if cluster[2] < min_var:
                cluster[2] = min_var
            if cluster[4] < min_var:
                cluster[4] = min_var
            if badvariances(cluster):
                cluster = fixvariances(cluster)
            cluster = [ str(e) for e in cluster ]
            line_out += ';' + (' ').join(cluster)

        g.write(line_out + '\n')

    f.close()
    g.close()
    changes_made = 0
    return


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-o', '--output', dest='output_fname', help='Where to write output.  Default: stdout')
    parser.add_option('-i', '--input_priors', dest='input_fname', help='')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    lstRequiredOptions = ['output_fname', 'input_fname']
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    fixpriors(dctOptions.input_fname, dctOptions.output_fname)
    return


if __name__ == '__main__':
    sys.exit(main())