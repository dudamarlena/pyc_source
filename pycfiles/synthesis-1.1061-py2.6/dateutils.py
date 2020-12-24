# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/dateutils.py
# Compiled at: 2010-09-15 00:35:01


def fixDate(self, inputDate):
    if isinstance(inputDate, datetime) or isinstance(inputDate, date):
        try:
            return inputDate.strftime(self.isIsoTimeFormat)
        except ValueError:
            print 'bad date string passed to fixDate: ', inputDate, ' so sending back blank date'
            inputDate = None
            return inputDate

    if inputDate == '' or inputDate == None:
        return datetime.now().strftime(self.isIsoTimeFormat)
    else:
        newDate = self.getDateTimeObj(inputDate).strftime(self.isIsoTimeFormat)
        if self.debug == True:
            self.debugMessages.log('FUNCTION: fixDate() incoming date is: %s and clean date is: %s\n' % (inputDate, newDate))
        return newDate
        return


def fixDateNoTime(self, inputDate):
    if input == '':
        print 'empty date encountered!' + self
    else:
        newDate = self.getDateTimeObj(inputDate).date()
        if self.debug == True:
            self.debugMessages.log('FUNCTION: fixDate() incoming date is: %s and clean date is: %s\n' % (inputDate, newDate))
        return newDate


def dateStringToDateObject(self, dateString):
    date_object = time.strptime(dateString, '%d/%m/%Y')
    return date_object


def convertIntegerToDate(self, intDate):
    if not intDate.isdigit():
        if intDate == '':
            return
        self.errorMsgs.append('WARNING: during conversion of an integer to date format this string was passed: %s which is not all numbers' % intDate)
        intDate = 0
    td = timedelta(days=int(intDate))
    newDate = date(1900, 1, 1) + td
    if self.debug == True:
        print 'Incoming Date is: %s and converted Date is: %s' % (intDate, newDate.isoformat())
    return newDate.isoformat()


def convertIntegerToDateTime(self, intDate):
    if not intDate.isdigit():
        if intDate == '':
            return
        self.errorMsgs.append('WARNING: during conversion of an integer to date format this string was passed: %s which is not all numbers' % intDate)
        intDate = 0
    td = timedelta(days=int(intDate))
    isodate = date(1900, 1, 1) + td
    isodatetime = str(isodate) + 'T00:00:00'
    if self.debug == True:
        print 'Incoming Date is: %s and converted Date is: %s' % (intDate, isodatetime)
    return isodatetime


def getDateTimeObj(self, inputDate):
    dateParts = inputDate.split('/')
    if len(dateParts[2]) == 4:
        inputDateFmt = '%m/%d/%Y'
    elif len(inputDate) == 10 or len(inputDate) == 9:
        inputDateFmt = '%m/%d/%Y'
    else:
        inputDateFmt = '%m/%d/%y'
    newDate = datetime(*strptime(inputDate, inputDateFmt)[0:3])
    return newDate