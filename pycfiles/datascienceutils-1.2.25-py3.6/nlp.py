# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/features/nlp.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 4480 bytes
import flashtext

def filter_letters_only(text):
    import re
    return re.sub('[^a-zA-Z]', ' ', text).lower()


def filter_stop_words(text, lang='english'):
    from nltk.corpus import stopwords
    stops = set(stopwords.words(lang))
    return set(text) - set(stops)


def bag_of_words(text):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(analyzer='word', tokenizer=None,
      preprocessor=None,
      stop_words=None,
      max_features=5000)
    vectorizer.fit_transform(text)
    return vectorizer


def word_match_share(row, lang='english'):
    from nltk.corpus import stopwords
    stops = set(stopwords.words(lang))
    q1words = {}
    q2words = {}
    for word in str(row['question1']).lower().split():
        if word not in stops:
            q1words[word] = 1

    for word in str(row['question2']).lower().split():
        if word not in stops:
            q2words[word] = 1

    if len(q1words) == 0 or len(q2words) == 0:
        return 0
    else:
        shared_words_in_q1 = [w for w in q1words.keys() if w in q2words]
        shared_words_in_q2 = [w for w in q2words.keys() if w in q1words]
        R = (len(shared_words_in_q1) + len(shared_words_in_q2)) / (len(q1words) + len(q2words))
        return R


def word_2_vector(sentences, size=200, **kwargs):
    num_features = 300
    min_word_count = 40
    num_workers = 4
    context = 10
    downsampling = 0.001
    from gensim.models import word2vec
    model = (word2vec.Word2Vec)(size=size, **kwargs)
    model.build_vocab(sentences)
    model.train(sentences)
    return model


def makeFeatureVec(words, model, num_features):
    featureVec = np.zeros((num_features,), dtype='float32')
    nwords = 0.0
    index2word_set = set(model.index2word)
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.0
            featureVec = np.add(featureVec, model[word])

    featureVec = np.divide(featureVec, nwords)
    return featureVec


def getAvgFeatureVecs(text, model, num_features):
    counter = 0.0
    reviewFeatureVecs = np.zeros((len(text), num_features), dtype='float32')
    for review in text:
        if counter % 1000.0 == 0.0:
            print('Review %d of %d' % (counter, len(text)))
        reviewFeatureVecs[counter] = makeFeatureVec(review, model, num_features)
        counter = counter + 1.0

    return reviewFeatureVecs


def word_cloud(train_qs):
    from wordcloud import WordCloud
    cloud = WordCloud(width=1440, height=1080).generate(' '.join(train_qs.astype(str)))
    plotter.show_image(cloud, figsize=(20, 15))


def word_similarity(word1, word2):
    from nltk.corpus import wordnet as wn
    return wn.synset(word1).path_similarity(wn.synset(word2))


def tfidf_model(corpus, gensim=False):
    if gensim:
        from gensim.models import tfidfmodel
        model = tfidfmodel.TfidfModel(corpus)
    else:
        from sklearn.feature_extraction.text import TfidfVectorizer
        model = TfidfVectorizer()
    return model