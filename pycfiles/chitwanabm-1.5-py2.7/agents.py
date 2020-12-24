# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chitwanabm\agents.py
# Compiled at: 2013-02-04 16:18:48
"""
Contains the classes for Person, Household, Neighborhood, and Region agents. 
Person agents are subclasses of the Agent class, while Household, Neighborhood, 
and Region agents are all subclasses of the Agent_set object.
"""
from __future__ import division
import os, csv, logging, numpy as np
from pyabm import IDGenerator, boolean_choice
from pyabm.statistics import draw_from_prob_dist
from pyabm.agents import Agent, Agent_set, Agent_Store
from chitwanabm import rc_params
from chitwanabm.statistics import calc_probability_death, calc_probability_migration_simple, calc_first_birth_time, calc_birth_interval, calc_hh_area, calc_des_num_children, calc_first_birth_prob_zvoleff, calc_migration_length, calc_education_level, calc_spouse_age_diff, choose_spouse, calc_num_inmigrant_households, calc_inmigrant_household_ethnicity, calc_inmigrant_household_size, calc_probability_HH_outmigration, calc_probability_divorce, calc_fuelwood_usage_probability
logger = logging.getLogger(__name__)
person_event_logger = logging.getLogger('person_events')
rcParams = rc_params.get_params()

def log_event_record(message, person, modeltime, **kwargs):
    extra = {'modeltime': modeltime, 'personinfo': (',').join(person.get_info())}
    person_event_logger.info(message, extra=extra, **kwargs)


if rcParams['submodel.parameterization.marriage'] == 'simple':
    from chitwanabm.statistics import calc_probability_marriage_simple as calc_probability_marriage
elif rcParams['submodel.parameterization.marriage'] == 'zvoleff':
    from chitwanabm.statistics import calc_probability_marriage_zvoleff as calc_probability_marriage
else:
    raise Exception("Unknown option for marriage parameterization: '%s'" % rcParams['submodel.parameterization.marriage'])
if rcParams['submodel.parameterization.migration'] == 'simple':
    from chitwanabm.statistics import calc_probability_migration_simple as calc_probability_migration
elif rcParams['submodel.parameterization.migration'] == 'zvoleff':
    from chitwanabm.statistics import calc_probability_migration_zvoleff as calc_probability_migration
else:
    raise Exception("Unknown option for migration parameterization: '%s'" % rcParams['submodel.parameterization.migration'])
if rcParams['submodel.parameterization.fuelwood_usage'] == 'simple':
    from chitwanabm.statistics import calc_daily_fuelwood_usage_simple as calc_daily_fuelwood_usage
elif rcParams['submodel.parameterization.fuelwood_usage'] == 'migrationfeedback':
    from chitwanabm.statistics import calc_daily_fuelwood_usage_migration_feedback as calc_daily_fuelwood_usage
else:
    raise Exception("Unknown option for fuelwood usage: '%s'" % rcParams['submodel.parameterization.fuelwood_usage'])

