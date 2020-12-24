# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/runsamtools.py
# Compiled at: 2010-10-12 17:55:41
import optparse
from mpgutils import utils
import sys, re
from optparse import OptionParser
import os, subprocess

def main(argv=None):
    if not argv:
        argv = sys.argv
    lstRequiredOptions = [
     'tgf', 'pif', 'ref']
    usage = 'usage: %prog [options] '
    parser = OptionParser(usage)
    parser.add_option('-s', '--samtoolspath', help='Samtools Path')
    parser.add_option('-f', '--ref', help='Reference Fasta File')
    parser.add_option('-i', '--pif', help='Pool Info File')
    parser.add_option('-t', '--tgf', help='Target Info File')
    parser.add_option('--ncpu')
    parser.add_option('--outputdir')
    parser.add_option('--bqthr')
    parser.add_option('--mqthr')
    parser.add_option('--chr')
    parser.add_option('-n', '--sndb', help='Specifiy Noise Annotation (true or false)')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    samtoolspath = os.path.expanduser(dctOptions.samtoolspath)
    if not os.path.exists(samtoolspath):
        (samtoolspath, tempexe) = os.path.split(samtoolspath)
        if os.path.exists(samtoolspath):
            samtoolsexe = findFiles(samtoolspath, re.compile(tempexe, re.IGNORECASE))
            if samtoolsexe:
                samtools = samtoolsexe[0]
        else:
            print 'Could not locate Sam Tools'
            sys.exit(1)
    else:
        samtools = os.path.join(samtoolspath, 'samtools')
    poolfile = open(os.path.expanduser(dctOptions.pif), 'r')
    poolfile = poolfile.readlines()
    for line in poolfile[1:]:
        line = line.rstrip()
        line = line.split()
        bamfile = line[0]
        lstArgs = [samtools, 'pileup', '-l', dctOptions.tgf + str('.cif'), '-f', dctOptions.ref, bamfile]
        lstArgs.append('-s')
        if dctOptions.sndb == 'true':
            lstArgs.append('-2')
        lstArgs.append(os.path.join(dctOptions.outputdir, str(bamfile) + '.pileup'))
        check_call(lstArgs)


def findFiles(folder_root, pattern):
    Files = []
    for (root, dirs, files) in os.walk(folder_root, False):
        for name in files:
            match = pattern.search(name)
            if match:
                Files.append(os.path.join(root, name))

    return Files


def check_call(lstArgs):
    print lstArgs[(-1)]
    retcode = subprocess.Popen(lstArgs[0:len(lstArgs) - 1], stdout=file(lstArgs[(-1)], 'w'))
    retcode.wait()


if __name__ == '__main__':
    main()