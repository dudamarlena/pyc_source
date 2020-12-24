# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/chemkin.py
# Compiled at: 2017-12-11 01:26:31
# Size of source mod 2**32: 15346 bytes
import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import numpy as np
from kinetics.nasa import getNASACoeff
import xml.etree.ElementTree as ET
from history import History as his

class ReactionParser:

    def __init__(self, input_path):
        try:
            tree = ET.parse(input_path)
        except ValueError as err:
            raise ValueError('Something went wrong with your XML file:\n' + str(err))

        self.root = tree.getroot()

    def get_species(self):
        """ Returns the species list of the current reaction
                
                        INPUTS
                        =======
                        self
                        
                        RETURNS
                        ========
                        species: list of string
                """
        species = self.root.find('phase').find('speciesArray')
        species = species.text.strip().split(' ')
        return species

    def parse_reactions(self):
        """ Parse the reactions from XML, and returns the reaction dictionary
                
                        INPUTS
                        =======
                        self
                        
                        RETURNS
                        ========
                        reaction_dict: a dictionary, where key is the reaction id, val is the reaction details
                        
                """
        reaction_dict = {}
        reactions = self.root.find('reactionData').findall('reaction')
        for i, reaction in enumerate(reactions):
            attributes = reaction.attrib
            rtype, rid = attributes['type'], attributes['id']
            reversible = 1 if attributes['reversible'] == 'yes' else 0
            equation = reaction.find('equation').text
            const_coeff = reaction.find('rateCoeff').find('Constant')
            if const_coeff is not None:
                k = const_coeff.find('k')
                coeff_params = {'K': float(k.text)}
            else:
                coeffs = reaction.find('rateCoeff').find('Arrhenius')
                if coeffs is None:
                    coeffs = reaction.find('rateCoeff').find('modifiedArrhenius')
                try:
                    A, E = float(coeffs.find('A').text), float(coeffs.find('E').text)
                except:
                    raise ValueError('did not capture Arrhenius prefactor A and activation energy E, please re-check input format')

                if coeffs.find('b') is not None:
                    coeff_params = {'A':A, 
                     'E':E,  'b':float(coeffs.find('b').text)}
                else:
                    coeff_params = {'A':A, 
                     'E':E}
            reactants = reaction.find('reactants').text.split(' ')
            products = reaction.find('products').text.split(' ')
            v1, v2 = {}, {}
            for specie in self.get_species():
                v1[specie], v2[specie] = (0, 0)

            for i in range(len(reactants)):
                if reactants[i].count(':') is not 1:
                    raise ValueError('check your reactants input format: ' + str(reactants))
                v1[reactants[i].split(':')[0]] = reactants[i].split(':')[1]

            for j in range(len(products)):
                if products[j].count(':') is not 1:
                    raise ValueError('check your products input format: ' + str(products))
                v2[products[j].split(':')[0]] = products[j].split(':')[1]

            reaction_dict[rid] = {'type':rtype, 
             'reversible':reversible, 
             'equation':equation, 
             'species':self.get_species(), 
             'coeff_params':coeff_params, 
             'v1':v1, 
             'v2':v2}

        return reaction_dict


