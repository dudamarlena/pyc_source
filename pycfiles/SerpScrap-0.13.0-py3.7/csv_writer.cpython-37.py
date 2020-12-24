# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\serpscrap\csv_writer.py
# Compiled at: 2018-08-26 07:33:12
# Size of source mod 2**32: 510 bytes
import csv, traceback

class CsvWriter:

    def write(self, file_name, my_dict):
        try:
            with open(file_name, 'w', encoding='utf-8', newline='') as (f):
                w = csv.DictWriter(f, (my_dict[0].keys()), dialect='excel', delimiter='\t', quotechar='"')
                w.writeheader()
                for row in my_dict[0:]:
                    w.writerow(row)

        except Exception:
            print(traceback.print_exc())
            raise Exception