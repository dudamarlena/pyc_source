# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/utils/lineselector/lineselection.py
# Compiled at: 2020-01-10 04:27:31
# Size of source mod 2**32: 2699 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '25/09/2017'
import re, numpy
SELECTION_PATTERN = re.compile('\\d?[:]?\\d?')

def selectionIsValid(selection):
    """
    Return true if the given selection as a string is valid

    :return: bool
    """
    assert type(selection) is str
    _selection = selection.replace(' ', '')
    selections = _selection.split(';')
    for sel in selections:
        if not re.match(SELECTION_PATTERN, sel):
            return False

    return True


def getSelection(projections, selection):
    """

    :param str selection:
    :return numpy.ndarray:
    """

    def evalSelection(projections, sel):
        assert type(projections) is numpy.ndarray
        return eval('projections[' + sel + ']')

    assert type(selection) is str
    if selection == '':
        return projections
    _selection = selection.replace(' ', '')
    selections = _selection.split(';')
    if len(selections) is 1:
        return evalSelection(projections, selection)
    res = None
    for iSel, sel in enumerate(range(len(selections))):
        if iSel is 0:
            res = evalSelection(projections, selections[iSel])
        else:
            res = numpy.append(res, evalSelection(projections, selections[iSel]))

    return res