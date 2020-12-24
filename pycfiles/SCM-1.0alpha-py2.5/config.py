# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/config.py
# Compiled at: 2009-05-29 13:49:17
import os
flag = ''
voce = [['tauZero1P', 'tauOne1P', 'thetaZero1P', 'thetaOne1P'],
 [
  'tauZero2P', 'tauOne2P', 'thetaZero2P', 'thetaOne2P'],
 [
  'tauZero3P', 'tauOne3P', 'thetaZero3P', 'thetaOne3P'],
 [
  'tauZero4P', 'tauOne4P', 'thetaZero4P', 'thetaOne4P'],
 [
  'tauZero5P', 'tauOne5P', 'thetaZero5P', 'thetaOne5P'],
 [
  'tauZero6P', 'tauOne6P', 'thetaZero6P', 'thetaOne6P'],
 [
  'tauZero7P', 'tauOne7P', 'thetaZero7P', 'thetaOne7P'],
 [
  'tauZero8P', 'tauOne8P', 'thetaZero8P', 'thetaOne8P']]
file_Texture = ['Random_1000.tex', 'Random_2916.tex', 'Random_23328.tex', 'Extruded_Mg_1944.tex', 'Extruded_Mg_15548.tex']
file_Diffraction = ['BCC.dif', 'FCC.dif', 'HCP.dif']
if os.name == 'nt' and flag == 'release':
    import _winreg
    handle = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    key = _winreg.OpenKey(handle, 'SOFTWARE\\EngDiff\\EPSC\\Settings')
    dirEpsc = _winreg.QueryValueEx(key, 'Path')[0]
    dirImages = dirEpsc + '\\epscApp\\images\\'
    dirEpscCore = dirEpsc + '\\epscApp\\epscCore\\'
    dirEpscCore_phase1 = dirEpsc + '\\epscApp\\epscCore\\'
    dirEshelbyCore = dirEpsc + '\\epscApp\\eshelbyCore\\'
    dirTemp = dirEpsc + '\\epscApp\\Temp\\'
else:
    dirImages = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'images' + os.sep
    dirEpscCore = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'epscCore' + os.sep
    dirEpscCore_phase1 = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'epscCore' + os.sep
    dirEshelbyCore = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'eshelbyCore' + os.sep
    dirTemp = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'Temp' + os.sep