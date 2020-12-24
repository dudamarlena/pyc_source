# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgMultiRepertoire/PlotManager.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = "\nAs of Fri Jun 29 14:42:16 AEST 2018\nThe only plots that STILL PLOTS IN PYTHON despite pythonPlotOn = False, because abseqR hasn't supported them are:\n    1) plotSeqLenDist           - only one that still depends on this is -t seqlen\n                                  (abseqR still doesn't have support for this task)\n    2) plotVenn                 - used by restriction sites and primer analysis\n    4) plotHeatmapFromDF        - restriction sites analysis (detailed and simple)\nThe plots that OBEY pythonPlotOn() = False is:\n    1) all diversity plots (rarefaction, duplication, recapture)\n    2) plotDist()\n    3) plotSeqLenDistClasses\n    4) barLogo                  - generateCumulativeLogo\n    5) plotHeatMap              - generateStatsHeatmap\n"

class PlotManager:
    """
    This class acts as a messenger between abseqPy and abseqR.

    It decides whether or not the python backend will be plotting anything (default = no).

    It also has methods that flush the required metadata for abseqR to determine
    what samples are being compared against each other in a file named after the value of _cfg
    """
    _pythonPlotting = False

    def __init__(self):
        PlotManager._pythonPlotting = False

    @staticmethod
    def pythonPlotOn():
        return PlotManager._pythonPlotting