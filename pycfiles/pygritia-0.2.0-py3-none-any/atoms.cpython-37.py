# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/gutz/atoms.py
# Compiled at: 2019-03-05 13:42:02
# Size of source mod 2**32: 9437 bytes
import numpy as np

class Atoms:
    """Atoms"""

    def __init__(self, symbols=None, positions=None, numbers=None, scaled_positions=None, cell=None, pbc=None):
        if cell is None:
            self.cell = None
        else:
            self.cell = np.array(cell, dtype=float)
        self.scaled_positions = None
        if self.cell is not None:
            if positions is not None:
                self.set_positions(positions)
        if scaled_positions is not None:
            self.set_scaled_positions(scaled_positions)
        else:
            self.symbols = symbols
            if numbers is None:
                self.numbers = None
            else:
                self.numbers = np.array(numbers, dtype=int)
            if self.numbers is not None:
                self.numbers_to_symbols()
            elif self.symbols is not None:
                self.symbols_to_numbers()

    def set_cell(self, cell):
        self.cell = np.array(cell, dtype=float)

    def get_cell(self):
        return self.cell.copy()

    def set_positions(self, cart_positions):
        self.scaled_positions = np.dot(cart_positions, np.linalg.inv(self.cell))

    def get_positions(self):
        return np.dot(self.scaled_positions, self.cell)

    def set_scaled_positions(self, scaled_positions):
        self.scaled_positions = np.array(scaled_positions, dtype=float)

    def get_scaled_positions(self):
        return self.scaled_positions.copy()

    def set_chemical_symbols(self, symbols):
        self.symbols = symbols

    def get_chemical_symbols(self):
        return self.symbols[:]

    def numbers_to_symbols(self):
        self.symbols = [atom_data[n][1] for n in self.numbers]

    def symbols_to_numbers(self):
        self.numbers = np.array([symbol_map[s] for s in self.symbols])

    def get_volume(self):
        return np.linalg.det(self.cell)


