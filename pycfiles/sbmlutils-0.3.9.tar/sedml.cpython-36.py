# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mkoenig/git/sbmlutils/sbmlutils/dfba/sedml.py
# Compiled at: 2017-11-11 18:07:31
# Size of source mod 2**32: 1243 bytes
"""
Helper functions to create SED-ML.
"""
import os, phrasedml

def create_sedml(sedml_location, sbml_location, directory, dt, tend, species_ids, reaction_ids):
    """ Creates SED-ML file for the given simulation.

    :param sedml_location:
    :param sbml_location:
    :param directory:
    :param dt:
    :param tend:
    :return:
    """
    phrasedml.setWorkingDirectory(directory)
    steps = int(1.0 * tend / dt)
    p = '\n          model1 = model "{}"\n          sim1 = simulate uniform(0, {}, {})\n          sim1.algorithm = kisao.500\n          task1 = run sim1 on model1\n          plot "Figure 1: DFBA species vs. time" time vs {}\n          plot "Figure 2: DFBA fluxes vs. time" time vs {}\n          report "Report 1: DFBA species vs. time" time vs {}\n          report "Report 2: DFBA fluxes vs. time" time vs {}\n\n    '.format(sbml_location, tend, steps, species_ids, reaction_ids, species_ids, reaction_ids)
    return_code = phrasedml.convertString(p)
    if return_code is None:
        print(phrasedml.getLastError())
    sedml = phrasedml.getLastSEDML()
    sedml_file = os.path.join(directory, sedml_location)
    with open(sedml_file, 'w') as (f):
        f.write(sedml)
    print(sedml_file)