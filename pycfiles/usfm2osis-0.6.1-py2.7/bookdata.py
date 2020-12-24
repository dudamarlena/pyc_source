# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/usfm2osis/bookdata.py
# Compiled at: 2015-05-07 21:33:17
"""usfm2osis.data

Copyright 2012-2015 by Christopher C. Little

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full text of the GNU General Public License is available at:
<http://www.gnu.org/licenses/gpl-3.0.txt>.
"""
from __future__ import unicode_literals
bookDict = {b'GEN': b'Gen', 
   b'EXO': b'Exod', b'LEV': b'Lev', b'NUM': b'Num', b'DEU': b'Deut', b'JOS': b'Josh', 
   b'JDG': b'Judg', b'RUT': b'Ruth', b'1SA': b'1Sam', b'2SA': b'2Sam', b'1KI': b'1Kgs', 
   b'2KI': b'2Kgs', b'1CH': b'1Chr', b'2CH': b'2Chr', b'EZR': b'Ezra', b'NEH': b'Neh', 
   b'EST': b'Esth', b'JOB': b'Job', b'PSA': b'Ps', b'PRO': b'Prov', b'ECC': b'Eccl', 
   b'SNG': b'Song', b'ISA': b'Isa', b'JER': b'Jer', b'LAM': b'Lam', b'EZK': b'Ezek', 
   b'DAN': b'Dan', b'HOS': b'Hos', b'JOL': b'Joel', b'AMO': b'Amos', b'OBA': b'Obad', 
   b'JON': b'Jonah', b'MIC': b'Mic', b'NAM': b'Nah', b'HAB': b'Hab', b'ZEP': b'Zeph', 
   b'HAG': b'Hag', b'ZEC': b'Zech', b'MAL': b'Mal', b'MAT': b'Matt', 
   b'MRK': b'Mark', b'LUK': b'Luke', b'JHN': b'John', b'ACT': b'Acts', b'ROM': b'Rom', 
   b'1CO': b'1Cor', b'2CO': b'2Cor', b'GAL': b'Gal', b'EPH': b'Eph', b'PHP': b'Phil', 
   b'COL': b'Col', b'1TH': b'1Thess', b'2TH': b'2Thess', b'1TI': b'1Tim', b'2TI': b'2Tim', 
   b'TIT': b'Titus', b'PHM': b'Phlm', b'HEB': b'Heb', b'JAS': b'Jas', b'1PE': b'1Pet', 
   b'2PE': b'2Pet', b'1JN': b'1John', b'2JN': b'2John', b'3JN': b'3John', b'JUD': b'Jude', 
   b'REV': b'Rev', b'TOB': b'Tob', 
   b'JDT': b'Jdt', b'ESG': b'EsthGr', b'WIS': b'Wis', b'SIR': b'Sir', b'BAR': b'Bar', 
   b'LJE': b'EpJer', b'S3Y': b'PrAzar', b'SUS': b'Sus', b'BEL': b'Bel', b'1MA': b'1Macc', 
   b'2MA': b'2Macc', b'3MA': b'3Macc', 
   b'4MA': b'4Macc', b'1ES': b'1Esd', b'2ES': b'2Esd', b'MAN': b'PrMan', b'PS2': b'AddPs', 
   b'ODA': b'Odes', 
   b'PSS': b'PssSol', b'EZA': b'4Ezra', 
   b'5EZ': b'5Ezra', b'6EZ': b'6Ezra', b'DAG': b'DanGr', 
   b'PS3': b'5ApocSyrPss', 
   b'2BA': b'2Bar', b'LBA': b'EpBar', b'JUB': b'Jub', 
   b'ENO': b'1En', b'1MQ': b'1Meq', b'2MQ': b'2Meq', b'3MQ': b'3Meq', b'REP': b'Reproof', 
   b'4BA': b'4Bar', b'LAO': b'EpLao', 
   b'XXA': b'XXA', 
   b'XXB': b'XXB', b'XXC': b'XXC', b'XXD': b'XXD', b'XXE': b'XXE', b'XXF': b'XXF', 
   b'XXG': b'XXG', b'FRT': b'FRONT', 
   b'INT': b'INTRODUCTION', b'BAK': b'BACK', b'CNC': b'CONCORDANCE', b'GLO': b'GLOSSARY', 
   b'TDX': b'INDEX', b'NDX': b'GAZETTEER', b'OTH': b'X-OTHER'}
