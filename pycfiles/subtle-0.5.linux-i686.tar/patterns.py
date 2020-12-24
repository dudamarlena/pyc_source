# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/patterns.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
import re
subtitle_exts = [
 b'srt', b'idx', b'sub', b'ssa']
video_exts = [
 b'3g2', b'3gp', b'3gp2', b'asf', b'avi', b'divx', b'flv', b'm4v', b'mk2',
 b'mka', b'mkv', b'mov', b'mp4', b'mp4a', b'mpeg', b'mpg', b'ogg', b'ogm',
 b'ogv', b'qt', b'ra', b'ram', b'rm', b'ts', b'wav', b'webm', b'wma', b'wmv']
group_delimiters = [
 b'()', b'[]', b'{}']
sep = b'[][)(}{+ /\\._-]'
deleted = b'_'
episode_rexps = [
 (
  b'season (?P<season>[0-9]+)', 1.0, (0, 0)),
 (
  b'saison (?P<season>[0-9]+)', 1.0, (0, 0)),
 (
  b'[Ss](?P<season>[0-9]{1,2}).?(?P<episodeNumber>(?:[Ee-][0-9]{1,2})+)[^0-9]', 1.0, (0, -1)),
 (
  b'[Ss](?P<season>[0-9]{1,2}).?(?P<bonusNumber>(?:[Xx][0-9]{1,2})+)[^0-9]', 1.0, (0, -1)),
 (
  b'[^0-9](?P<season>[0-9]{1,2}).?(?P<episodeNumber>(?:[xX][0-9]{1,2})+)[^0-9]', 0.8, (1, -1)),
 (
  b's(?P<season>[0-9]{1,2})[^0-9]', 0.6, (0, -1)),
 (
  b'(?P<episodeNumber>[0-9]{1,3})v[23]' + sep, 0.6, (0, 0)),
 (
  b'ep' + sep + b'(?P<episodeNumber>[0-9]{1,2})[^0-9]', 0.7, (0, -1)),
 (
  sep + b'e(?P<episodeNumber>[0-9]{1,2})' + sep, 0.6, (1, -1))]
weak_episode_rexps = [
 (
  sep + b'(?P<episodeNumber>[0-9]{2,4})' + sep, (1, -1))]
non_episode_title = [
 b'extras', b'rip']
video_rexps = [
 (
  b'cd ?(?P<cdNumber>[0-9])( ?of ?(?P<cdNumberTotal>[0-9]))?', 1.0, (0, 0)),
 (
  b'(?P<cdNumberTotal>[1-9]) cds?', 0.9, (0, 0)),
 (
  b'edition' + sep + b'(?P<edition>collector)', 1.0, (0, 0)),
 (
  b'(?P<edition>collector)' + sep + b'edition', 1.0, (0, 0)),
 (
  b'(?P<edition>special)' + sep + b'edition', 1.0, (0, 0)),
 (
  b'(?P<edition>criterion)' + sep + b'edition', 1.0, (0, 0)),
 (
  b"(?P<edition>director'?s?" + sep + b'cut)', 1.0, (0, 0)),
 (
  b'(?P<width>[0-9]{3,4})x(?P<height>[0-9]{3,4})', 0.9, (0, 0)),
 (
  b'(?P<website>www(\\.[a-zA-Z0-9]+){2,3})', 0.8, (0, 0)),
 (
  b'x(?P<bonusNumber>[0-9]{1,2})', 1.0, (0, 0)),
 (
  b'f(?P<filmNumber>[0-9]{1,2})', 1.0, (0, 0))]
websites = [
 b'tvu.org.ru', b'emule-island.com', b'UsaBit.com', b'www.divx-overnet.com',
 b'sharethefiles.com']
unlikely_series = [
 b'series']
