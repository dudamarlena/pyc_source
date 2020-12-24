# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/maegen/core/maegen.py
# Compiled at: 2011-11-21 11:50:14
"""
Created on Oct 14, 2011

@author: maemo
"""
from exceptions import *
from gedcom import *
import logging, pickle, os, os.path
from ..common import version
version.getInstance().submitRevision('$Revision: 72 $')

def get_maegen_storage_dir():
    """
    Compute the application storage dir.
    This is an utility function to retrieve the directory where maegen can
    store any file like settings or cached data.
    """
    storage = os.path.expanduser('~')
    storage = os.path.join(storage, '.maegen')
    return storage


class Maegen(object):
    """
    Main class of the Program. The GUI use this class like a Facade to any core functions.
    """

    def __init__(self):
        self._ensure_maegen_conf_store()
        settings = None
        self.database = None
        self.load_settings()
        self.apply_settings()
        return

    def get_maegen_settings_file(self):
        storage = get_maegen_storage_dir()
        storage = os.path.join(storage, 'settings.pickle')
        return storage

    def load_settings(self):
        """
        load the saved settings
        """
        self._ensure_maegen_conf_store()
        storage = self.get_maegen_settings_file()
        try:
            file = open(storage, 'rb')
            self.settings = pickle.load(file)
            file.close()
        except IOError, EOFError:
            logging.warning('failed to load the settings')
            self.settings = Settings()

    def save_settings(self):
        """
        save the current settings
        """
        self._ensure_maegen_conf_store()
        storage = self.get_maegen_settings_file()
        try:
            file = open(storage, 'wb')
            pickle.dump(self.settings, file)
            file.close()
        except IOError:
            logging.warning('failed to save the settings')

    def apply_settings(self):
        pass

    def _ensure_maegen_conf_store(self):
        storage = get_maegen_storage_dir()
        if os.path.exists(storage):
            pass
        else:
            os.makedirs(storage)

    def _save_database(self, filename):
        """
        Save the current database into a file
        """
        storage = filename
        try:
            file = open(storage, 'wb')
            pickle.dump(self.database, file)
            file.close()
        except IOError:
            logging.error('failed to save the database')
            raise

    def _load_database(self, filename):
        """
        Read a database from a file. The new database become the current database. 
        """
        storage = filename
        try:
            file = open(storage, 'rb')
            self.database = pickle.load(file)
            file.close()
        except IOError, EOFError:
            logging.error('failed to load the database')
            raise

    def export_to_gedcom(self, filepath=None):
        """
        Return the gedcom for current database
        Parameter:
          - filepath the file were the gedcom is written if supplied
        """
        gedcom_str = GedcomWriter(self.database).export()
        if filepath:
            f = open(filepath, 'w')
            try:
                f.write(gedcom_str)
            finally:
                f.close()

        return gedcom_str

    def get_families_for_parents(self, father, mother):
        """
        Return all family for given father and mother
        """
        return filter(lambda fam: fam.husband == father and fam.wife == mother, self.database.families)

    def get_families_for(self, individual):
        """
        Return all family where the given individual is a parent.
        """

        def is_parent_in(individual):
            return lambda fam: individual in [fam.husband, fam.wife]

        return filter(is_parent_in(individual), self.database.families)

    def get_family_with_child(self, individual):
        """
       Return family where given individual is child.
       Raise MaegenIntegrityException if more than one family are candidate
       """
        result = filter(lambda x: individual in x.children, self.database.families)
        if len(result) > 1:
            raise MaegenIntegrityException('individual ' + individual + ' is child of more than one family')
        elif len(result) == 1:
            return result[0]
        else:
            return
        return

    def individuals_count(self):
        """
        Return the number of individual in the current database
        """
        return len(self.database.individuals)

    def families_count(self):
        """
        Return the number of families in the current database
        """
        return len(self.database.families)

    def branches_count(self):
        """
        Return the count of branches (tree with ancestor as root) in the database
        """
        indi_without_parents = filter(lambda x: x.father is None and x.mother is None, self.database.individuals)
        return len(indi_without_parents)

    def names_count(self):
        """
        return the count of patronymic name in the database
        """
        return len(set(map(lambda indi: indi.name.upper(), self.database.individuals)))

    def children_count(self, individual):
        """
        Return the number of children for a given individual.
        Every family where the individual is a spouse are candidate to children count.
        """
        result = 0
        for family in self.get_families_for(individual):
            result += family.children_count()

        return result

    def retrieve_children(self, individual):
        """
        Return children for a given individual.
        Every family where the individual is a spouse are candidate to provide children.
        """
        result = []
        for family in self.get_families_for(individual):
            result.extend(family.children)

        return result

    def create_new_individual(self, name='inconnu', firstname='inconnu'):
        """
        Create a new individual and add it to the database
        Return a new individual
        """
        resu = Individual()
        resu.name = name
        resu.firstname = firstname
        self.database.individuals.add(resu)
        return resu

    def create_new_family(self, husband, wife):
        """
        Create a new family
        """
        resu = Family()
        resu.husband = husband
        resu.wife = wife
        self.database.families.add(resu)
        return resu

    def make_child(self, individual, family):
        """
        Promote the given individual to child of given family 
        """
        family.children.append(individual)
        individual.father = family.husband
        individual.mother = family.wife

    def remove_father(self, individual):
        """
        remove the father of an individual.
        Return the removed father.
        """
        old = individual.father
        self.set_father(individual, None)
        return old

    def remove_mother(self, individual):
        """
        remove the mother of an individual.
        Return the removed mother.
        """
        old = individual.mother
        self.set_mother(individual, None)
        return old

    def remove_parents(self, individual):
        """
        Remove both fatehr and mother of a given individual while ensuring
        database correctness.
        """
        old_father = individual.father
        old_mother = individual.mother
        individual.father = None
        individual.mother = None
        if old_father or old_mother:
            family = self.get_family_with_child(individual)
            if family:
                if family.husband == old_father or family.wife == old_mother:
                    family.children.remove(individual)
        return

    def set_parents(self, individual, father, mother):
        """
        Make an individual children of a given father and mother.
        Parameter:
            - father : must not be None
            - mother : must not be None
        """
        old_father = individual.father
        old_mother = individual.mother
        individual.father = father
        individual.mother = mother
        if old_father or old_mother:
            family = self.get_family_with_child(individual)
            if family:
                if family.husband == old_father or family.wife == old_mother:
                    family.children.remove(individual)
        fam_list = self.get_families_for_parents(father, mother)
        if len(fam_list) == 1:
            fam = fam_list[0]
            self.make_child(individual, fam)
        else:
            new_family = self.create_new_family(father, mother)
            self.make_child(individual, new_family)

    def set_father(self, individual, father):
        """
        Give a father to an individual        
        """
        old = individual.father
        individual.father = father
        if old:
            family = self.get_family_with_child(individual)
            if family:
                if family.husband == old:
                    family.children.remove(individual)
        family = self.get_family_with_child(individual)
        if family:
            if family.husband == None:
                family.husband = father
            elif not family.husband == father:
                raise MaegenIntegrityException(str(individual) + ' is already child in a family with an husband, cannot change husband')
        elif father:
            new_family = self.create_new_family(father, None)
            self.make_child(individual, new_family)
        elif individual.mother:
            new_family = self.create_new_family(None, individual.mother)
            self.make_child(individual, new_family)
        return old

    def set_mother(self, individual, mother):
        """
        Give a mother to an individual        
        """
        old = individual.mother
        individual.mother = mother
        if old:
            family = self.get_family_with_child(individual)
            if family:
                if family.wife == old:
                    family.children.remove(individual)
        family = self.get_family_with_child(individual)
        if family:
            if family.wife == None:
                family.wife = mother
            elif not family.husband == mother:
                raise MaegenIntegrityException(str(individual) + ' is already child in a family with a wife, cannot change wife')
        elif mother:
            new_family = self.create_new_family(None, mother)
            self.make_child(individual, new_family)
        elif individual.father:
            new_family = self.create_new_family(individual.father, None)
            self.make_child(individual, new_family)
        return old

    def retrieve_all_individuals(self):
        """
        return all individuals in the database as a list
        """
        return list(self.database.individuals)

    def retrieve_all_families(self):
        """
        return all families in the database as a list
        """
        return list(self.database.families)

    def retrieve_all_names(self):
        """
        return all names in the database as a set        
        """
        return set(map(lambda indi: indi.name.upper(), self.database.individuals))

    def retrieve_individual_for_name(self, name, exact=False):
        """
        Return all individual with given name.
        Parameter
            - name : the name to search
            - exact : if True exact match. If False the name of the individual should only containt the parameter name. 
        """
        if exact:
            return filter(lambda indi: name == indi.name.upper(), self.database.individuals)
        else:
            pattern = name.upper()
            return filter(lambda indi: indi.name.upper().find(pattern) > -1, self.database.individuals)

    def retrieve_branches(self):
        """
        Return all individuals which are root of a branch e.g. which don't have parents.  
        """
        indi_without_parents = filter(lambda x: x.father is None and x.mother is None, self.database.individuals)
        return indi_without_parents

    def update_marriage_status(self, family, married, marriage_date, marriage_place, divorced, divorce_date):
        """
        Update information about  marriage status of the given family.
        Parameter:
            - divorced : requires married to be True
        """
        if married:
            family.update_marriage(marriage_date, marriage_place)
        else:
            family.delete_marriage()
        if divorced and married:
            family.update_divorce(divorce_date)
        else:
            family.delete_divorce()

    def update_children_list(self, family, children_list):
        """
        Update the family children list with the given children list.
        The method ensure correctness of the database
        """
        for child in family.children:
            if child not in children_list:
                self.remove_parents(child)

        for child in children_list:
            if child not in family.children:
                self.make_child(child, family)

    def get_maegen_storage_dir(self):
        """
        Storage location of megen database
        """
        return get_maegen_storage_dir()

    def load_database(self, database_file):
        """
        Read a database from a file
        """
        self._load_database(database_file)

    def save_database(self, database_file):
        """
        Write current database into a file
        """
        self._save_database(database_file)

    def create_new_database(self, database_file):
        """
        Create a new empty database
        """
        self.database = Database()
        self._save_database(database_file)


