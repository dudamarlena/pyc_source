# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelleportfolio/createportfolioeod.py
# Compiled at: 2020-01-24 12:25:44
# Size of source mod 2**32: 14062 bytes
"""
Created on Sat Jul 27 13:38:33 2019
create a program that identifies the
bet combination of portfolio based on the following:
    best mean return +div_yield
    for:
        beta < 1.1
        SD < .15
        weighted capm > weighted mkt return
    for the the following:

@author: debaj
"""
from lykkelleconf.connecteod import connect
import pandas as pd, numpy as np, psycopg2 as pgs, datetime as dt, math as m
pd.options.mode.chained_assignment = None

class createportfolio:

    def __init__(self, Port, query, ind, fxr, cursor):
        print('Passing PorID:', Port)
        print('Passing Industry:', ind)
        lstins = []
        if ind == 'ZZZ':
            cursor.execute(query)
        else:
            cursor.execute(query, (ind,))
        symw = cursor.fetchall()
        print('Below is the query per passed parameter:')
        if len(symw) != 0:
            symwdf = pd.DataFrame(symw, columns=['symbol', 'industry', 'mean', 'mkt_mean', 'capm', 'SD', 'mkt_SD', 'div_y', 'price', 'currency', 'Mcapeur', 'per', 'beta', 'src', 'count', 'exchange', 'abbr'])
            total = symwdf['Mcapeur'].sum()
            symwdf['wt'] = symwdf['Mcapeur'] / total
            symwdf['wtmean'] = symwdf['mean'] * symwdf['wt']
            symwdf['wtmmean'] = symwdf['mkt_mean'] * symwdf['wt']
            symwdf['wtbeta'] = symwdf['beta'] * symwdf['wt']
            symwdf['wtcapm'] = symwdf['capm'] * symwdf['wt']
            cc = fxr
            maxprice = []
            maxsymbol = []
            prwt = []
            length = len(symw)
            print('Number of stocks:', length)
            print('order of stocks for verification:', symwdf['symbol'].values)
            minh = symwdf['count'].min()
            print('minimum observation used for covariance calculation:', minh)
            nsymc = np.array([])
            symwdf['msymbol'] = ''
            symwdf['mcnt'] = 0
            for i in range(length):
                sym = symwdf['symbol'].iloc[i]
                curr = symwdf['currency'].iloc[i]
                abbr = symwdf['abbr'].iloc[i]
                src = symwdf['src'].iloc[i]
                if curr == 'GBX':
                    ccr = cc.cur_rate.get('GBP', None)
                    ccr = ccr * 100
                else:
                    if curr == 'ZAc':
                        ccr = cc.cur_rate.get('ZAR', None)
                        ccr = ccr * 100
                    else:
                        ccr = cc.cur_rate.get(curr, None)
                mprice = symwdf['price'].iloc[i]
                if mprice is not None:
                    if ccr is not None:
                        eurprice = symwdf['price'].iloc[i] / ccr
                    else:
                        print('ccr was null and therefore marking price in eur same as mprice for', sym)
                        eurprice = mprice
                    maxprice.append(eurprice)
                    maxsymbol.append(sym)
                    prwt.append(symwdf['wt'].iloc[i])
                    try:
                        msymbol = abbr
                        symwdf['msymbol'].iloc[i] = msymbol
                        selc = 'select count(*) from benchmark_history where symbol=%s and (price_return is not null and price_return <> 0)'
                        cursor.execute(selc, (msymbol,))
                        mc = cursor.fetchone()
                        symwdf['mcnt'].iloc[i] = mc[0]
                    except TypeError:
                        print(abbr, ' was the response from stock exchanges for ', sym)
                        msymbol = None

                    selq = 'select price_return from stock_history where symbol=%s and (price_return is not null and price_return <> 0) order by price_date desc'
                    cursor.execute(selq, (sym,))
                    symres = cursor.fetchall()
                    nsym = np.array(symres)
                    nsym = nsym[:minh]
                    if i == 0:
                        nsymc = nsym
                else:
                    nsymc = np.append(nsymc, nsym, axis=1)

            minb = symwdf['mcnt'].min()
            print('minimum observation used for mkt covariance calculation:', minb)
            mm = symwdf['mcnt'] == 0
            mmdf = symwdf[mm]
            nbsymc = np.array([])
            mlength = len(symwdf['msymbol'])
            for i in range(mlength):
                msym = symwdf['msymbol'].iloc[i]
                MktC = 'T'
                if msymbol is not None and minb != 0:
                    selmq = 'select price_return from benchmark_history where symbol=%s and (price_return is not null or price_return <> 0) order by price_date desc'
                    cursor.execute(selmq, (msym,))
                    symbres = cursor.fetchall()
                    nbsym = np.array(symbres)
                    nbsym = nbsym[:minb]
                    if i == 0:
                        nbsymc = nbsym
                    else:
                        nbsymc = np.append(nbsymc, nbsym, axis=1)
                else:
                    MktC = 'F'

            nsymr = np.reshape(nsymc, (nsymc.shape[1], nsymc.shape[0]))
            nsymr = nsymr.astype('float64')
            print('shape of input array for calculating cov. matrix:', nsymr.shape)
            covmat = np.cov(nsymr)
            print('shape of covariance matrix:', covmat.shape)
            wtr = symwdf['wt'].values
            wtr = np.reshape(wtr, (wtr.shape[0], -1))
            wtc = np.reshape(wtr, (-1, wtr.shape[0]))
            varp = np.dot(np.dot(wtc, covmat), wtr)
            stdp = np.sqrt(varp[0][0])
            stdpa = np.sqrt(252) * stdp
            mean = symwdf['wtmean'].sum()
            mkt_mean = symwdf['wtmmean'].sum()
            beta = symwdf['wtbeta'].sum()
            capm = symwdf['wtcapm'].sum()
            var95 = -(1.65 * stdpa)
            var99 = -(2.33 * stdpa)
            totalmc = symwdf['Mcapeur'].sum()
            if MktC == 'T':
                nbsymr = np.reshape(nbsymc, (nbsymc.shape[1], nbsymc.shape[0]))
                nbsymr = nbsymr.astype('float64')
                covmatm = np.cov(nbsymr)
                print('shape of covariance matrix:', covmatm.shape)
                varmp = np.dot(np.dot(wtc, covmatm), wtr)
                mstdp = np.sqrt(varmp[0][0])
                mstdpa = np.sqrt(252) * mstdp
                mvar95 = -(1.65 * mstdpa)
                mvar99 = -(2.33 * mstdpa)
            else:
                mstdpa = None
                mvar95 = None
                mvar99 = None
                print('For Portfolio ', Port, ", the market statistics are None as the covariance matrix couldn't be formed")
                print('missing index:\n', mmdf.values)
            print('maximum price in portfolio:', Port, ' is', max(maxprice))
            pos = maxprice.index(max(maxprice))
            prwt = prwt[pos]
            porsymbol = maxsymbol[pos]
            porprice = m.ceil(maxprice[pos] / prwt)
            print('the max price of an individual symbol is', porprice, 'for symbol ', porsymbol, 'having weight', prwt)
            PorID = Port
            lstins = [PorID, mean, mkt_mean, stdpa, mstdpa, beta, var95, var99, mvar95, mvar99, capm, porprice, 'EUR', totalmc]
            print('Purchase price of ', PorID, ' is ', porprice, ' per unit in EURO')
            delpor = 'delete from index_acutulus where Portfolio_Id=%s'
            inspor = 'insert into index_acutulus\n            (Portfolio_Id, mean, mkt_mean, stdp, mkt_stdp,\n             beta, var95, var99, mkt_var95, mkt_var99, capm,price,currency,mkt_cap)\n            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)'
            statusM = 'F'
            try:
                cursor.execute(delpor, (PorID,))
                cursor.execute(inspor, lstins)
                statusM = 'S'
            except pgs.Error as e:
                try:
                    print('Unable to connect!')
                    print(e.pgerror)
                finally:
                    e = None
                    del e

            c = 0
            delconst = 'delete from index_acutulus_const where Portfolio_Id=%s'
            try:
                cursor.execute(delconst, (PorID,))
            except pgs.Error as e:
                try:
                    print('Unable to connect!')
                    print(e.pgerror)
                finally:
                    e = None
                    del e

            pdate = dt.datetime.today().date() - dt.timedelta(days=1)
            for i in range(len(symwdf)):
                symbol = symwdf['symbol'].iloc[i]
                price = symwdf['price'].iloc[i]
                currency = symwdf['currency'].iloc[i]
                wt = symwdf['wt'].iloc[i]
                src = symwdf['src'].iloc[i]
                msym = symwdf['msymbol'].iloc[i]
                lstconst = [PorID, symbol, price, wt, currency, src, msym]
                lstconsth = [PorID, symbol, price, wt, currency, src, msym, pdate]
                insconst = 'insert into index_acutulus_const\n                (Portfolio_Id, symbol, price, weight, currency, source_table, exch)\n                 values (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
                insconsth = 'insert into index_acutulus_const_history\n                (Portfolio_Id, symbol, price, weight, currency, source_table, exch, price_Date)\n                 values (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
                statusC = 'F'
                try:
                    cursor.execute(insconst, lstconst)
                    cursor.execute(insconsth, lstconsth)
                    statusC = 'S'
                    c = c + 1
                except pgs.Error as e:
                    try:
                        print('Unable to connect!')
                        print(e.pgerror)
                    finally:
                        e = None
                        del e

            print('missing index:\n', mmdf.values)
            lstins.append(pdate)
            print(lstins)
            insporh = 'insert into index_acutulus_history\n                    (portfolio_id, mean, mkt_mean, stdp, mkt_stdp,\n                     beta, var95, var99, mkt_var95, mkt_var99, capm,price,currency,mkt_cap, price_date)\n                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s, %s)\n                    ON CONFLICT (portfolio_id, price_date) DO UPDATE SET\n                        mean = EXCLUDED.mean, mkt_mean=EXCLUDED.mkt_mean,\n                        stdp=EXCLUDED.stdp, mkt_stdp = EXCLUDED.mkt_stdp,\n                        beta=EXCLUDED.beta, var95 = EXCLUDED.var95,\n                        var99=EXCLUDED.var99, mkt_var95 = EXCLUDED.mkt_var95,\n                        capm=EXCLUDED.capm, mkt_var99 = EXCLUDED.mkt_var99,\n                        price=EXCLUDED.price,currency=EXCLUDED.currency,\n                        mkt_cap=EXCLUDED.mkt_cap'
            statusH = 'F'
            try:
                cursor.execute(insporh, lstins)
                statusH = 'S'
            except pgs.Error as e:
                try:
                    print('Unable to connect!')
                    print(e.pgerror)
                finally:
                    e = None
                    del e

            if statusM == 'S' and statusC == 'S':
                if statusH == 'S':
                    print(PorID, ' was successfully added to the index. check index_acutulus for details')
                    print(c, ' out of ', len(symwdf), ' constituents were loaded')
                elif statusM == 'S' and statusC != 'S' and statusH != 'S':
                    print(PorID, ' was successfully inserted in master but failed in history and constituents')
                    print(c, ' out of ', len(symwdf), ' constituents were loaded')
                elif statusM != 'S' and statusC == 'S' and statusH != 'S':
                    print(PorID, ' was successfully inserted in conmstituents but failed in history and master')
                    print(c, ' out of ', len(symwdf), ' constituents were loaded')
            elif statusM != 'S' and statusC != 'S' and statusH == 'S':
                print(PorID, ' was successfully inserted in history but failed in master and constituents')
                print(c, ' out of ', len(symwdf), ' constituents were loaded')
            else:
                if statusM == 'S' and statusC == 'S' and statusH != 'S':
                    print(PorID, ' was successfully inserted in master n constituents but failed in history')
                    print(c, ' out of ', len(symwdf), ' constituents were loaded')
                else:
                    if statusM == 'S' and statusC != 'S' and statusH == 'S':
                        print(PorID, ' was successfully inserted in master and history but failed in constituents')
                        print(c, ' out of ', len(symwdf), ' constituents were loaded')
                    else:
                        if statusM != 'S' and statusC == 'S' and statusH == 'S':
                            print(PorID, ' was successfully inserted in constituent and history but failed in master')
                            print(c, ' out of ', len(symwdf), ' constituents were loaded')
                        else:
                            print(PorID, ' couldnt be loaded anywhere')
        else:
            print('This particular Portfolio group', Port, 'currently has no constituents')