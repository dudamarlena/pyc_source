# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ZOZO_intern/main.py
# Compiled at: 2018-05-21 09:46:27
# Size of source mod 2**32: 7246 bytes
import numpy as np, pandas as pd, datetime as dt, os, sys, pkgutil
from setuptools import setup, find_packages
rating_error = lambda r, p, q: r - np.dot(p, q)

class MatrixFactorization:

    def __init__(self):
        self.df = pd.read_csv('u.data', sep='\t', names=['user id', 'item id', 'rating', 'timestamp'])
        self.df.timestamp = [dt.datetime.fromtimestamp(time) for time in self.df.timestamp]
        self.df = self.df.set_index('user id')
        label_cols = [
         'movie id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        itemlist = pd.read_csv('u.item', sep='|', names=label_cols, encoding='latin-1')
        self.itemlist = itemlist.set_index('movie id')
        self.mat = self._user_item_mat()

    def _user_item_mat(self):
        """
        ここで、d.dataからuser idとitem id、ratingをまとめた行列を作成する。
        縦にuser id、横にitem idをとり、ratingが存在しない要素はすべて0.0とした。
        """
        self.df.index = self.df.index.astype('int')
        mat = []
        for user_id in range(self.df.index.max()):
            dfc = self.df[(self.df.index == user_id + 1)]
            ulist = np.zeros(self.df['item id'].max().astype('int'))
            for idx, con in enumerate(dfc['item id']):
                ulist[int(con) - 1] = dfc['rating'].tolist()[idx]

            mat.append(ulist)

        return np.array(mat)

    def _get_error(self, R, P, Q, beta):
        """
        Matrix Factorizationを行うため、元の行列(R)と、user成分(P)とitem成分(Q)に分解する行列の誤差を計算する。
        計算結果をすべて合計するため、リスト内包表記にして、計算速度を向上させた。
        Rの中にある0.0の要素以外のすべての要素から、PとQの行列を作成する。
        ちなみに、最後の +beta/2.0....は正則化の計算である。

        また、リスト内包表記をforループに変換すると、

        user,item = R.shape
        error = 0.0
        for i in range(user):
            for j in range(item):
                if R[i][j] == 0:
                    continue
                error += pow(get_rating_error(R[i][j], P.T[i], Q.T[j]), 2)
        error += beta/2.0 * (numpy.linalg.norm(P) + numpy.linalg.norm(Q))

        となる。
        """
        return sum([sum([pow(rating_error(rate, P.T[i], Q.T[j]), 2) for j, rate in enumerate(each) if rate != 0.0]) for i, each in enumerate(R)]) + beta / 2.0 * (pow(np.linalg.norm(P), 2) + pow(np.linalg.norm(Q), 2))

    def matrix_factorization(self, K=2, steps=500, alpha=0.0002, beta=0.02, threshold=0.001):
        """
        Matrix Factorizationの計算を行う関数。
        user成分(P)とitem成分(Q)の初期状態は乱数を用いて定義した。
        PとQの積とRの誤差を最小化させるように計算させる。
        """
        user, item = self.mat.shape
        P = np.random.rand(K, user)
        Q = np.random.rand(K, item)
        print('computing Time', steps)
        for step in range(steps):
            if divmod(step, 10)[1] == 0:
                print('Time remaining...', steps - step)
            else:
                for i, each in enumerate(self.mat):
                    for j, rate in enumerate(each):
                        if rate == 0:
                            pass
                        else:
                            err = rating_error(rate, P.T[i], Q.T[j])
                            for k in range(K):
                                P[k][i] += alpha * (2 * err * Q[k][j])
                                Q[k][j] += alpha * (2 * err * P[k][i])

                error = self._get_error(self.mat, P, Q, beta)
                if error < threshold:
                    break

        print('------------------------------------------------------------------------------')
        return (P, Q)

    def recommend(self, user_ids, rank=10):
        """
        指定された各userに対するitemのrecommendを行う関数。
        ratingの情報が事前になかったitemに対して、Matrix Factorizationから予測した上位10位のものを表示する。

        """
        print('Start recommendation by MF method!!!')
        nP, nQ = self.matrix_factorization()
        nR = np.dot(nP.T, nQ)
        user, item = nR.shape
        user_train_idx, item_train_idx = np.where(self.mat != 0.0)
        for i, j in zip(user_train_idx, item_train_idx):
            nR[i][j] = 0.0

        recommend_list = pd.DataFrame(nR).T
        recommend_list.index.name = 'item id'
        recommend_list.index = np.array(recommend_list.index) + 1
        for user_id in user_ids:
            print('User ID:', user_id)
            slist = recommend_list.iloc[:, [user_id - 1]]
            slist.columns = [
             'rating(Estimate)']
            slist = slist.sort_values(by=['rating(Estimate)'], ascending=False)
            re = np.array(slist.index) - 1
            item = self.itemlist.iloc[(re, [0])]
            item = pd.concat([item[0:rank], slist[0:rank]], axis=1)
            print(item)
            print('------------------------------------------------------------------------------')


if __name__ == '__main__':
    user_ids = [
     1, 20]
    MF = MatrixFactorization()
    MF.recommend(user_ids)