class Person(Agent):
    """Represents a single person agent"""

    def __init__(self, world, birthdate, ID=None, mother=None, father=None, age=None, sex=None, initial_agent=False, ethnicity=None, in_migrant=False):
        Agent.__init__(self, world, ID, initial_agent)
        self._birthdate = birthdate
        self._deathdate = None
        self._alive = True
        self._initial_agent = initial_agent
        self._in_migrant = in_migrant
        self._agemonths = age
        if father == None:
            self._father = None
        else:
            self._father = father
        if mother == None:
            self._mother = None
        else:
            self._mother = mother
        if sex == None:
            if boolean_choice():
                self._sex = 'female'
            else:
                self._sex = 'male'
        elif sex in ('male', 'female'):
            self._sex = sex
        else:
            raise ValueError('%s is not a valid gender' % sex)
        self._ethnicity = ethnicity
        self._des_num_children = None
        if self._sex == 'female':
            self._birth_interval = calc_birth_interval()
            self._last_birth_time = None
        self._first_birth_timing = calc_first_birth_time(self)
        self._spouse = None
        self._children = []
        self._number_of_children = 0
        self._marriage_time = None
        self._schooling = 0
        self._final_schooling_level = None
        if self._agemonths > 264:
            self._school_status = 'outofschool'
        else:
            self._school_status = 'undetermined'
        if self._sex == 'female':
            self._work = boolean_choice(0.205)
        else:
            self._work = boolean_choice(0.45)
        self._parents_contracep_ever = boolean_choice(0.53)
        if in_migrant:
            if self._agemonths / 12.0 > rcParams['education.start_school_age_years']:
                self._schooling = np.random.randint(1, 15)
                self._school_status == 'outofschool'
            self._mother_work = boolean_choice()
            self._father_work = boolean_choice()
            self._mother_years_schooling = np.random.randint(1, 15)
            self._father_years_schooling = np.random.randint(1, 15)
            self._mother_num_children = np.random.randint(1, 6)
            self._child_school_lt_1hr_ft = boolean_choice()
            self._child_health_lt_1hr_ft = boolean_choice()
            self._child_bus_lt_1hr_ft = boolean_choice()
            self._child_market_lt_1hr_ft = boolean_choice()
            self._child_employer_lt_1hr_ft = boolean_choice()
            if self._sex == 'female':
                self._des_num_children = calc_des_num_children()
        self._birth_household_ID = None
        self._birth_neighborhood_ID = None
        self._store_list = []
        self._last_migration = {'type': None, 'time': None, 'duration_months': None}
        self._away = False
        self._perm_away = False
        self._return_timestep = None
        self._ever_divorced = False
        self._ever_widowed = False
        self._last_divorce_check = -9999
        return

    def get_info(self):
        """Returns basic info about this person for use in logging."""
        if self._spouse != None:
            spouse = self._spouse.get_ID()
        else:
            spouse = None
        if self._mother != None:
            mother = self._mother.get_ID()
        else:
            mother = None
        if self._father != None:
            father = self._father.get_ID()
        else:
            father = None
        if self.is_away():
            household = self._last_household.get_ID()
            neighborhood = self._last_household.get_parent_agent().get_ID()
            region = self._last_household.get_parent_agent().get_parent_agent().get_ID()
        else:
            household = self.get_parent_agent().get_ID()
            neighborhood = self.get_parent_agent().get_parent_agent().get_ID()
            region = self.get_parent_agent().get_parent_agent().get_parent_agent().get_ID()
        return (str(self.get_ID()), str(household), str(neighborhood),
         str(region), str(self.get_sex()),
         str(self.get_age_years()), str(self.get_ethnicity()),
         str(mother), str(father), str(spouse),
         str(self._marriage_time), str(self._schooling),
         str(self._number_of_children),
         str(self._alive), str(self.is_away()),
         str(self.is_initial_agent()), str(self.is_in_migrant()),
         str(self.get_mother_num_children()),
         str(self.get_mother_years_schooling()),
         str(self.get_mother_work()),
         str(self.get_father_years_schooling()),
         str(self.get_father_work()),
         str(self._parents_contracep_ever))

    def get_mother(self):
        return self._mother

    def get_num_children(self):
        return self._number_of_children

    def get_father(self):
        return self._father

    def get_sex(self):
        return self._sex

    def get_age_months(self):
        return self._agemonths

    def get_age_years(self):
        return self._agemonths / 12.0

    def get_ethnicity(self):
        return self._ethnicity

    def get_spouse(self):
        return self._spouse

    def get_years_schooling(self):
        return self._schooling

    def get_work(self):
        return self._work

    def is_away(self):
        return self._away

    def is_in_school(self):
        if self._school_status == 'inschool':
            return True
        else:
            return False

    def get_mother_years_schooling(self):
        if self.is_initial_agent() or self.is_in_migrant():
            return self._mother_years_schooling
        else:
            return self.get_mother().get_years_schooling()

    def get_father_years_schooling(self):
        if self.is_initial_agent() or self.is_in_migrant():
            return self._father_years_schooling
        else:
            return self.get_father().get_years_schooling()

    def get_mother_work(self):
        if self.is_initial_agent() or self.is_in_migrant():
            return self._mother_work
        else:
            return self.get_mother().get_work()

    def get_father_work(self):
        if self.is_initial_agent() or self.is_in_migrant():
            return self._father_work
        else:
            return self.get_father().get_work()

    def get_mother_num_children(self):
        if self.is_initial_agent() or self.is_in_migrant():
            return self._mother_num_children
        else:
            return self.get_mother().get_num_children()

    def is_sibling(self, person):
        if person.get_mother() == None or person.is_in_migrant():
            return False
        if self in person.get_mother()._children:
            return True
        else:
            return False
            return

    def is_initial_agent(self):
        return self._initial_agent

    def is_in_migrant(self):
        return self._in_migrant

    def make_individual_LD_migration(self, time, timestep, region, BURN_IN=False):
        log_event_record('LD_migration', self, timestep)
        household = self.get_parent_agent()
        household._lastmigrant_time = time
        household._members_away.append(self)
        months_away = calc_migration_length(self, BURN_IN)
        self._return_timestep = timestep + months_away
        region._agent_stores['person']['LD_migr'].add_agent(self, self._return_timestep)
        self._last_migration['type'] = 'LD'
        self._last_migration['time'] = time
        self._last_migration['duration_months'] = months_away
        self._away = True

    def return_from_LD_migration(self):
        self.get_parent_agent()._members_away.remove(self)
        self._return_timestep = None
        self._away = False
        return

    def kill(self, time, timestep):
        log_event_record('Death', self, timestep)
        self._alive = False
        self._deathdate = time
        if self.is_married():
            spouse = self.get_spouse()
            self._spouse = None
            spouse._spouse = None
            spouse._ever_widowed = True
        if self.is_away():
            self._last_household._members_away.remove(self)
            self._last_household.destroy_if_empty()
        else:
            household = self.get_parent_agent()
            logger.debug('Agent %s removed from household after death' % self.get_ID())
            household.remove_agent(self)
        if self._store_list != []:
            for store in self._store_list:
                logger.debug('Away out-migrant %s died' % self.get_ID())
                store.remove_agent(self)

        return

    def make_permanent_outmigration(self, timestep):
        """
        Permanently removes an agent from a model. Will also work on people who 
        are not currently present in Chitwan Valley, and are resident only in 
        agent stores.
        """
        if not self.is_away():
            logger.debug('Person %s permanently out-migrated (while NOT away)' % self.get_ID())
            self._away = True
            household = self.get_parent_agent()
            household.remove_agent(self)
        else:
            logger.debug('Person %s permanently out-migrated (while away)' % self.get_ID())
            self._last_household._members_away.remove(self)
            self._last_household.destroy_if_empty()
        self._perm_away = True
        if self._store_list != []:
            for store in self._store_list:
                store.remove_agent(self)

    def marry(self, spouse, time):
        """Marries this agent to another Person instance."""
        assert self._spouse == None, 'Person %s already has spouse %s' % (person.get_ID(), person.get_spouse().get_ID())
        assert spouse._spouse == None, 'Person %s already has spouse %s' % (spouse.get_ID(), spouse.get_spouse().get_ID())
        assert spouse.get_sex() != self.get_sex(), 'Two people of the same sex cannot marry'
        assert spouse.get_ethnicity() == self.get_ethnicity(), 'Two people of different ethnicities cannot marry'
        self._spouse = spouse
        spouse._spouse = self
        if self.get_sex() == 'female':
            female = self
        else:
            female = spouse
            female._des_num_children = calc_des_num_children()
        self._marriage_time = time
        spouse._marriage_time = time
        return

    def get_marriage_age_years(self, time):
        assert self._spouse != None, 'Person %s does not have a spouse %s' % self.get_ID()
        marr_age_years = self.get_age_years() - (time - self._marriage_time)
        assert marr_age_years > 0, 'Person %s got married before they were borns' % self.get_ID()
        return marr_age_years

    def divorce(self):
        assert self.get_spouse() != None, 'Person %s cannot divorce as they are not married' % person.get_ID()
        spouse = self._spouse
        self._spouse = None
        spouse._spouse = None
        self._ever_divorced = True
        spouse._ever_divorced = True
        self._marriage_time = None
        spouse._marriage_time = None
        return

    def is_eligible_for_birth(self, time, timestep):
        """
        Check birth timing using Ghimire and Axinn, 2010 first birth timing 
        results or simple probability distribution for first birth timing, 
        depending on the choice of rcparams.
        """
        num_children = self.get_num_children()
        if not self.get_sex() == 'female' or not self.is_married() or num_children > self._des_num_children and self._des_num_children != -1 or self._agemonths > rcParams['birth.max_age.years'] * 12 or self._agemonths < rcParams['birth.min_age.years'] * 12:
            return False
        if num_children == 0:
            first_birth_flag = False
            if time - self._marriage_time >= 6.0:
                return False
            if rcParams['submodel.parameterization.firstbirth'] == 'simple':
                if time - self._marriage_time >= self._first_birth_timing / 12.0:
                    first_birth_flag = True
            else:
                if rcParams['submodel.parameterization.firstbirth'] == 'ghimireaxinn2010':
                    if (np.random.rand() < calc_first_birth_prob_ghimireaxinn2010(self, time)) & (time - self._marriage_time >= 0.75):
                        first_birth_flag = True
                elif rcParams['submodel.parameterization.firstbirth'] == 'zvoleff':
                    if (np.random.rand() < calc_first_birth_prob_zvoleff(self, time)) & (time - self._marriage_time >= 0.75):
                        first_birth_flag = True
                else:
                    raise Exception("Unknown option for first birth timing parameterization: '%s'" % rcParams['submodel.parameterization.firstbirth'])
                if first_birth_flag == True:
                    logger.debug('First birth to agent %s (age %.2f, marriage time %.2f)' % (self.get_ID(), self.get_age_years(), self._marriage_time))
                    log_event_record('First birth', self, timestep)
                    return True
            return False
        else:
            if time > self._last_birth_time + self._birth_interval / 12.0:
                log_event_record('Subsequent birth', self, timestep)
                return True
            else:
                return False

    def give_birth(self, time, timestep, father, simulate=False):
        """Agent gives birth. New agent inherits characterists of parents."""
        assert self.get_sex() == 'female', "Men can't give birth"
        assert self.get_spouse().get_ID() == father.get_ID(), 'All births must be in marriages'
        assert self.get_ID() != father.get_ID(), 'No immaculate conception (agent: %s)' % self.get_ID()
        if simulate:
            baby = None
        else:
            baby = self._world.new_person(birthdate=time, age=0, mother=self, father=father, ethnicity=self.get_ethnicity())
            neighborhood = self.get_parent_agent().get_parent_agent()
            baby._child_school_lt_1hr_ft = neighborhood._school_min_ft < 60
            baby._child_health_lt_1hr_ft = neighborhood._health_min_ft < 60
            baby._child_bus_lt_1hr_ft = neighborhood._bus_min_ft < 60
            baby._child_market_lt_1hr_ft = neighborhood._market_min_ft < 60
            baby._child_employer_lt_1hr_ft = neighborhood._employer_min_ft < 60
            baby._birth_household_ID = self.get_parent_agent().get_ID()
            baby._birth_neighborhood_ID = neighborhood.get_ID()
            for parent in [self, father]:
                parent._children.append(baby)
                parent._number_of_children += 1

            logger.debug('New birth to %s, (age %.2f, %s total children, %s desired, next birth %.2f)' % (self.get_ID(), self.get_age_years(), self._number_of_children, self._des_num_children, self._birth_interval))
            log_event_record('Birth', self, timestep)
        self._last_birth_time = time
        self._birth_interval = calc_birth_interval()
        return baby

    def is_married(self):
        """Returns a boolean indicating if person is married or not."""
        if self._spouse == None:
            return False
        else:
            return True
            return

    def __str__(self):
        return 'Person(PID: %s. Household: %s. Neighborhood: %s)' % (self.get_ID(), self.get_parent_agent().get_ID(), self.get_parent_agent().get_parent_agent().get_ID())


