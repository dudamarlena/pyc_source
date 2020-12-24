# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkellestatistics/allstatisticseod.py
# Compiled at: 2020-01-24 12:27:06
# Size of source mod 2**32: 7264 bytes
"""
Created on Tue Jul 16 00:17:24 2019
Python program to calculate the following using parameters stock ticker, benchmark ticker, country code, currency code:
    1 = Geometric return (stock and benchmark)
    2 = standard deviation using Garch/EWMA (stock and benchmark)
    3 = VAR 95% (stock and benchmark)
    4 = VAR 99% (stock and benchmark)
    5 = beta (stock)
    6 = market weight (stock), weighted beta
    7 = risk free rate (stock)
    8 = capm (stock)
@author: debmishra
"""
from lykkelleconf.connecteod import connect
import pandas as pd, numpy as np, math as m, psycopg2 as pgs

class allstatistics:

    def __init__(self, sticker, bticker, ctry, sourcetable, cursor):
        shist = 'select price_date, price_return,MA_50D,MA_200D from stock_history\n        where symbol=%s and abs(price_return)<0.45 order by price_date'
        bhist = 'select price_date, price_return from benchmark_history\n        where symbol=%s and abs(price_return)<0.45 order by price_date'
        cursor.execute(shist, (sticker,))
        shistr = cursor.fetchall()
        cursor.execute(bhist, (bticker,))
        bhistr = cursor.fetchall()
        if shistr == [] or len(shistr) <= 1:
            print('exiting code. check the history data for ', sticker)
        else:
            if bhistr == [] or len(bhistr) <= 1:
                print('exiting code. check the history data for ', bticker)
            else:
                shdf = pd.DataFrame(shistr, columns=['pricedate', 'return', 'MA_50D', 'MA_200D'])
                bhdf = pd.DataFrame(bhistr, columns=['pricedate', 'return'])
                is_valid_sreturn = shdf['return'].notnull()
                mshdf = shdf[is_valid_sreturn]
                is_valid_breturn = bhdf['return'].notnull()
                mbhdf = bhdf[is_valid_breturn]
                nz_sret = mshdf['return'] != 0
                nz_bret = mbhdf['return'] != 0
                mshdfz = mshdf[nz_sret]
                mbhdfz = mbhdf[nz_bret]
                nz_sret = mshdf['return'] != 0
                nz_bret = mbhdf['return'] != 0
                mshdfz = mshdf[nz_sret]
                mbhdfz = mbhdf[nz_bret]
                mshdfz = mshdfz.sort_values(['pricedate'], ascending=0)
                mbhdfz = mbhdfz.sort_values(['pricedate'], ascending=0)
                lstk = len(mshdfz['return'])
                lidx = len(mbhdfz['return'])
                if lstk is not None and lstk > 0:
                    samean = mshdfz['return'].empty or mshdfz['return'].mean()
                    if not mshdfz['MA_50D'].empty:
                        sa50dmean = mshdfz['MA_50D'].iloc[0]
                    else:
                        sa50dmean = None
                    if not mshdfz['MA_200D'].empty:
                        sa200dmean = mshdfz['MA_200D'].iloc[0]
                    else:
                        sa200dmean = None
                    stkmean = samean * 252
                    sstd = mshdfz['return'].std()
                    stkstd = sstd * m.sqrt(252)
                else:
                    print('No return found for ', sticker, 'length of returns-', lstk)
                    stkmean = None
                    stkstd = None
                    sa50dmean = None
                    sa200dmean = None
                if lidx is not None and lidx > 0:
                    iamean = mbhdfz['return'].mean()
                    idxmean = iamean * 252
                    istd = mbhdfz['return'].std()
                    idxstd = istd * m.sqrt(252)
                else:
                    print('No return found for ', bticker, 'length of returns-', lidx)
                    idxmean = None
                    idxstd = None
                if stkmean is not None and stkstd is not None:
                    stkvar95 = -(1.65 * stkstd)
                    stkvar99 = -(2.33 * stkstd)
                else:
                    stkvar95 = None
                    stkvar99 = None
                if idxmean is not None and idxstd is not None:
                    idxvar95 = -(1.65 * idxstd)
                    idxvar99 = -(2.33 * idxstd)
                else:
                    idxvar95 = None
                    idxvar99 = None
                if len(mshdfz['pricedate']) > 1 and len(mbhdfz['pricedate']) > 1:
                    smatch = mshdfz.loc[(mshdfz['pricedate'].isin(mbhdfz['pricedate'].values), ['pricedate', 'return'])]
                    imatch = mbhdfz.loc[(mbhdfz['pricedate'].isin(mshdfz['pricedate'].values), ['pricedate', 'return'])]
                    corr = np.corrcoef(smatch['return'].values, imatch['return'].values)
                    corr = corr[(0, 1)]
                else:
                    corr = None
                if corr is not None and stkstd is not None and idxstd is not None:
                    beta = corr * (stkstd / idxstd)
                else:
                    beta = None
                selrf = 'select risk_free_rate from benchmark_all where country=%s'
                cursor.execute(selrf, (ctry,))
                rf = cursor.fetchone()
                try:
                    rf = float(rf[0])
                except TypeError:
                    rf = None

                if rf is not None:
                    if beta is not None and idxmean is not None:
                        capm = rf + beta * (idxmean - rf)
                    else:
                        capm = None
                else:
                    selind = 'select mkt_cap_stocks_bill_eur\n            from stock_statistics where symbol=%s'
                    cursor.execute(selind, (sticker,))
                    mcap = cursor.fetchone()
                    if mcap is None:
                        mcap = None
                    else:
                        if len(mcap) > 0:
                            mcap = mcap[0]
                        else:
                            mcap = None
                if mcap is not None and mcap > 90:
                    ind = 'LCAP'
                else:
                    if mcap is not None and mcap >= 10 and mcap < 90:
                        ind = 'MCAP'
                    else:
                        ind = 'SCAP'
                statupd = 'update stock_statistics set capm_return = %s,\n            mean_annualized_Return = %s, beta = %s, var95_annualized = %s,\n            var99_annualized = %s, annual_rf_rate = %s,\n            mkt_mean_annualized_return = %s, std_annualized = %s,\n            mkt_annualized_std= %s, mkt_annualized_var95 = %s,\n            mkt_annualized_var99 = %s, ind_category=%s,bmk_symbol=%s,mean_50D=%s, mean_200D=%s where symbol=%s'
                statdata = [capm, stkmean, beta, stkvar95, stkvar99, rf, idxmean, stkstd, idxstd, idxvar95, idxvar99, ind, bticker, sa50dmean, sa200dmean, sticker]
                try:
                    cursor.execute(statupd, statdata)
                except pgs.Error as e:
                    try:
                        print('unsuccessful update for ticker', sticker)
                        print(e)
                    finally:
                        e = None
                        del e

                print('postgres connection successfully closed')