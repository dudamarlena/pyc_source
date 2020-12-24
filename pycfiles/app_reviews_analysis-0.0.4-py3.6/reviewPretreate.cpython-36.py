# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\app_reviews_analysis\reviewPretreate.py
# Compiled at: 2019-07-12 08:24:24
# Size of source mod 2**32: 22995 bytes
import pandas as pd
from dateutil.parser import parse
from datetime import timedelta
import langid, nltk, nltk.corpus, subprocess, shlex, re, emoji
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.collocations import *
from nltk.corpus import wordnet as wn
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class reviewPretreate:

    def __init__(self):
        self.sentimentPath = BASE_DIR + '/app_reviews_analysis/static/sentiment'
        self.SentiStrengthLocation = BASE_DIR + '/app_reviews_analysis/static/SentiStrength.jar'
        self.SentiStrengthLanguageFolder = BASE_DIR + '/app_reviews_analysis/static/SentStrength_Data/'

    def dataimport(self, path, encoding='utf-8'):
        df3 = pd.read_csv(path, encoding=encoding)
        ix = []
        for i in range(len(df3['review_text'])):
            if langid.classify(df3['review_text'][i])[0] == 'en':
                ix.append(i)

        df3 = df3.iloc[ix, :]
        df3['review_date'] = [parse(d) for d in df3['review_date']]
        path = self.sentimentPath
        sentimentword = []
        for filename in os.listdir(path):
            fo = open(os.path.join(path, filename), 'r')
            for line in fo.readlines():
                sentimentword.append(line.replace(' \n', '').replace('\n', ''))

        return (
         df3, sentimentword)

    def issynonyms(self, word1, word2):
        synonyms = []
        for word in word1:
            for syn in wn.synsets(word):
                for l in syn.lemmas():
                    synonyms.append(l.name())

        if set(word2).issubset(set(synonyms)):
            return 1
        else:
            return 0

    def pretreat(self, reviewslist, sentimentword):
        text1 = []
        lemmatizer = WordNetLemmatizer()
        sr = stopwords.words('english')
        sr.extend([
         'app', 'please', 'fix', 'android', 'google', 'youtube', 'as', 'uber', 'dont', 'cousin', 'pp', 'facebook',
         'fitbit'])
        english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '{',
         '}', '`', '<', '>', '/', '^', '-', '_', '``', "''", '...', '......']
        for text in reviewslist:
            try:
                text = text.lower()
                text = emoji.get_emoji_regexp().sub('', text)
                texts_filtered = [word for word in word_tokenize(text) if word not in english_punctuations]
                texts_filtered2 = [word for word in texts_filtered if word not in sr]
                texts_filtered3 = [word for word in texts_filtered2 if word not in sentimentword]
                texts_filtered4 = [lemmatizer.lemmatize(word) for word in texts_filtered3]
                texts_filtered5 = [word for word in texts_filtered4 if len(word) > 1]
                refiltered = nltk.pos_tag(texts_filtered5)
                filtered = [w for w, pos in refiltered if pos in ('NN', 'VB', 'VBG',
                                                                  'VBD', 'VBN', 'JJ',
                                                                  'NNS')]
                if len(filtered) >= 1:
                    text1.append(filtered)
            except:
                print('评论预处理失败：', text)

        return text1

    def flatten(self, a):
        for each in a:
            if not isinstance(each, list):
                yield each
            else:
                yield from self.flatten(each)

    def Cole(self, featurelist):
        featurecol1 = []
        featurecol2 = []
        featurecol3 = []
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(list(self.flatten(featurelist)))
        finder.apply_freq_filter(3)
        featurecol = finder.score_ngrams(bigram_measures.likelihood_ratio)
        for word, freq in featurecol:
            t = False
            for text in featurelist:
                if (word[0] in text) & (word[1] in text) and (abs(text.index(word[0]) - text.index(word[1])) <= 3) & (word[0] != word[1]):
                    t = True

            if t & (set(word) not in featurecol1):
                l = list(word)
                l.append(freq)
                featurecol3.append(l)
                featurecol1.append(set(word))
                featurecol2.append(word)

        for i in range(len(featurecol3)):
            for j in range(i + 1, len(featurecol3)):
                try:
                    if self.issynonyms(featurecol3[i][0:2], featurecol3[j][0:2]):
                        print('%s和%s是同义词' % (
                         featurecol3[i][0] + ' ' + featurecol3[i][1], featurecol3[j][0] + ' ' + featurecol3[j][1]))
                        featurecol3.pop(j)
                except:
                    continue

        print(featurecol2)
        return featurecol3

    def RateSentiment(self, reviewslist):
        sentiment = []
        reviewslist1 = []
        for text in reviewslist:
            try:
                text = text.lower()
                text = emoji.get_emoji_regexp().sub('', text)
                reviewslist1.append(text)
            except:
                print('无法处理该评论：', text)

        SentiStrengthLocation = self.SentiStrengthLocation
        SentiStrengthLanguageFolder = self.SentiStrengthLanguageFolder
        if not os.path.isfile(SentiStrengthLocation):
            print('SentiStrength not found at: ', SentiStrengthLocation)
        if not os.path.isdir(SentiStrengthLanguageFolder):
            print('SentiStrength data folder not found at: ', SentiStrengthLanguageFolder)
        for review in reviewslist1:
            p = subprocess.Popen((shlex.split("java -jar '" + SentiStrengthLocation + "' stdin sentidata '" + SentiStrengthLanguageFolder + "'")),
              stdin=(subprocess.PIPE),
              stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE))
            b = bytes(review.replace(' ', '+'), 'utf-8')
            stdout_byte, stderr_text = p.communicate(b)
            stdout_text = stdout_byte.decode('utf-8')
            stdout_text = stdout_text.rstrip().replace('\t', ' ')
            if stdout_text != '':
                sentiment.append('{' + stdout_text.replace('+', '') + '}' + review)

        return sentiment

    def RateSentimentWord(self, df3):
        df3 = df3.dropna()
        df3.index = range(len(df3))
        sentiment = []
        reviewwordscore = []
        reviewslist2 = []
        reviewslist = list(df3['review_text'])
        for i in range(len(reviewslist)):
            text = reviewslist[i]
            try:
                text = text.lower()
                text = emoji.get_emoji_regexp().sub('', text)
            except:
                df3 = df3.drop(i, axis=0)
                print('无法处理该评论：', text)

        reviewslist1 = list(df3['review_text'])
        df3.index = range(len(df3))
        SentiStrengthLocation = self.SentiStrengthLocation
        SentiStrengthLanguageFolder = self.SentiStrengthLanguageFolder
        if not os.path.isfile(SentiStrengthLocation):
            print('SentiStrength not found at: ', SentiStrengthLocation)
        if not os.path.isdir(SentiStrengthLanguageFolder):
            print('SentiStrength data folder not found at: ', SentiStrengthLanguageFolder)
        for r in range(len(reviewslist1)):
            review = reviewslist1[r]
            try:
                p = subprocess.Popen((shlex.split("java -jar '" + SentiStrengthLocation + "' stdin sentidata '" + SentiStrengthLanguageFolder + "' explain'" + "'")),
                  stdin=(subprocess.PIPE),
                  stdout=(subprocess.PIPE),
                  stderr=(subprocess.PIPE))
                b = bytes(review.replace(' ', '+'), 'utf-8')
                stdout_byte, stderr_text = p.communicate(b)
                stdout_text = stdout_byte.decode('utf-8')
                stdout_text = stdout_text.rstrip().replace('\t', ' ')
                if stdout_text != '':
                    sentiment.append('{' + stdout_text.replace('+', '')[0:4] + '}')
                    reviewwordscore.append(stdout_text.replace('+', '')[4:])
            except:
                df3 = df3.drop(r, axis=0)
                continue

        return (
         sentiment, reviewwordscore)

    def scoredfeature(self, sentiment, sentimentword):
        scorefeature = []
        lemmatizer = WordNetLemmatizer()
        sr = stopwords.words('english')
        sr.extend(['app', 'please', 'fix', 'android', 'google', 'youtube', 'uber', 'facebook'])
        english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '{',
         '}', '`', '<', '>', '/', '^', '-', '_', '``', "''"]
        for i in sentiment:
            text = emoji.get_emoji_regexp().sub('', i[7:])
            texts_filtered = [word for word in word_tokenize(text) if word not in english_punctuations]
            texts_filtered2 = [word for word in texts_filtered if word not in sr]
            texts_filtered3 = [word for word in texts_filtered2 if word not in sentimentword]
            texts_filtered4 = [lemmatizer.lemmatize(word) for word in texts_filtered3]
            texts_filtered5 = [word for word in texts_filtered4 if len(word) > 1]
            refiltered = nltk.pos_tag(texts_filtered5)
            filtered = [w for w, pos in refiltered if pos in ('NN', 'VB', 'VBG', 'VBD',
                                                              'VBN', 'JJ', 'NNS')]
            if len(filtered) >= 1:
                filtered.insert(0, i[0:6])
                scorefeature.append(filtered)

        return scorefeature

    def max_value(self, valuelist):
        maxValue = {}
        result = []
        for i in valuelist:
            maxValue[' '.join(i)] = valuelist.count(i)

        for key, val in maxValue.items():
            if val == max(maxValue.values()):
                result.append(key.split(' '))

        return result

    def featurescored(self, featurecol, scorefeature):
        feature_score = []
        for word in featurecol:
            scoretotal = 0
            feature = word[0] + '|' + word[1]
            for text in scorefeature:
                if (word[0] in text) & (word[1] in text):
                    scorenum = re.findall('[-]?\\d', text[0])
                    abs_score = [abs(int(num)) for num in scorenum]
                    if abs_score[0] == abs_score[1]:
                        scoretotal = scoretotal + int(min(scorenum))
                    else:
                        scoretotal = scoretotal + int(scorenum[abs_score.index(max(abs_score))])

            feature_score.append(word[0] + ' ' + word[1] + ', ' + str(round(word[2], 2)) + ', ' + str(scoretotal))

        return feature_score

    def featurescored1(self, featurecol, scorefeature):
        feature_score = []
        for word in featurecol:
            scoretotal = 0
            feature = word[0] + '|' + word[1]
            for text in scorefeature:
                if (word[0] in text) & (word[1] in text):
                    scorenum = re.findall('[-]?\\d', text[0])
                    abs_score = [abs(int(num)) for num in scorenum]
                    if abs_score[0] == abs_score[1]:
                        scoretotal = scoretotal + int(min(scorenum))
                    else:
                        scoretotal = scoretotal + int(scorenum[abs_score.index(max(abs_score))])

            feature_score.append(word[0] + ' ' + word[1])

        return feature_score

    def timeColname(self, df3, appname, time):
        colname = []
        app = df3[(df3['product_name'] == appname)]
        enddate = max(app['review_date'])
        startdate = min(app['review_date'])
        datecut = []
        date = startdate
        if time <= 0:
            print('时间段太短')
            print(app['review_date'])
            return
        else:
            while date <= enddate:
                datecut.append(date)
                date = date + timedelta(time)

            for i in range(len(datecut) - 1):
                colname.append(str(datecut[i]).split(' ')[0])

            return colname

    def outputdata(self, df3, reviewword, appname, reviewsRating):
        colname = []
        app = df3[(df3['product_name'] == appname)]
        enddate = max(app['review_date'])
        startdate = min(app['review_date'])
        datecut = []
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

            feature_scorelist = []
            for reviewlist in reviewsweek:
                featurecol = self.Cole(self.pretreat(reviewlist, reviewword))
                sentiment = self.RateSentiment(reviewlist)
                scorefeature = self.scoredfeature(sentiment, reviewword)
                print(scorefeature)
                feature_score = self.featurescored(featurecol, scorefeature)
                feature_scorelist.append(feature_score)

            print(feature_scorelist)
            Originreviewweeks = []
            for feature_score in feature_scorelist:
                Originreview = []
                if len(feature_score) > 3:
                    index = 3
                else:
                    index = len(feature_score)
                for i in feature_score[0:index]:
                    originreview = []
                    featureword = []
                    print(i.split(',')[0].split(' '))
                    for t in list(set(reviewlist)):
                        try:
                            if (i.split(',')[0].split(' ')[0] in list(self.flatten(self.pretreat([t])))) & (i.split(',')[0].split(' ')[1] in list(self.flatten(self.pretreat([t])))) & (list(self.flatten(self.pretreat([t]))) not in featureword):
                                print(t)
                                featureword.append(list(self.flatten(self.pretreat([t]))))
                                originreview.append(t)
                            else:
                                continue
                        except:
                            print('error')

                    try:
                        if originreview != []:
                            Originreview.append(min(originreview, key=len))
                    except:
                        continue

                Originreviewweeks.append(Originreview)

            time_feature = {}
            for t in range(len(colname)):
                time_feature[colname[t]] = feature_scorelist[t][0:5]

            reviewsweek_feature = []
            colname1 = []
            time = 7
            datecut_feature = []
            date = startdate
            while date <= enddate:
                datecut_feature.append(date)
                date = date + timedelta(time)

            for i in range(len(datecut_feature) - 1):
                print(i)
                colname1.append(str(datecut_feature[i]).split(' ')[0])
                reviewsweek_feature.append(app[((app['review_date'] >= datecut_feature[i]) & (app['review_date'] < datecut_feature[(i + 1)]))]['review_text'].values)

            print(reviewsweek_feature)
            feature_dist_lists = {}
            for i in range(len(colname1) - 1):
                featurecol = self.Cole(self.pretreat(list(set(reviewsweek_feature[i])), reviewword))
                sentiment = self.RateSentiment(reviewsweek_feature[i])
                scorefeature = self.scoredfeature(sentiment, reviewword)
                feature_score = self.featurescored(featurecol, scorefeature)
                feature_dist_list = []
                if len(feature_score) > 5:
                    l = 5
                else:
                    l = len(feature_score)
                for j in range(l):
                    feature_dist = {}
                    feature_dist['value'] = float(feature_score[j].split(',')[1])
                    feature_dist['name'] = feature_score[j].split(',')[0] + '(' + feature_score[j].split(',')[2].replace(' ', '') + ')'
                    feature_dist_list.append(feature_dist)

                feature_dist_lists[colname1[i]] = feature_dist_list

            print(feature_dist_lists)
            return (time_feature, feature_dist_lists, Originreviewweeks)