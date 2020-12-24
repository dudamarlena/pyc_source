# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/folmond/filereader.py
# Compiled at: 2018-05-05 06:15:22
from pandas import read_csv
from pandas import Series
from pandas import DataFrame
import pandas, datetime, os, glob, re

class CSVReader:

    def __init__(self, usage_location):
        self.path = usage_location
        self.df = DataFrame()

    def getBetweenDates(self, start_date, end_date):
        all_files = glob.glob(os.path.join(self.path, '*'))
        list_ = []
        series = None
        for f in all_files:
            file_date_match = re.search('\\d{4}-\\d{2}-\\d{2}', f)
            if file_date_match:
                file_date = datetime.datetime.strptime(file_date_match.group(), '%Y-%m-%d').date()
                if file_date >= start_date and file_date <= end_date:
                    if 'gz' in f:
                        series = read_csv(f, names=[
                         'date', 'folder', 'size'], header=0, index_col=0, parse_dates=[
                         0], compression='gzip')
                    else:
                        print f
                        series = read_csv(f, names=[
                         'date', 'folder', 'size'], header=0, index_col=0, parse_dates=[
                         0])
                    list_.append(series)

        df = pandas.concat(list_)
        return df.sort_index()

    def getToday(self):
        start_date = end_date = datetime.date.today()
        return self.getBetweenDates(start_date, end_date)

    def getLastNDays(self, num_days):
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=num_days)
        return self.getBetweenDates(start_date, end_date)

    def getRecent(self):
        start_date = end_date = datetime.date.today()
        today_df = self.getBetweenDates(start_date, end_date)
        return today_df.loc[today_df.index.max()]


if __name__ == '__main__':
    reader = CSVReader('/home/arun/Projects/bingoarun/folmon/sample-data')