atom_data = [
 [
  0, 'X', 'X', 0],
 [
  1, 'H', 'Hydrogen', 1.00794],
 [
  2, 'He', 'Helium', 4.002602],
 [
  3, 'Li', 'Lithium', 6.941],
 [
  4, 'Be', 'Beryllium', 9.012182],
 [
  5, 'B', 'Boron', 10.811],
 [
  6, 'C', 'Carbon', 12.0107],
 [
  7, 'N', 'Nitrogen', 14.0067],
 [
  8, 'O', 'Oxygen', 15.9994],
 [
  9, 'F', 'Fluorine', 18.9984032],
 [
  10, 'Ne', 'Neon', 20.1797],
 [
  11, 'Na', 'Sodium', 22.98976928],
 [
  12, 'Mg', 'Magnesium', 24.305],
 [
  13, 'Al', 'Aluminium', 26.9815386],
 [
  14, 'Si', 'Silicon', 28.0855],
 [
  15, 'P', 'Phosphorus', 30.973762],
 [
  16, 'S', 'Sulfur', 32.065],
 [
  17, 'Cl', 'Chlorine', 35.453],
 [
  18, 'Ar', 'Argon', 39.948],
 [
  19, 'K', 'Potassium', 39.0983],
 [
  20, 'Ca', 'Calcium', 40.078],
 [
  21, 'Sc', 'Scandium', 44.955912],
 [
  22, 'Ti', 'Titanium', 47.867],
 [
  23, 'V', 'Vanadium', 50.9415],
 [
  24, 'Cr', 'Chromium', 51.9961],
 [
  25, 'Mn', 'Manganese', 54.938045],
 [
  26, 'Fe', 'Iron', 55.845],
 [
  27, 'Co', 'Cobalt', 58.933195],
 [
  28, 'Ni', 'Nickel', 58.6934],
 [
  29, 'Cu', 'Copper', 63.546],
 [
  30, 'Zn', 'Zinc', 65.38],
 [
  31, 'Ga', 'Gallium', 69.723],
 [
  32, 'Ge', 'Germanium', 72.64],
 [
  33, 'As', 'Arsenic', 74.9216],
 [
  34, 'Se', 'Selenium', 78.96],
 [
  35, 'Br', 'Bromine', 79.904],
 [
  36, 'Kr', 'Krypton', 83.798],
 [
  37, 'Rb', 'Rubidium', 85.4678],
 [
  38, 'Sr', 'Strontium', 87.62],
 [
  39, 'Y', 'Yttrium', 88.90585],
 [
  40, 'Zr', 'Zirconium', 91.224],
 [
  41, 'Nb', 'Niobium', 92.90638],
 [
  42, 'Mo', 'Molybdenum', 95.96],
 [
  43, 'Tc', 'Technetium', 0],
 [
  44, 'Ru', 'Ruthenium', 101.07],
 [
  45, 'Rh', 'Rhodium', 102.9055],
 [
  46, 'Pd', 'Palladium', 106.42],
 [
  47, 'Ag', 'Silver', 107.8682],
 [
  48, 'Cd', 'Cadmium', 112.411],
 [
  49, 'In', 'Indium', 114.818],
 [
  50, 'Sn', 'Tin', 118.71],
 [
  51, 'Sb', 'Antimony', 121.76],
 [
  52, 'Te', 'Tellurium', 127.6],
 [
  53, 'I', 'Iodine', 126.90447],
 [
  54, 'Xe', 'Xenon', 131.293],
 [
  55, 'Cs', 'Caesium', 132.9054519],
 [
  56, 'Ba', 'Barium', 137.327],
 [
  57, 'La', 'Lanthanum', 138.90547],
 [
  58, 'Ce', 'Cerium', 140.116],
 [
  59, 'Pr', 'Praseodymium', 140.90765],
 [
  60, 'Nd', 'Neodymium', 144.242],
 [
  61, 'Pm', 'Promethium', 0],
 [
  62, 'Sm', 'Samarium', 150.36],
 [
  63, 'Eu', 'Europium', 151.964],
 [
  64, 'Gd', 'Gadolinium', 157.25],
 [
  65, 'Tb', 'Terbium', 158.92535],
 [
  66, 'Dy', 'Dysprosium', 162.5],
 [
  67, 'Ho', 'Holmium', 164.93032],
 [
  68, 'Er', 'Erbium', 167.259],
 [
  69, 'Tm', 'Thulium', 168.93421],
 [
  70, 'Yb', 'Ytterbium', 173.054],
 [
  71, 'Lu', 'Lutetium', 174.9668],
 [
  72, 'Hf', 'Hafnium', 178.49],
 [
  73, 'Ta', 'Tantalum', 180.94788],
 [
  74, 'W', 'Tungsten', 183.84],
 [
  75, 'Re', 'Rhenium', 186.207],
 [
  76, 'Os', 'Osmium', 190.23],
 [
  77, 'Ir', 'Iridium', 192.217],
 [
  78, 'Pt', 'Platinum', 195.084],
 [
  79, 'Au', 'Gold', 196.966569],
 [
  80, 'Hg', 'Mercury', 200.59],
 [
  81, 'Tl', 'Thallium', 204.3833],
 [
  82, 'Pb', 'Lead', 207.2],
 [
  83, 'Bi', 'Bismuth', 208.9804],
 [
  84, 'Po', 'Polonium', 0],
 [
  85, 'At', 'Astatine', 0],
 [
  86, 'Rn', 'Radon', 0],
 [
  87, 'Fr', 'Francium', 0],
 [
  88, 'Ra', 'Radium', 0],
 [
  89, 'Ac', 'Actinium', 0],
 [
  90, 'Th', 'Thorium', 232.03806],
 [
  91, 'Pa', 'Protactinium', 231.03588],
 [
  92, 'U', 'Uranium', 238.02891],
 [
  93, 'Np', 'Neptunium', 0],
 [
  94, 'Pu', 'Plutonium', 0],
 [
  95, 'Am', 'Americium', 0],
 [
  96, 'Cm', 'Curium', 0],
 [
  97, 'Bk', 'Berkelium', 0],
 [
  98, 'Cf', 'Californium', 0],
 [
  99, 'Es', 'Einsteinium', 0],
 [
  100, 'Fm', 'Fermium', 0],
 [
  101, 'Md', 'Mendelevium', 0],
 [
  102, 'No', 'Nobelium', 0],
 [
  103, 'Lr', 'Lawrencium', 0],
 [
  104, 'Rf', 'Rutherfordium', 0],
 [
  105, 'Db', 'Dubnium', 0],
 [
  106, 'Sg', 'Seaborgium', 0],
 [
  107, 'Bh', 'Bohrium', 0],
 [
  108, 'Hs', 'Hassium', 0],
 [
  109, 'Mt', 'Meitnerium', 0],
 [
  110, 'Ds', 'Darmstadtium', 0],
 [
  111, 'Rg', 'Roentgenium', 0],
 [
  112, 'Cn', 'Copernicium', 0],
 [
  113, 'Uut', 'Ununtrium', 0],
 [
  114, 'Uuq', 'Ununquadium', 0],
 [
  115, 'Uup', 'Ununpentium', 0],
 [
  116, 'Uuh', 'Ununhexium', 0],
 [
  117, 'Uus', 'Ununseptium', 0],
 [
  118, 'Uuo', 'Ununoctium', 0]]