class Settings():
    """
    Represents the settings for Maegen
    """

    def __init__(self):
        self.edit_new_individual = False


class Database(object):
    """
    genealogical data consist in a set of individuals related by a set of families
    """

    def __init__(self):
        self.individuals = set([])
        self.families = set([])


class Individual(object):
    """
    A person
    """

    def __init__(self):
        self.name = ''
        self.firstname = ''
        self.nickname = ''
        self.gender = None
        self.birthDate = None
        self.birthPlace = ''
        self.deathDate = None
        self.deathPlace = ''
        self.note = ''
        self.father = None
        self.mother = None
        self.occupation = ''
        return

    def __str__(self, *args, **kwrgs):
        return self.firstname.capitalize() + ' ' + self.name.upper()


class Family(object):
    """
    A family
    """

    def __init__(self):
        self.husband = None
        self.wife = None
        self.married = False
        self.divorced = False
        self.divorced_date = None
        self.married_date = None
        self.married_place = ''
        self.children = []
        return

    def __str__(self, *args, **kwrgs):
        return str(self.husband) + ' with ' + str(self.wife)

    def update_marriage(self, marriage_date, marriage_place):
        self.married = True
        self.married_date = marriage_date
        self.married_place = marriage_place

    def delete_marriage(self):
        self.married = False
        self.married_date = None
        self.married_place = ''
        return

    def update_divorce(self, divorced_date):
        self.divorced = True
        self.divorced_date = divorced_date

    def delete_divorce(self):
        self.divorced = False
        self.divorced_date = None
        return

    def children_count(self):
        return len(self.children)