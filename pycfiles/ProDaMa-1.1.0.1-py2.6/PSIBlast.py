# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/services/PSIBlast.py
# Compiled at: 2009-09-24 03:11:06
"""
An interface to PSI-BLAST
"""
from subprocess import Popen, PIPE
from config import PSIBLAST, DATA
import os, time

def callPSIBlast(sequence, ecutoff, iterations):
    """
    Invokes PSI-BLAST.

    arguments:
        sequence: the target sequence

        ecutoff: the E-value

        iterations: the number of PSI-BLAST iteractions

    return:
        a list of protein identifiers in the form of tuples (structure, chain)
    """
    service_file_name = '%s/%s' % (DATA, __createInputFile(sequence))
    result_file_name = str(time.time())
    arguments = ' --email manconi@diee.unica.it --mode PSI-Blast -d pdb -j %s -e %s -O %s %s' % (str(iterations), str(ecutoff), result_file_name, service_file_name)
    cwd = os.getcwd()
    os.chdir(DATA)
    process = Popen('perl %s/blastpgp.pl' % PSIBLAST + arguments, stdout=PIPE, shell=True)
    process.wait()
    os.chdir(cwd)
    return __getPSIBlastResponse(result_file_name)


def __createInputFile(sequence):
    """
    Generates a service file that contains the target sequence. The file is used by PSI-BLAST

    arguments:
        sequence: the target sequence

    return:
        the name of the service file
    """
    service_filename = '%s.txt' % str(time.time())
    path_service_filename = '%s/%s' % (DATA, service_filename)
    service_file = open(path_service_filename, 'w')
    service_file.write('%s\n' % sequence)
    service_file.close()
    return service_filename


def __getPSIBlastResponse(filename):
    """
    Reads the result of PSI-BLAST to gets the protein identifiers.

    arguments:
        filename: the name of the file used by PSI-BLAST to store the alignment

    return:
        a list of protein identifiers in the form of tuples (structure, chain)
    """
    psiblast_result = open('%s/%s.txt' % (DATA, filename), 'r').readlines()
    filtered_data = [ i for i in psiblast_result if i.find('PDB') != -1 if i.find('>') == -1 ]
    protein_ids = [ (i[4:8], i[9]) for i in filtered_data ]
    os.remove('%s/%s.txt' % (DATA, filename))
    os.remove('%s/%s.xml' % (DATA, filename))
    return protein_ids