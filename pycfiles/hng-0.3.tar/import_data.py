# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: hng/import_data.py
# Compiled at: 2017-01-03 10:24:05
from markdown import markdown
import pandas as pd, numpy as np
from pymongo import MongoClient

def joke():
    """It's a joke, you fool!"""
    return markdown('HAHA! patron')


def import_lab_data():
    """
    import_lab_data         :function to get *all* pure raw lab data (for all patients/encounters)
    parameters              :None
    returns                 :all labs data from DB
    """
    client = MongoClient('mongodb://localhost:27017')
    try:
        db = client.hng_ml
    except:
        return 'Are you using the correct database? Please check the DB name.'

    labs = hng.native_lab_procedures
    labs = pd.DataFrame(list(labs.find({}, {'_id': 0, 'lab_procedure_name': 1, 'encounter_id': 1, 'numeric_result': 1})))
    labs.numeric_result = labs.numeric_result.replace('', np.nan)
    labs.numeric_result = labs.numeric_result.astype(float)
    return labs


def fill_gaussian(df):
    """
    fill_gaussian           :function to fill missing values using Gaussian distribution with sigma and mu taken from normal_range_min, normal_range_high
    parameters              :labs DataFrame
    returns                 :labs DataFrame with missing values filled with Gaussian distribution
    """
    pass


def fill_na(df):
    """
    fillna                  :function to fill missing values with 0.0 on any df
    parameters              :DataFrame
    returns                 :DataFrame with missings filled with 0.0
    """
    pass


def column_convert():
    """
    Work on aggfunc for pivot_table
    """
    pass


def ckd_encounters(priority):
    """
    ckd_encounters          :function to return encounters with priority_code <= priority

    """
    ckd_codes = [
     '403', '403.01', '403.1', '403.11', '403.9', '403.91', '404', '404.01', '404.13', '404.9', '404.91', '404.93', '584.5', '585', 'N17.9', 'N18.2', 'N18.3', 'N18.4', 'N18.9', 'N20.0', 'I12.9', '403', '403.1', '403.9', '404', '404.9', '404.92', '285.21', 'D63.1', '582.9', '584.9', '592', 'V42.0', '585.1', '585.2', '585.3', '585.4', '585.5', '585.9']
    client = MongoClient('mongodb://localhost:27017')
    db = client.hng_ml
    comorb = hng.native_comorbs
    comorb = pd.DataFrame(list(comorb.find({'diagnosis_code': {'$in': ckd_codes}}, {'_id': 0, 'encounter_id': 1, 'diagnosis_priority': 1})))
    location = comorb[(comorb.diagnosis_priority < priority + 1)].index.tolist()