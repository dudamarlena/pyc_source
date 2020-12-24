# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: extensions/newresinter.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    Resinter extension\n\n    Print interaction energy between each residue pair in the protein. \n'
__date__ = '21 October 2011'
__authors__ = 'Kyle Monson and Emile Hogan'
import extensions
from src.hydrogens import Optimize
from itertools import product, permutations, izip, count
from src.hydrogens import hydrogenRoutines
_titrationSets = (
 (('AR0',), 'ARG'),
 (('ASH',), 'ASP'),
 (('CYX',), 'CYS'),
 (('GLU',), 'GLH'),
 (('HSD', 'HSE'), 'HSP'),
 (('HID', 'HIE'), 'HIP'),
 (('LYN',), 'LYS'),
 (('TYM',), 'TYR'),
 (('CTERM',), 'NEUTRAL-CTERM'),
 (('NEUTRAL-NTERM',), 'NTERM'))
_titrationSetsMap = {}
for tsSet in _titrationSets:
    for ts in tsSet[0]:
        _titrationSetsMap[ts] = tsSet

    _titrationSetsMap[tsSet[1]] = tsSet

_titrationSetsMap['HIS'] = _titrationSetsMap['HSD']
_titrationSetsMap['CYM'] = _titrationSetsMap['CYS']

def usage():
    """
    Returns usage text for newresinter.
    """
    txt = 'Print interaction energy between each residue pair in the protein to {output-path}.newresinter.'
    return txt


def run_extension(routines, outroot, options):
    outname = outroot + '.newresinter'
    with open(outname, 'w') as (outfile):
        processor = ResInter(routines, outfile, options)
        processor.generate_all()
        processor.write_resinter_output()


class ResInter(object):

    def __init__(self, routines, outfile, options):
        self.pairEnergyResults = {}
        self.combinationCount = 0
        self.totalCombinations = 0
        self.options = options
        self.output = extensions.extOutputHelper(routines, outfile)
        self.routines = routines

    def save_interation_energy(self, first, second):
        energy = get_residue_interaction_energy(first, second)
        pairText = str(first) + ' ' + str(second)
        if pairText in self.pairEnergyResults:
            txt = '#%s re-tested!!! LOLWAT?\n' % pairText
            self.output.write(txt)
        else:
            self.pairEnergyResults[pairText] = energy

    def save_all_residue_interaction_energies(self):
        """
        Writes out the residue interaction energy for each possible
        residue pair in the protein.
        """
        residuepairs = permutations(self.routines.protein.getResidues(), 2)
        for pair in residuepairs:
            self.save_interation_energy(pair[0], pair[1])

    def save_one_with_all_interaction_energies(self, i):
        """
        Writes out the residue interaction energy for each possible
        residue pair in the protein.
        """
        residues = list(self.routines.protein.getResidues())
        target = residues[i]
        del residues[i]
        for residue in residues:
            self.save_interation_energy(target, residue)
            self.save_interation_energy(residue, target)

    def save_pair_interaction_energies(self, i, j):
        """
        Writes out the residue interaction energy for each possible
        residue pair in the protein.
        """
        residues = list(self.routines.protein.getResidues())
        self.save_interation_energy(residues[i], residues[j])
        self.save_interation_energy(residues[j], residues[i])

    def create_all_protonated(self):
        residueSet = get_residue_titration_set_protonated(self.routines.protein.getResidues())
        self.process_residue_set(residueSet, clean=self.options.clean, neutraln=self.options.neutraln, neutralc=self.options.neutralc, ligand=self.options.ligand, assign_only=self.options.assign_only, chain=self.options.chain, debump=self.options.debump, opt=self.options.opt)
        self.save_all_residue_interaction_energies()

    def create_all_single_unprotonated(self):
        combinations = residue_set_single_unprotonated_combinations(self.routines.protein.getResidues())
        for residueSet, i in combinations:
            self.process_residue_set(residueSet, clean=self.options.clean, neutraln=self.options.neutraln, neutralc=self.options.neutralc, ligand=self.options.ligand, assign_only=self.options.assign_only, chain=self.options.chain, debump=self.options.debump, opt=self.options.opt)
            self.save_one_with_all_interaction_energies(i)

    def create_all_pair_unprotonated(self):
        combinations = residue_set_pair_unprotonated_combinations(self.routines.protein.getResidues())
        for residueSet, i, j in combinations:
            self.process_residue_set(residueSet, clean=self.options.clean, neutraln=self.options.neutraln, neutralc=self.options.neutralc, ligand=self.options.ligand, assign_only=self.options.assign_only, chain=self.options.chain, debump=self.options.debump, opt=self.options.opt)
            self.save_pair_interaction_energies(i, j)

    def count_combinations(self):
        n = 0
        k = 0
        allProtonated = get_residue_titration_set_protonated(self.routines.protein.getResidues())
        for name in allProtonated:
            if name in _titrationSetsMap:
                n += 1
                if len(_titrationSetsMap[name][0]) == 2:
                    k += 1

        self.totalCombinations = ((n + k) ** 2 + (n - k) + 2) / 2

    def generate_all(self):
        """
        For every titration state combination of residue output the 
        interaction energy for all possible residue pairs. 
        """
        self.routines.write('Printing residue interaction energies...\n')
        self.count_combinations()
        self.create_all_protonated()
        self.create_all_single_unprotonated()
        self.create_all_pair_unprotonated()

    def write_resinter_output(self):
        """
        Output the interaction energy between each possible residue pair.
        """
        for resultKey in sorted(self.pairEnergyResults.iterkeys()):
            self.output.write(resultKey + ' ' + str(self.pairEnergyResults[resultKey]) + '\n')

        self.routines.write(str(self.combinationCount) + ' residue combinations tried\n')

    def process_residue_set(self, residueSet, clean=False, neutraln=False, neutralc=False, ligand=None, assign_only=False, chain=False, debump=True, opt=True):
        self.combinationCount += 1
        txt = ('Running combination {0} of {1}\n').format(self.combinationCount, self.totalCombinations)
        self.routines.write(txt)
        self.routines.write(str(residueSet) + '\n')
        self.routines.removeHydrogens()
        for newResidueName, oldResidue, index in izip(residueSet, self.routines.protein.getResidues(), count()):
            if newResidueName is None:
                continue
            chain = self.routines.protein.chainmap[oldResidue.chainID]
            chainIndex = chain.residues.index(oldResidue)
            residueAtoms = oldResidue.atoms
            newResidue = self.routines.protein.createResidue(residueAtoms, newResidueName)
            newResidue.renameResidue(newResidueName)
            self.routines.protein.residues[index] = newResidue
            chain.residues[chainIndex] = newResidue

        self.routines.setTermini(neutraln, neutralc)
        self.routines.updateBonds()
        if not clean and not assign_only:
            self.routines.updateSSbridges()
            if debump:
                self.routines.debumpProtein()
            self.routines.addHydrogens()
            hydRoutines = hydrogenRoutines(self.routines)
            if debump:
                self.routines.debumpProtein()
            if opt:
                hydRoutines.setOptimizeableHydrogens()
                hydRoutines.initializeFullOptimization()
                hydRoutines.optimizeHydrogens()
            else:
                hydRoutines.initializeWaterOptimization()
                hydRoutines.optimizeHydrogens()
            hydRoutines.cleanup()
        return


