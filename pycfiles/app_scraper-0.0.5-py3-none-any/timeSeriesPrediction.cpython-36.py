# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\app_reviews_analysis\timeSeriesPrediction.py
# Compiled at: 2019-07-12 02:50:07
# Size of source mod 2**32: 6249 bytes
from datetime import timedelta
from app_reviews_analysis.reviewPretreate import reviewPretreate
import pandas as pd
from numpy import *
from dateutil.parser import parse

class timeSeriesPrediction:

    def __init__(self, appid, df):
        self.appname = appid
        self.df3 = df

    def computes(self):
        app = self.df3[(self.df3['product_name'] == self.appname)]
        enddate = max(app['review_date'])
        startdate = min(app['review_date'])
        datecut = []
        colname = []
        date = startdate
        reviewsweek = []
        if (enddate - startdate) / timedelta(7) < 20:
            time = int((enddate - startdate) / timedelta(20))
        else:
            time = 7
        print('time', time)
        if time <= 0:
            print('时间段太短')
            print(app['review_date'])
            return
        else:
            while date <= enddate:
                datecut.append(date)
                date = date + timedelta(time)

            for i in range(len(datecut) - 1):
                print(i)
                colname.append(str(datecut[i]).split(' ')[0])
                reviewsweek.append([text for text in app[((app['review_date'] >= datecut[i]) & (app['review_date'] < datecut[(i + 1)]))]['review_text']])

            revirescoreweek = []
            for reviewlist in reviewsweek:
                revirescoreweek.append(reviewPretreate().RateSentiment(reviewlist))

            print('评论分', revirescoreweek)
            reviewsRating = []
            for reviewlist in revirescoreweek:
                reviewsmean = []
                for rscore in reviewlist:
                    try:
                        scorenum = [int(i) for i in rscore[1:5].split(' ')]
                    except:
                        print('情感分格式不符合')

                    if abs(scorenum[0]) == abs(scorenum[1]):
                        reviewsmean.append(scorenum[1])
                    else:
                        if abs(scorenum[0]) > abs(scorenum[1]):
                            reviewsmean.append(scorenum[0])
                        else:
                            reviewsmean.append(scorenum[1])

                reviewsRating.append(np.mean(reviewsmean))

            print(reviewsRating)
            reviewsRating1 = pd.DataFrame(reviewsRating)
            return (
             reviewsRating1, colname, self.appname, time)

    def sk(self, Rt, k, p):
        bias = abs(Rt - Rt.mean(axis=1).reshape(Rt.shape[0], 1))
        s = 1 - (bias.min(axis=1) + p * bias.max(axis=1)) / (bias[:, Rt.shape[1] - k] + p * bias.max(axis=1))
        s[nonzero(isnan(s))] = 0
        return s

    def predictScored(self, Rt, p, L):
        Rt = Rt[:, -L:]
        fk = [np.exp(-self.sk(Rt, k, p) * k) for k in range(1, Rt.shape[1] + 1)]
        fk = np.array(fk)
        Rt1 = np.dot(Rt, fk) / fk.sum()
        return Rt1

    def MAE(self, y, yp):
        N = len(yp)
        return abs(y - yp).sum() / N

    def NMAE(self, y, yp):
        N = len(yp)
        return self.MAE(y, yp) / (y.sum() / N)

    def modelEvaluation(self, pstart=1, pend=9, pinterval=2, tsplit=0.8):
        reviewsRating1, colname, appname, time = self.computes(tsplit)
        print(colname)
        reviewsRating1.index = colname
        reviewsRating1 = reviewsRating1.dropna()
        colname = reviewsRating1.index
        reviewsRatingTrue = reviewsRating1
        minnmae = inf
        minmae = inf
        minp = inf
        minL = inf
        for p in np.arange(pstart, pend, pinterval):
            for L in range(len(reviewsRating1) - int(len(reviewsRating1) * tsplit), int(len(reviewsRating1) * tsplit)):
                print('p=%d,L=%d' % (p, L))
                preds = []
                for i in range(int(len(reviewsRating1) * tsplit - 1), len(reviewsRating1) - 1):
                    pred = self.predictScored(reviewsRating1.values[:i].T, p, L).diagonal()
                    preds.append(pred)

                print(preds)
                nmae = self.NMAE(reviewsRating1.values[int(len(reviewsRating1) * tsplit):len(reviewsRating1)], preds)
                mae = self.MAE(reviewsRating1.values[int(len(reviewsRating1) * tsplit):len(reviewsRating1)], preds)
                if minnmae > nmae:
                    minnmae = nmae
                    minmae = minmae
                    minp = p
                    minL = L

        print(minL, minp)
        print(colname)
        colname = list(colname)
        for i in range(len(reviewsRating1) - 1, len(reviewsRating1) + int(len(reviewsRating1) * (1 - tsplit)) - 1):
            print(i)
            print(str(parse(colname[i]) + timedelta(7)))
            pred = self.predictScored(reviewsRating1.values[:i].T, minp, minL).diagonal()
            colname.append(str(parse(colname[i]) + timedelta(time))[0:10])
            print(colname)
            print(list(pred))
            print(shape(reviewsRating1.values))
            print(reviewsRating1.values)
            print(np.insert((reviewsRating1.values), (i + 1), values=pred, axis=0))
            reviewsRating1 = pd.DataFrame(np.insert((reviewsRating1.values), (i + 1), values=pred, axis=0))
            print(reviewsRating1)
            preds.append(pred)

        print('preds', preds)
        print(reviewsRating1)
        reviewsRating1.index = colname
        return (
         reviewsRatingTrue, reviewsRating1, preds)