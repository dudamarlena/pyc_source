# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgRepReporting/restrictionReport.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\n    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    \n    Author: Monther Alhamdoosh    \n    Python Version: 2.7\n    Changes log: check git commits. \n'
from abseqPy.IgRepReporting.igRepPlots import plotVenn, plotHeatmapFromDF

def generateOverlapFigures(overlapResults, noSeqs, name, siteHitsFile, stream=None):
    """

    :param overlapResults: dictionary
        dictionary with optional keys:
            {
                "order1" : {'enzyme1': {'seq_id1', 'seq_id2', 'seq_id3', ...}, 'enzyme2': {'seq_id5', ...} , ... },
                "order2" : Dataframe of n^2(all-vs-all) rows where each row is a jaccard index of the ids that each
                           pairwise comparison of the enzyme yields. This dataframe has an index column and header
                           that is identical (i.e. a "named matrix") - see calcRSAOverlapOrder2's return value
            }
            "order1" is always there, "order2" only appears if the number of enzymes is at least 3(len(sitesInfo)) >= 3)
    :param noSeqs: total number of sequences
    :param name: string. sample name
    :param siteHitsFile: string. output file name
    :param stream: logger stream
    :return: None
    """
    if overlapResults is None:
        return
    else:
        if 'order1' in overlapResults and len(overlapResults['order1']) in (2, 3):
            title = 'Restriction sites in Sample ' + name
            title += ('\nTotal is {:,}').format(int(noSeqs))
            plotVenn(overlapResults['order1'], siteHitsFile.replace('.csv', '_venn.png'), title, stream=stream)
        if 'order2' in overlapResults:
            title = 'Restriction sites in Sample ' + name
            title += ('\nTotal is {:,}').format(int(noSeqs))
            plotHeatmapFromDF(overlapResults['order2'], siteHitsFile.replace('.csv', '_hm.png'), title=title, stream=stream)
        return