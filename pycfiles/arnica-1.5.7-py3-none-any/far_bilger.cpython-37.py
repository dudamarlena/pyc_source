# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duranton/Documents/CERFACS/CODES/arnica/src/arnica/phys/far_bilger.py
# Compiled at: 2020-04-10 17:21:39
# Size of source mod 2**32: 9340 bytes
""" Module for species and mixture """
import numpy as np
ATOMIC_MASS = {'C':12.0107, 
 'H':1.00784, 
 'O':15.999, 
 'N':14.0067}

class SpeciesAtomic:
    __doc__ = ' Class managing species '

    def __init__(self, name, mass_fraction, stream=None, mass_fraction_stream=0.0):
        """Initialize species class"""
        self._name = name.upper()
        self._atoms = self._get_atoms()
        self._molar_mass = self._get_molar_mass()
        self._mass_fraction = mass_fraction
        self._stream = stream
        self._mass_fraction_stream = mass_fraction_stream

    @property
    def atoms(self):
        """ returns dict['CHON'] of number of atoms """
        return self._atoms

    @property
    def molar_mass(self):
        """ returns species molar mass """
        return self._molar_mass

    @property
    def name(self):
        """returns species name """
        return self._name

    @property
    def stream(self):
        """ returns species stream index """
        return self._stream

    def mass_fraction(self, stream=None):
        """
        *Returns either mass fraction or stream-wize mass fraction*

        :returns: Mass Fraction of the species
        """
        if stream is None:
            mass_fraction = self._mass_fraction
        else:
            mass_fraction = self._mass_fraction_stream * (stream == self._stream)
        return mass_fraction

    def mass(self):
        """
        *Compute the mass of the species*

        :returns: Mass of the species
        """
        mass = 0.0
        for atom, n_atom in self.atoms.items():
            mass += n_atom * ATOMIC_MASS[atom]

        return mass

    def _get_atoms(self):
        """
        *Get number of atoms of "CHON" in the species*

        :returns: Dict['CHON'] of number of atoms
        """
        atoms = {}
        idx = 0
        size = len(self._name)
        while idx < size:
            atom = self._name[idx]
            n_atom = ''
            idx += 1
            while idx < size and self._name[idx] not in ATOMIC_MASS:
                n_atom += self._name[idx]
                idx += 1

            if n_atom == '':
                n_atom = '1.'
            atoms[atom] = float(n_atom)

        for atom in ATOMIC_MASS:
            if atom not in atoms:
                atoms[atom] = 0.0

        return atoms

    def _get_molar_mass(self):
        """
        *Compute the molar mass of the species*

            m_i = sum_j (n_i,j * M_j)

        with :

            - i : Species
            - j : Atom

        :returns: Molar mass of the species
        """
        molar_mass = 0.0
        for atom, n_atoms in self._atoms.items():
            molar_mass += n_atoms * ATOMIC_MASS[atom]

        return molar_mass


