# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/queryobject.py
# Compiled at: 2010-12-12 22:28:56
from optparse import OptionParser
from datetime import datetime

class QueryObject:

    def __init__(self):
        usage = 'usage: %prog [options] arg'
        parser = OptionParser(usage)
        parser.add_option('-i', '--IDconfig', dest='configID', type='string', help='Configuration ID of Vendor requesting report', metavar='ID')
        parser.add_option('-s', '--startdate', dest='startDate', type='string', help='start date of reporting', metavar='StartDate')
        parser.add_option('-e', '--enddate', dest='endDate', type='string', help='end date of reporting', metavar='EndDate')
        parser.add_option('-r', '--reported', action='store_true', dest='reported', help='Select data that has already been reported (reported = True).  Omit both -r and -u to simply use date selection', metavar='Reported')
        parser.add_option('-u', '--unreported', action='store_true', dest='unreported', help='Select data that has never been reported (reported = False or None).  Omit both -r and -u to simply use date selection', metavar='Reported')
        (self.options, self.arg) = parser.parse_args()
        if self.options.configID == None or self.options.startDate == None or self.options.endDate == None:
            parser.print_help()
            self.options = None
            return
        else:
            try:
                self.options.startDate = datetime.strptime(self.options.startDate, '%Y-%m-%d')
                self.options.endDate = datetime.strptime(self.options.endDate, '%Y-%m-%d')
            except:
                parser.print_help()
                raise

            return

    def getOptions(self):
        return self.options


def main():
    optParse = QueryObject()
    options = optParse.getOptions()
    if options != None:
        print options.configID
    return


if __name__ == '__main__':
    main()