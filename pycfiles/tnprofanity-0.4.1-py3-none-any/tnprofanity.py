# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: tnprofanity.py
# Compiled at: 2019-03-12 06:33:46
import re

class tnprofanity:

    def find_all(text, substring):
        return [ m.start() for m in re.finditer(substring, text) ]

    def compare_scheme(bt, wt, filter_black_list, mode):
        if mode == 'ignore':
            filter_black_list.append(bt)
        elif mode == 'preserve':
            if wt[0] <= bt[0] and bt[1] <= wt[1]:
                pass
            elif wt[0] <= bt[0] and wt[1] <= bt[1] and bt[0] < wt[1]:
                pass
            elif bt[0] <= wt[0] and bt[1] <= wt[1] and wt[0] < bt[1]:
                pass
            else:
                filter_black_list.append(bt)
        elif mode == 'overlap':
            if wt[0] <= bt[0] and bt[1] <= wt[1]:
                pass
            elif wt[0] <= bt[0] and wt[1] <= bt[1] and bt[0] < wt[1]:
                nt = (
                 wt[1], bt[1])
                filter_black_list.append(nt)
            elif bt[0] <= wt[0] and bt[1] <= wt[1] and wt[0] < bt[1]:
                nt = (
                 bt[0], wt[0])
                filter_black_list.append(nt)
            else:
                filter_black_list.append(bt)

    @staticmethod
    def censor(whitelist, blacklist, text, mark='*', mode='preserve'):
        white_hit_list = []
        for white_term in whitelist:
            for hit_id in find_all(text, white_term):
                white_hit_list.append((hit_id, hit_id + len(white_term)))

        black_hit_list = []
        for profane_term in blacklist:
            for hit_id in find_all(text, profane_term):
                black_hit_list.append((hit_id, hit_id + len(profane_term)))

        filter_black_list = []
        if len(white_hit_list) == 0:
            filter_black_list = black_hit_list
        else:
            for bt in black_hit_list:
                for wt in white_hit_list:
                    compare_scheme(bt, wt, filter_black_list, mode)

            censor_text = text
            for tobe_censor in filter_black_list:
                a = tobe_censor[0]
                b = tobe_censor[1]
                censor_text = censor_text.replace(censor_text[a:b], mark * ((b - a) / (1 if isinstance(censor_text[a:b], unicode) else 3)))

        return censor_text