class Household(Agent_set):
    """Represents a single household agent"""

    def __init__(self, world, ID=None, initial_agent=False):
        Agent_set.__init__(self, world, ID, initial_agent)
        self._any_non_wood_fuel = boolean_choice(0.93)
        self._own_house_plot = boolean_choice(0.829)
        self._own_land = boolean_choice(0.61)
        self._rented_out_land = boolean_choice(0.11)
        self._lastmigrant_time = None
        self._members_away = []
        self._hh_area = 0
        return

    def get_info(self):
        """Returns basic info about this household for use in logging."""
        return (
         str(self.get_ID()), str(self._any_non_wood_fuel),
         str(self._own_house_plot), str(self._own_land),
         str(self._rented_out_land), str(self._lastmigrant_time),
         str(self._hh_area), str(self.num_members()),
         str(self.num_away_members()))

    def any_non_wood_fuel(self):
        """Boolean for whether household uses any non-wood fuel"""
        return self._any_non_wood_fuel

    def get_away_members(self):
        """Returns any household members that are away (migrants)."""
        return self._members_away

    def num_away_members(self):
        """Returns number of household members that are away (migrants)."""
        return len(self._members_away)

    def get_all_HH_members(self):
        """Returns all household members (including away migrants)."""
        return self.get_agents() + self.get_away_members()

    def get_hh_head(self):
        max_age = -1
        if self.num_members() == 0:
            raise Exception('No household head for household %s. Household has no members' % self.get_ID())
        for person in self.get_agents():
            if person.get_age_months() > max_age:
                max_age = person.get_age_months()
                hh_head = person

        return hh_head

    def own_house_plot(self):
        """Boolean for whether household owns the plot of land on which it resides"""
        return self._own_house_plot

    def own_any_land(self):
        """Boolean for whether household owns any land"""
        return self._own_land

    def rented_out_land(self):
        """Boolean for whether household rented out any of its land"""
        return self._rented_out_land

    def is_initial_agent(self):
        return self._initial_agent

    def get_monthly_fw_usage_quantity(self, time):
        fw_usage = calc_daily_fuelwood_usage(self, time)
        fw_usage = fw_usage * 30
        return fw_usage

    def get_fw_usage_probability(self, time):
        return calc_fuelwood_usage_probability(self, time)

    def remove_agent(self, person):
        """
        Remove a person from this household. Override the default method for an 
        Agent_set so that we can check if the removal of this agent would leave 
        this household empty. It it would leave it empty, then destroy this 
        household after removing the agent.
        """
        Agent_set.remove_agent(self, person)
        self.destroy_if_empty()

    def add_agent(self, person):
        """
        Add a person to this household. Override the default method for an 
        Agent_set so that we can also set the _last_household attribute on the new household member.
        """
        Agent_set.add_agent(self, person)
        person._last_household = self

    def destroy_if_empty(self):
        """
        Checks to see if a households has:

            - No members present
            - No members away (migrants) that may return in the future

        If so, then destroy the household and return its land to agriculture.
        """
        if self.num_members() == 0 and self.get_away_members() == []:
            neighborhood = self.get_parent_agent()
            neighborhood._land_agveg += self._hh_area
            neighborhood._land_privbldg -= self._hh_area
            neighborhood.remove_agent(self)
            logger.debug('Household %s left empty - household removed from model' % self.get_ID())

    def out_migrate(self, timestep):
        neighborhood = self.get_parent_agent()
        hhsize = len(self.get_agents())
        for person in self.get_agents():
            person.make_permanent_outmigration(timestep)

        logger.debug('Household %s outmigrated from neighborhood %s (hhsize: %s)' % (
         self.get_ID(), neighborhood.get_ID(), hhsize))

    def mean_gender(self):
        gender_total = 0
        for member in self.get_agents():
            if member.get_sex() == 'female':
                gender_total += 1

        return gender_total / self.num_members()

    def __str__(self):
        return 'Household(HID: %s. %s person(s))' % (self.get_ID(), self.num_members())


