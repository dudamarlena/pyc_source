# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/analyze.py
# Compiled at: 2017-11-30 11:22:44
# Size of source mod 2**32: 19925 bytes
from bokeh.io import gridplot
from statsmodels.stats import outliers_influence
import operator, functools, itertools, random, numpy as np, pandas as pd
from . import sklearnUtils as sku
from . import plotter
from . import utils
from . import statsutils as su

def dist_analyze(df, column='', category='', is_normal=True, bayesian_hist=False, kdeplot=True, violinplot=False):
    plots = []
    if utils.is_numeric(df, column=column):
        print('Variance of %s' % column)
        print(df[column].var())
        print('Skewness of %s' % column)
        print(df[column].skew())
        su.distribution_tests(df, column)
        if is_normal:
            su.check_normality(df[column], column)
        if violinplot:
            plotter.sb_violinplot((df[column]), inner='box')
        plots.append(plotter.histogram(df, column, bayesian_bins=bayesian_hist))
    else:
        if df[column].nunique() < 7:
            plots.append(plotter.pieChart(df, column, title=('Distribution of %s' % column)))
        else:
            print("Too many categories for col: %s can't plot pie-chart" % column)
    if kdeplot:
        assert utils.is_numeric(df, column=column), 'KDE Plot Only available for numerical columns'
        df[column].plot.kde(label=column, title='Kernel density estimate')
    if category:
        plots.append(plotter.barplot(df, column, category))
        print('# Joint Distribution of Numerical vs Categorical Columns')
    grid = gridplot(list(utils.chunks(plots, size=2)))
    return grid


def outliers_analyze(df):
    rng = np.random.RandomState(42)
    n_samples = 200
    outliers_fraction = 0.25
    clusters_separation = [0, 1, 2]
    classifiers = {'One-Class SVM':svm.OneClassSVM(nu=0.95 * outliers_fraction + 0.05, kernel='rbf',
       gamma=0.1), 
     'Robust covariance':EllipticEnvelope(contamination=outliers_fraction), 
     'Isolation Forest':IsolationForest(max_samples=n_samples, contamination=outliers_fraction,
       random_state=rng)}
    plots = list()
    for i, (clf_name, clf) in enumerate(classifiers.items()):
        clf.fit(X)
        scores_pred = clf.decision_function(X)
        threshold = stats.scoreatpercentile(scores_pred, 100 * outliers_fraction)
        y_pred = clf.predict(X)
        predictions[clf_name] = y_pred
        n_errors = (y_pred != ground_truth).sum()

    return predictions


def correlation_analyze(df, col1, col2, categories=[], measures=[], summary_only=False, check_linearity=False, trellis=False):
    """
    Plot scatter plots of all combinations of numerical columns.
    If categories and measures are passed, plot heatmap of combination of categories by measure.

    @params:
        df: Dataframe table data.
        categories: list of categorical variable names
        measures: List of measures to plot heatmap of categories
        trellis: Plot trellis type plots for the categories only valid if categories is passed
    """
    if summary_only:
        plotter.heatmap(df.corr())
    else:
        for meas in measures:
            assert meas in list(df.columns)

        for catg in categories:
            assert catg in list(df.columns)

        if categories:
            if not measures:
                measures = [
                 'count']
        plots = []
        u, v = col1, col2
        plots.append(plotter.scatterplot(df, u, v))
        plotter.sb_jointplot(df[u], df[v])
        if check_linearity:
            u_2diff = np.gradient(df[u], 2)
            v_2diff = np.gradient(df[v], 2)
            print('Linearity btw %s and %s' % (u, v))
            print('No. of 2nd differences: %d' % len(u_2diff))
            linearity_2nd_diff = np.divide(u_2diff, v_2diff)
            linearity_2nd_diff = linearity_2nd_diff[(~np.isnan(linearity_2nd_diff))]
            linearity_2nd_diff = linearity_2nd_diff[(~np.isinf(linearity_2nd_diff))]
            print(np.mean(linearity_2nd_diff))
        print('# Correlation btw Numerical Columns')
        grid = gridplot(list(utils.chunks(plots, size=2)))
        plotter.show(grid)
        if categories:
            if measures:
                heatmaps = []
                combos = itertools.combinations(categories, 2)
                cols = list(df.columns)
                if 'count' in measures:
                    measures.remove('count')
                    for combo in combos:
                        print('# Correlation btw Columns %s & %s by count' % (combo[0], combo[1]))
                        group0 = df.groupby(list(combo)).size().reset_index()
                        group0.rename(columns={col1: 'counts'}, inplace=True)
                        heatmaps.append(plotter.heatmap(group0, combo[0], combo[1], 'counts'))

                for meas in measures:
                    for combo in combos:
                        print('# Correlation btw Columns %s & %s by measure %s' % (combo[0],
                         combo[1],
                         meas))
                        group0 = df.groupby(list(combo)).sum().reset_index()
                        group0.rename(columns={meas: 'sum_%s' % meas}, inplace=True)
                        heatmaps.append(plotter.heatmap(group0, (combo[0]), (combo[1]), ('sum_%s' % meas), title=('%s vs %s %s heatmap' % (combo[0], combo[1], meas))))

                hmGrid = gridplot(list(utils.chunks(heatmaps, size=2)))
                plotter.show(hmGrid)
                if trellis:
                    trellisPlots = list()


