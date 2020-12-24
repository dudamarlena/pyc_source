# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_wardinfo.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 6891 bytes
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field
from typing import List as _List
__all__ = [
 'WardInfo', 'WardInfos']

@_dataclass
class WardInfo:
    __doc__ = 'This class holds metadata about a ward, e.g. its name(s),\n       any ID code(s), any information about the region or\n       authority it is in etc.\n    '
    name = ''
    name: str
    alternate_names = _field(default_factory=list)
    alternate_names: _List[str]
    code = ''
    code: str
    alternate_codes = _field(default_factory=list)
    alternate_codes: _List[str]
    authority = ''
    authority: str
    authority_code = ''
    authority_code: str
    region = ''
    region: str
    region_code = ''
    region_code: str


@_dataclass
class WardInfos:
    __doc__ = 'Simple class that holds a list of WardInfo objects, and provides\n       useful search functions over that list. This prevents me from\n       cluttering up the interface of Network\n    '
    wards = _field(default_factory=list)
    wards: _List[WardInfo]

    def __len__(self):
        return len(self.wards)

    def __getitem__(self, index):
        return self.wards[index]

    def _find_ward(self, name: str, match: bool, include_alternates: bool):
        """Internal function that flexibly finds a ward by name"""
        import re
        if not isinstance(name, re.Pattern):
            search = re.compile(name, re.IGNORECASE)
        else:
            search = name
        if match:
            search = search.match
        else:
            search = search.search
        matches = []
        for i, ward in enumerate(self.wards):
            if ward is None:
                continue
            is_match = False
            if search(ward.name):
                is_match = True
            else:
                if search(ward.code):
                    is_match = True
                else:
                    if include_alternates:
                        for alternate in ward.alternate_names:
                            if search(alternate):
                                is_match = True
                                break

                        if not is_match:
                            for alternate in ward.alternate_codes:
                                if search(alternate):
                                    is_match = True
                                    break

            if is_match:
                matches.append(i)

        return matches

    def _find_authority(self, name: str, match: bool):
        """Internal function that flexibly finds a ward by authority"""
        import re
        if not isinstance(name, re.Pattern):
            search = re.compile(name, re.IGNORECASE)
        else:
            search = name
        if match:
            search = search.match
        else:
            search = search.search
        matches = []
        for i, ward in enumerate(self.wards):
            if ward is None:
                continue
            else:
                is_match = False
                if search(ward.authority):
                    is_match = True
                else:
                    if search(ward.authority_code):
                        is_match = True
            if is_match:
                matches.append(i)

        return matches

    def _find_region(self, name: str, match: bool):
        """Internal function that flexibly finds a ward by region"""
        import re
        if not isinstance(name, re.Pattern):
            search = re.compile(name, re.IGNORECASE)
        else:
            search = name
        if match:
            search = search.match
        else:
            search = search.search
        matches = []
        for i, ward in enumerate(self.wards):
            if ward is None:
                continue
            else:
                is_match = False
                if search(ward.region):
                    is_match = True
                else:
                    if search(ward.region_code):
                        is_match = True
            if is_match:
                matches.append(i)

        return matches

    def _intersect(self, list1, list2):
        """Return the intersection of two lists"""
        return [value for value in list1 if value in list2]

    def find(self, name: str=None, authority: str=None, region: str=None, match: bool=False, match_authority_and_region: bool=False, include_alternates: bool=True):
        """Generic search function that will search using any or all
           of the terms provided. This returns a list of indicies
           of wards that match the search

           Parameters
           ----------
           name: str or regexp
             Name or code of the ward to search
           authority: str or regexp
             Name or code of the authority to search
           region: str or regexp
             Name or code of the region to search
           match: bool (False)
             Use a regular expression match for the ward rather than a
             search. This forces the match to be at the start of the string
           match_authority_and_region: bool (False)
             Use a regular expression match for the authority and region
             rather than a search. This forces the match to be at the start
             of the string
           include_alternates: bool (True)
             Whether or not to include alternative names and codes when
             searching for the ward
        """
        wards = None
        if name is not None:
            wards = self._find_ward(name, match=match, include_alternates=include_alternates)
            if len(wards) == 0:
                return wards
        if authority is not None:
            authorities = self._find_authority(authority,
              match=match_authority_and_region)
            if len(authorities) == 0:
                return authorities
            if wards is None:
                wards = authorities
            else:
                wards = self._intersect(wards, authorities)
                wards.sort()
                if len(wards) == 0:
                    return wards
        elif region is not None:
            regions = self._find_region(region, match=match_authority_and_region)
            if len(regions) == 0:
                return regions
                if wards is None:
                    wards = regions
            else:
                wards = self._intersect(wards, regions)
                wards.sort()
        if wards is None:
            return list(range(1, len(self.wards)))
        return wards