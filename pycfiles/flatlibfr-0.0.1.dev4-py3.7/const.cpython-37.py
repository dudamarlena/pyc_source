# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/const.py
# Compiled at: 2019-10-17 02:47:07
# Size of source mod 2**32: 6631 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module defines the names of signs, objects, angles, 
    houses and fixed-stars used in the library.

"""
HOT = 'Chaud'
COLD = 'Froid'
DRY = 'Sec'
HUMID = 'Humide'
FIRE = 'Feu'
EARTH = 'Terre'
AIR = 'Air'
WATER = 'Eau'
CHOLERIC = 'Bilieux (coléreux)'
MELANCHOLIC = 'Nerveux (mélancholique)'
SANGUINE = 'Sanguin'
PHLEGMATIC = 'Lymphatique (flegmatique)'
MASCULINE = 'Masculin'
FEMININE = 'Feminin'
NEUTRAL = 'Neutre'
DIURNAL = 'Diurne'
NOCTURNAL = 'Nocturne'
SPRING = 'Printemps'
SUMMER = 'Été'
AUTUMN = 'Automne'
WINTER = 'Hivers'
MOON_FIRST_QUARTER = 'Premier quartier'
MOON_SECOND_QUARTER = 'Second quartier'
MOON_THIRD_QUARTER = 'Troisième quarter'
MOON_LAST_QUARTER = 'Dernier quartier'
ARIES = 'Belier'
TAURUS = 'Taureau'
GEMINI = 'Gemaux'
CANCER = 'Cancer'
LEO = 'Lion'
VIRGO = 'Vierge'
LIBRA = 'Balance'
SCORPIO = 'Scorpion'
SAGITTARIUS = 'Sagittaire'
CAPRICORN = 'Capricorne'
AQUARIUS = 'Verseau'
PISCES = 'Poisson'
ID_ARIES = 1
ID_TAURUS = 2
ID_GEMINI = 3
ID_CANCER = 4
ID_LEO = 5
ID_VIRGO = 6
ID_LIBRA = 7
ID_SCORPIO = 8
ID_SAGITTARIUS = 9
ID_CAPRICORN = 10
ID_AQUARIUS = 11
ID_PISCES = 12
CARDINAL = 'Cardinal'
FIXED = 'Fixe'
MUTABLE = 'Mutable'
SIGN_FIGURE_NONE = 'Aucun'
SIGN_FIGURE_BEAST = 'Bête'
SIGN_FIGURE_HUMAN = 'Humain'
SIGN_FIGURE_WILD = 'Sauvage'
SIGN_FERTILE = 'Fertile'
SIGN_STERILE = 'Stérile'
SIGN_MODERATELY_FERTILE = 'Modérément fertile'
SIGN_MODERATELY_STERILE = 'ModerModérémentately stérile'
SUN = 'Soleil'
MOON = 'Lune'
MERCURY = 'Mercure'
VENUS = 'Venus'
MARS = 'Mars'
JUPITER = 'Jupiter'
SATURN = 'Saturne'
URANUS = 'Uranus'
NEPTUNE = 'Neptune'
PLUTO = 'Pluton'
CHIRON = 'Chiron'
NORTH_NODE = 'Noeud nord'
SOUTH_NODE = 'Noeud sud'
SYZYGY = 'Syzygy'
PARS_FORTUNA = 'Part de fortune'
NO_PLANET = 'Aucun'
DIRECT = 'Direct'
RETROGRADE = 'Rétrogade'
STATIONARY = 'Stationnaire'
MEAN_MOTION_SUN = 0.9833
MEAN_MOTION_MOON = 13.1833
OBJ_PLANET = 'Planète'
OBJ_HOUSE = 'Maison'
OBJ_MOON_NODE = 'Noeud de lune'
OBJ_ARABIC_PART = 'Part arabe'
OBJ_FIXED_STAR = 'Étoile fixe'
OBJ_ASTEROID = 'Astéroïde'
OBJ_LUNATION = 'Lunation'
OBJ_GENERIC = 'Générique'
HOUSE1 = 'Maison1'
HOUSE2 = 'Maison2'
HOUSE3 = 'Maison3'
HOUSE4 = 'Maison4'
HOUSE5 = 'Maison5'
HOUSE6 = 'Maison6'
HOUSE7 = 'Maison7'
HOUSE8 = 'Maison8'
HOUSE9 = 'Maison9'
HOUSE10 = 'Maison10'
HOUSE11 = 'Maison11'
HOUSE12 = 'Maison12'
ANGULAR = 'Angulaire'
SUCCEDENT = 'Succédente'
CADENT = 'Cadente'
HOUSES_BENEFIC = [
 HOUSE1, HOUSE5, HOUSE11]
HOUSES_MALEFIC = [HOUSE6, HOUSE12]
HOUSES_PLACIDUS = 'Placidus'
HOUSES_KOCH = 'Koch'
HOUSES_PORPHYRIUS = 'Porphyrius'
HOUSES_REGIOMONTANUS = 'Regiomontanus'
HOUSES_CAMPANUS = 'Campanus'
HOUSES_EQUAL = 'Equal'
HOUSES_EQUAL_2 = 'Equal 2'
HOUSES_VEHLOW_EQUAL = 'Vehlow Equal'
HOUSES_WHOLE_SIGN = 'Whole Sign'
HOUSES_MERIDIAN = 'Meridian'
HOUSES_AZIMUTHAL = 'Azimuthal'
HOUSES_POLICH_PAGE = 'Polich Page'
HOUSES_ALCABITUS = 'Alcabitus'
HOUSES_MORINUS = 'Morinus'
HOUSES_DEFAULT = HOUSES_ALCABITUS
ASC = 'Asc'
DESC = 'Desc'
MC = 'MC'
IC = 'IC'
STAR_ALGENIB = 'Algenib'
STAR_ALPHERATZ = 'Alpheratz'
STAR_ALGOL = 'Algol'
STAR_ALCYONE = 'Alcyone'
STAR_PLEIADES = STAR_ALCYONE
STAR_ALDEBARAN = 'Aldebaran'
STAR_RIGEL = 'Rigel'
STAR_CAPELLA = 'Capella'
STAR_BETELGEUSE = 'Betelgeuse'
STAR_SIRIUS = 'Sirius'
STAR_CANOPUS = 'Canopus'
STAR_CASTOR = 'Castor'
STAR_POLLUX = 'Pollux'
STAR_PROCYON = 'Procyon'
STAR_ASELLUS_BOREALIS = 'Asellus Borealis'
STAR_ASELLUS_AUSTRALIS = 'Asellus Australis'
STAR_ALPHARD = 'Alphard'
STAR_REGULUS = 'Regulus'
STAR_DENEBOLA = 'Denebola'
STAR_ALGORAB = 'Algorab'
STAR_SPICA = 'Spica'
STAR_ARCTURUS = 'Arcturus'
STAR_ALPHECCA = 'Alphecca'
STAR_ZUBEN_ELGENUBI = 'Zuben Elgenubi'
STAR_ZUBEN_ELSCHEMALI = 'Zuben Eshamali'
STAR_UNUKALHAI = 'Unukalhai'
STAR_AGENA = 'Agena'
STAR_RIGEL_CENTAURUS = 'Rigel Kentaurus'
STAR_ANTARES = 'Antares'
STAR_LESATH = 'Lesath'
STAR_VEGA = 'Vega'
STAR_ALTAIR = 'Altair'
STAR_DENEB_ALGEDI = 'Deneb Algedi'
STAR_FOMALHAUT = 'Fomalhaut'
STAR_DENEB_ADIGE = 'Deneb'
STAR_ACHERNAR = 'Achernar'
NO_ASPECT = -1
CONJUNCTION = 0
SEXTILE = 60
SQUARE = 90
TRINE = 120
OPPOSITION = 180
SEMISEXTILE = 30
SEMIQUINTILE = 36
SEMISQUARE = 45
QUINTILE = 72
SESQUIQUINTILE = 108
SESQUISQUARE = 135
BIQUINTILE = 144
QUINCUNX = 150
APPLICATIVE = 'Applicative'
SEPARATIVE = 'Separative'
EXACT = 'Exact'
NO_MOVEMENT = 'None'
DEXTER = 'Dexter'
SINISTER = 'Sinister'
ASSOCIATE = 'Associate'
DISSOCIATE = 'Dissociate'
MAJOR_ASPECTS = [
 0, 60, 90, 120, 180]
MINOR_ASPECTS = [30, 36, 45, 72, 108, 135, 144, 150]
ALL_ASPECTS = MAJOR_ASPECTS + MINOR_ASPECTS
LIST_SIGNS = [
 ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA,
 SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES]
LIST_OBJECTS = [
 SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN,
 URANUS, NEPTUNE, PLUTO, CHIRON, NORTH_NODE,
 SOUTH_NODE, SYZYGY, PARS_FORTUNA]
LIST_OBJECTS_TRADITIONAL = [
 SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN,
 NORTH_NODE, SOUTH_NODE, SYZYGY, PARS_FORTUNA]
LIST_SEVEN_PLANETS = [
 SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN]
LIST_HOUSES = [
 HOUSE1, HOUSE2, HOUSE3, HOUSE4, HOUSE5, HOUSE6,
 HOUSE7, HOUSE8, HOUSE9, HOUSE10, HOUSE11, HOUSE12]
LIST_ANGLES = [
 ASC, MC, DESC, IC]
LIST_FIXED_STARS = [
 STAR_ALGENIB, STAR_ALPHERATZ, STAR_ALGOL, STAR_ALCYONE,
 STAR_PLEIADES, STAR_ALDEBARAN, STAR_RIGEL, STAR_CAPELLA,
 STAR_BETELGEUSE, STAR_SIRIUS, STAR_CANOPUS, STAR_CASTOR,
 STAR_POLLUX, STAR_PROCYON, STAR_ASELLUS_BOREALIS,
 STAR_ASELLUS_AUSTRALIS, STAR_ALPHARD, STAR_REGULUS,
 STAR_DENEBOLA, STAR_ALGORAB, STAR_SPICA, STAR_ARCTURUS,
 STAR_ALPHECCA, STAR_ZUBEN_ELSCHEMALI, STAR_UNUKALHAI,
 STAR_AGENA, STAR_RIGEL_CENTAURUS, STAR_ANTARES,
 STAR_LESATH, STAR_VEGA, STAR_ALTAIR, STAR_DENEB_ALGEDI,
 STAR_FOMALHAUT, STAR_DENEB_ADIGE, STAR_ACHERNAR]