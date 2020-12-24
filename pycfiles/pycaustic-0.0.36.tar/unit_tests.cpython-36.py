# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/PyCausality/Testing/unit_tests.py
# Compiled at: 2018-11-07 10:08:28
# Size of source mod 2**32: 10071 bytes
import numpy, pandas as pd
from scipy.stats import skewnorm, entropy
import os
from nose.tools import assert_almost_equal, assert_raises, raises
from PyCausality.TransferEntropy import *
from PyCausality.Testing.Test_Utils.Time_Series_Generate import *
import matplotlib.pyplot as plt

def test_NDHistogram():
    """
        Test function to ensure that the custom NDHistogram class correctly captures all
        data from 1 to 4 dimensions. Entropy must correspond to get_entropy() function.

    """
    data = pd.read_csv(os.path.join(os.getcwd(), 'PyCausality', 'Testing', 'Test_Utils', 'test_data.csv'))
    Hist1D = NDHistogram(df=(data[['S1']]))
    if not len(data) == np.sum(Hist1D.Hist):
        raise AssertionError
    else:
        Hist2D = NDHistogram(df=(data[['S1', 'S2']]))
        assert len(data) == np.sum(Hist2D.Hist)
        Hist3D = NDHistogram(df=(data[['S1', 'S2', 'S3']]))
        assert len(data) == np.sum(Hist3D.Hist)
        Hist4D = NDHistogram(df=(data[['S1', 'S2', 'S3', 'S4']]))
        assert len(data) == np.sum(Hist4D.Hist)
        AB1 = AutoBins(df=(data[['S1']]))
        assert sorted(Hist1D.Dedges) == sorted(AB1.sigma_bins()['S1'])


def test_equiprobable_Bins():
    """
        There will be a test that each bin in the 2D equiprobable bins contains (roughly) equal number of samples (height)
        
        Unfortunately we know that the current algorithm does not guarantee this, so future implementations
        will be tested on this basis. (see: https://scicomp.stackexchange.com/questions/30023/)
    """
    pass


def test_LaggedTimeSeries():
    """
        Test Function to ensure LaggedTimeSeries creates new lagged columns for each
        column passed in as a DataFrame
    """
    data = pd.read_csv(os.path.join(os.getcwd(), 'PyCausality', 'Testing', 'Test_Utils', 'test_data.csv'))
    data['date'] = pd.to_datetime((data['date']), format='%d/%m/%Y')
    data.set_index('date', inplace=True)
    LAG = 1
    lagDF = LaggedTimeSeries(df=data, lag=LAG).df
    for i, dim in enumerate(data.columns.values):
        assert len(lagDF.columns.values) == 2 * len(data.columns.values)

    for LAG in (1, 2, 3, 4):
        lagDF = LaggedTimeSeries(df=data, lag=LAG).df
        assert all(lagDF[('S1_lag' + str(LAG))].values == data['S1'][:-LAG].values)
        assert all(lagDF[('S2_lag' + str(LAG))].values == data['S2'][:-LAG].values)
        assert all(lagDF[('S3_lag' + str(LAG))].values == data['S3'][:-LAG].values)
        assert all(lagDF[('S4_lag' + str(LAG))].values == data['S4'][:-LAG].values)

    window_sizes = [
     {'YS':0, 
      'MS':0,  'D':10,  'H':0,  'min':0,  'S':0,  'ms':0},
     {'YS':0, 
      'MS':1,  'D':0,  'H':0,  'min':0,  'S':0,  'ms':0},
     {'YS':1, 
      'MS':0,  'D':0,  'H':0,  'min':0,  'S':0,  'ms':0},
     {'YS':0, 
      'MS':3,  'D':14,  'H':0,  'min':0,  'S':0,  'ms':0}]
    window_strides = [
     {'YS':0, 
      'MS':0,  'D':7,  'H':0,  'min':0,  'S':0,  'ms':0},
     {'YS':0, 
      'MS':3,  'D':0,  'H':0,  'min':0,  'S':0,  'ms':0},
     {'YS':1, 
      'MS':0,  'D':0,  'H':0,  'min':0,  'S':0,  'ms':0},
     None]
    for stride in window_strides:
        for size in window_sizes:
            lagDF = LaggedTimeSeries(df=(data[['S1', 'S2']]), lag=LAG, window_size=size, window_stride=stride)
            print('\n Number of Windows:', len(list(lagDF.windows)))
            try:
                print('Items per window:', len(next(lagDF.windows)))
            except:
                print('Items per window:', len(lagDF.df))


