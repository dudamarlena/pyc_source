# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ggui\autochop.py
# Compiled at: 2019-08-03 12:38:58
# Size of source mod 2**32: 4563 bytes
"""
.. module:: autochop.py
    :synopsis: Determines time windows of GALEX observations based on time 
.. moduleauthor:: Duy Nguyen <dtn5ah@virginia.edu>
"""
import numpy
from glue.core import Data

def lightcurveChopList(parentData, axis, timeInterval):
    """
    Breaks observation data into observations separated by timeInterval. Returns list of times
    
    :param parentData: Glue (Pandas) Data Object containing CSV lightcurve data
    :type parentData: glue.core.data.Data

    :param axis: parameter to split across (usual = time)
    :type axis: string

    :param timeInterval: interval/amount to split parameter 'axis' across
    :type timeInterval: numpy.float64

    :returns: list -- List of autochop regions
    """
    import numpy
    timeDifferences = numpy.diff(parentData[axis])
    obsWindows = []
    obsStart = parentData[(axis, 0)]
    for index, difference in enumerate(timeDifferences):
        if difference > timeInterval:
            obsEnd = parentData[('MeanTime', index)]
            obsWindows.append((index, obsStart, obsEnd))
            obsStart = parentData[('MeanTime', index + 1)]

    obsWindows.append((len(parentData[axis]), obsStart, parentData[('MeanTime', -1)]))
    return obsWindows


def lightcurveChopImport(glueApp, dataCollection, parentData, obsWindows):
    """
    Receives list of obs windows, breaks dataseries accordingly, imports data object to collection
    
    :param glueApp: Current instantiation of the Glue Application to spawn canvas into
    :type glueApp: glue.app.qt.application.GlueApplication

    :param dataCollection: Library of imported data objects to current Glue interface
    :type dataCollection: glue.core.data.DataCollection 

    :param parentData: Glue (Pandas) Data Object containing CSV lightcurve data
    :type parentData: glue.core.data.Data

    :param obsWindows: List of observation windows with indices upon which to chop
    :type obsWindows: list
    """
    from glue.core import Data
    indxStart = 0
    extensionList = parentData.component_ids()
    for window in obsWindows:
        indxEnd = window[0]
        newChop = Data(label=('AutoChop ' + str(indxStart)))
        for extension in extensionList:
            newChop[str(extension)] = parentData[extension][indxStart:indxEnd]

        dataCollection.append(newChop)
        indxStart = indxEnd + 1


def lightcurveChop(parentData, axis, timeInterval):
    timeDifferences = numpy.diff(parentData[axis])
    obsWindows = []
    obsStart = parentData[(axis, 0)]
    for index, difference in enumerate(timeDifferences):
        if difference > timeInterval:
            obsEnd = parentData[('MeanTime', index)]
            obsWindows.append((obsStart, obsEnd))
            obsStart = parentData[('MeanTime', index + 1)]

    obsWindows.append((obsStart, parentData[('MeanTime', -1)]))
    return obsWindows