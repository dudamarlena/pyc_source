# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_zexample2.py
# Compiled at: 2020-01-21 09:48:43
# Size of source mod 2**32: 3129 bytes
__doc__ = '\nThis example shows how to automatize the execution\nof ABINIT starting with just the input file "t44.in"\n\nThe abinit.files is written with the right\nlocations for the pseudopotentials and the results\nare post-process using the output in NetCDF format\n"abinit-o_OUT.nc"\n'
import os, shutil, json, tempfile, subprocess, pychemia, pychemia.code.abinit
from pychemia.utils.netcdf import netcdf2dict

def test_example2():
    """
    Example of a multiple calc                                  :
    """
    path = 'tests/data'
    assert os.path.isdir(path)
    if which('abinit') is None:
        print('The executable "abinit" is not in the PATH')
        print('Using the results of a previous calc')
        check_results(path + os.sep + 'abinit_04')
        return
    workdir = tempfile.mkdtemp()
    print('Work directory: %s' % workdir)
    assert os.path.isfile(path + '/abinit_04/t44.in')
    av = pychemia.code.abinit.AbinitInput(path + '/abinit_04/t44.in')
    print('Original input:\n%s' % av)
    abifiles = pychemia.code.abinit.AbiFiles(workdir)
    abifiles.set_input(av)
    abifiles.set_psps('LDA', 'FHI')
    abifiles.create()
    res = []
    wf = open(workdir + '/results.json', 'w')
    cwd = os.getcwd()
    os.chdir(workdir)
    for i in range(3):
        av.set_value('ecut', av.get_value('ecut') + 3)
        print(('Computing convergence study with ecut=%f ' % av.get_value('ecut')), end='')
        if i > 0:
            av.set_value('irdwfk', 1)
        av.write(abifiles.get_input_filename())
        abifile = open(workdir + '/abinit.files')
        logfile = open(workdir + '/abinit.log', 'w')
        subprocess.call(['abinit'], stdin=abifile, stdout=logfile)
        if os.path.isfile('abinit-o_WFK'):
            shutil.copyfile('abinit-o_WFK', 'abinit-i_WFK')
        data = netcdf2dict(workdir + '/abinit-o_OUT.nc')
        os.rename(workdir + '/abinit-o_OUT.nc', '%s/abinit-o_OUT.nc_%d' % (workdir, i))
        res.append({'ecut':data['ecut'],  'etotal':data['etotal']})
        print('Total energy: %f' % data['etotal'])

    os.chdir(cwd)
    json.dump(res, wf)
    wf.close()
    check_results(workdir)
    shutil.rmtree(workdir)


def check_results(workdir):
    res = json.load(open(workdir + os.sep + 'results.json'))
    assert res[0]['etotal'] + 4.19954643154 < 1e-06
    assert res[1]['etotal'] + 4.19954643154 < 1e-06
    assert res[2]['etotal'] + 4.19954643154 < 1e-06


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
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file


if __name__ == '__main__':
    test_example2()