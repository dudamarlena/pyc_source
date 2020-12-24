# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/services/PISCESInterface.py
# Compiled at: 2009-09-24 03:11:06
__doc__ = '\nAn interface to PISCES.\n'
from subprocess import Popen, PIPE
from config import PISCES, DATA
import os

def cullFromPDB(target_dset, MAX_percentage_identity=25, MIN_resolution=0.0, MAX_resolution=2.5, MIN_chain_length=20, MAX_chain_length=400, RFactor=0.3, skip_non_x=True, skip_CA_only=True):
    """
    Invokes PISCES.
    
    arguments:
        target_dset: the target dataset
        MAX_percentage_identity=25: the constraint for the sequence identity
        MIN_resolution=0.0: a lower limit for the resolution
        MAX_resolution=2.5: an upper limit for the resolution
        MIN_chain_length=20: a lower limit for the chain length
        MAX_chain_length=400: an upper limit for the chain length
        RFactor=0.3: the R factor
        skip_non_x=True,
        skip_CA_only=True
    
    return:
        a list of protein identifiers
    """
    service_file_name = 'pidslist.txt'
    __createInputFile(target_dset, service_file_name)
    arguments = ' -i %s -p %s -r %s-%s -l %s-%s -f %s -x %s -a %s' % (
     '%s/%s' % (DATA, service_file_name), str(MAX_percentage_identity), str(MIN_resolution), str(MAX_resolution),
     str(MIN_chain_length), str(MAX_chain_length), str(RFactor), skip_non_x and 'T' or 'F', skip_CA_only and 'T' or 'F')
    cwd = os.getcwd()
    os.chdir(DATA)
    process = Popen('%s/bin/Cull_for_UserPDB.pl' % PISCES + arguments, stdout=PIPE, shell=True)
    process.wait()
    os.chdir(cwd)
    return __getPISCESResponse()


def __createInputFile(target_dset, filename):
    """
    Generates a service file that contains the target dataset. The file is used by PISCES
    
    arguments:
        target_dset: the target dataset
        
        filename: the name of the service file
    
    return:
        the name of the service file
    """
    if not target_dset:
        target_dset = ['whole']
    file_name = '%s/%s' % (DATA, filename)
    list_file = open(file_name, 'w')
    for pid in target_dset:
        list_file.write('%s\n' % pid.replace(':', ''))

    list_file.close()


def __getPISCESResponse():
    """
    Reads the result of PISCES to gets the protein identifiers.
    
    return:
        a list of protein identifiers in the form of tuples (structure, chain)
    """
    listdir = os.listdir(DATA)
    filename = [ filename for filename in listdir if filename.find('cullpdb') != -1 if filename.find('fasta') == -1 ][0]
    outputPISCES = open(DATA + '/' + filename, 'r')
    protein_ids = [ line.split(' ')[0] for line in outputPISCES.readlines() ]
    outputPISCES.close()
    for file_to_remove in [ DATA + '/' + filename for filename in listdir if filename.find('cull') != -1 or filename.find('log') != -1 ]:
        os.remove(file_to_remove)

    return protein_ids[1:]