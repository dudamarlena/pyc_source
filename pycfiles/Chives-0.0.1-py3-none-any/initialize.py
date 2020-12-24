# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chitwanabm\initialize.py
# Compiled at: 2013-02-20 13:25:43
__doc__ = '\nSets up a chitwanabm model run: Initializes neighborhood/household/person agents \nand land use using the original CVFS data.\n'
from __future__ import division
import os, sys, logging, pickle, shutil, tempfile, subprocess
from pkg_resources import resource_filename
import numpy as np
from pyabm.file_io import read_single_band_raster
from chitwanabm import rc_params
from chitwanabm.agents import World
logger = logging.getLogger(__name__)
rcParams = rc_params.get_params()

def main():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    log_console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%I:%M:%S%p')
    ch.setFormatter(log_console_formatter)
    logger.addHandler(ch)
    world = generate_world()
    if world == 1:
        logger.critical('Problem generating world')
        return 1


def read_CVFS_data(textfile, key_field):
    """
    Reads in CVFS data from a CSV file into a dictionary of dictionary objects, 
    where the first line of the file gives the column headings (used as keys 
    within the nested dictionary object). No conversion of the fields is done: 
    they are all stored as strings, EXCEPT for the key_field, which is 
    converted and stored as an int.
    """
    try:
        file = open(textfile, 'r')
        lines = file.readlines()
        file.close()
    except:
        logger.exception('Error reading %s' % textfile)
        return 1

    col_names = lines[0].split(',')
    for n in xrange(len(col_names)):
        col_names[n] = col_names[n].strip('\n "')

    data = {}
    for line in lines[1:]:
        fields = line.split(',')
        for n in xrange(len(fields)):
            fields[n] = fields[n].strip('\n "')

        new_data = {}
        for field, column_name in zip(fields, col_names):
            new_data[column_name] = field

        data_key = int(new_data[key_field])
        if data_key in new_data:
            logger.critical('Error reading %s: key %s is already in use' % (textfile, data_key))
            return 1
        data[data_key] = new_data

    return data


def assemble_neighborhoods(neighborhoodsFile, neighborhoods_coords_file, model_world):
    """
    Reads in data from the CVFS (from dataset DS0014) on number of years 
    non-family services were available within a 30 min walk of each 
    neighborhood (SCHLFT, HLTHFT, BUSFT, MARFT, EMPFT) and on whether 
    neighborhood was electrified (ELEC).
    """
    neigh_datas = read_CVFS_data(neighborhoodsFile, 'NEIGHID')
    neigh_coords = read_CVFS_data(neighborhoods_coords_file, 'NEIGHID')
    neighborhoods = []
    for neigh_data in neigh_datas.itervalues():
        NEIGHID = int(neigh_data['NEIGHID'])
        neighborhood = model_world.new_neighborhood(NEIGHID, initial_agent=True)
        neighborhood._avg_yrs_services_lt15 = float(neigh_data['avg_yrs_services_lt15'])
        neighborhood._avg_yrs_services_lt30 = float(neigh_data['avg_yrs_services_lt30'])
        neighborhood._elec_available = bool(int(neigh_data['ELEC_AVAIL']))
        neighborhood._land_agveg = float(neigh_data['land.agveg'])
        neighborhood._land_nonagveg = float(neigh_data['land.nonagveg'])
        neighborhood._land_privbldg = float(neigh_data['land.privbldg'])
        neighborhood._land_pubbldg = float(neigh_data['land.pubbldg'])
        neighborhood._land_other = float(neigh_data['land.other'])
        neighborhood._land_total = neighborhood._land_agveg + neighborhood._land_nonagveg + neighborhood._land_privbldg + neighborhood._land_pubbldg + neighborhood._land_other
        neighborhood._forest_dist_BZ_km = float(neigh_data['BZ_meters']) / 1000.0
        neighborhood._forest_dist_CNP_km = float(neigh_data['CNP_meters']) / 1000.0
        neighborhood._forest_closest_km = float(neigh_data['closest_meters']) / 1000.0
        neighborhood._forest_closest_type = neigh_data['closest_type']
        neighborhood._school_min_ft = float(neigh_data['SCHLFT52'])
        neighborhood._health_min_ft = float(neigh_data['HLTHFT52'])
        neighborhood._bus_min_ft = float(neigh_data['BUSFT52'])
        neighborhood._market_min_ft = float(neigh_data['MARFT52'])
        neighborhood._employer_min_ft = float(neigh_data['EMPFT52'])
        neighborhood._x = float(neigh_coords[NEIGHID]['x'])
        neighborhood._y = float(neigh_coords[NEIGHID]['y'])
        neighborhood._distnara = float(neigh_data['dist_nara'])
        neighborhoods.append(neighborhood)

    return neighborhoods