addBookDict = {b'JSA': b'JoshA', 
   b'JDB': b'JudgB', b'TBS': b'TobS', b'SST': b'SusTh', b'DNT': b'DanTh', b'BLT': b'BelTh', 
   b'4ES': b'4Ezra', 
   b'5ES': b'5Ezra', b'6ES': b'6Ezra', b'PSB': b'PsMet', 
   b'PSO': b'PrSol', 
   b'PJE': b'PrJer', b'WSI': b'WSir', 
   b'COP': b'EpCorPaul', b'3CO': b'3Cor', b'EUT': b'PrEuth', b'DOJ': b'DormJohn', 
   b'1CL': b'1Clem', 
   b'2CL': b'2Clem', b'SHE': b'Herm', b'LBA': b'Barn', b'DID': b'Did', b'ODE': b'Odes', 
   b'ADE': b'AddEsth'}
canonicalOrder = [
 b'FRONT', b'INTRODUCTION',
 b'Gen', b'Exod', b'Lev', b'Num', b'Deut', b'Josh', b'JoshA', b'Judg', b'JudgB',
 b'Ruth', b'1Sam', b'2Sam', b'1Kgs', b'2Kgs', b'1Chr', b'2Chr', b'PrMan', b'Jub',
 b'1En', b'Ezra', b'Neh', b'Tob', b'TobS', b'Jdt', b'Esth', b'EsthGr', b'AddEsth',
 b'1Meq', b'2Meq', b'3Meq', b'Job', b'Ps', b'AddPs', b'5ApocSyrPss', b'PsMet',
 b'Odes', b'Prov', b'Reproof', b'Eccl', b'Song', b'Wis', b'Sir', b'WSir', b'PrSol',
 b'PssSol', b'Isa', b'Jer', b'Lam', b'PrJer', b'Bar', b'EpJer', b'2Bar', b'EpBar',
 b'4Bar', b'Ezek', b'Dan', b'DanGr', b'DanTh', b'PrAzar', b'Sus', b'SusTh', b'Bel',
 b'BelTh', b'Hos', b'Joel', b'Amos', b'Obad', b'Jonah', b'Mic', b'Nah', b'Hab',
 b'Zeph', b'Hag', b'Zech', b'Mal',
 b'1Esd', b'2Esd', b'4Ezra', b'5Ezra', b'6Ezra', b'1Macc', b'2Macc', b'3Macc',
 b'4Macc',
 b'Matt', b'Mark', b'Luke', b'John', b'Acts', b'Rom', b'1Cor', b'2Cor', b'Gal', b'Eph',
 b'Phil', b'Col', b'1Thess', b'2Thess', b'1Tim', b'2Tim', b'Titus', b'Phlm', b'Heb',
 b'Jas', b'1Pet', b'2Pet', b'1John', b'2John', b'3John', b'Jude', b'Rev',
 b'EpLao', b'EpCorPaul', b'3Cor', b'PrEuth', b'DormJohn',
 b'1Clem', b'2Clem', b'Herm', b'Barn', b'Did',
 b'XXA', b'XXB', b'XXC', b'XXD', b'XXE', b'XXF', b'XXG',
 b'BACK', b'CONCORDANCE', b'GLOSSARY', b'INDEX', b'GAZETTEER', b'X-OTHER']