class Neighborhood(Agent_set):
    """Represents a single neighborhood agent"""

    def __init__(self, world, ID=None, initial_agent=False):
        Agent_set.__init__(self, world, ID, initial_agent)
        self._elec_available = None
        self._land_agveg = None
        self._land_nonagveg = None
        self._land_privbldg = None
        self._land_pubbldg = None
        self._land_other = None
        self._distnara = None
        self._x = None
        self._y = None
        self._elev = None
        self._school_min_ft = None
        self._health_min_ft = None
        self._bus_min_ft = None
        self._market_min_ft = None
        self._employer_min_ft = None
        return

    def get_info(self):
        """Returns basic info about this neighborhood for use in logging."""
        return (
         str(self.get_ID()), str(self._land_agveg),
         str(self._land_nonagveg), str(self._land_privbldg),
         str(self._land_pubbldg), str(self._land_other),
         str(self._elec_available), str(self._school_min_ft),
         str(self._health_min_ft), str(self._bus_min_ft),
         str(self._market_min_ft), str(self._employer_min_ft),
         str(self._forest_dist_BZ_km), str(self._forest_dist_CNP_km),
         str(self._forest_closest_km), str(self._forest_closest_type))

    def add_agent(self, agent, initializing=False):
        """
        Subclass the Agent_set.add_agent function in order to account for LULC 
        change with new household addition.
        """
        if initializing == True:
            Agent_set.add_agent(self, agent)
        else:
            hh_area = calc_hh_area()
            if self._land_agveg - hh_area < 0:
                if self._land_nonagveg - hh_area < 0:
                    return False
                else:
                    self._land_nonagveg -= hh_area
                    self._land_privbldg += hh_area
                    Agent_set.add_agent(self, agent)
                    return True

            else:
                self._land_agveg -= hh_area
                self._land_privbldg += hh_area
                Agent_set.add_agent(self, agent)
                return True
            return False

    def is_initial_agent(self):
        return self._initial_agent

    def elec_available(self):
        """Boolean for whether neighborhood has electricity."""
        return self._elec_available

    def get_num_psn(self):
        """Returns the number of people in the neighborhood."""
        num_psn = 0
        for household in self.iter_agents():
            num_psn += household.num_members()

        return num_psn

    def get_num_marriages(self):
        """Returns the total number of marriages in this neighborhood."""
        num_marr = 0
        spouses = []
        for household in self.iter_agents():
            for person in household.iter_agents():
                if person.is_married() and person.get_spouse() not in spouses:
                    num_marr += 1
                    spouses.append(person)

        return num_marr

    def get_hh_sizes(self):
        hh_sizes = {}
        for household in self.iter_agents():
            hh_sizes[household.get_ID()] = household.num_members()

        return hh_sizes

    def get_coords(self):
        return (
         self._x, self._y)

    def __str__(self):
        return 'Neighborhood(NID: %s. %s household(s))' % (self.get_ID(), self.num_members())


