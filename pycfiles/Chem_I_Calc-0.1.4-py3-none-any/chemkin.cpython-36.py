# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/chem_G5/chemkin.py
# Compiled at: 2017-11-19 20:04:51
# Size of source mod 2**32: 12076 bytes
import numbers, xml.etree.ElementTree as ET, numpy as np, sqlite3, doctest
from chem_G5 import reaction_coeffs

class ElementaryRxn:
    """ElementaryRxn"""

    def __init__(self, filename):
        self.parse(filename)

    def parse(self, filename):
        root = ET.parse(filename).getroot()
        specieslist = root.find('phase').find('speciesArray').text.strip().split(' ')
        r_stoich = []
        p_stoich = []
        self.reversible = []
        self.rxnparams = []
        for reaction in root.find('reactionData').findall('reaction'):
            if reaction.attrib['reversible'] == 'yes':
                self.reversible.append(True)
            else:
                self.reversible.append(False)
            r_coeffs = [
             0] * len(specieslist)
            p_coeffs = [0] * len(specieslist)
            r_list = reaction.find('reactants').text.strip().split(' ')
            p_list = reaction.find('products').text.strip().split(' ')
            for r in r_list:
                specie_coeff = r.split(':')
                r_coeffs[specieslist.index(specie_coeff[0])] = float(specie_coeff[1])

            for p in p_list:
                specie_coeff = p.split(':')
                p_coeffs[specieslist.index(specie_coeff[0])] = float(specie_coeff[1])

            r_stoich.append(r_coeffs)
            p_stoich.append(p_coeffs)
            ratecoeff = reaction.find('rateCoeff')
            if ratecoeff.find('Arrhenius') is None:
                self.rxnparams.append([reaction_coeffs.const(float(ratecoeff.find('k').text))])
            else:
                if ratecoeff.find('Arrhenius').find('A') is None:
                    raise ValueError('A is not found')
                if ratecoeff.find('Arrhenius').find('E') is None:
                    raise ValueError('E is not found')
                A = float(ratecoeff.find('Arrhenius').find('A').text)
                E = float(ratecoeff.find('Arrhenius').find('E').text)
                b = ratecoeff.find('Arrhenius').find('b')
                self.rxnparams.append([A, E, b])

        self.r_stoich = np.array(r_stoich).transpose()
        self.p_stoich = np.array(p_stoich).transpose()
        self.specieslist = specieslist

    def prog_rate(self, x, T):
        """
        Returns the progress rate for N species going through M
        irreversible, elementary reactions.

        INPUTS
        ======
        x:       numeric list
                 concentrations of A, B, C

        RETURNS
        =======
        omega:   the progress rate for the reaction, numeric

        EXAMPLES
        =======
        >>> ElementaryRxn('chem_G5/test/doctest1.xml').prog_rate([1, 2, 4], 1200)
        [20.0]

        >>> ElementaryRxn('chem_G5/test/doctest2.xml').prog_rate([1,2,1], 1200)
        [40.0, 10.0]
        """
        k = []
        for elt in self.rxnparams:
            if len(elt) == 1:
                k.append(elt[0])
            else:
                if elt[2] is None:
                    k.append(reaction_coeffs.arrh(elt[0], elt[1], T))
                else:
                    k.append(reaction_coeffs.mod_arrh(elt[0], float(elt[2].text), elt[1], T))

        x = np.array(x)
        stoich = np.array(self.r_stoich)
        k = np.array(k)
        if not np.issubdtype(x.dtype, np.number):
            raise AssertionError('Species concentrations must be numeric')
        else:
            if not np.issubdtype(stoich.dtype, np.number):
                raise AssertionError('Stoichiometric coefficients must be numeric')
            elif not len(x) == stoich.shape[0]:
                raise AssertionError('All species must have stoichiometric coefficients')
            assert np.issubdtype(k.dtype, np.number), 'Reaction rate coefficients must be numeric'
        return list(k * np.product((x ** stoich.T), axis=1))

    def rxn_rate(self, x, T):
        """
        Returns the reaction rate, f, for each specie (listed in x)
        through one or multiple (number of columns in stoich_r)
        elementary, irreversible reactions.

        f = sum(omega_j*nu_ij) for i species in j reactions.

        INPUTS
        ======
        x:        numeric list or array
                  concentrations of reactants

        RETURNS
        =======
        f:        the reaction rate for each specie, numeric

        EXAMPLES
        =======
        >>> ElementaryRxn('chem_G5/test/doctest3.xml').rxn_rate([1,2,1], 1200)
        array([-30., -60.,  20.])

        """
        p_stoich = np.array(self.p_stoich)
        r_stoich = np.array(self.r_stoich)
        omega = self.prog_rate(x, T)
        if np.shape(p_stoich)[1] == 1:
            return np.sum(omega * (p_stoich - r_stoich))
        else:
            return np.sum((omega * (p_stoich - r_stoich)), axis=1)

    def __str__(self):
        return 'Stoichiometric coefficients of reactants: {}\n            Stoichiometric coefficients of reactants: {}\n            Reaction rate coefficient: {}'.format(self.r_stoich, self.p_stoich, self.k)


