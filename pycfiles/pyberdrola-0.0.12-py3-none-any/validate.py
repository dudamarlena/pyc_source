# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\Subrata Sarkar\Text\Class XI\kaka\bangla key1.4\banglakey1.4\BanglaKey 3.0\pyhinavrophonetic\utils\validate.py
# Compiled at: 2016-09-21 07:14:30
__doc__ = 'Python implementation of Avro Phonetic in hindi.\n\n-------------------------------------------------------------------------------\nCopyright (C) 2016 Subrata Sarkar <subrotosarkar32@gmail.com>\nmodified by:- Subrata Sarkar <subrotosarkar32@gmail.com>\noriginal by:- Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.\nCopyright (C) 2013 Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.\n\nThis file is part of pyAvroPhonetic.\n\npyAvroPhonetic is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\npyAvroPhonetic is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with pyAvroPhonetic.  If not, see <http://www.gnu.org/licenses/>.\n\n'
import config

def is_vowel(text):
    """Check if given string is a vowel"""
    return text.lower() in config.AVRO_VOWELS


def is_consonant(text):
    """Check if given string is a consonant"""
    return text.lower() in config.AVRO_CONSONANTS


def is_number(text):
    """Check if given string is a number"""
    return text.lower() in config.AVRO_NUMBERS


def is_punctuation(text):
    """Check if given string is a punctuation"""
    return not (text.lower() in config.AVRO_VOWELS or text.lower() in config.AVRO_CONSONANTS)


def is_case_sensitive(text):
    """Check if given string is case sensitive"""
    return text.lower() in config.AVRO_CASESENSITIVES


def is_exact(needle, haystack, start, end, matchnot):
    """Check exact occurrence of needle in haystack"""
    return (start >= 0 and end < len(haystack) and haystack[start:end] == needle) ^ matchnot


def fix_string_case(text):
    """Converts case-insensitive characters to lower case

    Case-sensitive characters as defined in config.AVRO_CASESENSITIVES
    retain their case, but others are converted to their lowercase
    equivalents. The result is a string with phonetic-compatible case
    which will the parser will understand without confusion.
    """
    fixed = []
    for i in text:
        if is_case_sensitive(i):
            fixed.append(i)
        else:
            fixed.append(i.lower())

    return ('').join(fixed)