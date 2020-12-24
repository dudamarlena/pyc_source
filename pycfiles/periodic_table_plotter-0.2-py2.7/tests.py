# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ptplotter/tests.py
# Compiled at: 2014-04-14 15:31:46
from plotter import ElementDataPlotter
import matplotlib.pylab as plt, random

def eneg(elt):
    """Electronegativity"""
    return elt['electronegativity']


def mass(elt):
    """Mass"""
    return elt['mass']


def rat(elt):
    """Mass/Electronegativity"""
    return elt['electronegativity'] / elt['mass']


def atomic_number(elt):
    """Atomic number"""
    return elt['z']


def test_pettifor():
    elts = [
     'H', 'Li', 'Be', 'Fe', 'Ni', 'Pd', 'Pt', 'F', 'Xe', 'O', 'S']
    epd = ElementDataPlotter(elements=elts)
    epd.pettifor(mass, eneg)
    plt.savefig('pettifor.png', bbox_inches='tight')


def test_periodic_table():
    epd = ElementDataPlotter()
    epd.ptable([eneg])
    plt.savefig('uni.png', bbox_inches='tight')
    epd = ElementDataPlotter()
    epd.ptable([eneg, mass])
    epd.create_guide_square(x=8, y=-1.5)
    plt.savefig('bi.png', bbox_inches='tight')
    epd = ElementDataPlotter()
    epd.ptable([[eneg, mass], rat])
    plt.savefig('tri.png', bbox_inches='tight')
    epd = ElementDataPlotter()
    epd.ptable([eneg, mass, rat, atomic_number], colorbar=False)
    plt.savefig('quad.png', bbox_inches='tight')


def test_grid():
    epd = ElementDataPlotter()
    elts = ['Ti', 'V', 'Sc', 'Ni', 'Co', 'Fe']
    epd.make_grid(xelts=elts, yelts=elts)
    plt.savefig('grid.png', bbox_inches='tight')


if __name__ == '__main__':
    test_pettifor()
    test_periodic_table()
    test_grid()