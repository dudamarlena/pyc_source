# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\文档\python\Geatpy_workplace\source\versions\2.5\geatpy\demo\soea_demo\soea_demo7\MyProblem.py
# Compiled at: 2020-02-08 05:16:53
# Size of source mod 2**32: 5359 bytes
import numpy as np, xlrd, geatpy as ea
from sklearn import svm
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from scoop import futures

class MyProblem(ea.Problem):

    def __init__(self):
        name = 'MyProblem'
        M = 1
        maxormins = [-1]
        Dim = 2
        varTypes = [0, 0]
        lb = [0.00390625, 0.00390625]
        ub = [256, 1]
        lbin = [1] * Dim
        ubin = [1] * Dim
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        workbook = xlrd.open_workbook('Data_User_Modeling_Dataset_Hamdi Tolga KAHRAMAN.xls')
        worksheet = workbook.sheet_by_name('Training_Data')
        self.data = np.vstack([worksheet.col_values(0)[1:],
         worksheet.col_values(1)[1:],
         worksheet.col_values(2)[1:],
         worksheet.col_values(3)[1:],
         worksheet.col_values(4)[1:]]).T
        self.data = preprocessing.scale(self.data)
        self.dataTarget = worksheet.col_values(5)[1:]

    def aimFunc(self, pop):
        Vars = pop.Phen
        args = list(zip(list(range(pop.sizes)), [Vars] * pop.sizes, [self.data] * pop.sizes, [self.dataTarget] * pop.sizes))
        pop.ObjV = np.array(list(futures.map(subAimFunc, args)))

    def test(self, C, G):
        workbook = xlrd.open_workbook('Data_User_Modeling_Dataset_Hamdi Tolga KAHRAMAN.xls')
        worksheet = workbook.sheet_by_name('Test_Data')
        data_test = np.vstack([worksheet.col_values(0)[1:],
         worksheet.col_values(1)[1:],
         worksheet.col_values(2)[1:],
         worksheet.col_values(3)[1:],
         worksheet.col_values(4)[1:]]).T
        data_test = preprocessing.scale(data_test)
        dataTarget_test = worksheet.col_values(5)[1:]
        svc = svm.SVC(C=C, kernel='rbf', gamma=G).fit(self.data, self.dataTarget)
        dataTarget_predict = svc.predict(data_test)
        print('测试集数据分类正确率 = %s%%' % (len(np.where(dataTarget_predict == dataTarget_test)[0]) / len(dataTarget_test) * 100))


def subAimFunc(args):
    i = args[0]
    Vars = args[1]
    data = args[2]
    dataTarget = args[3]
    C = Vars[(i, 0)]
    G = Vars[(i, 1)]
    svc = svm.SVC(C=C, kernel='rbf', gamma=G).fit(data, dataTarget)
    scores = cross_val_score(svc, data, dataTarget, cv=20)
    ObjV_i = [scores.mean()]
    return ObjV_i