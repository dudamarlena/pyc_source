# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vrishank/anaconda3/lib/python3.6/site-packages/tests/optimise.py
# Compiled at: 2018-12-16 02:37:38
# Size of source mod 2**32: 2611 bytes
import sys, os, numpy as np

def run_cci(year, stock, window, up, down):
    import test_cci
    return test_cci.test(year, stock, window, up, down, get_plots=False, verbose=False)


def run_sma(year, stock, window, up, down):
    import test_sma
    return test_sma.test(year, stock, window, up, down, get_plots=False, verbose=False)


def run_ema(year, stock, window, up, down):
    import test_ema
    return test_ema.test(year, stock, window, up, down, get_plots=False, verbose=False)


def run_dema(year, stock, window, up, down):
    import test_dema
    return test_dema.test(year, stock, window, up, down, get_plots=False, verbose=False)


def run_tema(year, stock, window, up, down):
    import test_tema
    return test_tema.test(year, stock, window, up, down, get_plots=False, verbose=False)


test_function = {'cci':run_cci, 
 'sma':run_sma, 
 'ema':run_ema, 
 'dema':run_dema, 
 'tema':run_tema}

def run_optimisation(algo, year, stock, window, up, down):
    year_list = []
    stock_list = []
    sharpes = []
    sortinos = []
    rois = []
    if year == 'all':
        year_list = map(str, list(range(2000, 2018)))
    else:
        year_list = [
         year]
    for yr in year_list:
        stocks_avail = os.listdir('../Historical Data/%s/' % yr)
        stocks_avail = [x.split('-')[0] for x in stocks_avail]
        if stock == 'all':
            stock_list = stocks_avail
        else:
            stock_list = [
             stock]
        for stck in stock_list:
            if stck not in stocks_avail:
                print('Data for stock %s not available for year %s' % (stck, yr))
            else:
                sharpe, sortino, roi = test_function[algo](yr, stck, window, up, down)
                sharpes.append(sharpe)
                sortinos.append(sortino)
                rois.append(roi)

    sharpes = np.array(sharpes)
    sortinos = np.array(sortinos)
    mean_sharpe = np.mean(sharpes)
    mean_sortino = np.mean(sortinos)
    std_sharpe = np.std(sharpes)
    std_sortino = np.std(sortinos)
    return (
     mean_sharpe, std_sharpe, mean_sortino, std_sortino)


def optimise(algo, year, stock, window, up, down):
    algo_list = []
    if algo == 'all':
        algo_list = test_function.keys()
    else:
        if algo not in test_function.keys():
            print('Algo %s is not available' % algo)
            return
        else:
            return run_optimisation(algo, year, stock, window, up, down)
    for alg in algo_list:
        mean_sharpe, std_sharpe, mean_sortino, std_sortino = run_optimisation(alg, year, stock, window, up, down)
        print(' Values in order ', mean_sharpe, stddev_sharpe, mean_sortino, std_sortino)


if __name__ == '__main__':
    if len(sys.argv) != 7:
        print('Invalid input')
        sys.exit(1)
    optimise(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])