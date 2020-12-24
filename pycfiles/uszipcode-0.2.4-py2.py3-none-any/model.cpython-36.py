# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/uszipcode-project/uszipcode/model.py
# Compiled at: 2019-05-20 14:26:11
# Size of source mod 2**32: 10764 bytes
"""
This module defines the zipcode data model.
"""
from __future__ import print_function
import json
from functools import total_ordering
from sqlalchemy import Column
from sqlalchemy import String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from .state_abbr import STATE_ABBR_SHORT_TO_LONG
from .pkg.sqlalchemy_mate import ExtendedBase
from .pkg.compressed_json_type import CompressedJSONType
from .pkg.haversine import great_circle

class ZipcodeType(object):
    __doc__ = '\n    zipcode type visitor class.\n    '
    Standard = 'Standard'
    PO_Box = 'PO Box'
    Unique = 'Unique'


Base = declarative_base()

@total_ordering
class BaseZipcode(Base, ExtendedBase):
    __doc__ = '\n    Base class for Zipcode.\n    '
    __abstract__ = True
    zipcode = Column(String, primary_key=True)
    zipcode_type = Column(String)
    major_city = Column(String)
    post_office_city = Column(String)
    common_city_list = Column(CompressedJSONType)
    county = Column(String)
    state = Column(String)
    lat = Column(Float, index=True)
    lng = Column(Float, index=True)
    timezone = Column(String)
    radius_in_miles = Column(Float)
    area_code_list = Column(CompressedJSONType)
    population = Column(Integer)
    population_density = Column(Float)
    land_area_in_sqmi = Column(Float)
    water_area_in_sqmi = Column(Float)
    housing_units = Column(Integer)
    occupied_housing_units = Column(Integer)
    median_home_value = Column(Integer)
    median_household_income = Column(Integer)
    bounds_west = Column(Float)
    bounds_east = Column(Float)
    bounds_north = Column(Float)
    bounds_south = Column(Float)
    _major_attrs = 'zipcode,zipcode_type,city,county,state,lat,lng,timezone'.split(',')

    @property
    def city(self):
        """
        Alias of ``.major_city``.
        """
        return self.major_city

    @property
    def bounds(self):
        """
        Border boundary.
        """
        return {'west':self.bounds_west, 
         'east':self.bounds_east, 
         'north':self.bounds_north, 
         'south':self.bounds_south}

    @property
    def state_abbr(self):
        """
        Return state abbreviation, two letters, all uppercase.
        """
        return self.state.upper()

    @property
    def state_long(self):
        """
        Return state full name.
        """
        return STATE_ABBR_SHORT_TO_LONG.get(self.state.upper())

    def __nonzero__(self):
        """
        For Python2 bool() method.
        """
        return self.zipcode is not None

    def __bool__(self):
        """
        For Python3 bool() method.
        """
        return self.zipcode is not None

    def __lt__(self, other):
        """
        For ``>`` comparison operator.
        """
        if self.zipcode is None or other.zipcode is None:
            raise ValueError("Empty Zipcode instance doesn't support comparison.")
        else:
            return self.zipcode < other.zipcode

    def __eq__(self, other):
        """
        For ``==`` comparison operator.
        """
        return self.zipcode == other.zipcode

    def __hash__(self):
        """
        For hash() method
        """
        return hash(self.zipcode)

    def dist_from(self, lat, lng, miles=True):
        """
        Calculate the distance of the center of this zipcode from a coordinator.

        :param lat: latitude.
        :param lng: longitude.
        :param miles: if False, the value is in `kilometers`.
        """
        return great_circle((self.lat, self.lng), (lat, lng), miles=miles)

    def to_json(self, include_null=True):
        """
        Convert to json.
        """
        data = self.to_OrderedDict(include_null=include_null)
        return json.dumps(data, indent=4)

    def glance(self):
        """
        Print its major attributes and values.
        """
        kwargs = [(key, getattr(self, key)) for key in self._major_attrs]
        s = 'Zipcode({})'.format(', '.join(['%s=%r' % (key, value) for key, value in kwargs]))
        print(s)


class SimpleZipcode(BaseZipcode):
    __doc__ = '\n    Simplized Zipcode, doesn\'t include rich Demography, Real Estate, Employment,\n    Education, geo boundary data.\n\n    :param zipcode: str,\n    :param zipcode_type: str, one of "Standard", "PO Box", "Unique",\n        recommend to use :class:`ZipcodeType` to access the value.\n    :param major_city: str,\n    :param post_office_city: str,\n    :param common_city_list: str list,\n    :param county: str,\n    :param state: str, state two letters abbrivation.\n    :param lat: float, lat\n    :param lng: float, lng\n    :param radius_in_miles: float,\n    :param timezone: str,\n    :param area_code_list: str list,\n\n    :param population: number,\n    :param population_density: number, total population per sqmi\n\n    :param land_area_in_sqmi: number, sqmi\n    :param water_area_in_sqmi: number, sqmi\n\n    :param housing_units: int,\n    :param occupied_housing_units: int,\n\n    :param median_home_value: int,\n    :param median_household_income: int,\n\n    :param bounds_west: number,\n    :param bounds_east: number,\n    :param bounds_north: number,\n    :param bounds_south: number,\n    '
    __tablename__ = 'simple_zipcode'
    __mapper_args__ = {'polymorphic_identity': 'simple_zipcode'}


