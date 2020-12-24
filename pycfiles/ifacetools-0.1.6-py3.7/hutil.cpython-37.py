# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ifacetools\util\hutil.py
# Compiled at: 2019-09-15 21:55:36
# Size of source mod 2**32: 1043 bytes


class HUtil:

    def objecttodict(self, obj):
        dict_o = obj.__dict__
        for key, value in dict_o.items():
            if isinstance(value, (str, int)):
                continue
            if value is None:
                continue
            if isinstance(value, list):
                valuelist = []
                for l in value:
                    if isinstance(l, (str, int)):
                        valuelist.append(l)
                    else:
                        valuelist.append(self.objecttodict(l))

                dict_o[key] = valuelist
            else:
                if isinstance(value, dict):
                    continue
                dict_o[key] = self.objecttodict(value)

        return dict_o