class Region(Agent_set):
    """Represents a set of neighborhoods sharing a spatial area (and therefore 
    land use data), and demographic characteristics."""

    def __init__(self, world, ID=None, initial_agent=False):
        Agent_set.__init__(self, world, ID, initial_agent)
        self._agent_stores = {}
        self._agent_stores['person'] = {}
        self._agent_stores['person']['LL_migr'] = Agent_Store()
        self._agent_stores['person']['LD_migr'] = Agent_Store()
        self._cemetery = {}

    def __str__(self):
        return 'Region(RID: %s, %s neighborhood(s), %s household(s), %s person(s))' % (self.get_ID(),
         len(self._members), self.num_households(), self.num_persons())

    def is_initial_agent(self):
        return self._initial_agent

    def iter_households(self):
        """Returns an iterator over all the households in the region"""
        for neighborhood in self.iter_agents():
            for household in neighborhood.iter_agents():
                yield household

    def get_households(self):
        """Returns a list of all the households in the region"""
        households = []
        for neighborhood in self.iter_agents():
            for household in neighborhood.iter_agents():
                households.append(household)

        return households

    def iter_persons(self):
        """
        Returns an iterator over all the persons in the region that are NOT 
        within an agent_store class instance (so only those resident in 
        Chitwan).
        """
        for household in self.iter_households():
            for person in household.iter_agents():
                yield person

    def iter_all_persons(self):
        """"
        Returns an iterator over all the persons in the region, including those 
        within agent store class instances. Necessary for doing things that 
        apply to all agents regardless of their status, like incrementing ages.
        """
        for household in self.iter_households():
            for person in household.iter_agents():
                yield person

        for agent_store in self.iter_person_agent_stores():
            for person in agent_store._stored_agents:
                yield person

    def iter_person_agent_stores(self):
        for agent_store_name in self._agent_stores['person'].keys():
            yield self._agent_stores['person'][agent_store_name]

    def births(self, time, timestep, simulate=False):
        """
        Runs through the population and agents give birth probabilistically 
        based on their birth interval and desired family size, and the first 
        birth timing model that was selected in rcParams. The 'simulate' 
        parameter allows running all functions in the model (setting last birth 
        time, next birth time, etc) during the burn-in period, WITHOUT actually 
        having women give birth.
        """
        logger.debug('Processing births')
        births = {}
        for household in self.iter_households():
            neighborhood = household.get_parent_agent()
            for person in household.iter_agents():
                if person.is_eligible_for_birth(time, timestep):
                    father = person.get_spouse()
                    baby = person.give_birth(time, timestep, father=father, simulate=simulate)
                    if not simulate:
                        household.add_agent(baby)
                        if rcParams['feedback.birth.nonagveg']:
                            if neighborhood._land_nonagveg - rcParams['feedback.birth.nonagveg.area'] >= 0:
                                neighborhood._land_nonagveg -= rcParams['feedback.birth.nonagveg.area']
                                neighborhood._land_other += rcParams['feedback.birth.nonagveg.area']
                    if neighborhood.get_ID() not in births:
                        births[neighborhood.get_ID()] = 0
                    births[neighborhood.get_ID()] += 1

        return births

    def deaths(self, time, timestep):
        """
        Runs through the population and kills agents probabilistically based on 
        their age and sex and the probability.death for this population.
        """
        logger.debug('Processing deaths')
        deaths = {}
        for person in self.iter_all_persons():
            if np.random.rand() < calc_probability_death(person):
                if not person.is_away():
                    neighborhood = person.get_parent_agent().get_parent_agent()
                    if neighborhood.get_ID() not in deaths:
                        deaths[neighborhood.get_ID()] = 0
                    deaths[neighborhood.get_ID()] += 1
                person.kill(time, timestep)
                self._cemetery[self.get_ID()] = self

        return deaths

    def marriages(self, time, timestep):
        """
        Runs through the population and marries agents probabilistically based 
        on their age and the probability_marriage for this population
        """
        logger.debug('Processing marriages')
        minimum_age = rcParams['marriage.minimum_age_years']
        maximum_age = rcParams['marriage.maximum_age_years']
        eligible_males = []
        eligible_females = []
        for household in self.iter_households():
            for person in household.iter_agents():
                if not person.is_married() and person.get_age_years() >= minimum_age and person.get_age_years() <= maximum_age and np.random.rand() < calc_probability_marriage(person, time):
                    if person.get_sex() == 'female':
                        eligible_females.append(person)
                    if person.get_sex() == 'male':
                        eligible_males.append(person)

        logger.debug('%s resident males and %s resident females eligible for marriage' % (len(eligible_males), len(eligible_females)))
        eligible_persons = eligible_males + eligible_females
        couples = []
        for person in eligible_persons:
            if len(eligible_persons) == 0:
                break
            spouse = choose_spouse(person, eligible_persons)
            if spouse == None:
                continue
            eligible_persons.remove(spouse)
            eligible_persons.remove(person)
            if person.get_sex() == 'male':
                couples.append((person, spouse))
            else:
                couples.append((spouse, person))

        logger.debug('%s resident couples formed, %s couples with in-migrants' % (len(couples), len(eligible_persons)))
        for person in eligible_persons:
            frac_year, years = np.modf(calc_spouse_age_diff(person))
            months = np.round(frac_year * 12)
            age_diff_months = years * 12 + months
            if person.get_sex() == 'female':
                spouse_sex = 'male'
                spouse_age_months = person.get_age_months() + age_diff_months
            else:
                spouse_sex = 'female'
                spouse_age_months = person.get_age_months() - age_diff_months
            if spouse_age_months < rcParams['marriage.minimum_age_years'] * 12.0:
                spouse_age_months = rcParams['marriage.minimum_age_years'] * 12.0
            spouse_birthdate = time - spouse_age_months / 12.0
            spouse = self._world.new_person(birthdate=spouse_birthdate, age=spouse_age_months, sex=spouse_sex, ethnicity=person.get_ethnicity(), in_migrant=True)
            logger.debug('New in migrant (%s) for marriage (%s, %.2f years old)' % (spouse.get_ID(), spouse.get_sex(), spouse.get_age_years()))
            if person.get_sex() == 'female':
                couples.append((spouse, person))
            else:
                couples.append((person, spouse))

        marriages = {}
        for male, female in couples:
            logger.debug('New marriage to %s (%.2f years old, %s) and %s (%.2f years old, %s)' % (
             male.get_ID(), male.get_age_years(), male.get_sex(),
             female.get_ID(), female.get_age_years(), female.get_sex()))
            male.marry(female, time)
            female._first_birth_timing = calc_first_birth_time(self)
            moveout_prob = rcParams['prob.marriage.moveout']
            if boolean_choice(moveout_prob) or male.get_parent_agent() == None:
                new_home = self._world.new_household()
                poss_neighborhoods = []
                for person in [male, female]:
                    old_household = person.get_parent_agent()
                    if old_household != None:
                        poss_neighborhoods.append(old_household.get_parent_agent())
                        old_household.remove_agent(person)
                        logger.debug('Agent %s removed from old household (for marriage)' % person.get_ID())
                    new_home.add_agent(person)

                if len(poss_neighborhoods) > 0:
                    neighborhood = poss_neighborhoods[0]
                else:
                    poss_neighborhoods = self.get_agents()
                    neighborhood = poss_neighborhoods[np.random.randint(len(poss_neighborhoods))]
                n = 0
                while neighborhood.add_agent(new_home) == False:
                    neighborhood = neighborhood._neighborhoods_by_distance[n]
                    n += 1

            else:
                old_household = female.get_parent_agent()
                if old_household != None:
                    old_household.remove_agent(female)
                    logger.debug('Agent %s removed from old household (for marriage)' % female.get_ID())
                male_household = male.get_parent_agent()
                male_household.add_agent(female)
                neighborhood = male.get_parent_agent().get_parent_agent()
            if neighborhood.get_ID() not in marriages:
                marriages[neighborhood.get_ID()] = 0
            marriages[neighborhood.get_ID()] += 1
            log_event_record('Marriage', male, timestep)
            log_event_record('Marriage', female, timestep)

        return marriages

    def divorces(self, time_float, timestep):
        """
        Runs through the population and marries agents probabilistically 
        based on their age and the probability_marriage for this population
        """
        logger.debug('Processing divorces')
        divorces = {}
        for person in self.iter_all_persons():
            if not person.is_married() or person._last_divorce_check == timestep or np.random.rand() >= calc_probability_divorce(person):
                person._last_divorce_check = timestep
                continue
            person._last_divorce_check = timestep
            if person.get_sex() == 'female':
                woman = person
                man = woman.get_spouse()
            else:
                woman = person.get_spouse()
                man = person
            if man.is_away():
                original_nbh = man._last_household.get_parent_agent()
            else:
                original_nbh = man.get_parent_agent().get_parent_agent()
            logger.debug('Agent %s divorced agent %s (marriage time %.2f)' % (woman.get_ID(), man.get_ID(), person._marriage_time))
            log_event_record('Divorce', man, timestep)
            log_event_record('Divorce', woman, timestep)
            person.divorce()
            if woman.is_away():
                if not woman._perm_away:
                    woman.make_permanent_outmigration(timestep)
                else:
                    logger.debug('Woman %s (permanent outmigrant) divorced resident husband' % woman.get_ID())
            elif woman.get_mother() == None or woman.get_mother().get_parent_agent() == None:
                woman.get_parent_agent().remove_agent(woman)
                logger.debug('Woman %s removed from old household to establish new household after divorce' % woman.get_ID())
                new_home = self._world.new_household()
                new_home.add_agent(woman)
                poss_neighborhoods = self.get_agents()
                new_neighborhood = poss_neighborhoods[np.random.randint(len(poss_neighborhoods))]
                new_neighborhood.add_agent(new_home)
            else:
                woman.get_parent_agent().remove_agent(woman)
                logger.debug("Woman %s removed from old household to move into mother's household after divorce" % woman.get_ID())
                new_home = woman.get_mother().get_parent_agent()
                new_home.add_agent(woman)
            if original_nbh.get_ID() not in divorces:
                divorces[original_nbh.get_ID()] = 0
            divorces[original_nbh.get_ID()] += 1

        return divorces

    def get_num_marriages(self):
        """Returns the total number of marriages in this region."""
        num_spouses = 0
        for person in self.iter_all_persons():
            if person.is_married():
                num_spouses += 1

        return num_spouses / 2

    def education(self, time):
        """
        Runs through the population and makes agents probabilistically attend 
        schooling based on their age and the education function for this 
        population.
        """
        logger.debug('Processing education')
        timestep = rcParams['model.timestep']
        start_school_age = rcParams['education.start_school_age_years']
        schooling = {}
        for person in self.iter_persons():
            if person._school_status == 'outofschool':
                pass
            elif (person._school_status == 'undetermined') & (person.get_age_years() >= start_school_age):
                person._school_status = 'inschool'
                person._final_schooling_level = calc_education_level(person)
                person._schooling = timestep / 12.0
            elif person._school_status == 'inschool':
                if person._schooling >= person._final_schooling_level:
                    person._school_status = 'outofschool'
                else:
                    person._schooling += timestep / 12.0
            neighborhood = person.get_parent_agent().get_parent_agent()

        return schooling

    def individual_migrations(self, time_float, timestep, BURN_IN=False):
        """
        Runs through the population and makes agents probabilistically migrate
        based on demographic characteristics.
        """
        logger.debug('Processing person-level migrations')
        n_outmigr_indiv = {}
        for household in self.iter_households():
            for person in household.iter_agents():
                if np.random.rand() < calc_probability_migration(person):
                    person.make_individual_LD_migration(time_float, timestep, self, BURN_IN)
                    neighborhood = household.get_parent_agent()
                    if neighborhood.get_ID() not in n_outmigr_indiv:
                        n_outmigr_indiv[neighborhood.get_ID()] = 0
                    n_outmigr_indiv[neighborhood.get_ID()] += 1

        n_ret_migr_indiv, released_persons = self._agent_stores['person']['LD_migr'].release_agents(timestep)
        for person in released_persons:
            person.return_from_LD_migration()

        return (
         n_outmigr_indiv, n_ret_migr_indiv)

    def get_rand_NBH(self, rand_NBH_type):
        if rand_NBH_type == 'inv_dist_forest_closest_km':
            probs = [ 1 / NBH._forest_closest_km for NBH in self.get_agents() ]
        elif rand_NBH_type == 'inv_dist_CNP_km':
            probs = [ 1 / NBH._forest_dist_CNP_km for NBH in self.get_agents() ]
        elif rand_NBH_type == 'inv_dist_BZ_km':
            probs = [ 1 / NBH._forest_dist_BZ_km for NBH in self.get_agents() ]
        elif rand_NBH_type == 'inv_dist_narayangar_km':
            probs = [ 1 / NBH._distnara for NBH in self.get_agents() ]
        elif rand_NBH_type == 'random':
            probs = np.ones(len(self.get_agents()))
        else:
            raise Exception("Unknown option %s for 'rand_NBH_type' in get_rand_NBH" % rand_NBH_type)
        probs = np.cumsum(probs) / np.sum(probs)
        index = sum(np.random.rand() > probs)
        return self.get_agents()[index]

    def household_migrations(self, time_float, timestep):
        """
        Runs through the list of households and allows household-level in and 
        out-migration. Household-level out-migration is handled 
        probabilistically based on household attributes.
        """
        logger.debug('Processing household-level migrations')
        n_inmigr_hh = {}
        num_in_migr_households = calc_num_inmigrant_households()
        household_list = self.get_households()
        for n in xrange(num_in_migr_households):
            hh_size = calc_inmigrant_household_size()
            hh_ethnicity = calc_inmigrant_household_ethnicity()
            np.random.shuffle(household_list)
            for model_hh in household_list:
                model_hh_size = model_hh.num_members() + model_hh.num_away_members()
                if model_hh_size == hh_size:
                    break

            new_household = self._world.new_household()
            clone_dict = {}
            for psn in model_hh.get_all_HH_members():
                new_psn = self._world.new_person(birthdate=psn._birthdate, age=psn.get_age_months(), sex=psn.get_sex(), ethnicity=hh_ethnicity, in_migrant=True)
                clone_dict[psn.get_ID()] = new_psn.get_ID()
                new_household.add_agent(new_psn)

            for psn in model_hh.get_all_HH_members():
                clone = new_household.get_agent(clone_dict[psn.get_ID()])
                if psn._mother != None and psn._mother.get_ID() in clone_dict.keys():
                    clone_mother_ID = clone_dict[psn._mother.get_ID()]
                    clone._mother = new_household.get_agent(clone_mother_ID)
                if psn._father != None and psn._father.get_ID() in clone_dict.keys():
                    clone_father_ID = clone_dict[psn._father.get_ID()]
                    clone._father = new_household.get_agent(clone_father_ID)
                if psn.get_sex() == 'female' and psn._last_birth_time != None:
                    clone._last_birth_time = psn._last_birth_time
                if psn._spouse != None and psn._spouse.get_ID() in clone_dict.keys():
                    clone_spouse_ID = clone_dict[psn._spouse.get_ID()]
                    clone._spouse = new_household.get_agent(clone_spouse_ID)
                    clone._marriage_time = psn._marriage_time

            poss_neighborhoods = self.get_agents()
            neighborhood = poss_neighborhoods[np.random.randint(len(poss_neighborhoods))]
            n = 0
            while neighborhood.add_agent(new_household) == False:
                neighborhood = neighborhood._neighborhoods_by_distance[n]
                n += 1

            if neighborhood.get_ID() not in n_inmigr_hh:
                n_inmigr_hh[neighborhood.get_ID()] = 0
            n_inmigr_hh[neighborhood.get_ID()] += 1
            logger.debug('New in-migrant household %s added to neighborhood %s (%s members)' % (
             new_household.get_ID(), neighborhood.get_ID(), hh_size))

        n_outmigr_hh = {}
        for household in self.get_households():
            if np.random.rand() < calc_probability_HH_outmigration(household, timestep):
                neighborhood = household.get_parent_agent()
                household.out_migrate(timestep)
                if neighborhood.get_ID() not in n_outmigr_hh:
                    n_outmigr_hh[neighborhood.get_ID()] = 0
                n_outmigr_hh[neighborhood.get_ID()] += 1

        return (
         n_inmigr_hh, n_outmigr_hh)

    def increment_age(self):
        """
        Adds one to the age of each agent. The units of age are dependent on 
        the units of the input rc parameters.
        """
        logger.debug('Incrementing ages')
        for person in self.iter_all_persons():
            timestep = rcParams['model.timestep']
            person._agemonths += timestep

    def establish_NFOs(self):
        NFO_types = rcParams['NFOs.change.type']
        new_NFOs = []
        if 'All' in NFO_types or 'school' in NFO_types:
            new_NFOs.append(('school',
             int(draw_from_prob_dist(rcParams['NFOs.change.prob_new_school']))))
        if 'All' in NFO_types or 'health' in NFO_types:
            new_NFOs.append(('health',
             int(draw_from_prob_dist(rcParams['NFOs.change.prob_new_health']))))
        if 'All' in NFO_types or 'bus' in NFO_types:
            new_NFOs.append(('bus',
             int(draw_from_prob_dist(rcParams['NFOs.change.prob_new_bus']))))
        if 'All' in NFO_types or 'market' in NFO_types:
            new_NFOs.append(('market',
             int(draw_from_prob_dist(rcParams['NFOs.change.prob_new_market']))))
        if 'All' in NFO_types or 'employer' in NFO_types:
            new_NFOs.append(('employer',
             int(draw_from_prob_dist(rcParams['NFOs.change.prob_new_employer']))))
        for change_tuple in new_NFOs:
            NBHs = [ self.get_rand_NBH(rcParams['NFOs.rand_NBH_type']) for n in xrange(change_tuple[1]) ]
            for NBH in NBHs:
                if change_tuple[0] == 'school':
                    initial = NBH._school_min_ft
                    NBH._school_min_ft = NBH._school_min_ft / 2
                    final = NBH._school_min_ft
                elif change_tuple[0] == 'health':
                    initial = NBH._health_min_ft
                    NBH._health_min_ft = NBH._health_min_ft / 2
                    final = NBH._health_min_ft
                elif change_tuple[0] == 'bus':
                    initial = NBH._bus_min_ft
                    NBH._bus_min_ft = NBH._bus_min_ft / 2
                    final = NBH._bus_min_ft
                elif change_tuple[0] == 'market':
                    initial = NBH._market_min_ft
                    NBH._market_min_ft = NBH._market_min_ft / 2
                    final = NBH._market_min_ft
                elif change_tuple[0] == 'employer':
                    initial = NBH._employer_min_ft
                    NBH._employer_min_ft = NBH._employer_min_ft / 2
                    final = NBH._employer_min_ft
                logger.debug('New %s established in NBH %s. Distance in min. on foot reduced from %s to %s' % (change_tuple[0], NBH.get_ID(), initial, final))

    def get_neighborhood_fw_usage(self, time):
        fw_usage = {}
        for neighborhood in self.iter_agents():
            fw_usage[neighborhood.get_ID()] = 0
            for household in neighborhood.iter_agents():
                fw_usage[neighborhood.get_ID()] += household.get_monthly_fw_usage_quantity(time) * household.get_fw_usage_probability(time)

        return {'fw_usage': fw_usage}

    def get_neighborhood_landuse(self):
        landuse = {'agveg': {}, 'nonagveg': {}, 'privbldg': {}, 'pubbldg': {}, 'other': {}}
        for neighborhood in self.iter_agents():
            landuse['agveg'][neighborhood.get_ID()] = neighborhood._land_agveg
            landuse['nonagveg'][neighborhood.get_ID()] = neighborhood._land_nonagveg
            landuse['privbldg'][neighborhood.get_ID()] = neighborhood._land_privbldg
            landuse['pubbldg'][neighborhood.get_ID()] = neighborhood._land_pubbldg
            landuse['other'][neighborhood.get_ID()] = neighborhood._land_other

        return landuse

    def get_neighborhood_nfo_context(self):
        nfocontext = {'school_min_ft': {}, 'health_min_ft': {}, 'bus_min_ft': {}, 'market_min_ft': {}, 'employer_min_ft': {}}
        for neighborhood in self.iter_agents():
            nfocontext['school_min_ft'][neighborhood.get_ID()] = neighborhood._school_min_ft
            nfocontext['health_min_ft'][neighborhood.get_ID()] = neighborhood._health_min_ft
            nfocontext['bus_min_ft'][neighborhood.get_ID()] = neighborhood._bus_min_ft
            nfocontext['market_min_ft'][neighborhood.get_ID()] = neighborhood._market_min_ft
            nfocontext['employer_min_ft'][neighborhood.get_ID()] = neighborhood._employer_min_ft

        return nfocontext

    def get_neighborhood_forest_distance(self):
        forest_dist = {'for_dist_BZ_km': {}, 'for_dist_CNP_km': {}, 'for_closest_km': {}, 'for_closest_type': {}}
        for neighborhood in self.iter_agents():
            forest_dist['for_dist_BZ_km'][neighborhood.get_ID()] = neighborhood._forest_dist_BZ_km
            forest_dist['for_dist_CNP_km'][neighborhood.get_ID()] = neighborhood._forest_dist_CNP_km
            forest_dist['for_closest_km'][neighborhood.get_ID()] = neighborhood._forest_closest_km
            forest_dist['for_closest_type'][neighborhood.get_ID()] = neighborhood._forest_closest_type

        return forest_dist

    def get_neighborhood_pop_stats(self):
        """
        Used each timestep to return a dictionary of neighborhood-level 
        population statistics.
        """
        pop_stats = {'num_psn': {}, 'num_hs': {}, 'num_marr': {}}
        for neighborhood in self.iter_agents():
            pop_stats['num_psn'][neighborhood.get_ID()] = neighborhood.get_num_psn()
            pop_stats['num_hs'][neighborhood.get_ID()] = neighborhood.num_members()
            pop_stats['num_marr'][neighborhood.get_ID()] = neighborhood.get_num_marriages()

        return pop_stats

    def num_persons(self):
        """Returns the number of persons in the population."""
        total = 0
        for household in self.iter_households():
            total += household.num_members()

        return total

    def num_households(self):
        total = 0
        for neighborhood in self.iter_agents():
            total += len(neighborhood.get_agents())

        return total

    def num_neighborhoods(self):
        return len(self._members.values())


