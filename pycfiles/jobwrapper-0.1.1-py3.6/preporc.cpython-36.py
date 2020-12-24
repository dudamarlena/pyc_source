# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/preporc.py
# Compiled at: 2018-09-07 06:03:06
# Size of source mod 2**32: 2561 bytes
import os
from .inputclass import inputparams
import numpy as np
me = 9.109e-31
q = 1.602176565e-19
kb = 1.3806488e-23
eps_0 = 8.8548782e-12
mi = 2.191134689e-25

def main(path):
    """Main function of the preproc script"""
    inputsobject = inputparams(path=path)
    inputs = inputsobject.parameters
    print('Initialisation parameters : ')
    print('density = ', inputs['n'], 'm^-3')
    print('Ly = ', inputs['Ly'] * 100, ' cm')
    print('Lx = ', inputs['Ly'] * inputs['xmax'] / inputs['ymax'] * 1000, ' mm')
    print('')
    print('Simulation parameters')
    print('Ny = ', inputs['ymax'])
    print('Dx = Dy = ', '{:3.1f}'.format(inputs['Ly'] / (inputs['ymax'] + 1) * 1000000.0), ' nm')
    print('Nx = ', inputs['xmax'])
    try:
        Ztheta = inputs['Z_theta']
    except KeyError:
        Ztheta = False

    if Ztheta:
        print('the run is Z-theta !!!!')
        print('Lch = ', inputs['Lch'])
        print('Vdc = ', inputs['V0'])
    else:
        try:
            Periodix = inputs['periodicx']
        except KeyError:
            Periodix = False

        if Periodix:
            print('This is Periodic in Ox !')
        else:
            print('This is a non periodic run ! ')
    test_expected(inputs)


def test_expected(inputs):
    """ printout the expected dX and dT
    """
    Te = inputs['Expected_Te']
    ne = inputs['Expected_ne']
    Lde = np.sqrt(eps_0 * Te / (ne * q))
    dX = inputs['Ly'] / (inputs['ymax'] + 1)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Validation of the Numerical values : ')
    print(f"Expected Debye Lenght: {Lde:2.2e} m")
    print(f"Used cell size: {dX:2.2e} m")
    if dX > Lde / 10:
        print('WARNING the cell size is too big (> Lde/10)!!!!\n')
    else:
        print('The cell size is alright\n')
    wpe = np.sqrt(ne * q ** 2 / (me * eps_0))
    dT = inputs['dT']
    print(f"Expected Plasma frequency: {wpe:2.2e} rad/s")
    print(f"Used sampling frequency: {1 / dT:2.2e} Hz")
    if 1 / dT > 10 * wpe:
        print('WARNING the time step is too big (> wpe/10)!!!!\n')
    else:
        print('The time step is alright\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def get_hostname():
    import socket
    return socket.gethostname()


if __name__ == '__main__':
    print(get_hostname())
    print(os.getcwd())
    main(os.getcwd())