def get_residue_titration_set_protonated(residues):
    """
    Returns residue set when everything is protonated.
    """
    result = []
    for residue in residues:
        residueTest = _titrationSetsMap.get(residue.name)
        if residueTest:
            residueTest = residueTest[1]
        else:
            residueTest = residue.name
        result.append(residueTest)

    return result


def residue_set_single_unprotonated_combinations(residues):
    """
    Yields pair (residue set, residue index) for 
    every "single unprotonated" combination.
    residue set - set for process_residue_set
    residue index - index of residue that was left unprotonated
    """
    protonatedNames = get_residue_titration_set_protonated(residues)
    for name, i in izip(protonatedNames, count()):
        if name not in _titrationSetsMap:
            continue
        tStateSet = _titrationSetsMap[name][0]
        for tState in tStateSet:
            result = list(protonatedNames)
            result[i] = tState
            yield (result, i)


def residue_set_pair_unprotonated_combinations(residues):
    """
    Yields pair (residue set, 1rst residue index, 2nd residue index) for 
    every "single unprotonated" combination.
    residue set - set for process_residue_set
    1rst residue index - index of 1rst residue that was left unprotonated
    2nd residue index - index of 2nd residue that was left unprotonated
    """
    protonatedNames = get_residue_titration_set_protonated(residues)
    for i in xrange(0, len(protonatedNames)):
        firstName = protonatedNames[i]
        if firstName not in _titrationSetsMap:
            continue
        firstStateSet = _titrationSetsMap[firstName][0]
        for j in xrange(0, i):
            secondName = protonatedNames[j]
            if secondName not in _titrationSetsMap:
                continue
            secondStateSet = _titrationSetsMap[secondName][0]
            for firstState in firstStateSet:
                for secondState in secondStateSet:
                    result = list(protonatedNames)
                    result[i] = firstState
                    result[j] = secondState
                    yield (result, i, j)


def get_residue_interaction_energy(residue1, residue2):
    """
    Returns to total energy of every atom pair between the two residues.
    
    Uses Optimize.getPairEnergy and it's donor/accepter model 
    to determine energy.
    
    residue1 - "donor" residue
    residue2 - "acceptor" residue
    
    THE RESULTS OF THIS FUNCTION ARE NOT SYMMETRIC. Swapping 
    residue1 and residue2 will not always produce the same result.
    """
    energy = 0.0
    for pair in product(residue1.getAtoms(), residue2.getAtoms()):
        energy += Optimize.getPairEnergy(pair[0], pair[1])

    return energy