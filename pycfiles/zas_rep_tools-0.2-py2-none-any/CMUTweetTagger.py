# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/extensions/tweet_nlp/ark_tweet_nlp_python/CMUTweetTagger.py
# Compiled at: 2018-07-06 21:45:41
"""Simple Python wrapper for runTagger.sh script for CMU's Tweet Tokeniser and Part of Speech tagger: http://www.ark.cs.cmu.edu/TweetNLP/

Usage:
results=runtagger_parse(['example tweet 1', 'example tweet 2'])
results will contain a list of lists (one per tweet) of triples, each triple represents (term, type, confidence)
"""
import subprocess, shlex
RUN_TAGGER_CMD = 'java -XX:ParallelGCThreads=2 -Xmx500m -jar ../ark_tweet_nlp/ark-tweet-nlp-0.3.2.jar'

def _split_results(rows):
    """Parse the tab-delimited returned lines, modified from: https://github.com/brendano/ark-tweet-nlp/blob/master/scripts/show.py"""
    for line in rows:
        line = line.strip()
        if len(line) > 0:
            if line.count('\t') == 2:
                parts = line.split('\t')
                tokens = parts[0]
                tags = parts[1]
                confidence = float(parts[2])
                yield (tokens, tags, confidence)


def _call_runtagger(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    """Call runTagger.sh using a named input file"""
    tweets_cleaned = [ tw.replace('\n', ' ') for tw in tweets ]
    message = ('\n').join(tweets_cleaned)
    message = message.encode('utf-8')
    args = shlex.split(run_tagger_cmd)
    args.append('--output-format')
    args.append('conll')
    po = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = po.communicate(message)
    pos_result = result[0].strip('\n\n')
    pos_result = pos_result.split('\n\n')
    pos_results = [ pr.split('\n') for pr in pos_result ]
    return pos_results


def runtagger_parse(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    """Call runTagger.sh on a list of tweets, parse the result, return lists of tuples of (term, type, confidence)"""
    pos_raw_results = _call_runtagger(tweets, run_tagger_cmd)
    pos_result = []
    for pos_raw_result in pos_raw_results:
        pos_result.append([ x for x in _split_results(pos_raw_result) ])

    return pos_result


def check_script_is_present(run_tagger_cmd=RUN_TAGGER_CMD):
    """Simple test to make sure we can see the script"""
    success = False
    try:
        args = shlex.split(run_tagger_cmd)
        print args
        args.append('--help')
        po = subprocess.Popen(args, stdout=subprocess.PIPE)
        while not po.poll():
            lines = [ l for l in po.stdout ]

        assert 'RunTagger [options]' in lines[0]
        success = True
    except OSError as err:
        print 'Caught an OSError, have you specified the correct path to runTagger.sh? We are using "%s". Exception: %r' % (run_tagger_cmd, repr(err))

    return success


if __name__ == '__main__':
    print 'Checking that we can see "%s", this will crash if we can\'t' % RUN_TAGGER_CMD
    success = check_script_is_present()
    if success:
        print 'Success.'
        print 'Now pass in two messages, get a list of tuples back:'
        tweets = ['this is a message', 'and a second message']
        print runtagger_parse(tweets)