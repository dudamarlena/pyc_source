# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/pymatgen_doping.py
# Compiled at: 2019-04-30 02:12:29
# Size of source mod 2**32: 6702 bytes
from pymatgen import Structure, Molecule, PeriodicSite
import random

def count_sites(structure, species=None, labels=None):
    """
     Given structure object and either specie string or label string,  it counts and returns the 
     number of sites with that species or label (or  both) in the structure

     Args:
         - structure (Structure): pymatgen structure object
         - species   ({str}): site species to count
         - labels     ({str}): site labels to count

     Returns:
         - (int): number of sites occupied by species or label (or both) in structure
    """
    if labels:
        if species:
            return len([i for i, site in enumerate(structure) if site.label in labels if site.species_string in species])
        if species:
            if not labels:
                return len([i for i, site in enumerate(structure) if site.species_string in species])
    else:
        if labels:
            if not species:
                return len([i for i, site in enumerate(structure) if site.label in labels])
    raise ValueError('Need to supply either specie, or label to count_sites')


def index_sites(structure, species=None, labels=None):
    """
    Return a list of the site indices in a structure that are occupied by specie or label (or both)

     Args:
         - structure (Structure): pymatgen structure object
         - species   ({str}): site species to count
         - label     ({str}): site label to count

     Returns:
         - ([int]): list with site indices occupied by species or label (or both) in structure

    """
    if labels:
        if species:
            return [i for i, site in enumerate(structure) if site.label in labels if site.species_string in species]
        if species:
            if not labels:
                return [i for i, site in enumerate(structure) if site.species_string in species]
    else:
        if labels:
            if not species:
                return [i for i, site in enumerate(structure) if site.label in labels]
    raise ValueError('Need to supply either specie, or label to index_sites')


def sort_structure(structure, order):
    """ 
    Given a pymatgen structure object sort the species so that their indices
    sit side by side in the structure, in given order - allows for POSCAR file to 
    be written in a readable way after doping

    Args:
       - structure (Structure): pymatgen structure object
       - order ([str,str..]): list of species str in order to sort

    Returns:
       - structure (Structure): ordered pymatgen Structure object
    """
    symbols = [species for species in structure.symbol_set]
    if 'X' in set(symbols):
        symbols.remove('X')
        symbols.append('X0+')
    else:
        if set(symbols) == set(order):
            structure_sorted = Structure(lattice=(structure.lattice), species=[], coords=[])
            for symbol in symbols:
                for i, site in enumerate(structure.sites):
                    if site.species_string == symbol:
                        structure_sorted.append(symbol,
                          (site.coords),
                          coords_are_cartesian=True,
                          properties=(site.properties))

        else:
            error_msg = 'Error: sort structure elements in list passed in order does not match that found in POSCAR\n'
            error_msg += 'Passed: {}\n'.format(order)
            error_msg += 'POSCAR: {}\n'.format(symbols)
            raise ValueError(error_msg)
    return structure_sorted


def dope_structure(structure, conc, species_to_rem, species_to_insert, label_to_remove=None):
    """
    Dope a pymatgen structure object to a particular concentration (within the bounds of integer sites).
    Removes conc * no(species_to_remove) from structure and inserts species to insert in 
    their place. Does so at random (excepting when label_to_remove is passed)

    Args:
       - structure (Structure): pymatgen structure object
       - conc (real): fractional % of sites to remove
       - species_to_rem (str): the species to remove from structure
       - species_to_insert ([str,str]): a list of species to equally distribute over sites that are removed
       - label_to_remove (str): label of sites to select for removal.

    """
    if {
     species_to_rem}.issubset(structure.symbol_set):
        no_sites = count_sites(structure,
          species=species_to_rem, labels=label_to_remove)
        site_indices = index_sites(structure,
          species=species_to_rem, labels=label_to_remove)
        no_dopants = int(round(conc * no_sites) / len(species_to_insert))
        random.shuffle(site_indices)
        for species in species_to_insert:
            for dopant in range(no_dopants):
                structure[site_indices.pop()] = species

        structure = sort_structure(structure=structure,
          order=[species for species in structure.symbol_set])
        return structure
    raise ValueError('dope_structure: species_to_rem is not in structure')


def dope_structure_by_no(structure, no_dopants, species_to_rem, species_to_insert, label_to_remove=None):
    """
    Dope a pymatgen structure object by swapping 'no_dopants' of 'species_to_rem' from the original structure.
    Removes no_dopants(species_to_remove) from structure and inserts species to insert in 
    their place. Does so at random (excepting when label_to_remove is passed)

    Args:
       - structure (Structure): pymatgen structure object
       - no_dopants (int): no of each type of dopant to insert
       - species_to_remove (str): the species to remove from structure
       - species_to_insert ([str,str]): a list of species to equally distribute over sites that are removed
       - label_to_remove (str): label of sites to select for removal.

    """
    if {
     species_to_rem}.issubset(structure.symbol_set):
        no_sites = count_sites(structure,
          species=species_to_rem, labels=label_to_remove)
        site_indices = index_sites(structure,
          species=species_to_rem, labels=label_to_remove)
        random.shuffle(site_indices)
        for species in species_to_insert:
            for dopant in range(no_dopants):
                structure[site_indices.pop()] = species

        structure = sort_structure(structure=structure,
          order=[species for species in structure.symbol_set])
        return structure
    raise ValueError('dope_struture_by_no: species_to_rem is not in structure')