def degrees_freedom(df, dof_range=[], categoricalCol=[]):
    """
    Find what are the maximum orthogonal dimensions in the data
    """
    if categoricalCol:
        assert len(categoricalCol) == 2, 'Only two categories supported'
        probabilities = dict()
        for col in categoricalCol:
            values = df[categoricalCol].unique()
            grouped_df = df.groupby(categoricalCol).count()
            for val in values:
                probabilities[(col, val)] = grouped_df[val] / df[categoricalCol].count()

        print(probabilities)
    else:
        for col1, col2 in utils.chunks(df.columns, 2):
            chi2_test_independence(df[col1], df[col2])


def measure_distance(dist_type='cosine', dof_range=[]):
    if not dof_range:
        dof_range = range(2, 3)
    elif not hasattr(dof_range, '__iter__'):
        raise AssertionError
    from scipy.spatial.distance import cosine, cityblock, jaccard, canberra, euclidean, minkowski, braycurtis
    dist_measure = eval(dist_type)
    dof_range = [2]
    all_cosine_dists = dict()
    for each in dof_range:
        combos = itertools.combinations(df.columns, each)
        cosine_dist = dict()
        for combo in combos:
            cosine_dist[combo] = dist_function(df[combo[0]], df[combo[1]])

        all_cosine_dists[each] = sorted((cosine_dist.items()), key=(operator.itemgetter(1)))

    print('%s Distance Method' % dist_type)
    return all_cosine_dists


def factor_analyze(df, target=None, model_type='pca', **kwargs):
    model = (utils.get_model_obj)(model_type, **kwargs)
    numericalColumns = df.select_dtypes(include=[np.number]).columns
    catColumns = set(df.columns).difference(set(numericalColumns))
    for col in catColumns:
        df[col] = sku.encode_labels(df, col)

    print('Model being used is :%s ' % model_type)
    if model_type == 'linear_da':
        assert target is not None, 'Target class/category necessary for Linear DA factor analysis'
        model.fit(df, target)
        print('Coefficients')
        print(model.coef_)
        print('Covariance')
        print(model.covariance_)
    else:
        if model_type == 'latent_da':
            print('Components')
            print(model.components_)
        else:
            model.fit(df[numericalColumns])
            print('No. of Components')
            print(model.n_components)
            print('Components')
            print(model.components_)
            print('Explained variance')
            print(model.explained_variance_)
            exp_var_df = pd.DataFrame(columns=['Principal Components', 'Explained variance'])
            plotter.show(plotter.barplot(exp_var_df, alpha=0.5, align='center', label='individual explained variance'))
    trans_df = pd.DataFrame(model.transform(df))
    print('Correlation of transformed')
    correlation_analyze(trans_df, 0, 1)


