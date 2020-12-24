# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/clockPy/clock.py
# Compiled at: 2018-02-05 08:17:03
import time, sys, os, threading, AlphabetPy

def getCurrentTime():
    global timer
    i = os.system('clear')
    j = os.system('cls')
    if i == 0:
        os.system('clear')
    if j == 0:
        os.system('cls')
    currentYear = time.localtime(time.time())[0]
    currentMonth = time.localtime(time.time())[1]
    currentDay = time.localtime(time.time())[2]
    currentHour = time.localtime(time.time())[3]
    currentMinute = time.localtime(time.time())[4]
    currentSecond = time.localtime(time.time())[5]
    currentWeekDay = time.strftime('%w', time.localtime(time.time()))
    if currentHour < 10:
        currentHourString = '0' + str(currentHour)
    else:
        currentHourString = str(currentHour)
    if currentMinute < 10:
        currentMinuteString = '0' + str(currentMinute)
    else:
        currentMinuteString = str(currentMinute)
    if currentSecond < 10:
        currentSecondString = '0' + str(currentSecond)
    else:
        currentSecondString = str(currentSecond)
    if currentMonth < 10:
        currentMonthString = '0' + str(currentMonth)
    else:
        currentMonthString = str(currentMonth)
    if currentDay < 10:
        currentDayString = '0' + str(currentDay)
    else:
        currentDayString = str(currentDay)
    if currentWeekDay == '1':
        currentWeekdayString = 'MO'
    else:
        if currentWeekDay == '2':
            currentWeekdayString = 'TU'
        else:
            if currentWeekDay == '3':
                currentWeekdayString = 'WE'
            else:
                if currentWeekDay == '4':
                    currentWeekdayString = 'TH'
                elif currentWeekDay == '5':
                    currentWeekdayString = 'FR'
                elif currentWeekDay == '6':
                    currentWeekdayString = 'SR'
                else:
                    currentWeekdayString = 'SU'
                currentYearString = str(currentYear)
                currentTime = '      ' + currentHourString + ':' + currentMinuteString + ':' + currentSecondString
                currentDate = '           ' + currentYearString + '年' + currentMonthString + '月' + currentDayString + '日' + ' ' + currentWeekdayString
                currentTimeString = AlphabetPy.getAlphabet(currentTime)
                currentDateString = AlphabetPy.getAlphabet(currentDate, 'calen')
                for i in range(10):
                    print '\n'

            for i in range(7):
                print currentTimeString[i]

        print '\n'
        for i in range(3):
            print currentDateString[i]

    timer = threading.Timer(1.0, getCurrentTime)
    timer.start()


def start():
    timer = threading.Timer(1.0, getCurrentTime)
    timer.start()