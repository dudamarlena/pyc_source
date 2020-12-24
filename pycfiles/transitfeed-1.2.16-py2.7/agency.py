# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/agency.py
# Compiled at: 2018-01-24 00:52:58
from gtfsobjectbase import GtfsObjectBase
from problems import default_problem_reporter
import util

class Agency(GtfsObjectBase):
    """Represents an agency in a schedule.

  Callers may assign arbitrary values to instance attributes. __init__ makes no
  attempt at validating the attributes. Call Validate() to check that
  attributes are valid and the agency object is consistent with itself.

  Attributes:
    All attributes are strings.
  """
    _REQUIRED_FIELD_NAMES = [
     'agency_name', 'agency_url', 'agency_timezone']
    _FIELD_NAMES = _REQUIRED_FIELD_NAMES + ['agency_id', 'agency_lang',
     'agency_phone', 'agency_fare_url', 'agency_email']
    _DEPRECATED_FIELD_NAMES = [('agency_ticket_url', 'agency_fare_url')]
    _TABLE_NAME = 'agency'

    def __init__(self, name=None, url=None, timezone=None, id=None, email=None, field_dict=None, lang=None, **kwargs):
        """Initialize a new Agency object.

    Args:
      field_dict: A dictionary mapping attribute name to unicode string
      name: a string, ignored when field_dict is present
      url: a string, ignored when field_dict is present
      timezone: a string, ignored when field_dict is present
      id: a string, ignored when field_dict is present
      kwargs: arbitrary keyword arguments may be used to add attributes to the
        new object, ignored when field_dict is present
    """
        self._schedule = None
        if not field_dict:
            if name:
                kwargs['agency_name'] = name
            if url:
                kwargs['agency_url'] = url
            if timezone:
                kwargs['agency_timezone'] = timezone
            if id:
                kwargs['agency_id'] = id
            if lang:
                kwargs['agency_lang'] = lang
            if email:
                kwargs['agency_email'] = email
            field_dict = kwargs
        self.__dict__.update(field_dict)
        return

    def ValidateAgencyUrl(self, problems):
        return not util.ValidateURL(self.agency_url, 'agency_url', problems)

    def ValidateAgencyLang(self, problems):
        return not util.ValidateLanguageCode(self.agency_lang, 'agency_lang', problems)

    def ValidateAgencyTimezone(self, problems):
        return not util.ValidateTimezone(self.agency_timezone, 'agency_timezone', problems)

    def ValidateAgencyFareUrl(self, problems):
        return not util.ValidateURL(self.agency_fare_url, 'agency_fare_url', problems)

    def ValidateAgencyEmail(self, problems):
        return not util.ValidateEmail(self.agency_email, 'agency_email', problems)

    def Validate(self, problems=default_problem_reporter):
        """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
        found_problem = False
        found_problem = not util.ValidateRequiredFieldsAreNotEmpty(self, self._REQUIRED_FIELD_NAMES, problems) or found_problem
        found_problem = self.ValidateAgencyUrl(problems) or found_problem
        found_problem = self.ValidateAgencyLang(problems) or found_problem
        found_problem = self.ValidateAgencyTimezone(problems) or found_problem
        found_problem = self.ValidateAgencyFareUrl(problems) or found_problem
        found_problem = self.ValidateAgencyEmail(problems) or found_problem
        return not found_problem

    def ValidateBeforeAdd(self, problems):
        return True

    def ValidateAfterAdd(self, problems):
        self.Validate(problems)

    def AddToSchedule(self, schedule, problems):
        schedule.AddAgencyObject(self, problems)