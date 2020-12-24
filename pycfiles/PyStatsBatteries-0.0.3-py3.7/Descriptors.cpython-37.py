# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyStatsBatteries/Descriptors.py
# Compiled at: 2020-02-04 11:00:26
# Size of source mod 2**32: 7888 bytes
import matplotlib.pyplot as plt
import seaborn as sns, pandas as pd
from sklearn.metrics import r2_score
from PyStatsBatteries import Management
plt.style.use('ggplot')
__all__ = [
 'Descriptors']

class Descriptors:
    __doc__ = '\n    This class provides several functions for descriptive analysis, included boxplots, barplots, plots, ...\n    You can use them through different python dataframes.\n    '

    def Per_feature(self, X, feature):
        """

        :param X: a dataframe
        :param feature: a string with the name of the feature to be plot
        :return: the estimated distribution of the feature
        """
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_alpha(0.7)
        sns.kdeplot((X[feature]), shade=True, color='r')
        plt.xlabel('bins')
        plt.ylabel('freq')
        plt.title('Kernel density estimated')
        plt.show()

    def Barplot(self, X, feature1, feature2):
        """

        :param X: a dataframe
        :param feature1: a sting with the name of the quantitative feature to be plot
        :param feature2: a string with the name of the feature which split the data
        :return: a barplot of the feature1 for each value of feature2
        """
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_alpha(0.7)
        sns.barplot(x=feature2, y=feature1, data=X)
        plt.title('Average distribution by group')
        plt.show()

    def Boxplot(self, X, feature1, feature2):
        """

        :param X: a dataframe
        :param feature1: a sting with the name of the quantitative feature to be plot
        :param feature2: a string with the name of the feature which split the data
        :return: a boxplot of the feature1 for each value of feature2
        """
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_alpha(0.7)
        sns.set(style='ticks', palette='pastel')
        sns.boxplot(x=feature2, y=feature1, data=X)
        sns.despine(offset=10, trim=True)
        plt.title('Boxplot for quatitative feature ' + feature2 + 'with respect to categories')
        plt.show()

    def Scatterplot(self, X, feature1, feature2):
        """

        :param X: a dataframe
        :param feature1: a sting with the name of the quantitative feature to be plot
        :param feature2: a string with the name of the quantitative feature which split the data
        :return: a plot of the feature2 versur feature1 with point
        """
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_alpha(0.7)
        sns.set(style='darkgrid')
        sns.scatterplot(x=feature2, y=feature1, data=X, label=feature1)
        plt.title('Scatterplot for the evolution of ' + feature1 + ' in terms of ' + feature2)
        plt.show()

    def MultiScatterplot(self, X, feature1, feature2):
        """

        :param X: a dataframe
        :param feature1: a list of stings with the name of the quantitative features to be plot in the same figure
        :param feature2: a string with the name of the quantitative feature which split the data
        :return: a plot of the feature2 versur feature1 with point
        """
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_alpha(0.7)
        sns.set(style='darkgrid')
        for feat in feature1:
            sns.scatterplot(x=feature2, y=feat, data=X, label=feat)

        plt.ylabel('values')
        plt.title('Comparaison of values by ' + feature2)
        plt.show()

    def Plot(self, X, feature1, feature2):
        """

        :param X: a dataframe
        :param feature1: a sting with the name of the quantitative feature to be plot
        :param feature2: a string with the name of the quantitative feature which split the data
        :return: a plot of the feature2 versur feature1 with lines
        """
        m = Management.Management()
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_alpha(0.7)
        sns.set(style='darkgrid')
        X = m.OrderBy(X, feature1, feature2)
        plt.plot((list(X[feature2])), (list(X[feature1])), label=feature1)
        plt.ylabel(feature1)
        plt.xlabel(feature2)
        plt.title('Scatterplot for the evolution of ' + feature1 + ' in terms of ' + feature2)
        plt.show()

    def MultiPlot(self, X, feature1, feature2):
        """

        :param X: a dataframe
        :param feature1: a list of stings with the name of the quantitative features to be plot
        :param feature2: a string with the name of the quantitative feature which split the data
        :return: a plot of the feature2 versur feature1 with lines
        """
        m = Management.Management()
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_alpha(0.7)
        sns.set(style='darkgrid')
        for feat in feature1:
            X = m.OrderBy(X, feat, feature2)
            plt.plot((list(X[feature2])), (list(X[feat])), label=feat)

        plt.ylabel('values')
        plt.xlabel(feature2)
        plt.title('Comparaison of values by ' + feature2)
        plt.show()

    def Correlation(self, X, feature1, feature2):
        """

        :param X: a dataframe
        :param feature1: a string with the feature1 to be analyse
        :param feature2: a string with the feature2 to be analyse
        :return: a 2D-plot with the marginal distribution and the supposed linearity which is tested
        """
        sns.set(style='darkgrid')
        sns.jointplot(feature1, feature2, data=X, kind='reg',
          truncate=False,
          xlim=(
         min(list(X[feature1])), max(list(X[feature1]))),
          ylim=(min(list(X[feature2])),
         max(list(X[feature2]))),
          color='b',
          height=7)
        plt.show()

    def Comparaison(self, YTest, predictions):
        """

        :param YTest: a dataframe with true values
        :param predictions: a dataframe with predictive values
        :return: a plot for each feature with compare true values versus predictive ones
        """
        for i in predictions.columns:
            fig = plt.figure(figsize=(12, 8))
            fig.patch.set_facecolor('#E0E0E0')
            fig.patch.set_alpha(0.7)
            xx = list([min(list(YTest[i])), max(list(YTest[i]))])
            plt.plot(xx, xx, label='1st bissector', color='blue', linestyle='dashed')
            plt.plot((list(YTest[i])), (list(predictions[i])), 'r+', label=i)
            plt.xlabel('True Values', fontsize=14)
            plt.ylabel('Predictions', fontsize=14)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            plt.title(('Feature : ' + i + '. R2 score = ' + str(r2_score(list(YTest[i]), list(predictions[i])))), fontsize=14)
            plt.legend(fontsize=15)
            plt.show()

    def plot_history(self, history):
        """

        :param history: a list from neural network with evolution of error through epochs
        :return: 2 graphics with the mse and mae
        """
        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch
        plt.figure(figsize=(12, 8))
        plt.xlabel('Epoch')
        plt.ylabel('Mean Abs Error')
        plt.plot((hist['epoch']), (hist['mean_absolute_error']), label='Train Error')
        plt.plot((hist['epoch']), (hist['val_mean_absolute_error']), label='Val Error')
        plt.ylim([0, 5])
        plt.legend()
        plt.figure(figsize=(12, 8))
        plt.xlabel('Epoch')
        plt.ylabel('Mean squared_error')
        plt.plot((hist['epoch']), (hist['mean_squared_error']), label='Train Error')
        plt.plot((hist['epoch']), (hist['val_mean_squared_error']), label='Val Error')
        plt.ylim([0, 5])
        plt.legend()
        plt.show()