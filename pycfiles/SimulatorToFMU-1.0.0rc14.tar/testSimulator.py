# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thierry/vmWareLinux/proj/simulatortofmu/SimulatorToFMU/simulatortofmu/parser/libraries/modelica/SimulatorToFMU/Resources/Python-Sources/testSimulator.py
# Compiled at: 2017-07-24 15:48:57
import numpy

def r1_r1(cS, iS, uS, uR, yS, iwR):
    f = open('r1_r1.txt', 'w')
    f.write(str(iS) + ' ' + str(uR) + ' ' + str(uS) + ' ' + str(yS) + ' ' + ' ' + str(iwR))
    f.close()
    return uR


def r2_r1(cS, iS, uS, uR, yS, iwR):
    f = open('r2_r1.txt', 'w')
    f.write(str(iS) + ' ' + str(uR) + ' ' + str(uS) + ' ' + str(yS) + ' ' + str(iwR))
    f.close()
    return uR[0] + uR[1]


def par3_r1(cS, iS, yS, parS, parR, iwR):
    f = open('par3_r1.txt', 'w')
    f.write(str(iS) + ' ' + str(yS) + ' ' + str(parR) + ' ' + str(parS) + ' ' + str(iwR))
    f.close()
    return parR[0] + parR[1] + parR[2]


def r1_r2(cS, iS, uS, uR, yS, iwR):
    f = open('r1_r2.txt', 'w')
    f.write(str(iS) + ' ' + str(uR) + ' ' + str(uS) + ' ' + str(yS) + ' ' + str(iwR))
    f.close()
    return [uR, uR * 2]


def r2p2_r2(cS, iS, uS, uR, yS, parS, parR, iwR):
    f = open('r2_r2.txt', 'w')
    f.write('The file reference value is: ' + str(iS) + '.' + ' The input names are: ' + uS[0] + ', ' + uS[1] + '.' + ' The output names are: ' + yS[0] + ', ' + yS[1] + '.' + ' The parameter names are: ' + parS[0] + ', ' + parS[1])
    f.close()
    return [uR[0] * parR[0], uR[1] * parR[1]]