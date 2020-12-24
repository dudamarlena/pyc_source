# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\amrmbruggeman\Documents\Repositories\kadmos\examples\knowledgebases\ssbj\deploy.py
# Compiled at: 2019-10-30 08:16:47
# Size of source mod 2**32: 1203 bytes
import os, shutil
import examples.knowledgebases.ssbj.create_cmdows_file as create_cmdows_file
from ssbjkadmos.utils.database import deploy, clean

def deploy_repo():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    clean(dir_path)
    deploy(dir_path)
    removes = [
     'Constraints-input.xml',
     'Constraints-output.xml',
     'Constraints-partials.xml',
     'Objective-input.xml',
     'Objective-output.xml',
     'Objective-partials.xml']
    for file in os.listdir(os.path.dirname(__file__)):
        checks = ['Aerodynamics-', 'Performance-', 'Propulsion-', 'Structures-', 'DpdxCalc-']
        replaces = ['AeroAnalysis-', 'PerformanceAnalysis-', 'PropulsionAnalysis-', 'StructuralAnalysis-', 'DpdxAnalysis-']
        for i, check in enumerate(checks):
            if check in file:
                shutil.move(os.path.join(dir_path, file), os.path.join(dir_path, replaces[i] + file[len(check):]))

        if file in removes:
            os.remove(os.path.join(dir_path, file))

    create_cmdows_file(dir_path)


if __name__ == '__main__':
    deploy_repo()