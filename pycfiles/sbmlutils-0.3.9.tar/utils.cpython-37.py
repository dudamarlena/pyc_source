# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mkoenig/git/sbmlutils/sbmlutils/dfba/utils.py
# Compiled at: 2019-10-27 06:58:29
# Size of source mod 2**32: 4072 bytes
"""
DFBA utility and helper functions.
"""
import os, logging, libsbml
from sbmlutils import history
from sbmlutils import factory

def set_model_info(model, notes=None, creators=None, units=None, main_units=None):
    """ Adds the shared information to the models.

    :param model: SBMLModel instance
    :return:
    """
    if creators:
        history.set_model_history(model, creators=creators)
    if units:
        set_units(model, units=units)
    if main_units:
        set_main_units(model, main_units=main_units)
    if notes:
        set_notes(model, notes=notes)


def set_notes(model, notes):
    """ Set notes information on model.

    :param model: Model
    :param notes: notes information (xml string)
    :return: 
    """
    factory.set_notes(model, notes)


def set_units(model, units):
    """ Set units information on model.

    :param model: Model
    :param units: units info
    """
    factory.create_objects(model, units)


def set_main_units(model, main_units):
    """ Set main units information on model.

    :param model: Model
    :param main_units: units info
    """
    factory.set_model_units(model, main_units)


def find_exchange_reactions(model):
    """ Finds the exchange reaction in given FBA model.

    Currently the exchange rids are found via 
    prefix EX_.
    
    :param model: SBML model
    :returns dictonary of ex_rids: sids
    """
    ex_rids = {}
    for reactions in model.getListOfReactions():
        rid = reactions.getId()
        if rid.startswith('EX_'):
            r = model.getReaction(rid)
            sid = r.getReactant(0).getSpecies()
            ex_rids[rid] = sid

    return ex_rids


def clip_prefixes_in_model(model, prefix_species='M_', prefix_reaction='R_', prefix_gene='G_'):
    """ Removes the unnecessary BiGG prefixes.
    
    R_ for reactions, M_ for metabolites and G_ for genes.
    
    :param model: 
    :type model: 
    :return: 
    :rtype: 
    """
    rename_dict = {}

    def find_replace_ids(parent_object, f_list, prefix):
        for obj in getattr(parent_object, f_list).__call__():
            oid = obj.getId()
            oid_clipped = clip(oid, prefix)
            if oid != oid_clipped:
                rename_dict[oid] = oid_clipped
                obj.setId(oid_clipped)

    if model:
        find_replace_ids(model, 'getListOfSpecies', prefix=prefix_species)
        find_replace_ids(model, 'getListOfReactions', prefix=prefix_reaction)
    fbc_model = model.getPlugin('fbc')
    if fbc_model:
        find_replace_ids(fbc_model, 'getListOfGeneProducts', prefix=prefix_gene)
    elements = model.getListOfAllElements()
    rename_elements(elements, rename_dict)
    elements_plugins = model.getListOfAllElementsFromPlugins()
    rename_elements(elements_plugins, rename_dict)


def rename_elements(elements, rename_dict):
    """ Rename elements. """
    for k in range(elements.getSize()):
        e = elements.get(k)
        for id_old, id_new in rename_dict.items():
            e.renameSIdRefs(id_old, id_new)


def clip(string, prefix):
    """clips a prefix from the beginning of a string if it exists
    """
    if string.startswith(prefix):
        return string[len(prefix):]
    return string


def versioned_directory(output_dir, version):
    """ Creates a versioned directory.

    :param output_dir:
    :param version:
    :return:
    :rtype:
    """
    if output_dir is None:
        raise ValueError('directory must exist')
    else:
        if not os.path.exists(output_dir):
            logging.info('Create directory: {}'.format(output_dir))
            os.mkdir(output_dir)
        directory = os.path.join(output_dir, 'v{}'.format(version))
        os.path.exists(directory) or print('Create directory: {}'.format(directory))
        os.mkdir(directory)
    return directory