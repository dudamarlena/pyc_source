# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/transformations/casts.py
# Compiled at: 2020-05-13 11:17:34
# Size of source mod 2**32: 5772 bytes
from typing import List, Union, Optional
from datalogue.errors import DtlError, _property_not_found
from datalogue.models.transformations.commons import Transformation
from datalogue.dtl_utils import _parse_string_list

class ToInt(Transformation):
    __doc__ = '\n      Allows to casts a node value to int\n      '
    type_str = 'ToInt'

    def __init__(self, path: List[str]):
        """
        Builds a Casting transformation to Int

        :param path: path to node to be cast to Int
        """
        Transformation.__init__(self, ToInt.type_str)
        self.path = path

    def __eq__(self, other: 'ToInt'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"ToInt({self.path})"

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['path'] = self.path
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'ToInt')]:
        path = json.get('path')
        if path is None:
            return _property_not_found('path', json)
        else:
            path = _parse_string_list(path)
            if isinstance(path, DtlError):
                return path
            return ToInt(path)


class ToDate(Transformation):
    __doc__ = "\n    Allows to casts a node value to a date time with timezone.\n\n    You can use the following symbols in the formatting string::\n\n        Symbol  Meaning                     Presentation      Examples\n        ------  -------                     ------------      -------\n        G       era                         text              AD; Anno Domini; A\n        u       year                        year              2004; 04\n        y       year-of-era                 year              2004; 04\n        D       day-of-year                 number            189\n        M/L     month-of-year               number/text       7; 07; Jul; July; J\n        d       day-of-month                number            10\n\n        Q/q     quarter-of-year             number/text       3; 03; Q3; 3rd quarter\n        Y       week-based-year             year              1996; 96\n        w       week-of-week-based-year     number            27\n        W       week-of-month               number            4\n        E       day-of-week                 text              Tue; Tuesday; T\n        e/c     localized day-of-week       number/text       2; 02; Tue; Tuesday; T\n        F       week-of-month               number            3\n\n        a       am-pm-of-day                text              PM\n        h       clock-hour-of-am-pm (1-12)  number            12\n        K       hour-of-am-pm (0-11)        number            0\n        k       clock-hour-of-am-pm (1-24)  number            0\n\n        H       hour-of-day (0-23)          number            0\n        m       minute-of-hour              number            30\n        s       second-of-minute            number            55\n        S       fraction-of-second          fraction          978\n        A       milli-of-day                number            1234\n        n       nano-of-second              number            987654321\n        N       nano-of-day                 number            1234000000\n\n        V       time-zone ID                zone-id           America/Los_Angeles; Z; -08:30\n        z       time-zone name              zone-name         Pacific Standard Time; PST\n        O       localized zone-offset       offset-O          GMT+8; GMT+08:00; UTC-08:00;\n        X       zone-offset 'Z' for zero    offset-X          Z; -08; -0830; -08:30; -083015; -08:30:15;\n        x       zone-offset                 offset-x          +0000; -08; -0830; -08:30; -083015; -08:30:15;\n        Z       zone-offset                 offset-Z          +0000; -0800; -08:00;\n        julian  JDE Julian Date Format      text              120060 (equivalent to 29/02/2020, midnight time)\n      "
    type_str = 'ToDate'

    def __init__(self, path: List[str], date_format: Optional[List[str]]=None, optional_input: bool=False):
        """
        Builds a Casting transformation to a datetime with timezone

        :param path: path to node to be cast to Int
        :param date_format: List of formats to be used to attempt to parse the string. Defaults to [YYYY-MM-DDTHH:mm:ss.VVZ]
        """
        Transformation.__init__(self, ToDate.type_str)
        self.path = path
        self.date_format = date_format
        self.optional_input = optional_input

    def __eq__(self, other: 'ToDate'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"ToDate({self.path!r}, {self.date_format!r}, {self.optional_input!r})"

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['path'] = self.path
        base['dateFormats'] = self.date_format
        base['optionalInput'] = self.optional_input
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'ToDate')]:
        path = json.get('path')
        dateformats = json.get('dateFormats')
        if path is None:
            return _property_not_found('path', json)
        if dateformats is None:
            return _property_not_found('dateFormats', json)
        optional_input = json.get('optionalInput')
        if optional_input is None:
            optional_input = False
        path = _parse_string_list(path)
        dateformats = _parse_string_list(dateformats)
        if isinstance(path, DtlError):
            return path
        else:
            if isinstance(dateformats, DtlError):
                return dateformats
            return ToDate(path, dateformats, optional_input)