class ChemKin:

    class reaction_coeff:

        @classmethod
        def constant(self, k):
            """Returns the constant reaction coeff
                
                        INPUTS
                        =======
                        k: float, the constant reaction coeff
                        
                        RETURNS
                        ========
                        k: float, the constant reaction coeff
                        
                        EXAMPLES
                        =========
                        >>> ChemKin.reaction_coeff.constant(1.0)
                        1.0
                        >>> ChemKin.reaction_coeff.constant(3.773)
                        3.773
                        """
            return k

        @classmethod
        def arr(self, T, R=8.314, **kwargs):
            """Returns the Arrhenius reaction rate coeff
                        
                        INPUTS
                        =======
                        kwargs:
                        A: positive float, Arrhenius prefactor
                        E: float, activation energy for the reaction

                        T: float, temperature in Kelvin scale
                        
                        RETURNS
                        ========
                        coeff: float, the Arrhenius reaction coeff
                        
                        EXAMPLES
                        =========
                        >>> ChemKin.reaction_coeff.arr(10**2, A=10**7, E=10**3)
                        3003549.0889639612
                        """
            A, E = kwargs['A'], kwargs['E']
            if type(A) is not int:
                if type(A) is not float:
                    raise TypeError('The Arrhenius prefactor A should be either int or float')
            if type(E) is not int:
                if type(E) is not float:
                    raise TypeError('Activation Energy should be either int or float')
            if type(T) is not int:
                if type(T) is not float:
                    raise TypeError('Temperature (in Kelvin scale) should be either int or float')
            if A >= float('inf') or A <= float('-inf'):
                raise ValueError('The Arrhenius prefactor A is under/overflow')
            if E >= float('inf') or E <= float('-inf'):
                raise ValueError('Activation Energy E is under/overflow')
            if T >= float('inf') or T <= float('-inf'):
                raise ValueError('Temperature T is under/overflow')
            if A <= 0:
                raise ValueError('The Arrhenius prefactor A is strictly positive')
            if T < 0:
                raise ValueError('Temperature in Kelvin scale should be positive')
            return A * np.exp(-E / (R * T))

        @classmethod
        def mod_arr(self, T, R=8.314, **kwargs):
            """Returns the modified Arrhenius reaction rate coeff

                        INPUTS
                        =======
                        kwargs
                        A: positive float, Arrhenius prefactor
                        b: real number, The modified Arrhenius parameter
                        E: float, activation energy for the reaction
                        
                        T: float, temperature in Kelvin scale
                        
                        RETURNS
                        ========
                        coeff: float, the Arrhenius reaction coeff
                        
                        EXAMPLES
                        =========
                        >>> ChemKin.reaction_coeff.mod_arr(10**2, A=10**7, b=0.5, E=10**3)
                        30035490.889639609
                        """
            A, E, b = kwargs['A'], kwargs['E'], kwargs['b']
            if type(A) is not int:
                if type(A) is not float:
                    raise TypeError('The Arrhenius prefactor A should be either int or float')
            if type(b) is not int:
                if type(b) is not float:
                    raise TypeError('The modified Arrhenius parameter b should be either int or float')
            if type(E) is not int:
                if type(E) is not float:
                    raise TypeError('Activation Energy E should be either int or float')
            if type(T) is not int:
                if type(T) is not float:
                    raise TypeError('Temperature (in Kelvin scale) T should be either int or float')
            if A >= float('inf') or A <= float('-inf'):
                raise ValueError('The Arrhenius prefactor A is under/overflow')
            if b >= float('inf') or b <= float('-inf'):
                raise ValueError('The modified Arrhenius parameter b is under/overflow')
            if E >= float('inf') or E <= float('-inf'):
                raise ValueError('Activation Energy E is under/overflow')
            if T >= float('inf') or T <= float('-inf'):
                raise ValueError('Temperature T is under/overflow')
            if A <= 0:
                raise ValueError('The Arrhenius prefactor A is strictly positive')
            if T < 0:
                raise ValueError('Temperature in Kelvin scale should be positive')
            return A * T ** b * np.exp(-E / (R * T))

    @classmethod
    def reaction_rate(self, v1, v2, x, k):
        """Returns the reaction rate for a system
                INPUTS
                =======
                v1: float vector
                v2: float vector
                x: float vector, species concentrations
                k: float/int list, reaction coeffs

                RETURNS
                ========
                reaction rates: 1x3 float array, the reaction rate for each specie

                EXAMPLES
                =========
                >>> ChemKin.reaction_rate([[1,0],[2,0],[0,2]], [[0,1],[0,2],[1,0]], [1,2,1], [10,10])
                array([-30, -60,  20])
                """
        try:
            x = np.array(x)
            v1 = np.array(v1).T
            v2 = np.array(v2).T
        except TypeError as err:
            raise TypeError('x and v should be either int or float vectors')

        if type(k) == tuple:
            coeffs, bw_coeffs, reversibles = k
            if np.any(coeffs < 0) or np.any(bw_coeffs < 0):
                raise ValueError("reaction constant can't be negative")
        else:
            coeffs = np.array(k)
        if np.any(coeffs < 0):
            raise ValueError("reaction constant can't be negative")
        else:
            fw_ws = coeffs * np.prod((x ** v1), axis=1)
            fw_rrs = np.sum(((v2 - v1) * np.array([fw_ws]).T), axis=0)
            if type(k) == tuple:
                if np.all(np.array(reversibles) == 1):
                    bw_ws = (bw_coeffs * np.prod((x ** v2), axis=1)).flatten()
                    bw_rrs = fw_rrs - np.sum(((v2 - v1) * np.array([bw_ws]).T), axis=0)
                    return bw_rrs
                else:
                    ws = []
                    for i, reversible in enumerate(reversibles):
                        if reversible:
                            ws += [bw_coeffs.flatten()[i] * np.prod(x ** v2[i])]
                        else:
                            ws += [coeffs[i] * np.prod(x ** v1[i])]

                    return np.sum(((v2 - v1) * np.array([ws]).T), axis=0)
            else:
                return fw_rrs


