# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\phaseshifts\gui\PeriodicTable.py
# Compiled at: 2014-01-30 16:33:20
"""
atorb.py

@author: Liam Deacon

@contact: liam.m.deacon@gmail.com

@copyright: Copyright (C) 2014 Liam Deacon

@license: MIT License (see LICENSE file for details)

@summary: Periodic Table using Qt

"""
import logging, ntpath, os, platform, sys
__APP_AUTHOR__ = 'Liam Deacon'
__APP_COPYRIGHT__ = b'\xa9' + ('2013 {0}').format(__APP_AUTHOR__)
__APP_DESCRIPTION__ = 'A simple Python-based program \nfor LEED-IV data extraction'
__APP_EMAIL__ = 'liam.m.deacon@gmail.com'
__APP_LICENSE__ = 'MIT License'
__APP_NAME__ = 'Peridic Table'
__APP_VERSION__ = '0.1-alpha'
__PYTHON__ = ('{0}.{1}.{2}').format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro, sys.version_info.releaselevel)
if platform.system() is 'Windows':
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(__APP_NAME__)
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def determineGuiFrontend():
    """Determine which GUI toolkit to use"""
    try:
        guiFrontend = ('PySide {0}').format(PySide.__version__)
    except NameError:
        guiFrontend = None

    if guiFrontend is None:
        try:
            guiFrontend = ('PyQt {0}').format(PYQT_VERSION_STR)
        except NameError:
            guiFrontend = None

    if guiFrontend != None:
        return ('Qt {0} (PyQt {1})').format(QtCore.qVersion(), guiFrontend)
    else:
        return


__APP_GUI__ = determineGuiFrontend()
import res_rc, elements, re
from collections import OrderedDict
elements_dict = OrderedDict([
 ('H', 'Hydrogen'),
 ('He', 'Helium'),
 ('Li', 'Lithium'),
 ('Be', 'Beryllium'),
 ('B', 'Boron'),
 ('C', 'Carbon'),
 ('N', 'Nitrogen'),
 ('O', 'Oxygen'),
 ('F', 'Fluorine'),
 ('Ne', 'Neon'),
 ('Na', 'Sodium'),
 ('Mg', 'Magnesium'),
 ('Al', 'Aluminium'),
 ('Si', 'Silicon'),
 ('P', 'Phosphorus'),
 ('S', 'Sulfur'),
 ('Cl', 'Chlorine'),
 ('Ar', 'Argon'),
 ('K', 'Potassium'),
 ('Ca', 'Calcium'),
 ('Sc', 'Scandium'),
 ('Ti', 'Titanium'),
 ('V', 'Vanadium'),
 ('Cr', 'Chromium'),
 ('Mn', 'Manganese'),
 ('Fe', 'Iron'),
 ('Co', 'Cobalt'),
 ('Ni', 'Nickel'),
 ('Cu', 'Copper'),
 ('Zn', 'Zinc'),
 ('Ga', 'Gallium'),
 ('Ge', 'Germanium'),
 ('As', 'Arsenic'),
 ('Se', 'Selenium'),
 ('Br', 'Bromine'),
 ('Kr', 'Krypton'),
 ('Rb', 'Rubidium'),
 ('Sr', 'Strontium'),
 ('Y', 'Yttrium'),
 ('Zr', 'Zirconium'),
 ('Nb', 'Niobium'),
 ('Mo', 'Molybdenum'),
 ('Tc', 'Technetium'),
 ('Ru', 'Ruthenium'),
 ('Rh', 'Rhodium'),
 ('Pd', 'Palladium'),
 ('Ag', 'Silver'),
 ('Cd', 'Cadmium'),
 ('In', 'Indium'),
 ('Sn', 'Tin'),
 ('Sb', 'Antimony'),
 ('Te', 'Tellurium'),
 ('I', 'Iodine'),
 ('Xe', 'Xenon'),
 ('Cs', 'Cesium'),
 ('Ba', 'Barium'),
 ('La', 'Lanthanum'),
 ('Ce', 'Cerium'),
 ('Pr', 'Praseodymium'),
 ('Nd', 'Neodymium'),
 ('Pm', 'Promethium'),
 ('Sm', 'Samarium'),
 ('Eu', 'Europium'),
 ('Gd', 'Gadolinium'),
 ('Tb', 'Terbium'),
 ('Dy', 'Dysprosium'),
 ('Ho', 'Holmium'),
 ('Er', 'Erbium'),
 ('Tm', 'Thulium'),
 ('Yb', 'Ytterbium'),
 ('Lu', 'Lutetium'),
 ('Hf', 'Hafnium'),
 ('Ta', 'Tantalum'),
 ('W', 'Tungsten'),
 ('Re', 'Rhenium'),
 ('Os', 'Osmium'),
 ('Ir', 'Iridium'),
 ('Pt', 'Platinum'),
 ('Au', 'Gold'),
 ('Hg', 'Mercury'),
 ('Tl', 'Thallium'),
 ('Pb', 'Lead'),
 ('Bi', 'Bismuth'),
 ('Po', 'Polonium'),
 ('At', 'Astatine'),
 ('Rn', 'Radon'),
 ('Fr', 'Francium'),
 ('Ra', 'Radium'),
 ('Ac', 'Actinium'),
 ('Th', 'Thorium'),
 ('Pa', 'Protactinium'),
 ('U', 'Uranium'),
 ('Np', 'Neptunium'),
 ('Pu', 'Plutonium'),
 ('Am', 'Americium'),
 ('Cm', 'Curium'),
 ('Bk', 'Berkelium'),
 ('Cf', 'Californium'),
 ('Es', 'Einsteinium'),
 ('Fm', 'Fermium'),
 ('Md', 'Mendelevium'),
 ('No', 'Nobelium'),
 ('Lr', 'Lawrencium'),
 ('Rf', 'Rutherfordium'),
 ('Db', 'Dubnium'),
 ('Sg', 'Seaborgium'),
 ('Bh', 'Bohrium'),
 ('Hs', 'Hassium'),
 ('Mt', 'Meitnerium'),
 ('Ds', 'Darmstadtium'),
 ('Rg', 'Roentgenium'),
 ('Cn', 'Copernicium'),
 ('Uut', 'Ununtrium'),
 ('Fl', 'Flerovium'),
 ('Uup', 'Ununpentium'),
 ('Lv', 'Livermorium'),
 ('Uus', 'Ununseptium'),
 ('Uuo', 'Ununoctium')])