_simple_zipcode_columns = [c.name for c in SimpleZipcode.__table__.columns]

class Zipcode(BaseZipcode):
    __doc__ = '\n    Zipcode that with rich info.\n\n    :param population_by_year: population change over year.\n    :param population_by_age: population distribution by gender and age.\n    :param population_by_gender: population distribution by gender.\n    :param population_by_race: population distribution by race.\n    :param head_of_household_by_age: head of household distribution by age.\n    :param families_vs_singles: population distribution by marital status.\n    :param households_with_kids: population by with or without kids.\n    :param children_by_age: children population distribution by age\n\n    :param housing_type: number of house distribution of house type.\n    :param year_housing_was_built: number of house distribution of built year.\n    :param housing_occupancy: number of house by occupancy status.\n    :param vancancy_reason: number of house by vancancy reason.\n    :param owner_occupied_home_values: number of house by home values.\n    :param rental_properties_by_number_of_rooms: number of rental properties\n        by number of rooms.\n\n    :param monthly_rent_including_utilities_studio_apt: see var name.\n    :param monthly_rent_including_utilities_1_b: see var name.\n    :param monthly_rent_including_utilities_2_b: see var name.\n    :param monthly_rent_including_utilities_3plus_b: see var name.\n\n    :param employment_status: see var name.\n    :param average_household_income_over_time: see var name.\n    :param household_income: see var name.\n    :param annual_individual_earnings: see var name.\n\n    :param sources_of_household_income____percent_of_households_receiving_income: see var name.\n    :param sources_of_household_income____average_income_per_household_by_income_source: see var name.\n\n    :param household_investment_income____percent_of_households_receiving_investment_income: see var name.\n    :param household_investment_income____average_income_per_household_by_income_source: see var name.\n\n    :param household_retirement_income____percent_of_households_receiving_retirement_incom: see var name.\n    :param household_retirement_income____average_income_per_household_by_income_source: see var name.\n\n    :param source_of_earnings: see var name.\n    :param means_of_transportation_to_work_for_workers_16_and_over: see var name.\n\n    :param travel_time_to_work_in_minutes: see var name.\n\n    :param educational_attainment_for_population_25_and_over: see var name.\n    :param school_enrollment_age_3_to_17: see var name.\n    '
    __tablename__ = 'zipcode'
    zipcode = Column(String, primary_key=True)
    polygon = Column(CompressedJSONType)
    population_by_year = Column(CompressedJSONType)
    population_by_age = Column(CompressedJSONType)
    population_by_gender = Column(CompressedJSONType)
    population_by_race = Column(CompressedJSONType)
    head_of_household_by_age = Column(CompressedJSONType)
    families_vs_singles = Column(CompressedJSONType)
    households_with_kids = Column(CompressedJSONType)
    children_by_age = Column(CompressedJSONType)
    housing_type = Column(CompressedJSONType)
    year_housing_was_built = Column(CompressedJSONType)
    housing_occupancy = Column(CompressedJSONType)
    vancancy_reason = Column(CompressedJSONType)
    owner_occupied_home_values = Column(CompressedJSONType)
    rental_properties_by_number_of_rooms = Column(CompressedJSONType)
    monthly_rent_including_utilities_studio_apt = Column(CompressedJSONType)
    monthly_rent_including_utilities_1_b = Column(CompressedJSONType)
    monthly_rent_including_utilities_2_b = Column(CompressedJSONType)
    monthly_rent_including_utilities_3plus_b = Column(CompressedJSONType)
    employment_status = Column(CompressedJSONType)
    average_household_income_over_time = Column(CompressedJSONType)
    household_income = Column(CompressedJSONType)
    annual_individual_earnings = Column(CompressedJSONType)
    sources_of_household_income____percent_of_households_receiving_income = Column(CompressedJSONType)
    sources_of_household_income____average_income_per_household_by_income_source = Column(CompressedJSONType)
    household_investment_income____percent_of_households_receiving_investment_income = Column(CompressedJSONType)
    household_investment_income____average_income_per_household_by_income_source = Column(CompressedJSONType)
    household_retirement_income____percent_of_households_receiving_retirement_incom = Column(CompressedJSONType)
    household_retirement_income____average_income_per_household_by_income_source = Column(CompressedJSONType)
    source_of_earnings = Column(CompressedJSONType)
    means_of_transportation_to_work_for_workers_16_and_over = Column(CompressedJSONType)
    travel_time_to_work_in_minutes = Column(CompressedJSONType)
    educational_attainment_for_population_25_and_over = Column(CompressedJSONType)
    school_enrollment_age_3_to_17 = Column(CompressedJSONType)
    __mapper_args__ = {'polymorphic_identity': 'zipcode'}