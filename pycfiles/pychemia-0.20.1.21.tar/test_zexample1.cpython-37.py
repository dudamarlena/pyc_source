# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_zexample1.py
# Compiled at: 2020-01-21 09:48:43
# Size of source mod 2**32: 3161 bytes
"""
This example shows how to automatize the execution
of ABINIT starting with just the input file "t44.in"

The abinit.files is written with the right
locations for the pseudopotentials and the results
are post-process using the output in NetCDF format
"abinit-o_OUT.nc"
"""
import os, sys, shutil, tempfile, subprocess, pychemia
from pychemia.utils.netcdf import netcdf2dict
import pychemia.code.abinit as pa
path = 'tests/data'

def test_example1():
    """
    Example of a simple calc                                    :
    """
    workdir = tempfile.mkdtemp()
    print(workdir)
    creation(workdir)
    execution(workdir)
    ecut, etotal = datamining(workdir)
    print('ecut=', ecut)
    print('etotal=', etotal)
    assert ecut == 15.0
    assert abs(etotal + 4.199348203363531) < 0.001
    shutil.rmtree(workdir)


def which(program):
    """
    Search for the presence of an executable
    Found in: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    import os

    def is_exe(filep):
        return os.path.isfile(filep) and os.access(filep, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for ipath in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(ipath, program)
            if is_exe(exe_file):
                return exe_file


def creation(filep):
    """
    Create the input file from the original and
    set the proper values for abinit.files
    """
    var = pa.AbinitInput(path + os.sep + 'abinit_04' + os.sep + 't44.in')
    abifile = pa.AbiFiles(filep)
    abifile.set_input(var)
    abifile.set_psps('LDA', 'FHI')
    var.write(abifile.get_input_filename())
    print(abifile)
    print(var)
    abifile.create()


def execution(filep):
    """
    Execute ABINIT in the given path
    """
    abifile = open(filep + '/abinit.files')
    logfile = open(filep + '/abinit.log', 'w')
    cwd = os.getcwd()
    os.chdir(filep)
    if which('abinit') is not None:
        subprocess.call(['abinit'], stdin=abifile, stdout=logfile)
    else:
        print('The executable "abinit" is not in the PATH')
        print('Using the results of a previous calc')
    os.chdir(cwd)
    abifile.close()
    logfile.close()


def datamining(filep):
    """
    Read some output variables from abinit-o_OUT.nc
    """
    print('Extracting ecut and etotal')
    if os.path.isfile(filep + os.sep + 'abinit-o_OUT.nc'):
        data = netcdf2dict(filep + os.sep + 'abinit-o_OUT.nc')
    else:
        data = netcdf2dict(path + os.sep + 'abinit_04' + os.sep + 'abinit-o_OUT.nc')
    print(data)
    print(data['ecut'], data['etotal'])
    return (data['ecut'], data['etotal'])


if __name__ == '__main__':
    workdir = tempfile.mkdtemp()
    if len(sys.argv) == 1:
        test_example1()
    else:
        if len(sys.argv) == 2:
            if sys.argv[1] == 'create':
                creation(workdir)
            elif sys.argv[1] == 'execute':
                execution(workdir)
            else:
                if sys.argv[1] == 'result':
                    datamining(workdir)