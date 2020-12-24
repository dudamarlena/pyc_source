# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grs/timeser.py
# Compiled at: 2011-10-05 02:42:28
from goristock import goristock

def oop(aa):
    """ For cmd output. """
    return ('%s %s %s %.2f %+.2f %s %s %s %s %+.2f %s %s %.2f %.4f %.4f' % (aa.stock_no, aa.stock_name, aa.data_date[(-1)], aa.raw_data[(-1)], aa.range_per, aa.MAC(3), aa.MAC(6), aa.MAC(18), aa.MAO(3, 6)[1], aa.MAO(3, 6)[0][1][(-1)], aa.MAO(3, 6)[0][0], aa.RABC, aa.stock_vol[(-1)] / 1000, aa.SD, aa.CV)).encode('utf-8')


def timetest(no):
    """ To list the stock at lest 19 days info. """
    a = goristock(no)
    while len(a.raw_data) > 19:
        if a.MAO(3, 6)[1] == ('↑').decode('utf-8') and (a.MAO(3, 6)[0][1][(-1)] < 0 or a.MAO(3, 6)[0][1][(-1)] < 1 and a.MAO(3, 6)[0][1][(-1)] > 0 and a.MAO(3, 6)[0][1][(-2)] < 0 and a.MAO(3, 6)[0][0] == 3) and a.VOLMAX3:
            print 'buy-: ' + oop(a)
        elif a.MAO(3, 6)[1] == ('↓').decode('utf-8') and a.MAO(3, 6)[0][1][(-1)] > 0 and a.MAO(3, 6)[0][0] <= 3:
            print 'sell: ' + oop(a)
        else:
            print '----: ' + oop(a)
        a.goback()


def overall(goback=0, case=1):
    """ To run all over the stock and to find who match the 'case'
      'goback' is back to what days ago.
        0 is the last day.
  """
    from twseno import twseno
    for i in twseno().allstock:
        try:
            if case == 1:
                try:
                    a = goristock(i)
                    if goback:
                        a.goback(goback)
                    if a.MAO(3, 6)[1] == ('↑').decode('utf-8') and (a.MAO(3, 6)[0][1][(-1)] < 0 or a.MAO(3, 6)[0][1][(-1)] < 1 and a.MAO(3, 6)[0][1][(-1)] > 0 and a.MAO(3, 6)[0][1][(-2)] < 0 and a.MAO(3, 6)[0][0] == 3) and a.VOLMAX3 and a.stock_vol[(-1)] > 1000 * 1000 and a.raw_data[(-1)] > 10:
                        print 'buy-: ' + oop(a)
                    elif a.MAO(3, 6)[1] == ('↓').decode('utf-8') and a.MAO(3, 6)[0][1][(-1)] > 0 and a.MAO(3, 6)[0][0] <= 3:
                        print 'sell: ' + oop(a)
                except KeyboardInterrupt:
                    print '::KeyboardInterrupt'
                    break
                except IndexError:
                    print i

            elif case == 2:
                try:
                    a = goristock(i)
                    if goback:
                        a.goback(goback)
                    if a.MAO(3, 6)[1] == ('↑').decode('utf-8') and (a.MAO(3, 6)[0][1][(-1)] < 0 or a.MAO(3, 6)[0][1][(-1)] < 1 and a.MAO(3, 6)[0][1][(-1)] > 0 and a.MAO(3, 6)[0][1][(-2)] < 0 and a.MAO(3, 6)[0][0] == 3) and a.stock_vol[(-1)] >= 1000 * 1000 and a.raw_data[(-1)] > 10 and sum(a.stock_vol[-45:]) / 45 <= 1000 * 1000:
                        print 'buy-: ' + oop(a)
                except KeyboardInterrupt:
                    print '::KeyboardInterrupt'
                    break
                except IndexError:
                    print i

            elif case == 3:
                try:
                    a = goristock(i)
                    if goback:
                        a.goback(goback)
                    if a.MA(3) > a.raw_data[(-1)] and a.MA(6) <= a.raw_data[(-1)] and a.MA(6) > a.MA(18):
                        print 'buy-: ' + oop(a)
                except KeyboardInterrupt:
                    print '::KeyboardInterrupt'
                    break
                except IndexError:
                    print i

        except KeyboardInterrupt:
            print 'KeyboardInterrupt'
            break