usfmNumericOrder = [
 b'FRONT', b'INTRODUCTION',
 b'Gen', b'Exod', b'Lev', b'Num', b'Deut', b'Josh', b'Judg', b'Ruth', b'1Sam', b'2Sam',
 b'1Kgs', b'2Kgs', b'1Chr', b'2Chr', b'Ezra', b'Neh', b'Esth', b'Job', b'Ps', b'Prov',
 b'Eccl', b'Song', b'Isa', b'Jer', b'Lam', b'Ezek', b'Dan', b'Hos', b'Joel', b'Amos',
 b'Obad', b'Jonah', b'Mic', b'Nah', b'Hab', b'Zeph', b'Hag', b'Zech', b'Mal',
 b'Matt', b'Mark', b'Luke', b'John', b'Acts', b'Rom', b'1Cor', b'2Cor', b'Gal', b'Eph',
 b'Phil', b'Col', b'1Thess', b'2Thess', b'1Tim', b'2Tim', b'Titus', b'Phlm', b'Heb',
 b'Jas', b'1Pet', b'2Pet', b'1John', b'2John', b'3John', b'Jude', b'Rev',
 b'Tob', b'Jdt', b'EsthGr', b'AddEsth', b'Wis', b'Sir', b'Bar', b'EpJer', b'PrAzar',
 b'Sus', b'Bel', b'1Macc', b'2Macc', b'3Macc', b'4Macc', b'1Esd', b'2Esd', b'PrMan',
 b'AddPs', b'Odes', b'PssSol',
 b'4Ezra', b'5Ezra', b'6Ezra',
 b'DanGr', b'5ApocSyrPss', b'2Bar', b'EpBar', b'Jub', b'1En', b'1Meq', b'2Meq',
 b'3Meq', b'Reproof', b'4Bar', b'EpLao',
 b'PsMet',
 b'PrSol', b'PrJer',
 b'WSir', b'EpCorPaul', b'3Cor', b'PrEuth', b'DormJohn',
 b'1Clem', b'2Clem', b'Herm', b'Barn', b'Did',
 b'JoshA', b'JudgB', b'TobS', b'DanTh', b'SusTh', b'BelTh',
 b'XXA', b'XXB', b'XXC', b'XXD', b'XXE', b'XXF', b'XXG',
 b'BACK', b'CONCORDANCE', b'GLOSSARY', b'INDEX', b'GAZETTEER', b'X-OTHER']
specialBooks = [
 b'FRONT', b'INTRODUCTION', b'BACK', b'CONCORDANCE', b'GLOSSARY',
 b'INDEX', b'GAZETTEER', b'X-OTHER']
peripherals = {b'Title Page': b'titlePage', 
   b'Half Title Page': b'x-halfTitlePage', b'Promotional Page': b'x-promotionalPage', 
   b'Imprimatur': b'imprimatur', b'Publication Data': b'publicationData', 
   b'Foreword': b'x-foreword', b'Preface': b'preface', 
   b'Table of Contents': b'tableofContents', b'Alphabetical Contents': b'x-alphabeticalContents', 
   b'Table of Abbreviations': b'x-tableofAbbreviations', 
   b'Chronology': b'x-chronology', 
   b'Weights and Measures': b'x-weightsandMeasures', b'Map Index': b'x-mapIndex', 
   b'NT Quotes from LXX': b'x-ntQuotesfromLXX', b'Cover': b'coverPage', 
   b'Spine': b'x-spine'}
introPeripherals = {b'Bible Introduction': b'bible', 
   b'Old Testament Introduction': b'oldTestament', b'Pentateuch Introduction': b'pentateuch', 
   b'History Introduction': b'history', b'Poetry Introduction': b'poetry', 
   b'Prophecy Introduction': b'prophecy', b'New Testament Introduction': b'newTestament', 
   b'Gospels Introduction': b'gospels', 
   b'Acts Introduction': b'acts', b'Epistles Introduction': b'epistles', 
   b'Letters Introduction': b'letters', b'Deuterocanon Introduction': b'deuterocanon'}
filename2osis = dict()