def assemble_households(householdsFile, model_world):
    """
    Reads in data from the CVFS (from dataset DS0002) on several statistics for 
    each household (BAA43, BAA44, BAA10A, BAA18A).
    """
    household_datas = read_CVFS_data(householdsFile, 'HHID')
    model_start_time = rcParams['model.timebounds'][0]
    model_start_time = model_start_time[0] + model_start_time[1] / 12.0
    households = []
    HHID_NEIGHID_map = {}
    for household_data in household_datas.itervalues():
        HHID = int(household_data['HHID'])
        NEIGHID = int(household_data['NEIGHID'])
        HHID_NEIGHID_map[HHID] = NEIGHID
        household = model_world.new_household(HID=HHID, initial_agent=True)
        household._own_house_plot = bool(int(household_data['BAA43']))
        household._rented_out_land = int(household_data['BAA44'])
        if np.random.rand() < 0.4:
            household._lastmigrant_time = model_start_time + np.random.randint(-12, 0) / 12.0
        else:
            household._lastmigrant_time = -9999
        household._own_any_bari = bool(int(household_data['BAA10A']))
        household._own_any_khet = bool(int(household_data['BAA18A']))
        household._own_household_plot = bool(int(household_data['BAA43']))
        if household._own_any_bari or household._own_any_khet or household._own_household_plot:
            household._own_any_land = True
        else:
            household._own_any_land = False
        households.append(household)

    return (
     households, HHID_NEIGHID_map)


