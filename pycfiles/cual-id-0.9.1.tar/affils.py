# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/anders/code/python/cuaffils/cuaffils/affils.py
# Compiled at: 2014-09-10 07:23:39
import re
TERMS = [
 'spring', 'summer', 'fall']

class InvalidWindString(Exception):
    pass


class InvalidLDAPString(Exception):
    pass


InvalidPamaceaString = InvalidLDAPString

class InvalidCourseDirString(Exception):
    pass


def generate_wind_string(**kwargs):
    fields = kwargs
    fields['term'] = TERMS.index(fields['term']) + 1
    fields['member'] = 'fc' if fields.get('member', 'student') == 'faculty' else 'st'
    return 't%(term)d.y%(year)04d.s%(section_number)s.c%(course_prefix_letter)s%(course_number)s.%(department_id)s.%(member)s.course:columbia.edu' % fields


def pad_to_four(s):
    if len(s) == 3:
        return s + '_'
    return s


def parse_wind_string(s):
    pattern = re.compile("\n        t\n        ([1-3]) # number 1,2, or 3 in 'term'.\n        .y\n        (\\d{4}) # exactly four digits in 'year'.\n        .s\n        (\\d{3}) # exactly three digits in 'section'.\n        .c\n        (\\D)    # exactly one letter in 'prefix'.\n        ([^\\.]{4}) # exactly four chars in 'course_number'.\n        .\n        ([^\\.]{3,4}) # three or four letters in 'department_code'.\n        .\n        ([^\\.]{2}) # 'fc' or 'st' for student/faculty\n        ", re.VERBOSE)
    r = pattern.search(s)
    if r is None:
        raise InvalidWindString
    t = r.groups()
    return dict(term=TERMS[(int(t[0]) - 1)], year=int(t[1]), section_number=t[2], course_prefix_letter=t[3], course_number=t[4], department_id=t[5], member='faculty' if t[6] == 'fc' else 'student')


def generate_ldap_string(**kwargs):
    fields = kwargs
    fields['term'] = TERMS.index(fields['term']) + 1
    fields['course_prefix_letter'] = fields['course_prefix_letter'].upper()
    fields['department_id'] = pad_to_four(fields['department_id'].upper())
    fields['course_number'] = fields['course_number'].upper()
    fields['member'] = 'instr' if fields.get('member', 'student') == 'faculty' else 'course'
    return 'CU%(member)s_%(department_id)s%(course_prefix_letter)s%(course_number)s_%(section_number)s_%(year)04d_%(term)d' % fields


generate_pamacea_string = generate_ldap_string

def parse_ldap_string(s):
    pattern = re.compile("\n        CU([^\\_]+)_ # 'course' or 'instr'\n        (\\D{4}) # exactly four letters in 'department_code'.\n        (\\D)    # exactly one letter in 'prefix'.\n        ([^_]{4}) # exactly four chars in 'course_number'.\n        _\n        (\\d{3}) # exactly three digits in 'section'.\n        _\n        (\\d{4}) # exactly four digits 'year'.\n        _\n        ([1-3]) # number 1,2, or 3 in 'term'.\n        ", re.VERBOSE)
    r = pattern.search(s)
    if r is None:
        raise InvalidLDAPString
    t = r.groups()
    return dict(member='faculty' if t[0] == 'instr' else 'student', term=TERMS[(int(t[6]) - 1)], year=int(t[5]), section_number=t[4], course_prefix_letter=t[2].lower(), course_number=t[3].lower(), department_id=t[1].lower().strip('_'))


parse_pamacea_string = parse_ldap_string

def generate_course_directory_string(**kwargs):
    fields = kwargs
    fields['term'] = TERMS.index(fields['term']) + 1
    fields['course_prefix_letter'] = fields['course_prefix_letter'].upper()
    fields['department_id'] = pad_to_four(fields['department_id'].upper())
    fields['course_number'] = fields['course_number'].upper()
    return '%(year)04d%(term)d%(department_id)s%(course_number)s%(course_prefix_letter)s%(section_number)s' % fields


def parse_course_directory_string(s):
    pattern = re.compile("\n        (\\d{4}) # exactly four digits in 'year'.\n        ([1-3]) # exactly one digit in 'term'.\n        (\\D{4}) # exactly four letters in 'department_code'.\n        (\\w{4}) # exactly four chars in 'course_number'.\n        (\\D)    # exactly one letter in 'prefix'.\n        (\\d{3}) # exactly 3 digits in 'section'.\n        ", re.VERBOSE)
    r = pattern.search(s)
    if r is None:
        raise InvalidCourseDirString
    t = r.groups()
    return dict(term=TERMS[(int(t[1]) - 1)], year=int(t[0]), section_number=t[5], course_prefix_letter=t[4].lower(), course_number=t[3].lower(), department_id=t[2].lower().strip('_'), member=None)