symbol_map = {'H':1, 
 'He':2, 
 'Li':3, 
 'Be':4, 
 'B':5, 
 'C':6, 
 'N':7, 
 'O':8, 
 'F':9, 
 'Ne':10, 
 'Na':11, 
 'Mg':12, 
 'Al':13, 
 'Si':14, 
 'P':15, 
 'S':16, 
 'Cl':17, 
 'Ar':18, 
 'K':19, 
 'Ca':20, 
 'Sc':21, 
 'Ti':22, 
 'V':23, 
 'Cr':24, 
 'Mn':25, 
 'Fe':26, 
 'Co':27, 
 'Ni':28, 
 'Cu':29, 
 'Zn':30, 
 'Ga':31, 
 'Ge':32, 
 'As':33, 
 'Se':34, 
 'Br':35, 
 'Kr':36, 
 'Rb':37, 
 'Sr':38, 
 'Y':39, 
 'Zr':40, 
 'Nb':41, 
 'Mo':42, 
 'Tc':43, 
 'Ru':44, 
 'Rh':45, 
 'Pd':46, 
 'Ag':47, 
 'Cd':48, 
 'In':49, 
 'Sn':50, 
 'Sb':51, 
 'Te':52, 
 'I':53, 
 'Xe':54, 
 'Cs':55, 
 'Ba':56, 
 'La':57, 
 'Ce':58, 
 'Pr':59, 
 'Nd':60, 
 'Pm':61, 
 'Sm':62, 
 'Eu':63, 
 'Gd':64, 
 'Tb':65, 
 'Dy':66, 
 'Ho':67, 
 'Er':68, 
 'Tm':69, 
 'Yb':70, 
 'Lu':71, 
 'Hf':72, 
 'Ta':73, 
 'W':74, 
 'Re':75, 
 'Os':76, 
 'Ir':77, 
 'Pt':78, 
 'Au':79, 
 'Hg':80, 
 'Tl':81, 
 'Pb':82, 
 'Bi':83, 
 'Po':84, 
 'At':85, 
 'Rn':86, 
 'Fr':87, 
 'Ra':88, 
 'Ac':89, 
 'Th':90, 
 'Pa':91, 
 'U':92, 
 'Np':93, 
 'Pu':94, 
 'Am':95, 
 'Cm':96, 
 'Bk':97, 
 'Cf':98, 
 'Es':99, 
 'Fm':100, 
 'Md':101, 
 'No':102, 
 'Lr':103, 
 'Rf':104, 
 'Db':105, 
 'Sg':106, 
 'Bh':107, 
 'Hs':108, 
 'Mt':109, 
 'Ds':110, 
 'Rg':111, 
 'Cn':112, 
 'Uut':113, 
 'Uuq':114, 
 'Uup':115, 
 'Uuh':116, 
 'Uus':117, 
 'Uuo':118}