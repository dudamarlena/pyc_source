# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\app_reviews_analysis\relation.py
# Compiled at: 2019-07-12 02:36:04
# Size of source mod 2**32: 4273 bytes
import matplotlib.pyplot as plt, seaborn as sns, numpy as np
from datetime import timedelta
import app_reviews_analysis.reviewPretreate as rP, pandas as pd, re
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Relation:

    def __init__(self, appname):
        self.appname = appname

    def WA(self, starlist):
        if len(starlist) != 0:
            return (starlist.count(5) * 5 + starlist.count(4) * 4 + starlist.count(3) * 3 + starlist.count(2) * 2 + starlist.count(1)) / len(starlist)
        else:
            return 0

    def relation(self, df3):
        app = df3[(df3['product_name'] == self.appname)]
        enddate = max(app['review_date'])
        startdate = min(app['review_date'])
        datecut = []
        date = startdate
        reviewsweek = []
        starweek = []
        if (enddate - startdate) / timedelta(7) < 20:
            time = int((enddate - startdate) / timedelta(20))
        else:
            time = 7
        print('time', time)
        if time <= 0:
            print('时间段太短')
            return
        else:
            while date <= enddate:
                datecut.append(date)
                date = date + timedelta(time)

            for i in range(len(datecut) - 1):
                print(i)
                reviewsweek.append([text for text in app[((app['review_date'] >= datecut[i]) & (app['review_date'] < datecut[(i + 1)]))]['review_text']])
                starweek.append([text for text in app[((app['review_date'] >= datecut[i]) & (app['review_date'] < datecut[(i + 1)]))]['rating_star']])

            revirescoreweek = []
            for reviewlist in reviewsweek:
                revirescoreweek.append(rP.reviewPretreate().RateSentiment(reviewlist))

            print('评论分', revirescoreweek)
            starsRating = []
            reviewsRating = []
            reviewsRatingLable = []
            for starlist in starweek:
                starmean = []
                for star in starlist:
                    starmean.append(int(re.findall('\\d', star)[0]))

                starsRating.append(self.WA(starmean))

            for reviewlist in revirescoreweek:
                reviewsmean = []
                posmean = []
                negmean = []
                for rscore in reviewlist:
                    try:
                        scorenum = [int(i) for i in rscore[1:5].split(' ')]
                    except:
                        print('情感分格式不符合')

                    posmean.append(scorenum[0])
                    negmean.append(scorenum[1])
                    if abs(scorenum[0]) == abs(scorenum[1]):
                        reviewsmean.append(scorenum[1])
                    else:
                        if abs(scorenum[0]) > abs(scorenum[1]):
                            reviewsmean.append(scorenum[0])
                        else:
                            reviewsmean.append(scorenum[1])

                reviewsRating.append(np.mean(reviewsmean))

            personcoef = pd.Series(starsRating).corr(pd.Series(reviewsRating))
            spearmancoef = pd.Series(starsRating).corr((pd.Series(reviewsRating)), method='spearman')
            print('皮尔逊线性相关系数为：', pd.Series(starsRating).corr(pd.Series(reviewsRating)))
            print('斯皮尔曼相关系数为：', pd.Series(starsRating).corr((pd.Series(reviewsRating)), method='spearman'))
            fig = plt.figure()
            ax = fig.add_subplot(111)
            x, y = pd.Series(starsRating, name='x_var'), pd.Series(reviewsRating, name='y_var')
            sns.regplot(x, y)
            plt.xlabel('SST(star_score)')
            plt.ylabel('average sentiment score')
            plt.title(self.appname)
            plt.show()
            return (
             personcoef, spearmancoef, starsRating, reviewsRating)