def test_shuffle_series():
    """
        Test function to ensure Inference.shuffle_series() reorders data within columns.
        If parameter 'only' is specified, only that column should be shuffled; otherwise
        all columns must be shufffled.
    """
    DF = coupled_random_walks(S1=100, S2=100, T=10, N=200,
      mu1=0.1,
      mu2=0.02,
      sigma1=0.01,
      sigma2=0.01,
      alpha=0.1,
      epsilon=0,
      lag=2)
    DF_shuffled = shuffle_series(DF)
    assert_almost_equal(np.mean(DF['S1']), np.mean(DF_shuffled['S1']))
    assert_almost_equal(np.mean(DF['S2']), np.mean(DF_shuffled['S2']))
    if not not np.sum(DF['S1'].head(20)) == np.sum(DF_shuffled['S1'].head(20)):
        raise AssertionError
    else:
        if not not DF.head(10).equals(DF_shuffled.head(10)):
            raise AssertionError
        else:
            S1_shuffled = shuffle_series(DF, only=['S1'])
            assert_almost_equal(np.mean(DF['S1']), np.mean(S1_shuffled['S1']))
            assert_almost_equal(np.mean(DF['S2']), np.mean(S1_shuffled['S2']))
            assert DF['S2'].head(10).equals(S1_shuffled['S2'].head(10))
            assert not DF['S1'].head(10).equals(S1_shuffled['S1'].head(10))
            S2_shuffled = shuffle_series(DF, only=['S2'])
            assert_almost_equal(np.mean(DF['S1']), np.mean(S1_shuffled['S1']))
            assert_almost_equal(np.mean(DF['S2']), np.mean(S1_shuffled['S2']))
            assert DF['S1'].head(10).equals(S2_shuffled['S1'].head(10))
        assert not DF['S2'].head(10).equals(S2_shuffled['S2'].head(10))


def test_get_pdf():
    """
        Test Function to check that get_pdf() accurately models a probability density function.
        Tests both kernel and histogram density estimation on a set of randonly skewed normals, such that
        the average cumulative distribution function is approximately equal to 1/2 

    """
    cdfs_kde = []
    cdfs_hist = []
    N = 1000
    sd = 0.5
    alphas = np.linspace(-5, 5, 10)
    means = np.linspace(-5, 5, 10)
    for a in alphas:
        for mean in means:
            data = skewnorm.rvs(size=N, a=a, loc=mean, scale=sd)
            TS = pd.DataFrame({'data': data})
            pdf_kde = get_pdf((TS[['data']]), estimator='kernel', gridpoints=20, bandwidth=0.6)
            pdf_hist = get_pdf((TS[['data']]), estimator='histogram')
            assert_almost_equal(pdf_hist.sum(), 1.0, 8)
            assert_almost_equal(pdf_kde.sum(), 1.0, 8)
            plt.plot(np.linspace(data.min(), data.max(), 20), pdf_kde)
            cdfs_kde.append(np.sum(pdf_kde[:10]))
            cdfs_hist.append(np.sum(pdf_kde[:10]))

    assert_almost_equal(np.average(cdfs_kde), 0.5, 1)
    assert_almost_equal(np.average(cdfs_hist), 0.5, 1)


def test_joint_entropy():
    """
        Test that our implemented function to return the entropy corresponds 
        to Scipy's entropy method
    """
    gridpoints = 10
    S = np.random.normal(0, 0.1, 10000)
    data = pd.DataFrame(S)
    pdf = get_pdf(data, gridpoints=gridpoints)
    assert_almost_equal(get_entropy(data, gridpoints=gridpoints), entropy(pdf, base=2), 5)


def test_joint_entropyND():
    """
        Test that our implemented function to return the entropy corresponds 
        to Scipy's entropy method in multiple dimensions.
    """
    gridpoints = 10
    X = skewnorm.rvs(size=1000, a=(-3), loc=0, scale=2)
    Y = skewnorm.rvs(size=1000, a=(-3), loc=0, scale=2)
    data = pd.DataFrame({'X':X,  'Y':Y})
    pdf = get_pdf(data, gridpoints=gridpoints)
    assert_almost_equal(get_entropy(data, gridpoints=gridpoints), entropy((pdf.flatten()), base=2), 5)


def test_sanitise():
    """
        Test function to ensure user-defined time series data is sanitised to minimise
        the risk of avoidable errors (i.e. univariate data in pd.Series form exposes no
        .columns() property, which is used widely in PyCausality functions.
    """
    series = pd.Series({'S1': [0, 1, 2, 3, 4, 5]})
    DF = pd.DataFrame({'S1':[0, 1, 2, 3, 4, 5],  'S2':[
      1, 2, 3, 4, 5, 6]})
    if not isinstance(series, pd.Series):
        raise AssertionError
    else:
        if not isinstance(DF, pd.DataFrame):
            raise AssertionError
        elif not isinstance(sanitise(series), pd.DataFrame):
            raise AssertionError
        assert isinstance(sanitise(DF), pd.DataFrame)