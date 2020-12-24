# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/dignities/tables.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 11543 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)
    
    This module defines relevant tables, such as
    the Essential Dignities.
  
"""
SIGN_LIST = [
 'Belier', 'Tareau', 'Gemaux', 'Cancer',
 'Lion', 'Vierge', 'Balance', 'Scorpion',
 'Sagittaire', 'Capricorne', 'Verseau',
 'Poisson']
CHALDEAN_FACES = {'Belier':[
  'Mars', 'Soleil', 'Venus'], 
 'Taureau':[
  'Mercure', 'Lune', 'Saturne'], 
 'Gemaux':[
  'Jupiter', 'Mars', 'Soleil'], 
 'Cancer':[
  'Venus', 'Mercure', 'Lune'], 
 'Lion':[
  'Saturne', 'Jupiter', 'Mars'], 
 'Vierge':[
  'Soleil', 'Venus', 'Mercure'], 
 'Balance':[
  'Lune', 'Saturne', 'Jupiter'], 
 'Scorpion':[
  'Mars', 'Soleil', 'Venus'], 
 'Sagittaire':[
  'Mercure', 'Lune', 'Saturne'], 
 'Capricorne':[
  'Jupiter', 'Mars', 'Soleil'], 
 'Verseau':[
  'Venus', 'Mercure', 'Lune'], 
 'Poisson':[
  'Saturne', 'Jupiter', 'Mars']}
TRIPLICITY_FACES = {'Belier':[
  'Mars', 'Soleil', 'Jupiter'], 
 'Taureau':[
  'Venus', 'Mercure', 'Saturne'], 
 'Gemaux':[
  'Mercure', 'Venus', 'Saturne'], 
 'Cancer':[
  'Moon', 'Mars', 'Jupiter'], 
 'Lion':[
  'Soleil', 'Jupiter', 'Mars'], 
 'Vierge':[
  'Mercure', 'Saturne', 'Venus'], 
 'Balance':[
  'Venus', 'Saturne', 'Mercure'], 
 'Scorpion':[
  'Mars', 'Jupiter', 'Moon'], 
 'Sagittaire':[
  'Jupiter', 'Mars', 'Soleil'], 
 'Capricorne':[
  'Saturne', 'Venus', 'Mercure'], 
 'Verseau':[
  'Saturne', 'Mercure', 'Venus'], 
 'Poisson':[
  'Jupiter', 'Moon', 'Mars']}
EGYPTIAN_TERMS = {'Belier':[
  [
   'Jupiter', 0, 6],
  [
   'Venus', 6, 12],
  [
   'Mercure', 12, 20],
  [
   'Mars', 20, 25],
  [
   'Saturne', 25, 30]], 
 'Taureau':[
  [
   'Venus', 0, 8],
  [
   'Mercure', 8, 14],
  [
   'Jupiter', 14, 22],
  [
   'Saturne', 22, 27],
  [
   'Mars', 27, 30]], 
 'Gemaux':[
  [
   'Mercure', 0, 6],
  [
   'Jupiter', 6, 12],
  [
   'Venus', 12, 17],
  [
   'Mars', 17, 24],
  [
   'Saturne', 24, 30]], 
 'Cancer':[
  [
   'Mars', 0, 7],
  [
   'Venus', 7, 13],
  [
   'Mercure', 13, 19],
  [
   'Jupiter', 19, 26],
  [
   'Saturne', 26, 30]], 
 'Lion':[
  [
   'Jupiter', 0, 6],
  [
   'Venus', 6, 11],
  [
   'Saturne', 11, 18],
  [
   'Mercure', 18, 24],
  [
   'Mars', 24, 30]], 
 'Vierge':[
  [
   'Mercure', 0, 7],
  [
   'Venus', 7, 17],
  [
   'Jupiter', 17, 21],
  [
   'Mars', 21, 28],
  [
   'Saturne', 28, 30]], 
 'Balance':[
  [
   'Saturne', 0, 6],
  [
   'Mercure', 6, 14],
  [
   'Jupiter', 14, 21],
  [
   'Venus', 21, 28],
  [
   'Mars', 28, 30]], 
 'Scorpion':[
  [
   'Mars', 0, 7],
  [
   'Venus', 7, 11],
  [
   'Mercure', 11, 19],
  [
   'Jupiter', 19, 24],
  [
   'Saturne', 24, 30]], 
 'Sagittaire':[
  [
   'Jupiter', 0, 12],
  [
   'Venus', 12, 17],
  [
   'Mercure', 17, 21],
  [
   'Saturne', 21, 26],
  [
   'Mars', 26, 30]], 
 'Capricorne':[
  [
   'Mercure', 0, 7],
  [
   'Jupiter', 7, 14],
  [
   'Venus', 14, 22],
  [
   'Saturne', 22, 26],
  [
   'Mars', 26, 30]], 
 'Verseau':[
  [
   'Mercure', 0, 7],
  [
   'Venus', 7, 13],
  [
   'Jupiter', 13, 20],
  [
   'Mars', 20, 25],
  [
   'Saturne', 25, 30]], 
 'Poisson':[
  [
   'Venus', 0, 12],
  [
   'Jupiter', 12, 16],
  [
   'Mercure', 16, 19],
  [
   'Mars', 19, 28],
  [
   'Saturne', 28, 30]]}
TETRABIBLOS_TERMS = {'Belier':[
  [
   'Jupiter', 0, 6],
  [
   'Venus', 6, 14],
  [
   'Mercure', 14, 21],
  [
   'Mars', 21, 26],
  [
   'Saturne', 26, 30]], 
 'Taureau':[
  [
   'Venus', 0, 8],
  [
   'Mercure', 8, 15],
  [
   'Jupiter', 15, 22],
  [
   'Saturne', 22, 24],
  [
   'Mars', 24, 30]], 
 'Gemaux':[
  [
   'Mercure', 0, 7],
  [
   'Jupiter', 7, 13],
  [
   'Venus', 13, 20],
  [
   'Mars', 20, 26],
  [
   'Saturne', 26, 30]], 
 'Cancer':[
  [
   'Mars', 0, 6],
  [
   'Jupiter', 6, 13],
  [
   'Mercure', 13, 20],
  [
   'Venus', 20, 27],
  [
   'Saturne', 27, 30]], 
 'Lion':[
  [
   'Jupiter', 0, 6],
  [
   'Mercure', 6, 13],
  [
   'Saturne', 13, 19],
  [
   'Venus', 19, 25],
  [
   'Mars', 25, 30]], 
 'Vierge':[
  [
   'Mercure', 0, 7],
  [
   'Venus', 7, 13],
  [
   'Jupiter', 13, 18],
  [
   'Saturne', 18, 24],
  [
   'Mars', 24, 30]], 
 'Balance':[
  [
   'Saturne', 0, 6],
  [
   'Venus', 6, 11],
  [
   'Mercure', 11, 16],
  [
   'Jupiter', 16, 24],
  [
   'Mars', 24, 30]], 
 'Scorpion':[
  [
   'Mars', 0, 6],
  [
   'Venus', 6, 13],
  [
   'Jupiter', 13, 21],
  [
   'Mercure', 21, 27],
  [
   'Saturne', 27, 30]], 
 'Sagittaire':[
  [
   'Jupiter', 0, 8],
  [
   'Venus', 8, 14],
  [
   'Mercure', 14, 19],
  [
   'Saturne', 19, 25],
  [
   'Mars', 25, 30]], 
 'Capricorne':[
  [
   'Venus', 0, 6],
  [
   'Mercure', 6, 12],
  [
   'Jupiter', 12, 19],
  [
   'Saturne', 19, 25],
  [
   'Mars', 25, 30]], 
 'Verseau':[
  [
   'Saturne', 0, 6],
  [
   'Mercure', 6, 12],
  [
   'Venus', 12, 20],
  [
   'Jupiter', 20, 25],
  [
   'Mars', 25, 30]], 
 'Poisson':[
  [
   'Venus', 0, 8],
  [
   'Jupiter', 8, 14],
  [
   'Mercure', 14, 20],
  [
   'Mars', 20, 25],
  [
   'Saturne', 25, 30]]}
LILLY_TERMS = {'Belier':[
  [
   'Jupiter', 0, 6],
  [
   'Venus', 6, 14],
  [
   'Mercure', 14, 21],
  [
   'Mars', 21, 26],
  [
   'Saturne', 26, 30]], 
 'Taureau':[
  [
   'Venus', 0, 8],
  [
   'Mercure', 8, 15],
  [
   'Jupiter', 15, 22],
  [
   'Saturne', 22, 26],
  [
   'Mars', 26, 30]], 
 'Gemaux':[
  [
   'Mercure', 0, 7],
  [
   'Jupiter', 7, 14],
  [
   'Venus', 14, 21],
  [
   'Saturne', 21, 25],
  [
   'Mars', 25, 30]], 
 'Cancer':[
  [
   'Mars', 0, 6],
  [
   'Jupiter', 6, 13],
  [
   'Mercure', 13, 20],
  [
   'Venus', 20, 27],
  [
   'Saturne', 27, 30]], 
 'Lion':[
  [
   'Saturne', 0, 6],
  [
   'Mercure', 6, 13],
  [
   'Venus', 13, 19],
  [
   'Jupiter', 19, 25],
  [
   'Mars', 25, 30]], 
 'Vierge':[
  [
   'Mercure', 0, 7],
  [
   'Venus', 7, 13],
  [
   'Jupiter', 13, 18],
  [
   'Saturne', 18, 24],
  [
   'Mars', 24, 30]], 
 'Balance':[
  [
   'Saturne', 0, 6],
  [
   'Venus', 6, 11],
  [
   'Jupiter', 11, 19],
  [
   'Mercure', 19, 24],
  [
   'Mars', 24, 30]], 
 'Scorpion':[
  [
   'Mars', 0, 6],
  [
   'Jupiter', 6, 14],
  [
   'Venus', 14, 21],
  [
   'Mercure', 21, 27],
  [
   'Saturne', 27, 30]], 
 'Sagittaire':[
  [
   'Jupiter', 0, 8],
  [
   'Venus', 8, 14],
  [
   'Mercure', 14, 19],
  [
   'Saturne', 19, 25],
  [
   'Mars', 25, 30]], 
 'Capricorne':[
  [
   'Venus', 0, 6],
  [
   'Mercure', 6, 12],
  [
   'Jupiter', 12, 19],
  [
   'Mars', 19, 25],
  [
   'Saturne', 25, 30]], 
 'Verseau':[
  [
   'Saturne', 0, 6],
  [
   'Mercure', 6, 12],
  [
   'Venus', 12, 20],
  [
   'Jupiter', 20, 25],
  [
   'Mars', 25, 30]], 
 'Poisson':[
  [
   'Venus', 0, 8],
  [
   'Jupiter', 8, 14],
  [
   'Mercure', 14, 20],
  [
   'Mars', 20, 25],
  [
   'Saturne', 25, 30]]}
ESSENTIAL_DIGNITIES = {'Belier':{'ruler':'Mars', 
  'exalt':[
   'Soleil', 19], 
  'trip':[
   'Soleil', 'Jupiter', 'Saturne'], 
  'faces':[
   'Mars', 'Soleil', 'Venus'], 
  'exile':'Venus', 
  'fall':[
   'Saturne', 21]}, 
 'Taureau':{'ruler':'Venus', 
  'exalt':[
   'Moon', 3], 
  'trip':[
   'Venus', 'Moon', 'Mars'], 
  'faces':[
   'Mercure', 'Moon', 'Saturne'], 
  'exile':'Mars', 
  'fall':[
   None, 0]}, 
 'Gemaux':{'ruler':'Mercure', 
  'exalt':[
   None, 0], 
  'trip':[
   'Saturne', 'Mercure', 'Jupiter'], 
  'faces':[
   'Jupiter', 'Mars', 'Soleil'], 
  'exile':'Jupiter', 
  'fall':[
   None, 0]}, 
 'Cancer':{'ruler':'Moon', 
  'exalt':[
   'Jupiter', 15], 
  'trip':[
   'Venus', 'Mars', 'Moon'], 
  'faces':[
   'Venus', 'Mercure', 'Moon'], 
  'exile':'Saturne', 
  'fall':[
   'Mars', 28]}, 
 'Lion':{'ruler':'Soleil', 
  'exalt':[
   None, 0], 
  'trip':[
   'Soleil', 'Jupiter', 'Saturne'], 
  'faces':[
   'Saturne', 'Jupiter', 'Mars'], 
  'exile':'Saturne', 
  'fall':[
   None, 0]}, 
 'Vierge':{'ruler':'Mercure', 
  'exalt':[
   'Mercure', 15], 
  'trip':[
   'Venus', 'Moon', 'Mars'], 
  'faces':[
   'Soleil', 'Venus', 'Mercure'], 
  'exile':'Jupiter', 
  'fall':[
   'Venus', 27]}, 
 'Balance':{'ruler':'Venus', 
  'exalt':[
   'Saturne', 21], 
  'trip':[
   'Saturne', 'Mercure', 'Jupiter'], 
  'faces':[
   'Moon', 'Saturne', 'Jupiter'], 
  'exile':'Mars', 
  'fall':[
   'Soleil', 19]}, 
 'Scorpion':{'ruler':'Mars', 
  'exalt':[
   None, 0], 
  'trip':[
   'Venus', 'Mars', 'Moon'], 
  'faces':[
   'Mars', 'Soleil', 'Venus'], 
  'exile':'Venus', 
  'fall':[
   'Moon', 3]}, 
 'Sagittaire':{'ruler':'Jupiter', 
  'exalt':[
   None, 0], 
  'trip':[
   'Soleil', 'Jupiter', 'Saturne'], 
  'faces':[
   'Mercure', 'Moon', 'Saturne'], 
  'exile':'Mercure', 
  'fall':[
   None, 0]}, 
 'Capricorne':{'ruler':'Saturne', 
  'exalt':[
   'Mars', 28], 
  'trip':[
   'Venus', 'Moon', 'Mars'], 
  'faces':[
   'Jupiter', 'Mars', 'Soleil'], 
  'exile':'Moon', 
  'fall':[
   'Jupiter', 15]}, 
 'Verseau':{'ruler':'Saturne', 
  'exalt':[
   None, 0], 
  'trip':[
   'Saturne', 'Mercure', 'Jupiter'], 
  'faces':[
   'Venus', 'Mercure', 'Moon'], 
  'exile':'Soleil', 
  'fall':[
   None, 0]}, 
 'Poisson':{'ruler':'Jupiter', 
  'exalt':[
   'Venus', 27], 
  'trip':[
   'Venus', 'Mars', 'Moon'], 
  'faces':[
   'Saturne', 'Jupiter', 'Mars'], 
  'exile':'Mercure', 
  'fall':[
   'Mercure', 15]}}

def termLons(TERMS):
    """ Returns a list with the absolute longitude 
    of all terms.
    
    """
    res = []
    for i, sign in enumerate(SIGN_LIST):
        termList = TERMS[sign]
        res.extend(([ID, sign, start + 30 * i] for ID, start, end in termList))

    return res