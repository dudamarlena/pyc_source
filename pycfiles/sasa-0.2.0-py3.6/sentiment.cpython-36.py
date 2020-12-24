# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sasa/sentiment.py
# Compiled at: 2019-04-09 16:59:41
# Size of source mod 2**32: 3702 bytes
from __future__ import division
from collections import defaultdict
import sys, re, json, os, errno, nltk, codecs, pickle, traceback
from htmlentitydefs import name2codepoint
__author__ = 'Abe Kazemzadeh, Dogan Can, Hao Wang'
__version__ = '$Revision: 1 $'
__date__ = '$Date: $'
__copyright__ = 'Copyright (c) University of Southern California'
__license__ = 'http://www.apache.org/licenses/LICENSE-2.0'
__maintainer__ = 'Last modified by Abe Kazemzadeh'
__email__ = "See the authors' website"
import gflags as flags
FLAGS = flags.FLAGS
name2codepoint['#39'] = 39
debug = False

def unescape(s):
    """unescape HTML code refs; c.f. http://wiki.python.org/moin/EscapingHtml"""
    return re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)


def features(tweet, n):
    feats = defaultdict(bool)
    words = ['<s>'] + tweet['tokens'] + ['</s>']
    for i in range(len(words)):
        for j in range(i + 1, i + n + 1):
            feat = ' '.join(words[i:j])
            feats[feat] = True

    return feats


def init(modelfile='model.naivebayes-bool-simple-1'):
    global classifier
    match = re.match('\\$Revision:\\s+(.*?)\\s+\\$', __version__)
    if match != None:
        ver = match.group(1)
    else:
        ver = __version__
    sys.stderr.write('init sentiment python script version ' + ver + '\n')
    if debug:
        return
    modelpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), modelfile)
    f = open(modelpath)
    classifier = pickle.load(f)
    f.close()


def getSentiment(tweet_json):
    try:
        tweet = codecs.decode(tweet_json, 'utf-8', 'replace')
        t = json.loads(tweet)
        if debug:
            t['valence'] = 0
            t['sentiment_classification'] = 'pos'
            return codecs.encode(json.dumps(t), 'utf-8')
    except Exception:
        traceback.print_exc()
        print('sentiment len =', (len(tweet_json)), ' text =', tweet_json, file=(sys.stderr))
        return
    else:
        text = t['text']
        text = unescape(text)
        labels = sorted(classifier.labels())
        feat = features(t, 1)
        hyp = classifier.classify(feat)
        classprobs = classifier.prob_classify(feat)
        if hyp == 'negative':
            valence = -classprobs.prob('negative')
        else:
            if hyp == 'positive':
                valence = classprobs.prob('positive')
            else:
                valence = 0
        t['valence'] = valence
        t['sentiment_classification'] = hyp
        return codecs.encode(json.dumps(t), 'utf-8')


if __name__ == '__main__':
    flags.DEFINE_string('model_path', 'model.naivebayes-bool-simple-1', 'pickled naive bayes model')
    argv = FLAGS(sys.argv)
    init(FLAGS.model_path)
    for t in sys.stdin:
        t = codecs.decode(t, 'utf-8')
        t = t.strip()
        if not t:
            pass
        else:
            t = getSentiment(t)
            if t != None:
                print(codecs.encode(t, 'utf-8'))