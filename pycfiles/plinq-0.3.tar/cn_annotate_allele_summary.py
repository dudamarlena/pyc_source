# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/cn_annotate_allele_summary.py
# Compiled at: 2010-07-13 12:32:47
__doc__ = '%prog [options]\n\nCreate a map between Affy probe set name and genomic position.  This can be done for\nCNP probes, SNP probesets, or both.  \n'
from __future__ import division
import optparse, os, string, subprocess, sys
from mpgutils import utils
lstRequiredOptions = [
 'probe_locus', 'summary']

def mapSNPs(dctOut, strSnpProbeInfoPath):
    fIn = open(strSnpProbeInfoPath)
    for strLine in fIn:
        lstFields = strLine.split()
        dctOut[lstFields[0]] = (utils.convertChromosomeStr(lstFields[1]), lstFields[2])

    fIn.close()


lstLocusHeaders = [
 'chr', 'position', 'probeset_type']
iStartLocusColumnIndex = 1
iEndLocusColumnIndex = iStartLocusColumnIndex + len(lstLocusHeaders)

class ProbeExtractor(object):

    def __init__(self, strProbeLocusPath, fUnmappedProbesOut, strTempDir=None, bOmitLocusColumns=False):
        self.bOmitLocusColumns = bOmitLocusColumns
        self.fUnmappedProbesOut = fUnmappedProbesOut
        self.dctProbeToGenomicPosition = {}
        self.dctProbeToGenomicPosition = utils.loadProbeLocus(strProbeLocusPath)
        if strTempDir is not None:
            self.lstTempDirArgs = [
             '-T', strTempDir]
        else:
            self.lstTempDirArgs = []
        self.procSort = subprocess.Popen(['sort', '--key=2,2n', '--key=3,3n', '--key=1,1'] + self.lstTempDirArgs, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return

    def processSummary(self, strSummaryPath, fOut):
        fIn = open(strSummaryPath)
        for strLine in fIn:
            if strLine.startswith('#'):
                fOut.write(strLine)
            elif strLine.startswith('probeset_id'):
                lstHeaders = strLine.split()
                lstOutputHeaders = ['probeset_id']
                if not self.bOmitLocusColumns:
                    lstOutputHeaders += lstLocusHeaders
                print >> fOut, ('\t').join(lstOutputHeaders + lstHeaders[1:])
            else:
                break

        fOut.flush()
        self._processSummaryLine(strLine)
        for strLine in fIn:
            self._processSummaryLine(strLine)

        fIn.close()

    def writeOutput(self, fOut):
        print >> sys.stderr, 'Finishing sorted output.'
        self._sloshOutput(fOut, self.procSort)

    def _processSummaryLine(self, strLine):
        lstFields = strLine.split('\t', 1)
        strProbeSetName = lstFields[0]
        if strProbeSetName.endswith('-A') or strProbeSetName.endswith('-B'):
            strProbeSetType = strProbeSetName[(-1)]
            strProbeSetName = strProbeSetName[:-2]
        else:
            strProbeSetType = 'C'
        try:
            tupGenomicPosition = self.dctProbeToGenomicPosition[strProbeSetName]
            lstGenomicPosition = [ str(val) for val in tupGenomicPosition ]
            strOut = ('\t').join(lstFields[0:1] + lstGenomicPosition + [strProbeSetType] + lstFields[1:])
            self.procSort.stdin.write(strOut)
        except KeyError:
            if self.fUnmappedProbesOut is not None:
                self.fUnmappedProbesOut.write(strLine)

        return

    def _sloshOutput(self, fOut, proc):
        proc.stdin.flush()
        proc.stdin.close()
        if self.bOmitLocusColumns:
            for strLine in proc.stdout:
                lstFields = strLine.split()
                del lstFields[iStartLocusColumnIndex:iEndLocusColumnIndex]
                print >> fOut, ('\t').join(lstFields)

        for strLine in proc.stdout:
            fOut.write(strLine)

        if proc.wait() != 0:
            raise Exception('ERROR: %d exit status from sort.' % proc.returncode)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--probe_locus', help='(Required)  SNP and CN probe positions.')
    parser.add_option('--summary', help='(Required) Input file containing probeset summaries as produced by apt-probeset-summarize.')
    parser.add_option('-o', '--output', dest='output', help='Where to write output.  Default: stdout')
    parser.add_option('-u', '--unmapped-probes-output', dest='unmappedProbesOut', help="Where to write summaries of probes for which genomic position is not known.\n                      Default: Don't write.")
    parser.add_option('-t', '--tmpdir', dest='tempdir', help="If /tmp doesn't have enough room to sort, specify a temp directory with more room.")
    parser.add_option('--omit-locus-columns', dest='omitLocusColumns', action='store_true', default=False, help='Do not emit the columns with locus or probe type.  If this argument is used,\n                      all this program does is sort the input by genomic position.')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    if dctOptions.output:
        fOut = open(dctOptions.output, 'w')
    else:
        fOut = sys.stdout
    if dctOptions.unmappedProbesOut:
        fUnmappedProbesOut = open(dctOptions.unmappedProbesOut, 'w')
    else:
        fUnmappedProbesOut = None
    print >> sys.stderr, 'Reading probe info files...'
    probeExtractor = ProbeExtractor(dctOptions.probe_locus, fUnmappedProbesOut, strTempDir=dctOptions.tempdir, bOmitLocusColumns=dctOptions.omitLocusColumns)
    print >> sys.stderr, 'Read summary file...'
    probeExtractor.processSummary(dctOptions.summary, fOut)
    print >> sys.stderr, 'Finishing sort and writing output...'
    probeExtractor.writeOutput(fOut)
    if dctOptions.output:
        fOut.close()
    if fUnmappedProbesOut is not None:
        fUnmappedProbesOut.close()
    return


if __name__ == '__main__':
    sys.exit(main())