# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/omkarpathak27/Documents/GITS/py-resume-parser/pyresparser/constants.py
# Compiled at: 2019-11-09 21:30:55
# Size of source mod 2**32: 1743 bytes
from nltk.corpus import stopwords
NAME_PATTERN = [
 {'POS': 'PROPN'}, {'POS': 'PROPN'}]
EDUCATION = [
 'BE', 'B.E.', 'B.E', 'BS', 'B.S', 'ME', 'M.E',
 'M.E.', 'MS', 'M.S', 'BTECH', 'MTECH',
 'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII']
NOT_ALPHA_NUMERIC = '[^a-zA-Z\\d]'
NUMBER = '\\d+'
MONTHS_SHORT = '(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)\n                   |(aug)|(sep)|(oct)|(nov)|(dec)'
MONTHS_LONG = '(january)|(february)|(march)|(april)|(may)|(june)|(july)|\n                   (august)|(september)|(october)|(november)|(december)'
MONTH = '(' + MONTHS_SHORT + '|' + MONTHS_LONG + ')'
YEAR = '(((20|19)(\\d{2})))'
STOPWORDS = set(stopwords.words('english'))
RESUME_SECTIONS_PROFESSIONAL = [
 'experience',
 'education',
 'interests',
 'professional experience',
 'publications',
 'skills',
 'certifications',
 'objective',
 'career objective',
 'summary',
 'leadership']
RESUME_SECTIONS_GRAD = [
 'accomplishments',
 'experience',
 'education',
 'interests',
 'projects',
 'professional experience',
 'publications',
 'skills',
 'certifications',
 'objective',
 'career objective',
 'summary',
 'leadership']