def assemble_persons(relationshipsFile, model_world):
    """
    Reads data in from the CVFS census (dataset DS0004 (restricted)) and from 
    the household relationship grid, CVFS DS0016 (restricted), which were 
    combined into one file, hhrel.csv, by the data_preprocess.R R script. This 
    function then assembles person agents from the data, including their 
    relationships (parent, child, etc.) with other agents.
    """
    relations = read_CVFS_data(relationshipsFile, 'RESPID')
    SUBJECT_RESPID_map = {}
    for relation in relations.itervalues():
        RESPID = int(relation['RESPID'])
        SUBJECT = int(relation['SUBJECT'])
        HHID = int(relation['HHID'])
        if HHID in SUBJECT_RESPID_map:
            SUBJECT_RESPID_map[HHID][SUBJECT] = RESPID
        else:
            SUBJECT_RESPID_map[HHID] = {}
            SUBJECT_RESPID_map[HHID][SUBJECT] = RESPID

    personsDict = {}
    RESPID_HHID_map = {}
    model_start_time = rcParams['model.timebounds'][0]
    model_start_time = model_start_time[0] + model_start_time[1] / 12.0
    extra_spouses = []
    for relation in relations.itervalues():
        RESPID = int(relation['RESPID'])
        HHID = int(relation['HHID'])
        RESPID_HHID_map[RESPID] = HHID
        try:
            AGEMNTHS = int(relation['AGEMNTHS'])
            CENGENDR = relation['CENGENDR']
            ETHNICITY = int(relation['ETHNIC'])
        except KeyError as ValueError:
            logger.warning('Person %s skipped because they are not in the census' % RESPID)
            continue

        mother_SUBJECT = int(relation['PARENT1'])
        father_SUBJECT = int(relation['PARENT2'])
        spouse_1_SUBJECT = int(relation['SPOUSE1'])
        spouse_2_SUBJECT = int(relation['SPOUSE2'])
        spouse_3_SUBJECT = int(relation['SPOUSE3'])
        if father_SUBJECT != 0:
            try:
                father_RESPID = SUBJECT_RESPID_map[HHID][father_SUBJECT]
            except KeyError:
                father_RESPID = None
                logger.warning('Father of person %s was excluded from the model - father field set to None' % RESPID)

        else:
            father_RESPID = None
        if mother_SUBJECT != 0:
            try:
                mother_RESPID = SUBJECT_RESPID_map[HHID][mother_SUBJECT]
            except KeyError:
                mother_RESPID = None
                logger.warning('Mother of person %s was excluded from the model - mother field set to None' % RESPID)

        else:
            mother_RESPID = None
        if spouse_1_SUBJECT != 0:
            try:
                spouse_RESPID = SUBJECT_RESPID_map[HHID][spouse_1_SUBJECT]
            except KeyError:
                spouse_RESPID = None
                logger.warning('Spouse of person %s was excluded from the model - spouse field set to None' % RESPID)

        else:
            spouse_RESPID = None
        if spouse_2_SUBJECT != 0:
            try:
                spouse_2_RESPID = SUBJECT_RESPID_map[HHID][spouse_2_SUBJECT]
                extra_spouses.append(spouse_2_RESPID)
            except KeyError:
                logger.warning('Spouse two of person %s was excluded from the model' % RESPID)

        if spouse_3_SUBJECT != 0:
            try:
                spouse_3_RESPID = SUBJECT_RESPID_map[HHID][spouse_3_SUBJECT]
                extra_spouses.append(spouse_3_RESPID)
            except KeyError:
                logger.warning('Spouse three of person %s was excluded from the model' % RESPID)

        if CENGENDR == '1':
            CENGENDR = 'male'
        elif CENGENDR == '2':
            CENGENDR = 'female'
        if ETHNICITY == 1:
            ETHNICITY = 'HighHindu'
        elif ETHNICITY == 2:
            ETHNICITY = 'HillTibeto'
        elif ETHNICITY == 3:
            ETHNICITY = 'LowHindu'
        elif ETHNICITY == 4:
            ETHNICITY = 'Newar'
        elif ETHNICITY == 5:
            ETHNICITY = 'TeraiTibeto'
        assert ETHNICITY != 6, "'Other' ethnicity should be dropped from the model"
        person = model_world.new_person(None, PID=RESPID, mother=mother_RESPID, father=father_RESPID, age=AGEMNTHS, sex=CENGENDR, initial_agent=True, ethnicity=ETHNICITY)
        person._spouse = spouse_RESPID
        person._des_num_children = int(relation['desnumchild'])
        person._schooling = int(relation['schooling'])
        person._child_school_lt_1hr_ft = int(relation['child_school_1hr'])
        person._child_health_lt_1hr_ft = int(relation['child_health_1hr'])
        person._child_bus_lt_1hr_ft = int(relation['child_bus_1hr'])
        person._child_employer_lt_1hr_ft = int(relation['child_emp_1hr'])
        person._child_market_lt_1hr_ft = int(relation['child_market_1hr'])
        person._parents_contracep_ever = bool(int(relation['parents_contracep_ever']))
        person._father_work = bool(int(relation['father_work']))
        person._father_years_schooling = int(relation['father_years_schooling'])
        person._mother_work = bool(int(relation['mother_work']))
        person._mother_years_schooling = int(relation['mother_years_schooling'])
        person._mother_num_children = int(relation['mother_num_children'])
        marr_time = relation['marr_date']
        if marr_time == 'NA':
            person._marriage_time = None
        else:
            person._marriage_time = float(marr_time)
        recent_birth = int(relation['recent_birth'])
        if recent_birth == 1:
            person._last_birth_time = model_start_time + np.random.randint(-12, 0) / 12.0
        else:
            person._last_birth_time = model_start_time + np.random.randint(-24, 0) / 12.0
        personsDict[RESPID] = person
        n_children = int(relation['n_children'])
        person._number_of_children = n_children

    for extra_spouse in extra_spouses:
        personsDict[extra_spouse]._spouse = None

    persons = []
    for person in personsDict.values():
        try:
            if person._mother != None:
                person._mother = personsDict[person._mother]
                if person._mother == person:
                    logger.warning("Person %s skipped because it is it's own mother" % person.get_ID())
                    continue
            if person._father != None:
                person._father = personsDict[person._father]
                if person._father == person:
                    logger.warning("Person %s skipped because it is it's own father" % person.get_ID())
                    continue
            if person._spouse != None:
                person._spouse = personsDict[person._spouse]
                if person._marriage_time == None:
                    if person._agemonths < person._spouse._agemonths:
                        youngests_age_mnths = person._agemonths
                    else:
                        youngests_age_mnths = person._spouse._agemonths
                    if youngests_age_mnths / 12.0 < 16:
                        marriage_time = model_start_time + np.random.randint(-12, 0) / 12.0
                    else:
                        if youngests_age_mnths / 12.0 < 27:
                            max_marr_age = youngests_age_mnths / 12.0
                        else:
                            max_marr_age = 27.0
                        marriage_age_mnths = np.random.randint(15, max_marr_age) * 12.0
                        marriage_time = model_start_time - (youngests_age_mnths - marriage_age_mnths) / 12.0
                    person._marriage_time = marriage_time
                    person._spouse._marriage_time = marriage_time
                if person._spouse == person:
                    logger.warning('Person %s skipped because it is married to itself' % person.get_ID())
                    continue
            persons.append(person)
        except KeyError:
            logger.warning('Person %s skipped due to mother/father/spouse KeyError' % person.get_ID())

    for person in persons:
        if person._father != None:
            person._father._children.append(person)
        if person._mother != None:
            person._mother._children.append(person)

    return (persons, RESPID_HHID_map)


