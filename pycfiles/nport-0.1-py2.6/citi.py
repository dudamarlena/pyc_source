# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nport/citi.py
# Compiled at: 2010-11-18 12:41:24
import re, os
from datetime import datetime
import numpy as np, nport

def read(file_path, verbose=False):
    """
    Load the contents of a CITI file into an NPort
    
    :returns: NPort holding data contained in the CITI file
    :rtype: :class:`nport.NPort`
    
    """
    file_path = os.path.abspath(file_path)
    citifile = CITIFile(file_path)
    assert citifile.params[0][0][0] == 'freq'
    freqs = citifile.data[0][0]
    ports = np.sqrt(len(citifile.params[0]) - 1)
    assert ports == int(ports)
    ports = int(ports)
    re_param = re.compile('^S\\[(\\d+),(\\d+)\\]$')
    indices = []
    for param in citifile.params[0][1:]:
        name = param[0]
        m = re_param.match(name)
        port1 = int(m.group(1))
        port2 = int(m.group(2))
        indices.append((port1, port2))

    matrices = []
    for index in range(len(freqs)):
        matrix = np.array([ [ None for i in range(ports) ] for j in range(ports)
                          ], dtype=complex)
        for (i, port) in enumerate(indices):
            port1 = port[0]
            port2 = port[1]
            matrix[(port1 - 1, port2 - 1)] = citifile.data[0][(i + 1)][index]

        matrices.append(matrix)

    return nport.NPort(freqs, matrices, nport.SCATTERING, 50)


def write(instance, file_path):
    """Write the n-port data held in `instance` to a CITI file at file_path.
    
    :param instance: n-port data
    :type instance: :class:`nport.NPort`
    :param file_path: filename to write to (without extension)
    :type file_path: str
    
    """
    file_path = file_path + '.citi'
    file = open(file_path, 'wb')
    creationtime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    file.write('# Created by the Python nport module\n')
    file.write('# Creation time: %s\n' % creationtime)
    file.write('CITIFILE A.01.01\n')
    file.write('VAR freq MAG %d\n' % len(instance.freqs))
    instance = instance.convert(nport.S, 50)
    for i in range(instance.ports):
        for j in range(instance.ports):
            file.write('DATA S[%d,%d] RI\n' % (i + 1, j + 1))

    file.write('VAR_LIST_BEGIN\n')
    for freq in instance.freqs:
        file.write('\t%g\n' % freq)

    file.write('VAR_LIST_END\n')
    for i in range(instance.ports):
        for j in range(instance.ports):
            file.write('BEGIN\n')
            for parameter in instance.get_parameter(i + 1, j + 1):
                file.write('\t%g, %g\n' % (parameter.real, parameter.imag))

            file.write('END\n')

    file.write('\n')


import string, sys

class CITIFile:

    def __init__(self, filename):
        self.filename = filename
        self.packages = {}
        self.constants = []
        self.params = []
        self.data = []
        self.instrmnt = []
        myfile = open(self.filename, 'r')
        packagecounter = -1
        packagenames = []
        while 1:
            line = myfile.readline()
            if not line:
                break
            linetxt = string.strip(line)
            line = string.split(linetxt)
            if len(line) > 0:
                if line[0] == 'CITIFILE':
                    packagecounter = packagecounter + 1
                    packagenames.append('')
                    self.constants.append([])
                    self.params.append([])
                    self.data.append([])
                    self.instrmnt.append([])
                    indata = 'NO'
                    invarlist = 'NO'
                    datacount = 0
                if line[0][0] == '#':
                    continue
                elif line[0] == 'NAME':
                    packagenames[packagecounter] = line[1]
                elif line[0] == 'CONSTANT':
                    self.constants[packagecounter].append((line[1], line[2]))
                elif line[0] == 'VAR':
                    self.params[packagecounter].append((line[1], line[2], line[3]))
                elif line[0] == 'SEG_LIST_BEGIN':
                    invarlist = 'SEG'
                    self.data[packagecounter].append([])
                elif line[0] == 'SEG' and invarlist == 'SEG':
                    start = float(line[1])
                    stop = float(line[2])
                    numpoints = int(line[3])
                    step = (stop - start) / (numpoints - 1)
                    next = start
                    count = 0
                    while next <= stop:
                        count = count + 1
                        self.data[packagecounter][datacount].append(next)
                        next = next + step

                elif line[0] == 'SEG_LIST_END':
                    invarlist = 'NO'
                    datacount = datacount + 1
                elif line[0] == 'VAR_LIST_BEGIN':
                    invarlist = 'VARLIST'
                    self.data[packagecounter].append([])
                elif line[0] != 'VAR_LIST_END' and invarlist == 'VARLIST':
                    datum = float(line[0])
                    self.data[packagecounter][datacount].append(datum)
                elif line[0] == 'VAR_LIST_END':
                    invarlist = 'NO'
                    datacount = datacount + 1
                elif line[0] == 'DATA':
                    self.params[packagecounter].append((line[1], line[2]))
                elif line[0] == 'BEGIN':
                    indata = 'YES'
                    self.data[packagecounter].append([])
                elif line[0] != 'END' and indata == 'YES':
                    if self.params[packagecounter][datacount][1] == 'RI':
                        (real, imag) = string.split(linetxt, ',')
                        value = complex(float(real), float(imag))
                    elif self.params[packagecounter][datacount][1] == 'MAG':
                        value = float(line[0])
                    self.data[packagecounter][datacount].append(value)
                elif line[0] == 'END':
                    indata = 'NO'
                    datacount = datacount + 1
                else:
                    self.instrmnt[packagecounter].append(line)

        for values in range(0, packagecounter + 1):
            self.packages[values] = packagenames[values]