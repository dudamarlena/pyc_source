# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sasa/happyfuntokenizing.py
# Compiled at: 2019-04-09 16:18:21
# Size of source mod 2**32: 7736 bytes
"""
This code implements a basic, Twitter-aware tokenizer.

A tokenizer is a function that splits a string of text into words. In
Python terms, we map string and unicode objects into lists of unicode
objects.

There is not a single right way to do tokenizing. The best method
depends on the application.  This tokenizer is designed to be flexible
and this easy to adapt to new domains and tasks.  The basic logic is
this:

1. The tuple regex_strings defines a list of regular expression
   strings.

2. The regex_strings strings are put, in order, into a compiled
   regular expression object called word_re.

3. The tokenization is done by word_re.findall(s), where s is the
   user-supplied string, inside the tokenize() method of the class
   Tokenizer.

4. When instantiating Tokenizer objects, there is a single option:
   preserve_case.  By default, it is set to True. If it is set to
   False, then the tokenizer will downcase everything except for
   emoticons.

The __main__ method illustrates by tokenizing a few examples.

I've also included a Tokenizer method tokenize_random_tweet(). If the
twitter library is installed (http://code.google.com/p/python-twitter/)
and Twitter is cooperating, then it should tokenize a random
English-language tweet.
"""
__author__ = 'Christopher Potts'
__copyright__ = 'Copyright 2011, Christopher Potts'
__credits__ = []
__license__ = 'http://www.apache.org/licenses/LICENSE-2.0'
__version__ = '1.0'
__maintainer__ = 'Christopher Potts'
__email__ = "See the author's website"
import re, sasa.htmlentitydefs
emoticon_string = "\n    (?:\n      [<>]?\n      [:;=8]                     # eyes\n      [\\-o\\*\\']?                 # optional nose\n      [\\)\\]\\(\\[dDpP/\\:\\}\\{@\\|\\\\] # mouth\n      |\n      [\\)\\]\\(\\[dDpP/\\:\\}\\{@\\|\\\\] # mouth\n      [\\-o\\*\\']?                 # optional nose\n      [:;=8]                     # eyes\n      [<>]?\n    )"
regex_strings = (
 '\n    (?:\n      (?:            # (international)\n        \\+?[01]\n        [\\-\\s.]*\n      )?\n      (?:            # (area code)\n        [\\(]?\n        \\d{3}\n        [\\-\\s.\\)]*\n      )?\n      \\d{3}          # exchange\n      [\\-\\s.]*\n      \\d{4}          # base\n    )',
 emoticon_string,
 '<[^>]+>',
 '(?:@[\\w_]+)',
 "(?:\\#+[\\w_]+[\\w\\'_\\-]*[\\w_]+)",
 "\n    (?:[a-z][a-z'\\-_]+[a-z])       # Words with apostrophes or dashes.\n    |\n    (?:[+\\-]?\\d+[,/.:-]\\d+[+\\-]?)  # Numbers, including fractions, decimals.\n    |\n    (?:[\\w_]+)                     # Words without apostrophes or dashes.\n    |\n    (?:\\.(?:\\s*\\.){1,})            # Ellipsis dots.\n    |\n    (?:\\S)                         # Everything else that isn't whitespace.\n    ")
word_re = re.compile('(%s)' % '|'.join(regex_strings), re.VERBOSE | re.I | re.UNICODE)
emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)
html_entity_digit_re = re.compile('&#\\d+;')
html_entity_alpha_re = re.compile('&\\w+;')
amp = '&amp;'

class Tokenizer:

    def __init__(self, preserve_case=False):
        self.preserve_case = preserve_case

    def tokenize(self, s):
        """
        Argument: s -- any string or unicode object
        Value: a tokenize list of strings; conatenating this list returns the original string if preserve_case=False
        """
        s = self._Tokenizer__html2unicode(s)
        words = word_re.findall(s)
        if not self.preserve_case:
            words = map(lambda x: x if emoticon_re.search(x) else x.lower(), words)
        return words

    def tokenize_random_tweet(self):
        """
        If the twitter library is installed and a twitter connection
        can be established, then tokenize a random tweet.
        """
        try:
            import twitter
        except ImportError:
            print('Apologies. The random tweet functionality requires the Python twitter library: http://code.google.com/p/python-twitter/')

        from random import shuffle
        api = twitter.Api()
        tweets = api.GetPublicTimeline()
        if tweets:
            for tweet in tweets:
                if tweet.user.lang == 'en':
                    return self.tokenize(tweet.text)

        else:
            raise Exception("Apologies. I couldn't get Twitter to give me a public English-language tweet. Perhaps try again")

    def __html2unicode(self, s):
        """
        Internal metod that seeks to replace all the HTML entities in
        s with their corresponding unicode characters.
        """
        ents = set(html_entity_digit_re.findall(s))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    s = s.replace(ent, unichr(entnum))
                except:
                    pass

        ents = set(html_entity_alpha_re.findall(s))
        ents = filter(lambda x: x != amp, ents)
        for ent in ents:
            entname = ent[1:-1]
            try:
                s = s.replace(ent, unichr(htmlentitydefs.name2codepoint[entname]))
            except:
                pass

            s = s.replace(amp, ' and ')

        return s


if __name__ == '__main__':
    tok = Tokenizer(preserve_case=False)
    samples = ('RT @ #happyfuncoding: this is a typical Twitter tweet :-)', "HTML entities &amp; other Web oddities can be an &aacute;cute <em class='grumpy'>pain</em> >:(",
               "It's perhaps noteworthy that phone numbers like +1 (800) 123-4567, (800) 123-4567, and 123-4567 are treated as words despite their whitespace.")
    for s in samples:
        print('======================================================================')
        print(s)
        tokenized = tok.tokenize(s)
        print('\n'.join(tokenized))