def assemble_world(data_path):
    """
    Puts together a single world (with, currently, only a single region) from 
    the CVFS data using the above functions to input restricted CVFS data on 
    persons, households, and neighborhoods.
    """
    model_world = World()
    relationships_grid_file = os.path.join(data_path, 'hhrel.csv')
    households_file = os.path.join(data_path, 'hhag.csv')
    neighborhoods_file = os.path.join(data_path, 'neigh.csv')
    neighborhoods_coords_file = os.path.join(data_path, 'neigh_coords.csv')
    persons, RESPID_HHID_map = assemble_persons(relationships_grid_file, model_world)
    households, HHID_NEIGHID_map = assemble_households(households_file, model_world)
    neighborhoods = assemble_neighborhoods(neighborhoods_file, neighborhoods_coords_file, model_world)
    for neighborhood in neighborhoods:
        this_x = neighborhood._x
        this_y = neighborhood._y
        neighborhood._neighborhoods_by_distance = sorted(neighborhoods, key=lambda neighborhood: np.sqrt((neighborhood._x - this_x) ** 2 + (neighborhood._y - this_y) ** 2))
        neighborhood._neighborhoods_by_distance.pop(0)

    raw_data_path = rcParams['path.raw_input_data']
    DEM_file = os.path.join(raw_data_path, rcParams['DEM_file'])
    DEM, gt, prj = read_single_band_raster(DEM_file)
    model_world.set_DEM_data(DEM, gt, prj)
    world_mask_file = os.path.join(raw_data_path, rcParams['world_mask_file'])
    world_mask, gt, prj = read_single_band_raster(world_mask_file)
    model_world.set_world_mask_data(world_mask, gt, prj)
    region = model_world.new_region()
    for neighborhood in neighborhoods:
        region.add_agent(neighborhood)

    for household in households:
        HHID = household.get_ID()
        NEIGHID = HHID_NEIGHID_map[HHID]
        neighborhood = region.get_agent(NEIGHID)
        neighborhood.add_agent(household, initializing=True)

    for person in persons:
        RESPID = person.get_ID()
        HHID = RESPID_HHID_map[RESPID]
        try:
            NEIGHID = HHID_NEIGHID_map[HHID]
        except KeyError:
            logger.warning('Household %s skipped because it is not in DS0002' % HHID)
            continue

        neighborhood = region.get_agent(NEIGHID)
        household = neighborhood.get_agent(HHID)
        household.add_agent(person)

    for region in model_world.iter_regions():
        for neighborhood in region.iter_agents():
            for household in neighborhood.iter_agents():
                if household.num_members() == 0:
                    logger.warning('Household %s skipped because it has no members' % household.get_ID())
                    neighborhood.remove_agent(household)

    for region in model_world.iter_regions():
        for neighborhood in region.iter_agents():
            if neighborhood.num_members() == 0:
                logger.warning('Neighborhood %s skipped because it has no members' % neighborhood.get_ID())
                continue

    logger.info('World generated with %s persons, %s households, and %s neighborhoods' % (region.num_persons(), region.num_households(), region.num_neighborhoods()))
    return model_world


def save_world(world, filename):
    """Pickles a world for later reloading."""
    file = open(filename, 'w')
    pickle.dump(world, file)


def generate_world():
    """
    Performs the complete process necessary for initializing the model from    
    CVFS restricted data.

        1) Calls the necessary R script  (data_preprocess.R) for preparing the 
        necessary CSV initialization files from the CVFS data. 

        2) Calls the assemble_world function to prepare an instance of the 
        World class to be used in the model.

        3) Saves this World instance in the specified location. NOTE: This must 
        be an encrypted directory that is not publicly accessible to conform 
        to ICPSR and IRB requirements.
    """
    try:
        logger.info('Calling R to preprocess CVFS data')
        raw_data_path = rcParams['path.raw_input_data']
        Rscript_binary = rcParams['path.Rscript_binary']
        preprocess_script = resource_filename(__name__, 'R/data_preprocess.R')
        processed_data_path = tempfile.mkdtemp()
        subprocess.check_call([Rscript_binary, preprocess_script,
         raw_data_path, processed_data_path, str(rcParams['random_seed'])])
    except subprocess.CalledProcessError:
        logger.exception('Problem running data_preprocess.R.')
        return 1

    logger.info('Generating world from preprocessed CVFS data')
    model_world = assemble_world(processed_data_path)
    shutil.rmtree(processed_data_path)
    return model_world


if __name__ == '__main__':
    sys.exit(main())