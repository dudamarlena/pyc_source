# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\datadict.py
# Compiled at: 2017-01-26 21:09:36
# Size of source mod 2**32: 8788 bytes
"""Access dicom dictionary information"""
import logging
logger = logging.getLogger('pydicom')
from dicom.tag import Tag
from dicom._dicom_dict import DicomDictionary
from dicom._dicom_dict import RepeatersDictionary
from dicom._private_dict import private_dictionaries
import warnings
from dicom import in_py3
masks = {}
for mask_x in RepeatersDictionary:
    mask1 = int(mask_x.replace('x', '0'), 16)
    mask2 = int(''.join(['F0'[(c == 'x')] for c in mask_x]), 16)
    masks[mask_x] = (mask1, mask2)

shortNames = [
 ('BeamLimitingDevice', 'BLD'),
 ('RTBeamLimitingDevice', 'RTBLD'),
 ('ControlPoint', 'CP'),
 ('Referenced', 'Refd')]

def mask_match(tag):
    for mask_x, (mask1, mask2) in list(masks.items()):
        if (tag ^ mask1) & mask2 == 0:
            return mask_x


def get_entry(tag):
    """Return the tuple (VR, VM, name, is_retired, keyword) from the DICOM dictionary

    If the entry is not in the main dictionary, check the masked ones,
    e.g. repeating groups like 50xx, etc.
    """
    tag = Tag(tag)
    try:
        return DicomDictionary[tag]
    except KeyError:
        mask_x = mask_match(tag)
        if mask_x:
            return RepeatersDictionary[mask_x]
        raise KeyError('Tag {0} not found in DICOM dictionary'.format(tag))


def dictionary_description(tag):
    """Return the descriptive text for the given dicom tag."""
    return get_entry(tag)[2]


def dictionaryVM(tag):
    """Return the dicom value multiplicity for the given dicom tag."""
    return get_entry(tag)[1]


def dictionaryVR(tag):
    """Return the dicom value representation for the given dicom tag."""
    return get_entry(tag)[0]


def dictionary_has_tag(tag):
    """Return True if the dicom dictionary has an entry for the given tag."""
    return tag in DicomDictionary


def dictionary_keyword(tag):
    """Return the official DICOM standard (since 2011) keyword for the tag"""
    return get_entry(tag)[4]


chars_to_remove = ' !@#$%^&*(),;:.?\\|{}[]+-="\'’/'
if in_py3:
    translate_table = dict((ord(char), None) for char in chars_to_remove)
else:
    import string
    translate_table = string.maketrans('', '')

def keyword_for_tag(tag):
    """Return the DICOM keyword for the given tag. Replaces old CleanName()
    method using the 2011 DICOM standard keywords instead.

    Will return GroupLength for group length tags,
    and returns empty string ("") if the tag doesn't exist in the dictionary.
    """
    try:
        return dictionary_keyword(tag)
    except KeyError:
        return ''


def CleanName(tag):
    """Return the dictionary descriptive text string but without bad characters.

    Used for e.g. *named tags* of Dataset instances (before DICOM keywords were
    part of the standard)

    """
    tag = Tag(tag)
    if tag not in DicomDictionary:
        if tag.element == 0:
            return 'GroupLength'
        return ''
    s = dictionary_description(tag)
    if in_py3:
        s = s.translate(translate_table)
    else:
        s = s.translate(translate_table, chars_to_remove)
    if dictionaryVR(tag) == 'SQ' and not s.startswith('OtherPatientIDs') and s.endswith('Sequence'):
        s = s[:-8] + 's'
        if s.endswith('ss'):
            s = s[:-1]
        if s.endswith('xs'):
            s = s[:-1] + 'es'
        if s.endswith('Studys'):
            s = s[:-2] + 'ies'
    return s


logger.debug('Reversing DICOM dictionary so can look up tag from a name...')
NameDict = dict([(CleanName(tag), tag) for tag in DicomDictionary])
keyword_dict = dict([(dictionary_keyword(tag), tag) for tag in DicomDictionary])

def short_name(name):
    """Return a short *named tag* for the corresponding long version.

    Return a blank string if there is no short version of the name.

    """
    for longname, shortname in shortNames:
        if name.startswith(longname):
            return name.replace(longname, shortname)

    return ''


def long_name(name):
    """Return a long *named tag* for the corresponding short version.

    Return a blank string if there is no long version of the name.

    """
    for longname, shortname in shortNames:
        if name.startswith(shortname):
            return name.replace(shortname, longname)

    return ''


def tag_for_name(name):
    """Return the dicom tag corresponding to name, or None if none exist."""
    if name in keyword_dict:
        return keyword_dict[name]
    if name in NameDict:
        tag = NameDict[name]
        msg = "'%s' as tag name has been deprecated; use official DICOM keyword '%s'" % (
         name, dictionary_keyword(tag))
        warnings.warn(msg, DeprecationWarning)
        return tag
    longname = long_name(name)
    if longname:
        return NameDict.get(longname, None)


def all_names_for_tag(tag):
    """Return a list of all (long and short) names for the tag"""
    longname = keyword_for_tag(tag)
    shortname = short_name(longname)
    names = [longname]
    if shortname:
        names.append(shortname)
    return names


def get_private_entry(tag, private_creator):
    """Return the tuple (VR, VM, name, is_retired) from a private dictionary"""
    tag = Tag(tag)
    try:
        private_dict = private_dictionaries[private_creator]
    except KeyError:
        raise KeyError('Private creator {0} not in private dictionary'.format(private_creator))

    try:
        dict_entry = private_dict[tag]
    except KeyError:
        group_str = '%04x' % tag.group
        elem_str = '%04x' % tag.elem
        key = '%sxx%s' % (group_str, elem_str[-2:])
        if key not in private_dict:
            raise KeyError('Tag {0} not in private dictionary for private creator {1}'.format(key, private_creator))
        dict_entry = private_dict[key]

    return dict_entry


def private_dictionary_description(tag, private_creator):
    """Return the descriptive text for the given dicom tag."""
    return get_private_entry(tag, private_creator)[2]


def private_dictionaryVM(tag, private_creator):
    """Return the dicom value multiplicity for the given dicom tag."""
    return get_private_entry(tag, private_creator)[1]


def private_dictionaryVR(tag, private_creator):
    """Return the dicom value representation for the given dicom tag."""
    return get_private_entry(tag, private_creator)[0]