class Reaction:

    def __init__(self, parser, T):
        self.species = parser.get_species()
        self.reactions = parser.parse_reactions()
        self.V1, self.V2 = self.reaction_components()
        self.p0 = 100000.0
        self.R = 8.314
        if type(T) is not int:
            if type(T) is not float:
                raise TypeError('Temperature (in Kelvin scale) should be either int or float')
        else:
            if T < 0:
                raise ValueError('Temperature T should be postiive')
            else:
                if T >= float('inf') or T <= float('-inf'):
                    raise ValueError('Temperature T is under/overflow')
                else:
                    self.T = T
        self.gamma = np.sum((self.V2 - self.V1), axis=0)
        self.get_nasa_coeffs()

    def __repr__(self):
        reaction_str = ''
        for rid, reaction in self.reactions.items():
            reaction_str += rid + '\n' + str(reaction) + '\n'

        return 'Reactions:\n---------------\n' + reaction_str

    def __len__(self):
        return len(self.reactions)

    def get_nasa_coeffs(self):
        """ Return the NASA polynomial coeffs for each species
                INPUTS
                =======
                self

                RETURNS
                ========
                nasa_coeffs: a list, where nasa_coeffs[i] is the NASA coeffs for the ith species"""
        self.nasa_coeffs = np.zeros((len(self.species), 7))
        for i, specie in enumerate(self.species):
            self.nasa_coeffs[i] = getNASACoeff(specie, self.T)

    def H_over_RT(self):
        """ Return H over RT, Enthalpy
                INPUTS
                =======
                self

                RETURNS
                ========
                H_RT: a list, where H_RT[i] is the enthalpy for the ith species"""
        a = self.nasa_coeffs
        H_RT = a[:, 0] + a[:, 1] * self.T / 2.0 + a[:, 2] * self.T ** 2.0 / 3.0 + a[:, 3] * self.T ** 3.0 / 4.0 + a[:, 4] * self.T ** 4.0 / 5.0 + a[:, 5] / self.T
        return H_RT

    def S_over_R(self):
        """ Return S over R, Entropy
                INPUTS
                =======
                self

                RETURNS
                ========
                S_R: a list, where S_R[i] is the entropy for the ith species"""
        a = self.nasa_coeffs
        S_R = a[:, 0] * np.log(self.T) + a[:, 1] * self.T + a[:, 2] * self.T ** 2.0 / 2.0 + a[:, 3] * self.T ** 3.0 / 3.0 + a[:, 4] * self.T ** 4.0 / 4.0 + a[:, 6]
        return S_R

    def backward_coeffs(self, kf):
        """ Return backward reation coeffs for each reactions
                INPUTS
                =======
                kf: the forward reaction coeffs

                RETURNS
                ========
                coeffs: a list, where coeffs[i] is the reaction coeffs for the i_th reaction"""
        h_over_rt = self.H_over_RT()
        s_over_r = self.S_over_R()
        delta_H_over_RT = np.matmul(h_over_rt.reshape(1, len(h_over_rt)), self.V2 - self.V1)
        delta_S_over_R = np.matmul(s_over_r.reshape(1, len(s_over_r)), self.V2 - self.V1)
        delta_G_over_RT = delta_S_over_R - delta_H_over_RT
        fact = self.p0 / self.R / self.T
        ke = fact ** self.gamma * np.exp(delta_G_over_RT)
        return kf / ke

    def reaction_components(self):
        """ Return the V1 and V2 of the reactions
                INPUTS
                =======
                self

                RETURNS
                ========
                V1: a numpy array, shows each specie's coeff in formula in the forward reaction
                V2: a numpy array, shows each specie's coeff in formula in the backward reaction
                """
        V1 = np.zeros((len(self.species), len(self.reactions)))
        V2 = np.zeros((len(self.species), len(self.reactions)))
        for i, (_, reaction) in enumerate(self.reactions.items()):
            V1[:, i] = [val for _, val in reaction['v1'].items()]
            V2[:, i] = [val for _, val in reaction['v2'].items()]

        return (V1, V2)

    def reaction_coeff_params(self):
        """ Return reation coeffs for each reactions
                INPUTS
                =======
                self

                RETURNS
                ========
                coeffs: a list, where coeffs[i] is the reaction coefficient for the i_th reaction
                """
        coeffs = []
        reversibles = []
        for _, reaction in self.reactions.items():
            if 'K' in reaction['coeff_params']:
                coeffs.append(ChemKin.reaction_coeff.constant(reaction['coeff_params']['K']))
            else:
                if 'b' in reaction['coeff_params']:
                    coeffs.append(ChemKin.reaction_coeff.mod_arr((self.T), A=(reaction['coeff_params']['A']), b=(reaction['coeff_params']['b']),
                      E=(reaction['coeff_params']['E'])))
                else:
                    coeffs.append(ChemKin.reaction_coeff.arr((self.T), A=(reaction['coeff_params']['A']), E=(reaction['coeff_params']['E'])))
            reversibles += [reaction['reversible']]

        if np.sum(reversibles) == 0:
            return np.array(coeffs)
        else:
            return (
             np.array(coeffs), self.backward_coeffs(coeffs), reversibles)


def compute(path, T, X):
    try:
        reactions = Reaction(ReactionParser(path), T)
        V1, V2 = reactions.reaction_components()
        k = reactions.reaction_coeff_params()
        rr = ChemKin.reaction_rate(V1, V2, X, k)
    except:
        raise Exception('Something went wrong while calculating the reaction rate')

    filename = path.split('/')[(-1)]
    his(filename, reactions, T, X, rr).write()
    return rr


if __name__ == '__main__':
    T = 750
    X1 = [2, 1, 0.5, 1, 1, 0.5, 0.5, 0.5]
    X2 = [2, 1, 0.5, 1, 1]
    compute('test/xml/xml_homework.xml', T, X2)
    compute('test/xml/rxns_reversible.xml', 2000, X1)
    compute('test/xml/xml_reversible_and_irreversible.xml', 1500, X2)