class ReversibleRxn(ElementaryRxn):

    def __init__(self, filename):
        self.parse(filename)
        self.s = self.specieslist
        self.r = self.r_stoich
        self.p = self.p_stoich
        self.nuij = self.p - self.r
        self.p0 = 100000.0
        self.R = 8.3144598
        self.gamma = np.sum((self.nuij), axis=0)

    def read_SQL(self, T):

        def choose_t_range(T):
            t_range = []
            for species in self.s:
                v = cursor.execute('SELECT THIGH\n                from LOW WHERE species_name= ?', (species,)).fetchall()
                if v[0][0] > T:
                    t_range.append('high')
                else:
                    t_range.append('low')

            return t_range

        def get_coeffs(species_name, temp_range):
            if temp_range == 'low':
                v = cursor.execute('SELECT COEFF_1,COEFF_2,COEFF_3,COEFF_4,COEFF_5,COEFF_6,COEFF_7\n                from LOW WHERE species_name= ?', (species_name,)).fetchall()
            else:
                if temp_range == 'high':
                    v = cursor.execute('SELECT COEFF_1,COEFF_2,COEFF_3,COEFF_4,COEFF_5,COEFF_6,COEFF_7\n                from HIGH WHERE species_name= ?', (species_name,)).fetchall()
            coeffs = v[0]
            return coeffs

        assert isinstance(T, numbers.Number), 'Please enter a numeric temperature.'
        db = sqlite3.connect('chem_G5/data/NASA.sqlite')
        cursor = db.cursor()
        coefs = []
        t_range = choose_t_range(T)
        s_t = zip(self.s, t_range)
        for species, tmp in s_t:
            coef = get_coeffs(species, tmp)
            coefs.append(coef)

        self.nasa = np.array(coefs)

    def Cp_over_R(self, T):
        a = self.nasa
        Cp_R = a[:, 0] + a[:, 1] * T + a[:, 2] * T ** 2.0 + a[:, 3] * T ** 3.0 + a[:, 4] * T ** 4.0
        return Cp_R

    def H_over_RT(self, T):
        a = self.nasa
        H_RT = a[:, 0] + a[:, 1] * T / 2.0 + a[:, 2] * T ** 2.0 / 3.0 + a[:, 3] * T ** 3.0 / 4.0 + a[:, 4] * T ** 4.0 / 5.0 + a[:, 5] / T
        return H_RT

    def S_over_R(self, T):
        a = self.nasa
        S_R = a[:, 0] * np.log(T) + a[:, 1] * T + a[:, 2] * T ** 2.0 / 2.0 + a[:, 3] * T ** 3.0 / 3.0 + a[:, 4] * T ** 4.0 / 4.0 + a[:, 6]
        return S_R

    def backward_coeffs(self, T):
        delta_H_over_RT = np.dot(self.nuij.T, self.H_over_RT(T))
        delta_S_over_R = np.dot(self.nuij.T, self.S_over_R(T))
        delta_G_over_RT = delta_S_over_R - delta_H_over_RT
        fact = self.p0 / self.R / T
        print('prefactor in Ke: ', fact)
        ke = fact ** self.gamma * np.exp(delta_G_over_RT)
        print('ke: ', ke)
        kf = []
        for elt in self.rxnparams:
            if len(elt) == 1:
                kf.append(elt)
            else:
                if elt[2] is None:
                    kf.append(reaction_coeffs.arrh(elt[0], elt[1], T))
                else:
                    kf.append(reaction_coeffs.mod_arrh(elt[0], float(elt[2].text), elt[1], T))

        self.kf = np.array(kf)
        self.kb = np.copy(self.kf)
        for i in range(len(self.kb)):
            if self.reversible[i]:
                self.kb[i] = self.kf[i] / ke[i]

        print('kb: ', self.kb)

    def prog_rate(self, x, T):
        self.read_SQL(T)
        self.backward_coeffs(T)
        x = np.array(x)
        omega = self.kf * np.product(x ** self.r.T) - self.kb * np.product(x ** self.p.T)
        return omega

    def rxn_rate(self, x, T):
        omega = self.prog_rate(x, T)
        return np.sum((omega * self.nuij), axis=1)

    def reversible_rxn_rate(x):
        """
        Returns the reaction rate, f, for each specie (listed in x)
        through one or multiple (number of columns in stoich_r)
        reversible reactions.

        f = sum(omega_j*nu_ij) for i species in j reactions.

        INPUTS
        ======
        x:        numeric list or array
                  concentrations of reactants

        RETURNS
        =======
        f:        the reaction rate for each specie, numeric
        """
        raise NotImplementedError


class NonelRxn(ElementaryRxn):

    def nonel_rxn_rate(x):
        """
        Returns the reaction rate, f, for each specie (listed in x)
        through one or multiple (number of columns in stoich_r)
        nonelementary reactions.

        f = sum(omega_j*nu_ij) for i species in j reactions.

        INPUTS
        ======
        x:        numeric list or array
                  concentrations of reactants

        RETURNS
        =======
        f:        the reaction rate for each specie, numeric
        """
        raise NotImplementedError