# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/datasets/test_movebank.py
# Compiled at: 2020-05-11 03:03:44
# Size of source mod 2**32: 721 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.datasets.movebank import API

def test_movebank_api():
    api = API()
    allstudies = api.getStudies()
    gpsstudies = api.getStudiesBySensor(allstudies, 'GPS')
    api.prettyPrint(gpsstudies)
    individuals = api.getIndividualsByStudy(study_id=9493874)
    api.prettyPrint(individuals)
    gpsevents = api.getIndividualEvents(study_id=9493874, individual_id=11522613, sensor_type_id=653)
    if len(gpsevents) > 0:
        api.prettyPrint(api.transformRawGPS(gpsevents))
    accevents = api.getIndividualEvents(study_id=9493874, individual_id=11522613, sensor_type_id=2365683)
    if len(accevents) > 0:
        api.prettyPrint(api.transformRawACC(accevents))