def regression_analyze(df, col1, col2, trainsize=0.8, non_linear=False, check_heteroskedasticity=True, check_vif=True, check_dist_similarity=True, **kwargs):
    """
    Plot regressed data vs original data for the passed columns.
    @params:
        col1: x column,
        col2: y column

    @optional:
        non_linear: Use the python ace module to calculate non-linear correlations too.(Warning can
        be very slow)
        check_heteroskedasticity: self-evident
    """
    from . import predictiveModels as pm
    if non_linear:
        plots = list()
        import ace
        model = ace.model.Model()
        model.build_model_from_xy([df[col1].as_matrix()], [df[col2].as_matrix()])
        print(' # Ace Models btw numerical cols')
        plot = plotter.lineplot((df[[col1, col2]]), title=('%s Vs %s' % (col1, col2)))
        plotter.show(plot)
    if check_dist_similarity:
        print('P-value and test statistic for distribution similarity between %s and %s' % (col1, col2))
        is_similar_distribution(df[col1], df[col2])
    new_df = df[[col1, col2]].copy(deep=True)
    target = new_df[col2]
    models = [
     pm.train(new_df, target, column=col1, modelType='LinearRegression'),
     pm.train(new_df, target, column=col1, modelType='RidgeRegression'),
     pm.train(new_df, target, column=col1, modelType='RidgeRegressionCV'),
     pm.train(new_df, target, column=col1, modelType='LassoRegression'),
     pm.train(new_df, target, column=col1, modelType='ElasticNetRegression'),
     pm.train(new_df, target, column=col1, modelType='SVMRegression')]
    plots = list()
    for model in models:
        scatter = plotter.scatterplot(new_df, col1, col2, plttitle=(model.__repr__()))
        source = new_df[col1].as_matrix().reshape(-1, 1)
        predicted = list(model.predict(source))
        flatSrc = [item for sublist in source for item in sublist]
        scatter.line(flatSrc, predicted, line_color='red')
        plots.append(scatter)
        print('Regression Score: %s' % model.__repr__())
        print(model.score(source, new_df[col2].as_matrix().reshape(-1, 1)))
        if check_vif:
            exog = df.as_matrix().reshape(-1, 1)
            for col in [col1, col2]:
                print('Variance Inflation Factors for %s' % col)
                col_idx = list(df.columns).index(col)
                print(outliers_influence.variance_inflation_factor(exog, col_idx))

        if check_heteroskedasticity:
            if not kwargs.get('exog', None):
                other_cols = list(set(df.columns) - set([col1, col2]))
                kwargs['exog'] = random.choice(other_cols)
            exog = df[kwargs.get('exog')].as_matrix().reshape(-1, 1)
            print('Hetero-Skedasticity test(Breush-Pagan)')
            print(diagnostic.het_breushpagan((model.residues_), exog_het=exog))

    grid = gridplot(list(utils.chunks(plots, size=2)))
    plotter.show(grid)


def time_series_analysis(df, timeCol='date', valueCol=None, timeInterval='30min', plot_title='timeseries', skip_stationarity=False, skip_autocorrelation=False, skip_seasonal_decompose=False, psf_analyze=False, **kwargs):
    """
    Plot time series, rolling mean, rolling std , autocorrelation plot, partial autocorrelation plot
    and seasonal decompose
    """
    from . import timeSeriesUtils as tsu
    if 'create' in kwargs:
        ts = (tsu.create_timeseries_df)(df, timeCol=timeCol, timeInterval=timeInterval, **kwargs.get('create'))
    else:
        ts = tsu.create_timeseries_df(df, timeCol=timeCol, timeInterval=timeInterval)
    if 'stationarity' in kwargs:
        plot = (tsu.test_stationarity)(ts, timeCol=timeCol, valueCol=valueCol, title=plot_title, 
         skip_stationarity=skip_stationarity, **kwargs.get('stationarity'))
    else:
        plot = tsu.test_stationarity(ts, timeCol=timeCol, valueCol=valueCol, title=plot_title,
          skip_stationarity=skip_stationarity)
        plotter.show(plot)
    if not skip_autocorrelation:
        if 'autocorrelation' in kwargs:
            (tsu.plot_autocorrelation)(ts, valueCol=valueCol, **kwargs.get('autocorrelation'))
            (tsu.plot_autocorrelation)(ts, valueCol=valueCol, partial=True, **kwargs.get('autocorrelation'))
        else:
            tsu.plot_autocorrelation(ts, valueCol=valueCol)
            tsu.plot_autocorrelation(ts, valueCol=valueCol, partial=True)
        if skip_seasonal_decompose or 'seasonal' in kwargs:
            seasonal_args = kwargs.get('seasonal')
            (tsu.seasonal_decompose)(ts, **seasonal_args)
    else:
        tsu.seasonal_decompose(ts)