class PeriodicTableDialog(QtGui.QFrame):
    """Periodic table dialog class"""

    def __init__(self, parent=None, toggle=True):
        super(PeriodicTableDialog, self).__init__(parent)
        self.ui = uic.loadUi('gui/PeriodicTable.ui', self)
        self.ui.show()
        self.selectedElement = 'H'
        self.initUi()

    def closeEvent(self, evnt):
        print self.selectedElement
        sys.exit(0)

    def initUi(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        for i in range(1, len(elements.ELEMENTS)):
            symbol = elements_dict.keys()[(i - 1)]
            element = elements.ELEMENTS[symbol]
            config = re.sub('([spdf])', '\\1<sup>', element.eleconfig)
            config = config.replace(' ', '</sup>&nbsp;') + '</sup>'
            element.description
            tooltip = ('\n                <html>\n                    <span style=" font-weight:600;">{name}</span><br/>\n                    Z={protons}<br/>\n                    {mass}&nbsp;amu<br/>\n                    {config}<br/>\n                    T<sub>melt</sub>={tmelt}&nbsp;K<br/>\n                    T<sub>boil</sub>={tboil}&nbsp;K<br/>\n                    &#961;={density}&nbsp;g/L<br/>\n                    &#967;={eleneg}                   \n                </html>').format(protons=element.protons, name=element.name, tmelt=element.tmelt, tboil=element.tboil, config=config, mass=element.mass, density=element.density, eleneg=element.eleneg)
            eval('self.element_%i.clicked.connect(self.buttonClick)' % i)
            eval('self.element_%i.setToolTip(tooltip)' % i)

    def buttonClick(self):
        self.selectedElement = elements.ELEMENTS[(elements_dict.keys().index(self.sender().text()) + 1)]
        self.ui.labelMass.setText('<html><sup>%.1f</sup></html>' % float(self.selectedElement.mass))
        self.ui.labelZ.setText('<html><sup>%s</sup></html>' % self.selectedElement.protons)
        self.ui.labelElement.setText('<html><head/><body><p><span style=" \n                                        font-size:12pt;">%s</span></p></body>\n                                        </html>' % self.selectedElement.symbol)


def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('gui/res/periodictable_32x32.png'))
    window = PeriodicTableDialog()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()