class MixtureAtomic:
    __doc__ = ' Class managing mixture '

    def __init__(self, species_list, fuel_name):
        """ Initialize MixtureAtomic """
        self._species = species_list
        self._fuel = self.species_by_name(fuel_name)
        self._check_mass_fraction()
        self._mixture_fraction = self._compute_mixture_fraction()
        self._far = self._compute_far()
        self._far_st = self._compute_far_st()
        self._phi = self._compute_equivalence_ratio()

    @property
    def species(self):
        """ return list of SpeciesAtomic object """
        return self._species

    @property
    def species_name(self):
        """ Return list of species names """
        return [species.name for species in self._species]

    @property
    def mixture_fraction(self):
        """ Return mixture fraction """
        return self._mixture_fraction

    @property
    def far(self):
        """ return Fuel Air Ratio """
        return self._far

    @property
    def afr(self):
        """ return Air Fuel Ratio """
        return 1 / self._far

    @property
    def far_st(self):
        """ return stoechiometric Fuel Air Ratio """
        return self._far_st

    @property
    def equivalence_ratio(self):
        """ returns equivalence ratio """
        return self._phi

    def species_by_stream(self, stream):
        """
        *Gets species list by stream number*

        :param stream: Stream number
        :type stream: int

        :returns: List of SpeciesAtomic object matching with stream number
        """
        return [species for species in self._species if species.stream == stream]

    def species_by_name(self, name):
        """
        *Gets SpeciesAtomic by name*

        :param name: Name of the species
        :type name: str

        :returns: SpeciesAtomic object matching with name
        """
        try:
            idx = self.species_name.index(name)
        except ValueError:
            msg = "Species name '" + name + "' does not match with any species :"
            msg += '\n - '
            msg += '\n - '.join(self.species_name)
            raise NameError(msg)

        return self._species[idx]

    def _check_mass_fraction(self):
        """
        """
        mass_fraction = 0.0
        for species in self._species:
            mass_fraction += species.mass_fraction()

        if not np.allclose(mass_fraction, 1.0, atol=0.0001):
            print(mass_fraction)
            raise RuntimeError('Sum of mass fractions is not equal to 1.')

    def elem_mass_frac(self, atom, stream=None):
        """
        *Compute elemental mass fraction of atom j in mixture*

        For each species i, get the elemental mass fraction of the atom j.

                          \xa0a_i,j * M_j * Y_i
            Y_j = sum_i (---------------------)
                                  M_i
        with :

            - **a_i,j** : Number of atom j in species i
            - **M_j** : Molar mass of atom j
            - **M_i** : Molar mass of species i
            - **Y_i** : Mass fraction of species i

        If stream is not None, the mass_fraction is defined as the mass_fraction of         the species i in a the stream s :

            - s = 1 : Fuel stream
            - s = 2 : Oxydizer stream

                           \xa0a_i,j * M_j * Y_i,s
            Y_j,s = sum_i (---------------------)
                                   M_i
        with :

            - **Y_i,s** : Mass fraction of species i in stream s
        """
        el_mass_frac = 0.0
        for species in self._species:
            el_mass_frac += np.divide(species.atoms[atom] * ATOMIC_MASS[atom] * species.mass_fraction(stream), species.molar_mass)

        return el_mass_frac

    def _compute_mixture_fraction(self):
        """
        *Compute mixture fraction of the mixture*

        The mixture fraction Z defined by Bilger as :

              Y_C  / m.M_C  + Y_H  / n.M_H + (Y_O,2 - Y_O) / nu_O2.M_O
        Z = -----------------------------------------------------------
             Y_C,1 / m.M_C + Y_H,1 / n.M_H   +    Y_O,2    / nu_O2.M_O

        with :

            - **Y_j** : Elemental mass fraction of element j
            - **Y_j,s** : Elemental mass fraction of element j in stream s
            - **m, n** : Respectively number of carbon and hydrogen atoms in fuel
            - **M_j** : Molar mass of element j
            - **nu_O2** : Number of moles of O2
        """
        nu_o2 = np.add(self._fuel.atoms['C'], self._fuel.atoms['H'] / 4)
        num_C = np.divide(self.elem_mass_frac('C'), self._fuel.atoms['C'] * ATOMIC_MASS['C'])
        num_H = np.divide(self.elem_mass_frac('H'), self._fuel.atoms['H'] * ATOMIC_MASS['H'])
        num_O = np.divide(self.elem_mass_frac('O', 2) - self.elem_mass_frac('O'), nu_o2 * ATOMIC_MASS['O'])
        num = num_C + num_H + num_O
        den_C = np.divide(self.elem_mass_frac('C', 1), self._fuel.atoms['C'] * ATOMIC_MASS['C'])
        den_H = np.divide(self.elem_mass_frac('H', 1), self._fuel.atoms['H'] * ATOMIC_MASS['H'])
        den_O = np.divide(self.elem_mass_frac('O', 2), nu_o2 * ATOMIC_MASS['O'])
        den = den_C + den_H + den_O
        mixture_fraction = np.divide(num, den)
        return mixture_fraction

    def _compute_far(self):
        """
        *Compute FAR (Fuel Air Ratio) from mixture fraction*

        FAR = Z / (1 - Z)
        """
        far = np.divide(self.mixture_fraction, 1.0 - self.mixture_fraction)
        return far

    def _compute_far_st(self):
        """
        *Compute stoechiometric FAR from stoechiometric quantities*

                sum_j(s=1) m_j    Y_O2,2 * (m*M_C + n*M_h)
        FAR_s = --------------- = ------------------------
                sum_j(s=2) m_j        M_O2 * (m + n/4)
        """
        fuel_mass = 1.0 * self._fuel.molar_mass
        nu_o2 = np.add(self._fuel.atoms['C'], self._fuel.atoms['H'] / 4)
        far_st = np.divide(self.species_by_name('O2').mass_fraction(2) * fuel_mass, self.species_by_name('O2').molar_mass * nu_o2)
        return far_st

    def _compute_equivalence_ratio(self):
        """
        *Compute equivalence ratio phi*

        phi = FAR / FAR_st
        """
        return np.divide(self.far, self.far_st)