def fractal_analyze(dataframe, column, L=None, dim_type='box'):
    if dim_type == 'box':
        plotter.show(_box_dimension(dataframe, column, L=L))
    else:
        plotter.show(_hausdorff_dimension((dataframe[column]), L=L))


def _box_dimension(dataframe, column, L=None):
    if not L:
        L = dataframe[column].max()
    r = np.array([L / 2.0 ** i for i in range(12, 0, -1)])
    N = [utils.count_boxes(dataframe[column], ri, L) for ri in r]

    def f(x, A, Df):
        """
        User defined function for scipy.optimize.curve_fit(),
        which will find optimal values for A and Df.
        """
        return Df * x + A

    import scipy
    popt, pcov = scipy.optimize.curve_fit(f, np.log(1.0 / r), np.log(N))
    A, Df = popt
    new_df = pd.DataFrame(columns=['Box Size(1/r)', 'No. of Boxes'])
    new_df['Box Size(1/r)'] = 1 / r
    new_df['No. of Boxes'] = N
    return plotter.lineplot(new_df, title='Box Size(1/r) Vs No. of Boxes')


def _hausdorff_dimension(pixels):
    scales = np.logspace(1, 8, num=20, endpoint=False, base=2)
    Ns = []
    for scale in scales:
        print('Scale ', scale)
        H, edges = np.histogramdd(pixels, bins=(np.arange(0, Lx, scale), np.arange(0, Ly, scale)))
        Ns.append(np.sum(H > 0))

    plot_df = pd.DataFrame(columns=['log(scales)', 'log(Ns)'])
    plot_df['Log(scales)'] = np.log(scales)
    plot_df['Log(Ns)'] = np.log(Ns)
    coeffs = np.polyfit(np.log(scales), np.log(Ns), 1)
    plotter.lineplot(plot_df, title='log(scales) Vs log(Ns)')


def fractal_dimension(image, threshold=0.9):
    import scipy.misc, numpy as np
    assert len(image.shape) == 2

    def boxcount(image, k):
        S = np.add.reduceat(np.add.reduceat(image, (np.arange(0, image.shape[0], k)), axis=0),
          (np.arange(0, image.shape[1], k)),
          axis=1)
        return len(np.where((S > 0) & (S < k * k))[0])

    image = image < threshold
    p = min(image.shape)
    n = 2 ** np.floor(np.log(p) / np.log(2))
    n = int(np.log(n) / np.log(2))
    sizes = 2 ** np.arange(n, 1, -1)
    counts = []
    for size in sizes:
        counts.append(boxcount(image, size))

    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return -coeffs[0]


def dimension_analyze(dataframe, group=None, **kwargs):
    if not group:
        (plotter.hyper_plot)(dataframe, **kwargs)
    else:
        groupVals = dataframe[group]
        groupLabels = dataframe[group].unique()
        dataframe.drop(group, 1, inplace=True)
        (plotter.hyper_plot)(dataframe, group=groupVals, legend=groupLabels, **kwargs)


def recommend_nn(dataframe, **kwargs):
    pass


def causal_analyze(dataframe):
    for each in dataframe.columns:
        assert utils.is_numeric(dataframe, column=each)

    import networkx
    from networkx import drawing
    import causality
    from causality.inference.independence_tests import RobustRegressionTest
    from causality.inference.search import IC
    variable_types = dict(zip(dataframe.columns, ['c'] * len(dataframe)))
    ic_algorithm = IC(RobustRegressionTest)
    graph = ic_algorithm.search(dataframe, variable_types)
    drawing.draw_networkx(graph)


def chaid_tree(dataframe, targetCol):
    import CHAID as ch
    columns = dataframe.columns
    columns = list(filter(lambda x: x not in [targetCol], dataframe.columns))
    print(ch.Tree.from_pandas_df(dataframe, columns, targetCol))