prop_multi = {b'format': {b'DVD': [b'DVD', b'DVD-Rip', b'VIDEO-TS', b'DVDivX'], b'HD-DVD': [
                         b'HD-(?:DVD)?-Rip', b'HD-DVD'], 
               b'BluRay': [
                         b'Blu-ray', b'B[DR]Rip'], 
               b'HDTV': [
                       b'HD-TV'], 
               b'DVB': [
                      b'DVB-Rip', b'DVB', b'PD-TV'], 
               b'WEBRip': [
                         b'WEB-Rip'], 
               b'Screener': [
                           b'DVD-SCR', b'Screener'], 
               b'VHS': [
                      b'VHS'], 
               b'WEB-DL': [
                         b'WEB-DL']}, 
   b'screenSize': {b'480p': [b'480p?'], b'720p': [
                           b'720p?'], 
                   b'1080p': [
                            b'1080p?']}, 
   b'videoCodec': {b'XviD': [b'Xvid'], b'DivX': [
                           b'DVDivX', b'DivX'], 
                   b'h264': [
                           b'[hx]-264'], 
                   b'Rv10': [
                           b'Rv10']}, 
   b'audioCodec': {b'AC3': [b'AC3'], b'DTS': [
                          b'DTS'], 
                   b'AAC': [
                          b'He-AAC', b'AAC-He', b'AAC']}, 
   b'audioChannels': {b'5.1': [b'5\\.1', b'DD5\\.1', b'5ch']}, b'episodeFormat': {b'Minisode': [b'Minisodes?']}}
prop_single = {b'releaseGroup': [b'ESiR', b'WAF', b'SEPTiC', b'\\[XCT\\]', b'iNT', b'PUKKA',
                   b'CHD', b'ViTE', b'TLF', b'DEiTY', b'FLAiTE',
                   b'MDX', b'GM4F', b'DVL', b'SVD', b'iLUMiNADOS', b'FiNaLe',
                   b'UnSeeN', b'aXXo', b'KLAXXON', b'NoTV', b'ZeaL', b'LOL',
                   b'SiNNERS', b'DiRTY', b'REWARD', b'ECI', b'KiNGS', b'CLUE',
                   b'CtrlHD', b'POD', b'WiKi', b'DIMENSION', b'IMMERSE', b'FQM',
                   b'2HD', b'REPTiLE', b'CTU', b'HALCYON', b'EbP', b'SiTV',
                   b'SAiNTS', b'HDBRiSe', b'AlFleNi-TeaM', b'EVOLVE', b'0TV',
                   b'TLA', b'NTB', b'ASAP', b'MOMENTUM'], 
   b'other': [
            b'PROPER', b'REPACK', b'LIMITED', b'DualAudio', b'Audiofixed', b'R5',
            b'complete', b'classic',
            b'ws']}
_dash = b'-'
_psep = b'[-\\. _]?'

def _to_rexp(prop):
    return re.compile(prop.replace(_dash, _psep), re.IGNORECASE)


properties_rexps = dict((type, dict((canonical_form, [ _to_rexp(pattern) for pattern in patterns ]) for canonical_form, patterns in props.items())) for type, props in prop_multi.items())
properties_rexps.update(dict((type,
 dict((canonical_form, [_to_rexp(canonical_form)]) for canonical_form in props)) for type, props in prop_single.items()))

def find_properties(string):
    result = []
    for property_name, props in properties_rexps.items():
        for canonical_form, rexps in props.items():
            for value_rexp in rexps:
                match = value_rexp.search(string)
                if match:
                    start, end = match.span()
                    if start > 0 and string[(start - 1)] not in sep or end < len(string) and string[end] not in sep:
                        continue
                    result.append((property_name, canonical_form, start, end))

    return result


property_synonyms = {b'Special Edition': [b'Special'], b'Collector Edition': [
                        b'Collector'], 
   b'Criterion Edition': [
                        b'Criterion']}

def revert_synonyms():
    reverse = {}
    for canonical, synonyms in property_synonyms.items():
        for synonym in synonyms:
            reverse[synonym.lower()] = canonical

    return reverse


reverse_synonyms = revert_synonyms()

def canonical_form(string):
    return reverse_synonyms.get(string.lower(), string)


def compute_canonical_form(property_name, value):
    """Return the canonical form of a property given its type if it is a valid
    one, None otherwise."""
    for canonical_form, rexps in properties_rexps[property_name].items():
        for rexp in rexps:
            if rexp.match(value):
                return canonical_form

    return