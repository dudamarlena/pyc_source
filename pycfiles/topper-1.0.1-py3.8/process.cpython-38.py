# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/topper/process.py
# Compiled at: 2020-02-16 17:56:08
# Size of source mod 2**32: 2063 bytes
from operator import itemgetter

class Process:
    __doc__ = '\n    Computation class providing top songs by country or by user, depending on mode\n    '

    def __init__(self, mode):
        self.mode = mode
        self.count_songs_aggregated = {}

    def update_result(self, agg_item, sng_id):
        """
        Increment song id for the aggregation item
        :param agg_item: item of aggregation, a country or a user
        :param sng_id: song id to increment
        """
        if agg_item not in self.count_songs_aggregated:
            self.count_songs_aggregated.update({agg_item: {}})
        elif sng_id not in self.count_songs_aggregated[agg_item]:
            self.count_songs_aggregated[agg_item].update({sng_id: 1})
        else:
            self.count_songs_aggregated[agg_item][sng_id] = self.count_songs_aggregated[agg_item][sng_id] + 1

    def reduce_days(self, list_days):
        """
        Group by data by day
        :param list_days: list(tuple()): list of data for each day
        :return: dict(): dictionary grouped by and aggregated
        """
        for day in list_days:
            for data in day:
                country, user_id, song_id = data
                if self.mode == 'user':
                    self.update_result(user_id, song_id)
                else:
                    self.update_result(country, song_id)
            else:
                return self.count_songs_aggregated

    def get_top50(self):
        """
        Format aggregated dict to get top 50 elements ordered for each entry
        :return: dict(key:list(tuple)
        """
        result = {}
        for country, data in self.count_songs_aggregated.items():
            tmp = []
            for song, nber in data.items():
                tmp.append((song, nber))
            else:
                country_sorted_50 = sorted(tmp, key=(itemgetter(1)), reverse=True)[:50]
                result.update({country: country_sorted_50})

        else:
            return result