# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/madjuice/Documents/Python/crosspredict/crosspredict/report_binary/_report_binary.py
# Compiled at: 2020-04-05 11:54:02
# Size of source mod 2**32: 10770 bytes
from typing import List, Tuple, Dict
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product
from ._curves import PrecisionRecallCurve, RocAucCurve, MeanProbCurve, GenGINICurve, DistributionCurve

class ReportBinary:
    """ReportBinary"""

    def __init__(self, cols_score: List[str], cols_target: List[str], col_generation_apps: str=None, col_generation_deals: str=None):
        self._report_shape = None
        self._report = None
        self._product_plots = None
        self.fig = None
        self._col_generation_deals = col_generation_deals
        self._col_generation_apps = col_generation_apps
        self._cols_score = cols_score
        self._cols_target = cols_target
        tuples = [(i, j) for i, j in product(self._cols_score, self._cols_target)]
        index = pd.MultiIndex.from_tuples(tuples,
          names=['cols_score', 'cols_target'])
        self.stats = pd.DataFrame(index=index)

    def fit(self, df: pd.DataFrame) -> 'ReportBinary':
        """
        Precalculates metrics and statistics for given pd.DataFrame
        :param df: pd.DataFrame
        :return: self class
        """
        if not all([i in df.columns for i in self._cols_score]):
            raise AssertionError
        else:
            assert all([i in df.columns for i in self._cols_target])
            if self._col_generation_deals:
                assert self._col_generation_deals in df.columns, f'DataFrame does not have column col_generation_deals="{self._col_generation_deals}"'
            if self._col_generation_apps and not self._col_generation_apps in df.columns:
                raise AssertionError(f'DataFrame does not have column _col_generation_apps="{self._col_generation_apps}"')
        mask_score = ~df[self._cols_score].isnull().any(axis=1)
        df_app = df[mask_score]
        for col_target in self._cols_target:
            mask_target = ~df[col_target].isnull()
            df_deal = df[(mask_score & mask_target)]
            for col_score in self._cols_score:
                self.stats.at[((col_score, col_target), 'distribution')] = DistributionCurve(col_score, col_target).fit(df_deal)
                if self._col_generation_deals is not None:
                    self.stats.at[((col_score, col_target), 'gen-gini')] = GenGINICurve(col_score, col_target, self._col_generation_deals).fit(df_deal)
                self.stats.at[((col_score, col_target), 'mean-prob')] = MeanProbCurve(col_score, col_target).fit(df_deal)
                self.stats.at[((col_score, col_target), 'roc-auc')] = RocAucCurve(col_score, col_target).fit(df_deal)
                self.stats.at[((col_score, col_target), 'precision-recall')] = PrecisionRecallCurve(col_score, col_target).fit(df_deal)

        return self

    def _draw_template(self):
        """
        отрисовка шаблона графиков
        """
        height = self._report_shape[0]
        width = self._report_shape[1]
        self.fig = plt.gcf()
        self.fig.set_size_inches(width * 6, height * 5)
        plt.subplots_adjust(left=0.125, right=0.9,
          bottom=0.1,
          top=0.95,
          wspace=0.35,
          hspace=0.6)
        for report, locations in self._report.items():
            res = []
            if report == 'roc-auc':
                if isinstance(locations, tuple) | isinstance(locations, list):
                    assert len(locations) == 1, f"Location of Roc-Auc plot should have `len`==1, passed `len`={len(locations)}"
                    loc = locations[0]
                else:
                    loc = locations
                ax = (plt.subplot2grid)((height, width), **loc)
                res = {'ax': ax}
            elif report == 'precision-recall':
                if isinstance(locations, tuple) | isinstance(locations, list):
                    assert len(locations) == 1, f"Location of Precision-Recall plot should have `len`==1, passed `len`={len(locations)}"
                    loc = locations[0]
                else:
                    loc = locations
                ax = (plt.subplot2grid)((height, width), **loc)
                res = {'ax': ax}
            elif report == 'mean-prob':
                res = []
                if isinstance(locations, tuple) | isinstance(locations, list):
                    for loc in locations:
                        res.append({'ax': (plt.subplot2grid)((height, width), **loc)})

                else:
                    loc = locations
                    res.append({'ax': (plt.subplot2grid)((height, width), **loc)})
                if not len(res) == self._product_plots:
                    raise AssertionError(f"Location of Mean-Probability plot should have `len`=={self._product_plots}, passed `len`={len(res)}")
            elif report == 'gen-gini':
                if not self._col_generation_deals is not None:
                    raise AssertionError('To plot GINI by generations you need to pass `col_generation_deals`')
                elif isinstance(locations, tuple) | isinstance(locations, list):
                    assert len(locations) == 1, f"Location of GINI by generations plot should have `len`==1, passed `len`={len(locations)}"
                    loc = locations[0]
                else:
                    loc = locations
                ax = (plt.subplot2grid)((height, width), **loc)
                res = {'ax':ax,  'ax_twinx':ax.twinx()}
            else:
                if report == 'distribution':
                    res = []
                    if isinstance(locations, tuple) | isinstance(locations, list):
                        for loc in locations:
                            res.append({'ax': (plt.subplot2grid)((height, width), **loc)})

                else:
                    loc = locations
                    res.append({'ax': (plt.subplot2grid)((height, width), **loc)})
                assert len(res) == self._product_plots, f"Location of Distribution plot should have `len`=={self._product_plots}, passed `len`={len(res)}"
            self._report[report] = res

    def plot_report(self, report_shape: List[int], report: Dict=None, cols_score: List[str]=None, cols_target: List[str]=None):
        """
        Plots report of given configuration.

        :param report_shape: List[int] Shape of subplot axes. Read more https://matplotlib.org/3.1.1/gallery/userdemo/demo_gridspec01.html#sphx-glr-gallery-userdemo-demo-gridspec01-py
        :param report: Dict Dict with reports and their location. Read more https://matplotlib.org/3.1.1/gallery/userdemo/demo_gridspec01.html#sphx-glr-gallery-userdemo-demo-gridspec01-py
        :param cols_score: List[str] SubList of column names with model probabilities
        :param cols_target: List[str] SubList of column names with true binary labels
        :return:
        """
        if cols_score is None:
            cols_score = self._cols_score
        else:
            cols = [col for col in cols_score if col not in self._cols_score]
        if not len(cols) == 0:
            raise AssertionError(f"Columns {cols} did not calculated in `fit` method. `cols_score`={self._cols_score} were passed in ReportBinary class")
        elif cols_target is None:
            cols_target = self._cols_target
        else:
            cols = [col for col in cols_target if col not in self._cols_target]
            assert len(cols) == 0, f"Columns {cols} did not calculated in `fit` method. `cols_target`={self._cols_target} were passed in ReportBinary class"
        self._product_plots = len(cols_score) * len(cols_target)
        self._report_shape = report_shape
        self._report = report
        self._draw_template()
        for report, locations in self._report.items():
            if report == 'roc-auc':
                for col_score, col_target in product(cols_score, cols_target):
                    self.stats.at[((col_score, col_target), report)].plot((self._report[report]['ax']),
                      title='Roc-Auc')

            elif report == 'precision-recall':
                for col_score, col_target in product(cols_score, cols_target):
                    self.stats.at[((col_score, col_target), report)].plot((self._report[report]['ax']),
                      title='Precision-Recall')

            elif report == 'mean-prob':
                for i, (col_score, col_target) in enumerate(product(cols_score, cols_target)):
                    self.stats.at[((col_score, col_target), report)].plot((self._report[report][i]['ax']),
                      title=(col_score + ' | ' + col_target))

            elif report == 'gen-gini':
                for col_score, col_target in product(cols_score, cols_target):
                    self.stats.at[(
                     (col_score,
                      col_target),
                     report)].plot((self._report[report]['ax']), ax_twinx=(self._report[report]['ax_twinx']),
                      title='GINI by generations')

            elif report == 'distribution':
                for i, (col_score, col_target) in enumerate(product(cols_score, cols_target)):
                    self.stats.at[((col_score, col_target), report)].plot((self._report[report][i]['ax']),
                      title='Predict Distribution')

        return self