# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mark/PycharmProjects/multi_label_classification/mlclas/svm/ranking_svm.py
# Compiled at: 2016-06-17 11:47:53
# Size of source mod 2**32: 12169 bytes
import numpy as np, cvxpy as cvx, operator
from mlclas.svm.rankingsvm_models import *
from mlclas.neural.bpmll_models import ThresholdFunction
from mlclas.utils import check_feature_input, check_target_input
from mlclas.stats import Normalizer, RankResults

class RankingSVM:
    __doc__ = '\n    RankingSVM algorithm based on:\n    >   Elisseeff, André, and Jason Weston.\n        "Kernel methods for Multi-labelled classification and Categorical regression problems"\n        Advances in neural information processing systems. 2001.\n\n    Init Parameters\n    ----------\n    print_procedure:\n    decide whether print the middle status of the training process to the std output\n    '

    def __init__(self, normalize=False, axis=0, print_procedure=False):
        self.w = None
        self.threshold = None
        self.normalize = normalize
        self.axis = axis
        self.print_procedure = print_procedure
        self.trained = False

    def fit(self, x, y, c_factor):
        x = check_feature_input(x)
        y = check_target_input(y)
        self.features = x.shape[1]
        x = Normalizer.normalize(x, self.normalize, self.axis)
        sample_num, feature_num = x.shape
        class_num = y.shape[1]
        class_info = AllLabelInfo()
        for sample_index in range(sample_num):
            sample_y = y[sample_index]
            labels = []
            not_labels = []
            for label_index in range(class_num):
                if sample_y[label_index] == 1:
                    labels.append(label_index)
                else:
                    not_labels.append(label_index)

            class_info.append(labels, not_labels)

        alpha = np.zeros(class_info.totalProduct)
        alpha_var = cvx.Variable(class_info.totalProduct)
        c = [[0 for k in range(class_num)] for i in range(sample_num)]
        for i in range(sample_num):
            sample_shape, labels, not_labels = class_info.get_shape(i, True)
            for k in range(class_num):
                matrix = np.zeros(sample_shape)
                if k in labels:
                    index = labels.index(k)
                    matrix[index, :] = 1
                else:
                    index = not_labels.index(k)
                    matrix[:, index] = -1
                c[i][k] = matrix.flatten()

        c = np.array(c)
        beta = np.zeros((class_num, sample_num))
        beta_new = np.zeros((class_num, sample_num))
        wx_inner = np.zeros((class_num, sample_num))
        x_inner = np.array([[np.inner(x[i], x[j]) for j in range(sample_num)] for i in range(sample_num)])
        g_ikl = np.zeros(class_info.totalProduct)
        c_i = class_info.eachProduct
        bnds = []
        for i in range(sample_num):
            bnds += [c_factor / c_i[i] for j in range(c_i[i])]

        bnds = np.array(bnds)
        zeros = np.zeros(class_info.totalProduct)
        zeros.fill(1e-05)
        A_lp = []
        for k in range(1, class_num):
            A_lp.append(np.concatenate(c[:, k]).tolist())

        A_lp = np.array(A_lp)
        b_lp = np.zeros(class_num - 1)
        cons = [
         zeros <= alpha_var, alpha_var <= bnds, A_lp * alpha_var == b_lp]
        converge = False
        iteration_count = 0
        while not converge:
            iteration_count += 1
            for i in range(sample_num):
                alpha_range = class_info.get_range(i)
                alpha_piece = alpha[alpha_range[0]:alpha_range[1]]
                c_list = c[i]
                for k in range(class_num):
                    beta[k][i] = np.inner(c_list[k], alpha_piece)

            for k in range(class_num):
                beta_list = beta[k]
                for j in range(sample_num):
                    x_innerlist = x_inner[:, j]
                    wx_inner[k][j] = np.inner(beta_list, x_innerlist)

            for i in range(sample_num):
                g_range = class_info.get_range(i)
                shape, labels, not_labels = class_info.get_shape(i, True)
                wx_list = wx_inner[:, i]
                g_ikl[g_range[0]:g_range[1]] = np.repeat(wx_list[labels], shape[1]) - np.tile(wx_list[not_labels], shape[0]) - 1

            if self.print_procedure:
                print('iteration %d...' % iteration_count)
            obj = cvx.Minimize(cvx.sum_entries(g_ikl * alpha_var))
            prob = cvx.Problem(obj, cons)
            prob.solve()
            alpha_new = np.array(alpha_var.value).T[0]
            for i in range(sample_num):
                alpha_range = class_info.get_range(i)
                alpha_piece = alpha_new[alpha_range[0]:alpha_range[1]]
                c_list = c[i]
                for k in range(class_num):
                    beta_new[k][i] = np.inner(c_list[k], alpha_piece)

            lambda_11 = np.sum(beta_new.T.dot(beta) * x_inner)
            lambda_12 = np.sum(beta.T.dot(beta_new) * x_inner)
            lambda_13 = np.sum(alpha_new)
            lambda_1 = lambda_13 - lambda_11 / 2 - lambda_12 / 2
            lambda_2 = np.sum(beta_new.T.dot(beta_new) * x_inner) / -2
            left_vec = -alpha
            right_vec = bnds - alpha
            left = float('-inf')
            right = float('inf')
            for alpha_index in range(class_info.totalProduct):
                if not alpha_new[alpha_index] == 0:
                    left = max(left_vec[alpha_index] / alpha_new[alpha_index], left)
                    right = min(right_vec[alpha_index] / alpha_new[alpha_index], right)

            optifunc = lambda z: lambda_2 * z * z + lambda_1 * z
            if lambda_2 < 0:
                opti_lambda = -lambda_1 / (lambda_2 * 2)
                if opti_lambda < left:
                    final_lambda = left
                else:
                    if opti_lambda > right:
                        final_lambda = right
                    else:
                        final_lambda = opti_lambda
            else:
                if lambda_2 == 0:
                    if lambda_1 >= 0:
                        final_lambda = right
                    else:
                        final_lambda = left
                else:
                    worst_lambda = -lambda_1 / (lambda_2 * 2)
                    if worst_lambda < left:
                        final_lambda = right
                    else:
                        if worst_lambda > right:
                            final_lambda = left
                        else:
                            final_lambda = left if optifunc(left) >= optifunc(right) else right
                if self.print_procedure:
                    print('final lambda: ' + str(final_lambda))
                    print('optifunc: ' + str(optifunc(final_lambda)))
            if optifunc(final_lambda) <= 1 or final_lambda <= 0.001:
                converge = True
            else:
                alpha += final_lambda * alpha_new

        w = [0 for i in range(class_num)]
        for k in range(class_num):
            beta_vec = np.asarray([beta[k]])
            w[k] = beta_vec.dot(x)[0]

        w = np.array(w)
        b = np.zeros(class_num)
        x_list = x[0]
        shape, labels, not_labels = class_info.get_shape(0, True)
        for l in not_labels:
            b[l] = np.inner(w[labels[0]] - w[l], x_list) - 1

        falselabelb = b[not_labels[0]]
        falselabel_index = not_labels[0]
        for labelIndex in range(1, len(labels)):
            b[labels[labelIndex]] = 1 + falselabelb - np.inner(w[labels[labelIndex]] - w[falselabel_index], x_list)

        x_extend = np.concatenate((x, np.array([np.ones(sample_num)]).T), axis=1)
        w_extend = np.concatenate((w, np.array([b]).T), axis=1)
        model_outputs = np.dot(x_extend, w_extend.T)
        self.threshold = ThresholdFunction(model_outputs, y)
        self.w = w_extend
        self.trained = True
        return self

    def predict(self, x, rank_results=False):
        if self.trained is False:
            raise Exception('this classifier has not been trained')
        x = check_feature_input(x)
        x = Normalizer.normalize(x, self.normalize, self.axis)
        sample_num, feature_num = x.shape
        class_num = self.w.shape[0]
        if feature_num != self.w.shape[1] - 1:
            raise Exception('testing samples have inconsistent shape of training samples!')
        x_extend = np.concatenate((x, np.array([np.ones(sample_num)]).T), axis=1)
        threshold = self.threshold
        outputs = np.dot(x_extend, self.w.T)
        result = RankResults()
        for index in range(sample_num):
            sample_result = []
            op = outputs[index]
            th = threshold.compute_threshold(op)
            top_label = None
            max_value = float('-inf')
            count = 0
            for j in range(class_num):
                if op[j] >= th:
                    count += 1
                    sample_result.append(j)
                if op[j] > max_value:
                    top_label = j
                    max_value = op[j]

            if count == 0:
                sample_result.append(top_label)
            result.add(sample_result, top_label, op)

        if rank_results is False:
            result = result.predictedLabels
        return result