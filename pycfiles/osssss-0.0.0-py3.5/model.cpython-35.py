# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\osuapi\model.py
# Compiled at: 2016-03-31 16:35:28
# Size of source mod 2**32: 1453 bytes
import warnings, datetime

def JsonList(oftype):

    class _:

        def __new__(cls, lis):
            return [oftype(entry) for entry in lis]

    return _


class JsonDateTime:

    def __new__(cls, val):
        return datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')


class JsonObjWrapper:

    def __init__(self, dic):
        for k, v in dic.items():
            try:
                setattr(self, k, getattr(self, k)(v))
            except AttributeError:
                warnings.warn('Unknown attribute in API response: {}'.format(k), Warning)


class Score(JsonObjWrapper):
    beatmap_id = str
    score = int
    maxcombo = int
    count50 = int
    count100 = int
    count300 = int
    countmiss = int
    countkatu = int
    countgeki = int
    perfect = bool
    enabled_mods = int
    user_id = int
    date = JsonDateTime
    rank = str
    pp = float


class User(JsonObjWrapper):
    user_id = int
    username = str
    count300 = int
    count100 = int
    count50 = int
    playcount = int
    ranked_score = int
    total_score = int
    pp_rank = int
    level = float
    pp_raw = float
    accuracy = float
    count_rank_ss = int
    count_rank_s = int
    count_rank_a = int
    country = str
    pp_country_rank = int
    events = JsonList(str)

    @property
    def total_hits(self):
        return self.count300 + self.count100 + self.count50