class World():
    """
    The world class generates new agents, while tracking ID numbers to ensure 
    that they are always unique across each agent type. It also contains a 
    dictionary with all the regions in the model.
    """

    def __init__(self):
        self._members = {}
        self._PIDGen = IDGenerator()
        self._HIDGen = IDGenerator()
        self._NIDGen = IDGenerator()
        self._RIDGen = IDGenerator()

    def set_DEM_data(self, DEM, gt, prj):
        self._DEM_array = DEM
        self._DEM_gt = gt
        self._DEM_prj = prj
        return 0

    def get_DEM(self):
        return self._DEM_array

    def get_DEM_data(self):
        return (
         self._DEM_array, self._DEM_gt, self._DEM_prj)

    def set_world_mask_data(self, world_mask, gt, prj):
        self._world_mask_array = world_mask
        self._world_mask_gt = gt
        self._world_mask_prj = prj
        return 0

    def get_world_mask(self):
        return self._world_mask_array

    def get_world_mask_data(self):
        return (
         self._world_mask_array, self._world_mask_gt, self._world_mask_prj)

    def new_person(self, birthdate, PID=None, **kwargs):
        """Returns a new person agent."""
        if PID == None:
            PID = self._PIDGen.next()
        else:
            self._PIDGen.use_ID(PID)
        return Person(self, birthdate, ID=PID, **kwargs)

    def new_household(self, HID=None, **kwargs):
        """Returns a new household agent."""
        if HID == None:
            HID = self._HIDGen.next()
        else:
            self._HIDGen.use_ID(HID)
        return Household(self, ID=HID, **kwargs)

    def new_neighborhood(self, NID=None, **kwargs):
        """Returns a new neighborhood agent."""
        if NID == None:
            NID = self._NIDGen.next()
        else:
            self._NIDGen.use_ID(NID)
        return Neighborhood(self, ID=NID, **kwargs)

    def new_region(self, RID=None, initial_agent=False):
        """Returns a new region agent, and adds it to the world member list."""
        if RID == None:
            RID = self._RIDGen.next()
        else:
            self._RIDGen.use_ID(RID)
        region = Region(self, RID, initial_agent)
        self._members[region.get_ID()] = region
        return region

    def get_regions(self):
        return self._members.values()

    def iter_regions(self):
        """Convenience function for iteration over all regions in the world."""
        for region in self._members.values():
            yield region

    def iter_persons(self):
        """Convenience function used for things like migrations and births."""
        for region in self.iter_regions():
            for person in region.iter_persons():
                yield person

    def iter_all_persons(self):
        """
        Convenience function used for processes that apply to ALL agents, even 
        those in agent_stores (things like incrementing agent ages).
        """
        for region in self.iter_regions():
            for person in region.iter_all_persons():
                yield person

    def write_persons_to_csv(self, timestep, results_path):
        """
        Writes a list of persons, with a header row, to CSV.
        """
        psn_csv_file = os.path.join(results_path, 'psns_time_%s.csv' % timestep)
        out_file = open(psn_csv_file, 'wb')
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(['pid', 'hid', 'nid', 'rid', 'gender', 'age',
         'ethnicity', 'mother_id', 'father_id',
         'spouseid', 'marrtime', 'schooling',
         'num_children', 'alive', 'is_away',
         'is_initial_agent', 'is_in_migrant',
         'mother_num_children',
         'mother_years_schooling', 'mother_work',
         'father_years_schooling', 'father_work',
         'parents_contracep'])
        for region in self.iter_regions():
            for person in region.iter_persons():
                csv_writer.writerow(person.get_info())

        out_file.close()

    def write_NBHs_to_csv(self, timestep, results_path):
        """
        Writes a list of neighborhoods, with a header row, to CSV.
        """
        NBH_csv_file = os.path.join(results_path, 'NBHs_time_%s.csv' % timestep)
        out_file = open(NBH_csv_file, 'wb')
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(['nid', 'rid', 'x', 'y', 'numpsns', 'numhs', 'agveg',
         'nonagveg', 'pubbldg', 'privbldg', 'other', 'total_area',
         'perc_agveg', 'perc_veg', 'perc_bldg'])
        for region in self.iter_regions():
            for neighborhood in region.iter_agents():
                new_row = []
                new_row.append(neighborhood.get_ID())
                new_row.append(neighborhood.get_parent_agent().get_ID())
                x, y = neighborhood.get_coords()
                new_row.append(x)
                new_row.append(y)
                new_row.append(neighborhood.get_num_psn())
                new_row.append(neighborhood.num_members())
                new_row.append(neighborhood._land_agveg)
                new_row.append(neighborhood._land_nonagveg)
                new_row.append(neighborhood._land_pubbldg)
                new_row.append(neighborhood._land_privbldg)
                new_row.append(neighborhood._land_other)
                total_area = neighborhood._land_agveg + neighborhood._land_nonagveg + neighborhood._land_pubbldg + neighborhood._land_privbldg + neighborhood._land_other
                perc_agveg = neighborhood._land_agveg / total_area
                perc_veg = (neighborhood._land_agveg + neighborhood._land_nonagveg) / total_area
                perc_bldg = (neighborhood._land_privbldg + neighborhood._land_pubbldg) / total_area
                new_row.append(total_area)
                new_row.append(perc_agveg)
                new_row.append(perc_veg)
                new_row.append(perc_bldg)
                csv_writer.writerow(new_row)

        out_file.close()