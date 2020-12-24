# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/anaconda/lib/python2.7/site-packages/DHCstat/datamining.py
# Compiled at: 2018-05-08 03:50:56
import numpy as np, sklearn, pandas as pd, json, codecs, matplotlib.pyplot as plt
pd.set_option('precision', 4)

class LuwakMining:

    def __init__(self):
        self.splits = 10
        print 'Welcome to LuwakMining!'

    def random_forest(self):
        pass

    def flex_gridsearch(self, X, Y, model, params):
        pass

    def predict_results_binary(self, model, X, Y):
        """
        for certain types of models,we calculate predict results,accuracy,auroc,best thresholds
        """
        assert len(X) == len(Y)
        assert type(model) in [sklearn.tree.tree.DecisionTreeClassifier,
         sklearn.ensemble.gradient_boosting.GradientBoostingClassifier,
         sklearn.ensemble.gradient_boosting.AdaBoostClassifier,
         sklearn.ensemble.forest.RandomForestClassifier,
         sklearn.linear_model.logistic.LogisticRegression]
        from sklearn.metrics import confusion_matrix, roc_curve, auc
        model.fit(X, Y)
        prob = pd.DataFrame(model.predict_proba(X=X)[:, 1], index=X.index, columns=['probablity'])
        predict = pd.Series(model.predict(X.iloc[:, :]), index=X.index, name='predict')
        result = prob.join(predict).join(Y)
        accuracy = (Y == predict).mean()
        cm = confusion_matrix(y_true=Y, y_pred=predict)
        fpr, tpr, threshold = roc_curve(Y, result.iloc[:, 0])
        auroc = auc(fpr, tpr)
        rate = pd.DataFrame(tpr - fpr)
        threshold_df = pd.DataFrame(threshold)
        for i in rate.index:
            if rate.ix[(i, 0)] == max(np.array(rate)):
                max_i = i
                best_threshold = threshold_df.ix[(max_i, 0)]

        print (
         'accuracy:', accuracy, 'auroc:', auroc, 'best_threshold:', best_threshold, 'confusion_matrix:', cm)
        return (result, accuracy, auroc, best_threshold, cm)

    def cross_validation_binary(self, X, Y, model, splits, picture=True):
        """
        For certain types of models, do the cross validation and plot the ROC results.
            X:features

            Y:Outcome

            model:Trained classification model

            splits:N of splits in k-fold cross validation

            picture:draw the ROC curve if True,default False
        """
        if splits == None:
            splits = self.splits
            print 'use default splits=10'
        assert type(model) in [sklearn.tree.tree.DecisionTreeClassifier,
         sklearn.ensemble.gradient_boosting.GradientBoostingClassifier,
         sklearn.ensemble.gradient_boosting.AdaBoostClassifier,
         sklearn.ensemble.forest.RandomForestClassifier,
         sklearn.linear_model.logistic.LogisticRegression]
        result, _, _, _, _ = self.predict_results_binary(model=model, X=X, Y=Y)
        from sklearn.model_selection import StratifiedKFold
        skf = StratifiedKFold(n_splits=splits)
        result_10 = pd.DataFrame()
        Y_10 = pd.Series()
        for train, test in skf.split(X, Y):
            X_train_10, X_test_10 = X.iloc[train, :], X.iloc[test, :]
            Y_train_10, Y_test_10 = Y.iloc[train], Y.iloc[test]
            model.fit(X=X_train_10, y=Y_train_10)
            try:
                Y_10 = Y_10.append(Y_test_10)
                result_10 = result_10.append(pd.DataFrame(model.predict_proba(X=X_test_10)[:, 1], index=X_test_10.index, columns=[
                 '预测']).join(Y_test_10))
            except:
                print 'Warning:Error in cross-validation'
                return

        from sklearn.metrics import roc_curve, auc
        fpr_10, tpr_10, threshold_10 = roc_curve(Y_10, result_10.iloc[:, 0])
        auroc_10 = auc(fpr_10, tpr_10)
        fpr, tpr, threshold = roc_curve(Y, result.iloc[:, 0])
        auroc = auc(fpr, tpr)
        rate = pd.DataFrame(tpr - fpr)
        threshold_df = pd.DataFrame(threshold)
        rate_10 = pd.DataFrame(tpr_10 - fpr_10)
        threshold_df = pd.DataFrame(threshold_10)
        for i in rate_10.index:
            if rate_10.ix[(i, 0)] == max(np.array(rate_10)):
                max_i = i
                best_threshold_10 = threshold_df.ix[(max_i, 0)]

        if picture:
            lw = 2
            plt.figure()
            plt.plot(fpr_10, tpr_10, label='ROC-10fold = %f' % auroc_10, lw=lw)
            plt.plot(fpr, tpr, label='ROC = %f' % auroc, lw=lw)
            plt.plot([0, 1], [0, 1], '--', lw=lw)
            plt.axis('square')
            plt.xlim([0, 1])
            plt.ylim([0, 1])
            plt.xlabel('False Positive')
            plt.ylabel('True Positive')
            plt.title('ROC Curve')
            plt.legend(loc='lower right')
            plt.show()
        print (
         'auroc_10_fold:', auroc_10, 'best_threshold_10_fold:', best_threshold_10)
        return (auroc_10, best_threshold_10, tpr_10, fpr_10)