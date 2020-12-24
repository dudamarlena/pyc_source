# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/samplePairsGaussian/prob_calculator_multispecies.py
# Compiled at: 2019-07-01 17:03:31
# Size of source mod 2**32: 16950 bytes
from .prob_calculator import *

class ProbCalculatorMultiSpecies:
    __doc__ = 'Calculates distances and probabilities for a set of particles of multiple species by holding a set of ProbCalculator objects.\n\n    Attributes:\n    posns_dict ({str: np.array([float])}): dict of species to posns for each species.\n    dim (int): dimensionality of each point\n\n    std_dev (float): standard deviation\n    std_dev_clip_mult (float): multiplier for the standard deviation cutoff, else None\n\n    dists_species (np.array([int])): species for the distances squared\n    dists_idxs_first_particle (np.array([int])): idx of the first particle. Only unique combinations together with idxs 2\n    dists_idxs_second_particle (np.array([int])): idx of the second particle. Only unique combinations together with idxs 1\n    dists_squared (np.array(float)): distances squared between all particles\n    no_dists (int): # distances possible\n\n    probs_species (np.array([str])): species possible.\n    probs_idxs_first_particle (np.array([int])): idx of the first particle. Only unique combinations together with idxs_2.\n    probs_idxs_second_particle (np.array([int])): idx of the second particle. Only unique combinations together with idxs_1.\n    probs (np.array([float])): probs of each pair of particles.\n    no_idx_pairs_possible (int): # idx pairs possible\n    max_prob (float): the maximum probability value, useful for rejection sampling\n\n    Private attributes:\n    _logger (logger): logging\n    '

    def __init__(self, posns_dict, dim, std_dev, std_dev_clip_mult=3.0):
        """Constructor.

        Args:
        posns_dict ({str: np.array([float])}): dict of species to posns for each species.
        dim (int): dimensionality of each point
        std_dev (float): standard deviation
        std_dev_clip_mult (float): multiplier for the standard deviation cutoff, else None
        """
        self._logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.setLevel(logging.ERROR)
        self._posns_dict = posns_dict
        self._dim = dim
        self._std_dev = std_dev
        self._std_dev_clip_mult = std_dev_clip_mult
        self._n = {}
        for species, posns in self._posns_dict.items():
            self._n[species] = len(posns)

        self._reset()
        self._compute_probs()

    def set_logging_level(self, level):
        """Sets the logging level
        Args:
        level (logging): logging level
        """
        self._logger.setLevel(level)

    def _reset(self):
        """Reset structures
        """
        self._dists_species = np.array([]).astype(str)
        self._dists_idxs_first_particle = np.array([]).astype(int)
        self._dists_idxs_second_particle = np.array([]).astype(int)
        self._dists_squared = np.array([]).astype(float)
        self._no_dists = 0
        self._probs_species = np.array([]).astype(str)
        self._probs_idxs_first_particle = np.array([]).astype(int)
        self._probs_idxs_second_particle = np.array([]).astype(int)
        self._probs = np.array([]).astype(float)
        self._max_prob = None
        self._norm = None
        self._no_idx_pairs_possible = 0

    @property
    def posns_dict(self):
        return self._posns_dict

    @property
    def n(self):
        return self._n

    @property
    def dim(self):
        return self._dim

    @property
    def std_dev(self):
        return self._std_dev

    @property
    def std_dev_clip_mult(self):
        return self._std_dev_clip_mult

    @property
    def dists_species(self):
        return self._dists_species

    @property
    def dists_idxs_first_particle(self):
        return self._dists_idxs_first_particle

    @property
    def dists_idxs_second_particle(self):
        return self._dists_idxs_second_particle

    @property
    def dists_squared(self):
        return self._dists_squared

    @property
    def no_dists(self):
        return self._no_dists

    @property
    def probs_species(self):
        return self._probs_species

    @property
    def probs_idxs_first_particle(self):
        return self._probs_idxs_first_particle

    @property
    def probs_idxs_second_particle(self):
        return self._probs_idxs_second_particle

    @property
    def probs(self):
        return self._probs

    @property
    def max_prob(self):
        return self._max_prob

    @property
    def norm(self):
        return self._norm

    @property
    def no_idx_pairs_possible(self):
        return self._no_idx_pairs_possible

    def set_std_dev(self, std_dev, std_dev_clip_mult=3.0):
        """Set the std dev and clip multiplier, and recalculate the probabilities.

        Args:
        std_dev (float): standard deviation
        std_dev_clip_mult (float): multiplier for the standard deviation cutoff, else None
        """
        self._std_dev = std_dev
        self._std_dev_clip_mult = std_dev_clip_mult
        self._compute_probs_from_dists()

    def _compute_probs(self):
        """Compute un-normalized probabilities for drawing the first particle out of n possible particles.
        """
        self._reset()
        for species, posns in self._posns_dict.items():
            pc = ProbCalculator(posns=posns, dim=(self._dim), std_dev=(self._std_dev), std_dev_clip_mult=(self._std_dev_clip_mult))
            self._dists_squared = np.append(self._dists_squared, pc.dists_squared)
            self._dists_idxs_first_particle = np.append(self._dists_idxs_first_particle, pc.dists_idxs_first_particle)
            self._dists_idxs_second_particle = np.append(self._dists_idxs_second_particle, pc.dists_idxs_second_particle)
            self._dists_species = np.append(self._dists_species, np.full(pc.no_dists, species))

        self._no_dists = len(self._dists_squared)
        self._compute_probs_from_dists()

    def _compute_probs_from_dists(self):
        """Compute normalized probabilities given distances squared
        """
        two_var = 2.0 * pow(self._std_dev, 2)
        if self._std_dev_clip_mult != None:
            max_dist_squared = pow(self._std_dev_clip_mult * self._std_dev, 2)
            idxs_within = self._dists_squared < max_dist_squared
            self._probs_species = self._dists_species[idxs_within]
            self._probs_idxs_first_particle = self._dists_idxs_first_particle[idxs_within]
            self._probs_idxs_second_particle = self._dists_idxs_second_particle[idxs_within]
            dists_squared_filtered = self._dists_squared[idxs_within]
            self._probs = np.exp(-dists_squared_filtered / two_var) / pow(np.sqrt(np.pi * two_var), self._dim)
        else:
            self._probs_species = np.copy(self._dists_species)
            self._probs_idxs_first_particle = np.copy(self._dists_idxs_first_particle)
            self._probs_idxs_second_particle = np.copy(self._dists_idxs_second_particle)
            self._probs = np.exp(-self._dists_squared / two_var) / pow(np.sqrt(np.pi * two_var), self._dim)
        self._no_idx_pairs_possible = len(self._probs)
        self._norm = np.sum(self._probs)
        self._probs /= self._norm
        if self._no_idx_pairs_possible > 0:
            self._max_prob = max(self._probs)
        else:
            self._max_prob = None

    def add_particle(self, species, idx, posn):
        """Add a particle

        Args:
        species (str): species
        idx (int): position at which to insert the particle
        posn (np.array([float])): position in d dimensions
        """
        self._posns_dict[species] = np.insert((self._posns_dict[species]), idx, posn, axis=0)
        self._n[species] += 1
        probs_idxs_all = np.arange(self._no_idx_pairs_possible)
        probs_idxs_this_species = self._probs_species == species
        shift_1 = probs_idxs_all[np.logical_and(probs_idxs_this_species, self._probs_idxs_first_particle >= idx)]
        self._probs_idxs_first_particle[shift_1] += 1
        shift_2 = probs_idxs_all[np.logical_and(probs_idxs_this_species, self._probs_idxs_second_particle >= idx)]
        self._probs_idxs_second_particle[shift_2] += 1
        dists_idxs_all = np.arange(self._no_dists)
        dists_idxs_this_species = self._dists_species == species
        shift_1 = dists_idxs_all[np.logical_and(dists_idxs_this_species, self._dists_idxs_first_particle >= idx)]
        self._dists_idxs_first_particle[shift_1] += 1
        shift_2 = dists_idxs_all[np.logical_and(self._dists_idxs_second_particle >= idx, dists_idxs_this_species)]
        self._dists_idxs_second_particle[shift_2] += 1
        idxs_add_1 = np.full(self._n[species] - 1, idx)
        idxs_add_2 = np.delete(np.arange(self._n[species]), idx)
        species_add = np.full(self._n[species] - 1, species)
        dr = self._posns_dict[species][idxs_add_1] - self._posns_dict[species][idxs_add_2]
        dists_squared_add = np.sum((dr * dr), axis=1)
        self._dists_species = np.append(self._dists_species, species_add)
        self._dists_idxs_first_particle = np.append(self._dists_idxs_first_particle, idxs_add_1)
        self._dists_idxs_second_particle = np.append(self._dists_idxs_second_particle, idxs_add_2)
        self._dists_squared = np.append(self._dists_squared, dists_squared_add)
        self._no_dists += len(dists_squared_add)
        if self._std_dev_clip_mult != None:
            max_dist_squared = pow(self._std_dev_clip_mult * self._std_dev, 2)
            idxs_within = dists_squared_add < max_dist_squared
            idxs_add_1 = idxs_add_1[idxs_within]
            idxs_add_2 = idxs_add_2[idxs_within]
            species_add = species_add[idxs_within]
            dists_squared_add = dists_squared_add[idxs_within]
        else:
            two_var = 2.0 * pow(self._std_dev, 2)
            probs_add = np.exp(-dists_squared_add / two_var) / pow(np.sqrt(np.pi * two_var), self._dim)
            self._probs *= self._norm
            self._probs_species = np.append(self._probs_species, species_add)
            self._probs_idxs_first_particle = np.append(self._probs_idxs_first_particle, idxs_add_1)
            self._probs_idxs_second_particle = np.append(self._probs_idxs_second_particle, idxs_add_2)
            self._probs = np.append(self._probs, probs_add)
            self._norm += np.sum(probs_add)
            self._probs /= self._norm
            self._no_idx_pairs_possible += len(idxs_add_1)
            if self._no_idx_pairs_possible > 0:
                self._max_prob = max(self._probs)
            else:
                self._max_prob = None

    def remove_particle(self, species, idx):
        """Remove a particle

        Args:
        species (str): species
        idx (int): idx of the particle to remove
        """
        self._posns_dict[species] = np.delete((self._posns_dict[species]), idx, axis=0)
        self._n[species] -= 1
        probs_idxs_all = np.arange(self._no_idx_pairs_possible)
        probs_idxs_this_species = self._probs_species == species
        probs_idxs_delete_1 = probs_idxs_all[np.logical_and(probs_idxs_this_species, self._probs_idxs_first_particle == idx)]
        probs_idxs_delete_2 = probs_idxs_all[np.logical_and(probs_idxs_this_species, self._probs_idxs_second_particle == idx)]
        probs_idxs_delete = np.append(probs_idxs_delete_1, probs_idxs_delete_2)
        dists_idxs_all = np.arange(self._no_dists)
        dists_idxs_this_species = self._dists_species == species
        dists_idxs_delete_1 = dists_idxs_all[np.logical_and(dists_idxs_this_species, self._dists_idxs_first_particle == idx)]
        dists_idxs_delete_2 = dists_idxs_all[np.logical_and(dists_idxs_this_species, self._dists_idxs_second_particle == idx)]
        dists_idxs_delete = np.append(dists_idxs_delete_1, dists_idxs_delete_2)
        self._probs *= self._norm
        self._norm -= np.sum(self._probs[probs_idxs_delete])
        self._probs = np.delete(self._probs, probs_idxs_delete)
        self._probs_idxs_first_particle = np.delete(self._probs_idxs_first_particle, probs_idxs_delete)
        self._probs_idxs_second_particle = np.delete(self._probs_idxs_second_particle, probs_idxs_delete)
        self._probs_species = np.delete(self._probs_species, probs_idxs_delete)
        self._dists_squared = np.delete(self._dists_squared, dists_idxs_delete)
        self._dists_idxs_first_particle = np.delete(self._dists_idxs_first_particle, dists_idxs_delete)
        self._dists_idxs_second_particle = np.delete(self._dists_idxs_second_particle, dists_idxs_delete)
        self._dists_species = np.delete(self._dists_species, dists_idxs_delete)
        self._no_dists -= len(dists_idxs_delete)
        self._probs /= self._norm
        self._no_idx_pairs_possible -= len(probs_idxs_delete)
        if self._no_idx_pairs_possible > 0:
            self._max_prob = max(self._probs)
        else:
            self._max_prob = None
        probs_idxs_all = np.arange(self._no_idx_pairs_possible)
        probs_idxs_this_species = self._probs_species == species
        shift_1 = probs_idxs_all[np.logical_and(probs_idxs_this_species, self._probs_idxs_first_particle > idx)]
        self._probs_idxs_first_particle[shift_1] -= 1
        shift_2 = probs_idxs_all[np.logical_and(probs_idxs_this_species, self._probs_idxs_second_particle > idx)]
        self._probs_idxs_second_particle[shift_2] -= 1
        dists_idxs_all = np.arange(self._no_dists)
        dists_idxs_this_species = self._dists_species == species
        shift_1 = dists_idxs_all[np.logical_and(dists_idxs_this_species, self._dists_idxs_first_particle > idx)]
        self._dists_idxs_first_particle[shift_1] -= 1
        shift_2 = dists_idxs_all[np.logical_and(self._dists_idxs_second_particle > idx, dists_idxs_this_species)]
        self._dists_idxs_second_particle[shift_2] -= 1

    def move_particle(self, species, idx, new_posn):
        """Move a particle

        Args:
        idx (int): idx of the particle to move
        new_posn (np.array([float])): new position in d dimensions
        """
        self.remove_particle(species, idx)
        self.add_particle(species, idx, new_posn)

    def compute_gaussian_sum_between_particle_and_existing(self, species, posn, excluding_idxs=[]):
        """Compute normalization = sum_{j} exp( -(xi-xj)^2 / 2*sigma^2 ) for a given particle xi and all other existing particles, possibly excluding some idxs

        Args:
        species (str): the species
        posn (np.array([float])): position of the particle
        excluding_idxs ([int]): list of particle idxs in [0,n) to exclude
        """
        if self._n[species] == 0:
            return
        idxs = np.array(range(0, self._n[species]))
        if excluding_idxs != []:
            idxs = np.delete(idxs, excluding_idxs)
        posns = self._posns_dict[species][idxs]
        if len(posns) == 0:
            return
        dr = posns - posn
        dists_squared = np.sum((dr * dr), axis=1)
        if self._std_dev_clip_mult != None:
            max_dist_squared = pow(self._std_dev_clip_mult * self._std_dev, 2)
            stacked = np.array([idxs, dists_squared]).T
            idxs, dists_squared = stacked[(stacked[:, 1] < max_dist_squared)].T
        two_var = 2.0 * pow(self._std_dev, 2)
        gauss = np.exp(-dists_squared / two_var) / pow(np.sqrt(np.pi * two_var), self._dim)
        return np.sum(gauss)