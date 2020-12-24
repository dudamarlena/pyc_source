# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/total_scattering/isis/polaris/generate_input.py
# Compiled at: 2019-10-03 13:30:51
import os
from total_scattering.utils import ROOT_DIR
POLARIS_DIR = os.path.join(ROOT_DIR, 'total_scattering', 'isis', 'polaris')
JSON_MSG = '\n{\n"Facility": "ISIS",\n"Instrument": "POLARIS",\n"Title": "Silicon (NIST SRM 640b)",\n"Sample": {"Runs": "97947",\n           "Background": {"Runs": "97948-97951",\n                          "Background": {"Runs": "97952-97954"}\n                          },\n           "Material": "Si",\n           "MassDensity": 2.328,\n           "PackingFraction": 0.35,\n           "Geometry": {"Radius": 0.3175,\n                        "Height": 4.0},\n           "AbsorptionCorrection": {"Type": "Carpenter"},\n           "MultipleScatteringCorrection": {"Type": "Carpenter"},\n           "InelasticCorrection": {"Type": "Placzek",\n                                   "Order": "1st",\n                                   "Self": true,\n                                   "Interference": false,\n                                   "FitSpectrumWith": "GaussConvCubicSpline",\n                                   "LambdaBinningForFit": "0.16,0.04,2.8",\n                                   "LambdaBinningForCalc": "0.16,0.0001,2.9"}\n           },\n"Vanadium": {"Runs": "97942-97946",\n             "Background": {"Runs": "97952-97954"},\n             "Material": "V",\n             "MassDensity": 6.11,\n             "PackingFraction": 1.0,\n             "Geometry": {"Radius": 0.025,\n                          "Height": 4.0},\n             "AbsorptionCorrection": {"Type": "Carpenter"},\n             "MultipleScatteringCorrection": {"Type": "Carpenter"},\n             "InelasticCorrection": {"Type": "Placzek",\n                                     "Order": "1st",\n                                     "Self": true,\n                                     "Interference": false,\n                                     "FitSpectrumWith": "GaussConvCubicSpline",\n                                     "LambdaBinningForFit": "0.16,0.04,2.8",\n                                     "LambdaBinningForCalc": "0.1,0.0001,3.0"}\n             },\n"Calibration": {"Filename": "%s"},\n"HighQLinearFitRange": 0.60,\n"Merging": {"QBinning": [0.35, 0.05, 11.4],\n            "SumBanks": [3],\n            "Characterizations": {"Filename": "%s"}\n            },\n"CacheDir": "%s",\n"OutputDir": "%s"\n}\n'

def generate_input_json():
    calib_path = os.path.join(ROOT_DIR, 'examples', 'isis', 'polaris_grouping.cal')
    character_path = os.path.join(POLARIS_DIR, 'character.txt')
    cache_path = os.path.join(ROOT_DIR, 'cache')
    output_path = os.path.join(ROOT_DIR, 'output')
    if os.name == 'nt':
        calib_path = calib_path.replace('\\', '\\\\')
        character_path = character_path.replace('\\', '\\\\')
        cache_path = cache_path.replace('\\', '\\\\')
        output_path = output_path.replace('\\', '\\\\')
    with open(os.path.join(POLARIS_DIR, 'test_input.json'), 'w') as (input_file):
        input_file.write(JSON_MSG % (calib_path,
         character_path,
         cache_path,
         output_path))


def clean_up():
    os.removedirs(os.path.join(ROOT_DIR, 'cache'))
    os.removedirs(os.path.join(ROOT_DIR, 'output'))
    os.remove(os.path.join(POLARIS_DIR, 'test_input.json'))