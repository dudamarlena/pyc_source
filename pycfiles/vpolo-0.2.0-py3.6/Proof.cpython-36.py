# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vpolo/avs_tools/Proof.py
# Compiled at: 2019-09-19 11:28:06
# Size of source mod 2**32: 1343 bytes
from EqClass import Eqclasses
import Alevin, Utools, Kallisto, CellRanger, Alevin_MST, sys

def plot_predictions(alv, utl, kal, crn, alv_mst):
    print('\n\n\n\n===================')
    print('IGNORE logs above this\n===================')
    print('Alevin Predictions: ')
    print(alv)
    print('Alevin_MST Predictions: ')
    print(alv_mst)
    print('Utools Predictions: ')
    print(utl)
    print('Kallisto Predictions: ')
    print(kal)
    print('CellRanger Predictions: ')
    print(crn)


def run(eq_file):
    """
    Run tests for all the methods
    :param eq_file: path of the file having eqclass structure
    :return: None
    """
    eq_class_obj = Eqclasses(eq_file)
    utl_prediction = Utools.get_prediction(eq_class_obj)
    alv_prediction = Alevin.get_prediction(eq_class_obj)
    alv_mst_prediction = Alevin_MST.get_prediction(eq_class_obj)
    kal_prediction = Kallisto.get_prediction(eq_class_obj)
    crn_prediction = CellRanger.get_prediction(eq_class_obj)
    plot_predictions(alv_prediction, utl_prediction, kal_prediction, crn_prediction, alv_mst_prediction)


if __name__ == '__main__':
    run(sys.argv[1])