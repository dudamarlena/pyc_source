# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cblog/widgets/validators.py
# Compiled at: 2006-12-06 04:38:10
from turbogears import config, validators
from cblog import spamfilters
import logging
log = logging.getLogger('turbogears.controllers')

class SpamFilter(validators.FancyValidator):
    """A spam filter for comments.
    
    Comment submissions are sent through a series of filters that
    give a score to the comment, signifying the likelihood that it is spam.
    A higher score means a higher spam probability.
    
    The score from each filter can be weighted by setting a weighting in 
    the config file with 'spam_filter.filters.<filter>.weight'. A value of 1
    means that the score from the filter contributes to the overall score in
    an equal share as all other filters. A value of 2 means its score 
    contributes twice as much to the overall score, and so on
    
    The list of filter to use, can be set with the config setting
    'spam_filter.filterlist'. This should be a list of filter names.
    Filters are modules in the 'spamfilters' package. Each of this modules
    contains a function named 'filter' that receives the comment as a 
    dictionary and a state object and must return an integer score. 
    The state object defaults to None but can be an arbitrary object providing
    state information, e.g. the current web request, a user object or similar.
    The score can be positive or negative. Sugested values are:
    
        10 = High spam probability
         5 = Medium spam probability
         0 = Neutral / indecisive
        -5 = Probably not spam
       -10 = Very probably not spam
    
    See the source of the provided filter modules in the spamfilter package
    as an example.
    """
    __module__ = __name__
    messages = {'default': 'Your submission was rejected as spam.'}

    def validate_python(self, value, state):
        filterlist = config.get('spam_filter.filterlist', [])
        filtercount = len(filterlist)
        scores = []
        for filter in filterlist:
            weight = config.get('spam_filter.filters.' + filter + '.weight', 1)
            try:
                filter_module = getattr(spamfilters, filter)
                scores.append((filter_module.filter(value, state), weight))
            except AttributeError:
                scores.append((0, 1))

        log.info('Scores: %r' % scores)
        norm_factor = sum([ x[1] for x in scores ]) / float(filtercount)
        log.info('Normalization factor: %f' % norm_factor)
        score = sum([ x[1] * norm_factor * x[0] for x in scores ])
        treshold = config.get('spam_filter.reject.treshold', 100)
        if score > treshold:
            log.info('Comment rejected. Score: %i, treshold: %i' % (score, treshold))
            raise validators.Invalid(self.message('default', None), value, state)
        log.info('Comment accepted. Score: %i, treshold: %i' % (score, treshold))
        return value