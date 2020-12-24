# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\crypto\symmetric.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 1919 bytes
import importlib, importlib.util
preftable = {'DES':[
  'pyCrypto', 'pure'], 
 'TDES':[
  'pyCrypto', 'pure'], 
 'AES':[
  'cryptography', 'pyCrypto', 'pure'], 
 'RC4':[
  'cryptography', 'pyCrypto', 'pure']}
available_modules = [
 'pure']
if importlib.util.find_spec('cryptography') is not None:
    print('Found cryptography package!')
    available_modules.append('cryptography')
else:
    if importlib.util.find_spec('pyCrypto') is not None:
        print('Found cryptography package!')
        available_modules.append('pyCrypto')

def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def getPreferredCipher(cipherName):
    if cipherName not in preftable:
        raise Exception('Cipher %s doesnt have any preferences set!' % cipherName)
    possible_prefmodule = list(set(preftable[cipherName]).intersection(set(available_modules)))
    selected_module = None
    for moduleName in preftable[cipherName]:
        if moduleName in possible_prefmodule:
            selected_module = moduleName

    if selected_module is None:
        raise Exception('Could not find any modules to load cipher %s' % cipherName)
    print('Preferred module selected for cipher %s is %s' % (cipherName, selected_module))
    moduleName = 'responder3.crypto.%s' % cipherName
    objectName = selected_module + cipherName
    return import_from(moduleName, objectName)


def getSpecificCipher(cipherName, moduleBaseName):
    moduleName = 'responder3.crypto.%s' % cipherName
    objectName = '%s%s' % (moduleBaseName, cipherName)
    return import_from(moduleName, objectName)


DES = getPreferredCipher('DES')
AES = getPreferredCipher('AES')
RC4 = getPreferredCipher('RC4')