# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gapml/syntax.py
# Compiled at: 2018-09-05 20:59:55
# Size of source mod 2**32: 70705 bytes
""" Syntax Module for Processing PDF Documents 
Copyright 2018(c), Andrew Ferlitsch
"""
version = '0.9.2'
import re, json, os
from nltk.stem import *
import nltk
from nltk import pos_tag
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from unidecode import unidecode
from .vocabulary import Vocabulary, vocab
from .address import Address

class Words(object):
    __doc__ = ' Base class for NLP tokenized words '
    DECIMAL = '.'
    THOUSANDS = ','

    def __init__(self, text=None, bare=False, stem='gap', pos=False, roman=False, stopwords=False, punct=False, conjunction=False, article=False, demonstrative=False, preposition=False, question=False, pronoun=False, quantifier=False, date=False, number=False, ssn=False, telephone=False, name=False, address=False, sentiment=False, gender=False, age=False, dob=False, unit=False, standard=False, metric=False, spell=None):
        """ Constructor 
        text - raw text as string to tokenize
        """
        self._text = text
        self._words = None
        self._punct = punct
        self._stemming = stem
        self._pos = pos
        self._roman = roman
        self._porter = stopwords
        self._bare = bare
        self._standard = standard
        self._metric = metric
        self._spell = None
        self._bow = None
        self._freq = None
        self._tf = None
        if self._bare == False:
            self._spell = spell
            if stopwords is True:
                self._quantifier = True
                self._preposition = True
                self._article = True
                self._conjunction = True
                self._demonstrative = True
                self._question = True
                self._pronoun = True
                self._sentiment = True
                self._number = True
                self._date = True
                self._ssn = True
                self._telephone = True
                self._address = True
                self._name = True
                self._gender = True
                self._age = True
                self._dob = True
                self._unit = True
            else:
                self._quantifier = quantifier
                self._preposition = preposition
                self._article = article
                self._conjunction = conjunction
                self._demonstrative = demonstrative
                self._question = question
                self._pronoun = pronoun
                self._sentiment = sentiment
                self._number = number
                self._date = date
                self._ssn = ssn
                self._telephone = telephone
                self._address = address
                self._name = name
                self._gender = gender
                self._age = age
                self._dob = dob
                self._unit = unit
        elif isinstance(stopwords, bool) is False:
            raise TypeError('Stopwords must be a boolean')
        elif isinstance(bare, bool) is False:
            raise TypeError('Bare must be a boolean')
        elif isinstance(quantifier, bool) is False:
            raise TypeError('Quantifier must be a boolean')
        else:
            if isinstance(preposition, bool) is False:
                raise TypeError('Preposition must be a boolean')
            else:
                if isinstance(conjunction, bool) is False:
                    raise TypeError('Conjunction must be a boolean')
                if isinstance(article, bool) is False:
                    raise TypeError('Article must be a boolean')
                if isinstance(demonstrative, bool) is False:
                    raise TypeError('Demonstrative must be a boolean')
                if isinstance(question, bool) is False:
                    raise TypeError('Question must be a boolean')
                if isinstance(pronoun, bool) is False:
                    raise TypeError('Pronoun must be a boolean')
                if isinstance(number, bool) is False:
                    raise TypeError('Number must be a boolean')
                if isinstance(date, bool) is False:
                    raise TypeError('Date must be a boolean')
                if isinstance(ssn, bool) is False:
                    raise TypeError('SSN must be a boolean')
                if isinstance(telephone, bool) is False:
                    raise TypeError('Telephone must be a boolean')
                if isinstance(name, bool) is False:
                    raise TypeError('Name must be a boolean')
                if isinstance(address, bool) is False:
                    raise TypeError('Address must be a boolean')
                if isinstance(sentiment, bool) is False:
                    raise TypeError('Sentiment must be a boolean')
                if isinstance(gender, bool) is False:
                    raise TypeError('Gender must be a boolean')
                if isinstance(dob, bool) is False:
                    raise TypeError('Gender must be a boolean')
                if isinstance(age, bool) is False:
                    raise TypeError('Age must be a boolean')
                if isinstance(punct, bool) is False:
                    raise TypeError('Punct must be a boolean')
                if isinstance(unit, bool) is False:
                    raise TypeError('Unit must be a boolean')
                if isinstance(standard, bool) is False:
                    raise TypeError('Standard must be a boolean')
                if isinstance(metric, bool) is False:
                    raise TypeError('Metric must be a boolean')
                if text is not None and isinstance(text, str) is False:
                    raise TypeError('String expected for text')
            if spell is not None:
                if spell not in ('en', 'fr', 'es', 'it', 'de'):
                    raise ValueError('Wrong value for spell: en, es, fr, it or de')
                if text is not None:
                    self._split()
                    if self._bare == False:
                        self._preprocess()
                        if self._stemming == 'gap':
                            self._stem()
            elif self._stemming == 'porter':
                self._nltkStemmer('porter')
            else:
                if self._stemming == 'snowball':
                    self._nltkStemmer('snowball')
                else:
                    if self._stemming == 'lancaster':
                        self._nltkStemmer('lancaster')
                    else:
                        if self._stemming == 'lemma':
                            self._lemma()
        self._stopwords()
        self._conversion()
        if self._pos == True:
            self._partsofspeech()

    @property
    def text(self):
        """ Getter for text """
        return self._text

    @property
    def words(self):
        """ Getter for words """
        return self._words

    def _split(self):
        """ Tokenize the Text
            1. Expand contractions.
            2. Replace newlines, carriage returns, tabs with space.
            3. Reduce multi-spaces into single space.
            4. Split text by whitespace (tokenize).
            5. Separate Punctuation.
        """
        self._words = []
        text = self._text.replace("'m ", ' am ')
        text = text.replace("'d ", ' would ')
        text = text.replace("'ll ", ' will ')
        text = text.replace("'ve ", ' have ')
        text = text.replace("'re ", ' are ')
        text = text.replace("can't ", 'can not ')
        text = text.replace("won't ", 'will not ')
        text = text.replace("n't ", ' not ')
        text = text.replace("'s ", ' is ')
        text = text.replace("s' ", 's ')
        text = re.sub('[\r\n\t\x0c]', ' ', text)
        text = re.sub(' +', ' ', text.strip())
        if len(text) == 0:
            return
        words = text.split(' ')
        for word in words:
            length = len(word)
            begin = 0
            for i in range(0, length):
                if word[i].isdigit() or word[i].isalpha() or word[i] in ('.', ',',
                                                                         '/') and i < length - 1:
                    if word[(i + 1)].isdigit():
                        continue
                    if word[i] in ('°', ):
                        if i < length - 1:
                            if word[(i + 1)] in ('f', 'F', 'c', 'C'):
                                continue
                    if word[i] in ('-', '+'):
                        if i < length - 1 and not word[(i + 1)].isdigit():
                            if word[(i + 1)] in ('.', ','):
                                if begin == i or word[(i - 1)] in ('e', 'E'):
                                    continue
                                else:
                                    if begin != i:
                                        self._words.append({'word':word[begin:i],  'tag':Vocabulary.UNTAG})
                                    if word[i] in ('.', '?', '!', ',', ':', ';', '(',
                                                   ')', '[', ']', '"', "'", '¿',
                                                   '¡'):
                                        self._words.append({'word':word[i],  'tag':Vocabulary.PUNCT})
                                    else:
                                        if ord(word[i]) >= 0 and ord(word[i]) <= 7 or ord(word[i]) >= 14 and ord(word[i]) <= 31:
                                            pass
                                        else:
                                            self._words.append({'word':word[i],  'tag':Vocabulary.SYMBOL})
                            begin = i + 1

            if begin < length:
                self._words.append({'word':word[begin:],  'tag':Vocabulary.UNTAG})

    def _preprocess(self):
        """ Preprocess Token List.
                1.  Remove periods from Abbreviations
                2.  Identify Acronyms
                3.  Identify Proper Names (Capitalized).
                4.  Lowercase.
        """
        _words = []
        wasCaps = False
        nwords = len(self._words)
        for index in range(nwords):
            word = self._words[index]
            length = len(word['word'])
            if word['word'] == '.':
                if len(_words) > 0 and len(_words[(-1)]['word']) == 1 and _words[(-1)]['word'].isalpha():
                    if _words[(-1)]['tag'] not in [Vocabulary.NAME, Vocabulary.TITLE]:
                        _words[(-1)]['tag'] = Vocabulary.ABBR
                elif self._punct == False and len(_words) > 0 and (_words[(-1)]['tag'] in [Vocabulary.NAME, Vocabulary.TITLE] or _words[(-1)]['tag']) == Vocabulary.DATE:
                    pass
                else:
                    _words.append(word)
            else:
                if length == 1:
                    if word['word'].isupper():
                        word['word'] = word['word'].lower()
                    if word['word'].isalpha():
                        if len(_words) > 0:
                            if _words[(-1)]['tag'] == Vocabulary.NAME:
                                word['tag'] = Vocabulary.NAME
                            _words.append(word)
                            wasCaps = False
                        elif word['word'].isupper():
                            word['word'] = word['word'][0].isdigit() or word['word'][0] == '°' or word['word'].lower()
                            if index + 1 < nwords and not self._words[(index + 1)]['word'].isupper() or index + 1 != nwords:
                                if wasCaps == False:
                                    try:
                                        v = vocab[word['word']]
                                        if Vocabulary.NAME in v['tag']:
                                            word['tag'] = Vocabulary.NAME
                                        else:
                                            if Vocabulary.TITLE in v['tag']:
                                                word['tag'] = Vocabulary.TITLE
                                                itag = v['tag'].index(Vocabulary.TITLE)
                                                word['word'] = v['lemma'][itag]
                                            else:
                                                word['tag'] = Vocabulary.ACRONYM
                                    except:
                                        word['tag'] = Vocabulary.ACRONYM

                                wasCaps = True
                    elif len(_words) == 0 if word['word'][0].isupper() else len(_words) > 1 and _words[(-1)]['word'] == '.' and _words[(-2)]['tag'] == Vocabulary.TITLE:
                        word['tag'] = Vocabulary.NAME
                    else:
                        if _words[(-1)]['tag'] == Vocabulary.PUNCT and _words[(-1)]['word'] not in (',',
                                                                                                    ':'):
                            pass
                        elif word['word'] in ('Jan', 'January', 'Feb', 'February',
                                              'Mar', 'March', 'Apr', 'April', 'May',
                                              'Jun', 'June', 'Jul', 'July', 'Aug',
                                              'August', 'Sep', 'Sept', 'September',
                                              'Oct', 'October', 'Nov', 'November',
                                              'Dec', 'December'):
                            word['tag'] = Vocabulary.DATE
                        else:
                            word['tag'] = Vocabulary.NAME
                    if len(_words) > 0 and _words[(-1)]['tag'] == Vocabulary.ACRONYM:
                        _words[(-1)]['tag'] = Vocabulary.NAME
                    else:
                        try:
                            v = vocab[_words[(-1)]['word']]
                            if Vocabulary.TITLE in v['tag']:
                                _words[(-1)]['tag'] = Vocabulary.TITLE
                                itag = v['tag'].index(Vocabulary.TITLE)
                                _words[(-1)]['word'] = v['lemma'][itag]
                        except:
                            try:
                                v = vocab[word['word'].lower()]
                                if Vocabulary.TITLE in v['tag']:
                                    if Vocabulary.STREET_TYPE not in v['tag']:
                                        if Vocabulary.STATE not in v['tag']:
                                            word['tag'] = Vocabulary.TITLE
                                            itag = v['tag'].index(Vocabulary.TITLE)
                                            word['word'] = v['lemma'][itag]
                            except:
                                pass

                        wasCaps = False
                else:
                    if word['word'][0].isdigit():
                        cont = False
                        for i in range(1, len(word['word'])):
                            if word['word'][i].isalpha():
                                token = word['word'][i:].lower()
                                try:
                                    v = vocab[token]
                                    if Vocabulary.UNIT in v['tag']:
                                        itag = v['tag'].index(Vocabulary.UNIT)
                                        _words.append({'word':word['word'][0:i],  'tag':Vocabulary.NUMBER})
                                        _words.append({'word':v['lemma'][itag],  'tag':Vocabulary.UNIT})
                                        cont = True
                                except:
                                    pass

                                break

                        if cont == True:
                            continue
                    word['word'] = word['word'].lower()
                    if self._roman:
                        word['word'] = unidecode(word['word'])
                    _words.append(word)

        self._words = _words

    def _stem--- This code section failed: ---

 L. 397         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _words
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  STORE_FAST               'length'

 L. 398     10_12  SETUP_LOOP         2326  'to 2326'
               14  LOAD_GLOBAL              range
               16  LOAD_FAST                'length'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  GET_ITER         
             22_0  COME_FROM          2298  '2298'
             22_1  COME_FROM          2012  '2012'
             22_2  COME_FROM          1518  '1518'
            22_24  FOR_ITER           2324  'to 2324'
               26  STORE_FAST               'i'

 L. 399        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _words
               32  LOAD_FAST                'i'
               34  BINARY_SUBSCR    
               36  LOAD_STR                 'word'
               38  BINARY_SUBSCR    
               40  STORE_FAST               'word'

 L. 400        42  LOAD_GLOBAL              len
               44  LOAD_FAST                'word'
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  STORE_FAST               'l'

 L. 403        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _words
               54  LOAD_FAST                'i'
               56  BINARY_SUBSCR    
               58  LOAD_STR                 'tag'
               60  BINARY_SUBSCR    
               62  LOAD_GLOBAL              Vocabulary
               64  LOAD_ATTR                UNTAG
               66  COMPARE_OP               !=
               68  POP_JUMP_IF_FALSE    72  'to 72'

 L. 404        70  CONTINUE             22  'to 22'
             72_0  COME_FROM            68  '68'

 L. 407        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _spell
               76  LOAD_CONST               None
               78  COMPARE_OP               is-not
               80  POP_JUMP_IF_FALSE   126  'to 126'

 L. 408        82  LOAD_GLOBAL              Norvig
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _spell
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  STORE_FAST               'spell'

 L. 409        92  LOAD_FAST                'spell'
               94  LOAD_METHOD              correction
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _words
              100  LOAD_FAST                'i'
              102  BINARY_SUBSCR    
              104  LOAD_STR                 'word'
              106  BINARY_SUBSCR    
              108  CALL_METHOD_1         1  '1 positional argument'
              110  STORE_FAST               'replace'

 L. 410       112  LOAD_FAST                'replace'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _words
              118  LOAD_FAST                'i'
              120  BINARY_SUBSCR    
              122  LOAD_STR                 'word'
              124  STORE_SUBSCR     
            126_0  COME_FROM            80  '80'

 L. 413       126  SETUP_EXCEPT        238  'to 238'

 L. 414       128  LOAD_GLOBAL              vocab
              130  LOAD_FAST                'word'
              132  BINARY_SUBSCR    
              134  STORE_FAST               'v'

 L. 415       136  LOAD_FAST                'v'
              138  LOAD_STR                 'tag'
              140  BINARY_SUBSCR    
              142  STORE_FAST               't'

 L. 416       144  LOAD_GLOBAL              len
              146  LOAD_FAST                't'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  LOAD_CONST               1
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   232  'to 232'

 L. 417       156  LOAD_FAST                't'
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  LOAD_GLOBAL              Vocabulary
              164  LOAD_ATTR                QUANTIFIER
              166  LOAD_GLOBAL              Vocabulary
              168  LOAD_ATTR                UNIT
              170  LOAD_GLOBAL              Vocabulary
              172  LOAD_ATTR                MEASUREMENT
              174  BUILD_LIST_3          3 
              176  COMPARE_OP               not-in
              178  POP_JUMP_IF_FALSE   232  'to 232'

 L. 418       180  LOAD_FAST                'v'
              182  LOAD_STR                 'lemma'
              184  BINARY_SUBSCR    
              186  STORE_FAST               'l'

 L. 419       188  LOAD_FAST                'l'
              190  LOAD_CONST               None
              192  COMPARE_OP               is-not
              194  POP_JUMP_IF_FALSE   232  'to 232'

 L. 420       196  LOAD_FAST                'l'
              198  LOAD_CONST               0
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                _words
              206  LOAD_FAST                'i'
              208  BINARY_SUBSCR    
              210  LOAD_STR                 'word'
              212  STORE_SUBSCR     

 L. 421       214  LOAD_FAST                't'
              216  LOAD_CONST               0
              218  BINARY_SUBSCR    
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                _words
              224  LOAD_FAST                'i'
              226  BINARY_SUBSCR    
              228  LOAD_STR                 'tag'
              230  STORE_SUBSCR     
            232_0  COME_FROM           194  '194'
            232_1  COME_FROM           178  '178'
            232_2  COME_FROM           154  '154'

 L. 422       232  CONTINUE_LOOP        22  'to 22'
              234  POP_BLOCK        
              236  JUMP_FORWARD        250  'to 250'
            238_0  COME_FROM_EXCEPT    126  '126'

 L. 423       238  POP_TOP          
              240  POP_TOP          
              242  POP_TOP          

 L. 423       244  POP_EXCEPT       
              246  JUMP_FORWARD        250  'to 250'
              248  END_FINALLY      
            250_0  COME_FROM           246  '246'
            250_1  COME_FROM           236  '236'

 L. 426       250  LOAD_FAST                'l'
              252  LOAD_CONST               4
              254  COMPARE_OP               <
          256_258  POP_JUMP_IF_FALSE   262  'to 262'

 L. 427       260  CONTINUE             22  'to 22'
            262_0  COME_FROM           256  '256'

 L. 430       262  LOAD_FAST                'word'
              264  LOAD_METHOD              endswith
              266  LOAD_STR                 'ies'
              268  CALL_METHOD_1         1  '1 positional argument'
          270_272  POP_JUMP_IF_FALSE   336  'to 336'

 L. 431       274  LOAD_FAST                'l'
              276  LOAD_CONST               4
              278  COMPARE_OP               >
          280_282  POP_JUMP_IF_FALSE   312  'to 312'

 L. 432       284  LOAD_FAST                'word'
              286  LOAD_CONST               0
              288  LOAD_CONST               -3
              290  BUILD_SLICE_2         2 
              292  BINARY_SUBSCR    
              294  LOAD_STR                 'y'
              296  BINARY_ADD       
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                _words
              302  LOAD_FAST                'i'
              304  BINARY_SUBSCR    
              306  LOAD_STR                 'word'
              308  STORE_SUBSCR     
              310  JUMP_FORWARD        334  'to 334'
            312_0  COME_FROM           280  '280'

 L. 434       312  LOAD_FAST                'word'
              314  LOAD_CONST               0
              316  LOAD_CONST               -1
              318  BUILD_SLICE_2         2 
              320  BINARY_SUBSCR    
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                _words
              326  LOAD_FAST                'i'
              328  BINARY_SUBSCR    
              330  LOAD_STR                 'word'
              332  STORE_SUBSCR     
            334_0  COME_FROM           310  '310'
              334  JUMP_FORWARD        480  'to 480'
            336_0  COME_FROM           270  '270'

 L. 435       336  LOAD_FAST                'word'
              338  LOAD_METHOD              endswith
              340  LOAD_STR                 'ches'
              342  CALL_METHOD_1         1  '1 positional argument'
          344_346  POP_JUMP_IF_TRUE    384  'to 384'
              348  LOAD_FAST                'word'
              350  LOAD_METHOD              endswith
              352  LOAD_STR                 'ses'
              354  CALL_METHOD_1         1  '1 positional argument'
          356_358  POP_JUMP_IF_TRUE    384  'to 384'
              360  LOAD_FAST                'word'
              362  LOAD_METHOD              endswith
              364  LOAD_STR                 'xes'
              366  CALL_METHOD_1         1  '1 positional argument'
          368_370  POP_JUMP_IF_TRUE    384  'to 384'
              372  LOAD_FAST                'word'
              374  LOAD_METHOD              endswith
              376  LOAD_STR                 'zes'
              378  CALL_METHOD_1         1  '1 positional argument'
          380_382  POP_JUMP_IF_FALSE   408  'to 408'
            384_0  COME_FROM           368  '368'
            384_1  COME_FROM           356  '356'
            384_2  COME_FROM           344  '344'

 L. 436       384  LOAD_FAST                'word'
              386  LOAD_CONST               0
              388  LOAD_CONST               -2
              390  BUILD_SLICE_2         2 
              392  BINARY_SUBSCR    
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                _words
              398  LOAD_FAST                'i'
              400  BINARY_SUBSCR    
              402  LOAD_STR                 'word'
              404  STORE_SUBSCR     
              406  JUMP_FORWARD        480  'to 480'
            408_0  COME_FROM           380  '380'

 L. 439       408  LOAD_FAST                'word'
              410  LOAD_METHOD              endswith
              412  LOAD_STR                 'ss'
              414  CALL_METHOD_1         1  '1 positional argument'
          416_418  POP_JUMP_IF_TRUE    480  'to 480'
              420  LOAD_FAST                'word'
              422  LOAD_METHOD              endswith
              424  LOAD_STR                 'is'
              426  CALL_METHOD_1         1  '1 positional argument'
          428_430  POP_JUMP_IF_TRUE    480  'to 480'
              432  LOAD_FAST                'word'
              434  LOAD_METHOD              endswith
              436  LOAD_STR                 'us'
              438  CALL_METHOD_1         1  '1 positional argument'
          440_442  POP_JUMP_IF_FALSE   446  'to 446'

 L. 440       444  JUMP_FORWARD        480  'to 480'
            446_0  COME_FROM           440  '440'

 L. 441       446  LOAD_FAST                'word'
              448  LOAD_METHOD              endswith
              450  LOAD_STR                 's'
              452  CALL_METHOD_1         1  '1 positional argument'
          454_456  POP_JUMP_IF_FALSE   480  'to 480'

 L. 442       458  LOAD_FAST                'word'
              460  LOAD_CONST               0
              462  LOAD_CONST               -1
              464  BUILD_SLICE_2         2 
              466  BINARY_SUBSCR    
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                _words
              472  LOAD_FAST                'i'
              474  BINARY_SUBSCR    
              476  LOAD_STR                 'word'
              478  STORE_SUBSCR     
            480_0  COME_FROM           454  '454'
            480_1  COME_FROM           444  '444'
            480_2  COME_FROM           428  '428'
            480_3  COME_FROM           416  '416'
            480_4  COME_FROM           406  '406'
            480_5  COME_FROM           334  '334'

 L. 444       480  LOAD_FAST                'self'
              482  LOAD_ATTR                _words
              484  LOAD_FAST                'i'
              486  BINARY_SUBSCR    
              488  LOAD_STR                 'word'
              490  BINARY_SUBSCR    
              492  STORE_FAST               'word'

 L. 447       494  SETUP_EXCEPT        600  'to 600'

 L. 448       496  LOAD_GLOBAL              vocab
              498  LOAD_FAST                'word'
              500  BINARY_SUBSCR    
              502  STORE_FAST               'v'

 L. 449       504  LOAD_FAST                'v'
              506  LOAD_STR                 'tag'
              508  BINARY_SUBSCR    
              510  STORE_FAST               't'

 L. 450       512  LOAD_GLOBAL              len
              514  LOAD_FAST                't'
              516  CALL_FUNCTION_1       1  '1 positional argument'
              518  LOAD_CONST               1
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   594  'to 594'

 L. 451       526  LOAD_FAST                't'
              528  LOAD_CONST               0
              530  BINARY_SUBSCR    
              532  LOAD_GLOBAL              Vocabulary
              534  LOAD_ATTR                QUANTIFIER
              536  COMPARE_OP               !=
          538_540  POP_JUMP_IF_FALSE   594  'to 594'
              542  LOAD_FAST                't'
              544  LOAD_CONST               0
              546  BINARY_SUBSCR    
              548  LOAD_GLOBAL              Vocabulary
              550  LOAD_ATTR                UNIT
              552  COMPARE_OP               !=
          554_556  POP_JUMP_IF_FALSE   594  'to 594'

 L. 452       558  LOAD_FAST                'v'
              560  LOAD_STR                 'lemma'
              562  BINARY_SUBSCR    
              564  STORE_FAST               'l'

 L. 453       566  LOAD_FAST                'l'
              568  LOAD_CONST               None
              570  COMPARE_OP               is-not
          572_574  POP_JUMP_IF_FALSE   594  'to 594'

 L. 454       576  LOAD_FAST                'l'
              578  LOAD_CONST               0
              580  BINARY_SUBSCR    
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                _words
              586  LOAD_FAST                'i'
              588  BINARY_SUBSCR    
              590  LOAD_STR                 'word'
              592  STORE_SUBSCR     
            594_0  COME_FROM           572  '572'
            594_1  COME_FROM           554  '554'
            594_2  COME_FROM           538  '538'
            594_3  COME_FROM           522  '522'

 L. 455       594  CONTINUE_LOOP        22  'to 22'
              596  POP_BLOCK        
              598  JUMP_FORWARD        612  'to 612'
            600_0  COME_FROM_EXCEPT    494  '494'

 L. 456       600  POP_TOP          
              602  POP_TOP          
              604  POP_TOP          

 L. 456       606  POP_EXCEPT       
              608  JUMP_FORWARD        612  'to 612'
              610  END_FINALLY      
            612_0  COME_FROM           608  '608'
            612_1  COME_FROM           598  '598'

 L. 458       612  LOAD_GLOBAL              len
              614  LOAD_FAST                'word'
              616  CALL_FUNCTION_1       1  '1 positional argument'
              618  STORE_FAST               'l'

 L. 461       620  LOAD_FAST                'l'
              622  LOAD_CONST               5
              624  COMPARE_OP               >
          626_628  POP_JUMP_IF_FALSE   942  'to 942'

 L. 462       630  LOAD_FAST                'word'
              632  LOAD_METHOD              endswith
              634  LOAD_STR                 'nning'
              636  CALL_METHOD_1         1  '1 positional argument'
          638_640  POP_JUMP_IF_TRUE    654  'to 654'
              642  LOAD_FAST                'word'
              644  LOAD_METHOD              endswith
              646  LOAD_STR                 'tting'
              648  CALL_METHOD_1         1  '1 positional argument'
          650_652  POP_JUMP_IF_FALSE   680  'to 680'
            654_0  COME_FROM           638  '638'

 L. 463       654  LOAD_FAST                'word'
              656  LOAD_CONST               0
              658  LOAD_CONST               -4
              660  BUILD_SLICE_2         2 
              662  BINARY_SUBSCR    
              664  LOAD_FAST                'self'
              666  LOAD_ATTR                _words
              668  LOAD_FAST                'i'
              670  BINARY_SUBSCR    
              672  LOAD_STR                 'word'
              674  STORE_SUBSCR     
          676_678  JUMP_FORWARD        942  'to 942'
            680_0  COME_FROM           650  '650'

 L. 464       680  LOAD_FAST                'word'
              682  LOAD_METHOD              endswith
              684  LOAD_STR                 'tring'
              686  CALL_METHOD_1         1  '1 positional argument'
          688_690  POP_JUMP_IF_TRUE    716  'to 716'
              692  LOAD_FAST                'word'
              694  LOAD_METHOD              endswith
              696  LOAD_STR                 'yzing'
              698  CALL_METHOD_1         1  '1 positional argument'
          700_702  POP_JUMP_IF_TRUE    716  'to 716'
              704  LOAD_FAST                'word'
              706  LOAD_METHOD              endswith
              708  LOAD_STR                 'ysing'
              710  CALL_METHOD_1         1  '1 positional argument'
          712_714  POP_JUMP_IF_FALSE   744  'to 744'
            716_0  COME_FROM           700  '700'
            716_1  COME_FROM           688  '688'

 L. 465       716  LOAD_FAST                'word'
              718  LOAD_CONST               0
              720  LOAD_CONST               -3
              722  BUILD_SLICE_2         2 
              724  BINARY_SUBSCR    
              726  LOAD_STR                 'e'
              728  BINARY_ADD       
              730  LOAD_FAST                'self'
              732  LOAD_ATTR                _words
              734  LOAD_FAST                'i'
              736  BINARY_SUBSCR    
              738  LOAD_STR                 'word'
              740  STORE_SUBSCR     
              742  JUMP_FORWARD        942  'to 942'
            744_0  COME_FROM           712  '712'

 L. 466       744  LOAD_FAST                'word'
              746  LOAD_METHOD              endswith
              748  LOAD_STR                 'ding'
              750  CALL_METHOD_1         1  '1 positional argument'
          752_754  POP_JUMP_IF_TRUE    792  'to 792'
              756  LOAD_FAST                'word'
              758  LOAD_METHOD              endswith
              760  LOAD_STR                 'king'
              762  CALL_METHOD_1         1  '1 positional argument'
          764_766  POP_JUMP_IF_TRUE    792  'to 792'
              768  LOAD_FAST                'word'
              770  LOAD_METHOD              endswith
              772  LOAD_STR                 'zing'
              774  CALL_METHOD_1         1  '1 positional argument'
          776_778  POP_JUMP_IF_TRUE    792  'to 792'
              780  LOAD_FAST                'word'
              782  LOAD_METHOD              endswith
              784  LOAD_STR                 'ting'
              786  CALL_METHOD_1         1  '1 positional argument'
          788_790  POP_JUMP_IF_FALSE   868  'to 868'
            792_0  COME_FROM           776  '776'
            792_1  COME_FROM           764  '764'
            792_2  COME_FROM           752  '752'

 L. 467       792  LOAD_FAST                'self'
              794  LOAD_ATTR                _words
              796  LOAD_FAST                'i'
              798  BINARY_SUBSCR    
              800  LOAD_STR                 'word'
              802  BINARY_SUBSCR    
              804  LOAD_CONST               -5
              806  BINARY_SUBSCR    
              808  LOAD_CONST               ('a', 'e', 'i', 'o', 'u', 'y')
              810  COMPARE_OP               in
          812_814  POP_JUMP_IF_FALSE   844  'to 844'

 L. 468       816  LOAD_FAST                'word'
              818  LOAD_CONST               0
              820  LOAD_CONST               -3
              822  BUILD_SLICE_2         2 
              824  BINARY_SUBSCR    
              826  LOAD_STR                 'e'
              828  BINARY_ADD       
              830  LOAD_FAST                'self'
              832  LOAD_ATTR                _words
              834  LOAD_FAST                'i'
              836  BINARY_SUBSCR    
              838  LOAD_STR                 'word'
              840  STORE_SUBSCR     
              842  JUMP_FORWARD        866  'to 866'
            844_0  COME_FROM           812  '812'

 L. 470       844  LOAD_FAST                'word'
              846  LOAD_CONST               0
              848  LOAD_CONST               -3
              850  BUILD_SLICE_2         2 
              852  BINARY_SUBSCR    
              854  LOAD_FAST                'self'
              856  LOAD_ATTR                _words
              858  LOAD_FAST                'i'
              860  BINARY_SUBSCR    
              862  LOAD_STR                 'word'
              864  STORE_SUBSCR     
            866_0  COME_FROM           842  '842'
              866  JUMP_FORWARD        942  'to 942'
            868_0  COME_FROM           788  '788'

 L. 471       868  LOAD_FAST                'word'
              870  LOAD_METHOD              endswith
              872  LOAD_STR                 'ving'
              874  CALL_METHOD_1         1  '1 positional argument'
          876_878  POP_JUMP_IF_FALSE   908  'to 908'

 L. 472       880  LOAD_FAST                'word'
              882  LOAD_CONST               0
              884  LOAD_CONST               -3
              886  BUILD_SLICE_2         2 
              888  BINARY_SUBSCR    
              890  LOAD_STR                 'e'
              892  BINARY_ADD       
              894  LOAD_FAST                'self'
              896  LOAD_ATTR                _words
              898  LOAD_FAST                'i'
              900  BINARY_SUBSCR    
              902  LOAD_STR                 'word'
              904  STORE_SUBSCR     
              906  JUMP_FORWARD        942  'to 942'
            908_0  COME_FROM           876  '876'

 L. 473       908  LOAD_FAST                'word'
              910  LOAD_METHOD              endswith
              912  LOAD_STR                 'ing'
              914  CALL_METHOD_1         1  '1 positional argument'
          916_918  POP_JUMP_IF_FALSE   942  'to 942'

 L. 474       920  LOAD_FAST                'word'
              922  LOAD_CONST               0
              924  LOAD_CONST               -3
              926  BUILD_SLICE_2         2 
              928  BINARY_SUBSCR    
              930  LOAD_FAST                'self'
              932  LOAD_ATTR                _words
              934  LOAD_FAST                'i'
              936  BINARY_SUBSCR    
              938  LOAD_STR                 'word'
              940  STORE_SUBSCR     
            942_0  COME_FROM           916  '916'
            942_1  COME_FROM           906  '906'
            942_2  COME_FROM           866  '866'
            942_3  COME_FROM           742  '742'
            942_4  COME_FROM           676  '676'
            942_5  COME_FROM           626  '626'

 L. 476       942  LOAD_FAST                'self'
              944  LOAD_ATTR                _words
              946  LOAD_FAST                'i'
              948  BINARY_SUBSCR    
              950  LOAD_STR                 'word'
              952  BINARY_SUBSCR    
              954  STORE_FAST               'word'

 L. 477       956  LOAD_GLOBAL              len
              958  LOAD_FAST                'word'
              960  CALL_FUNCTION_1       1  '1 positional argument'
              962  STORE_FAST               'l'

 L. 480       964  SETUP_EXCEPT       1070  'to 1070'

 L. 481       966  LOAD_GLOBAL              vocab
              968  LOAD_FAST                'word'
              970  BINARY_SUBSCR    
              972  STORE_FAST               'v'

 L. 482       974  LOAD_FAST                'v'
              976  LOAD_STR                 'tag'
              978  BINARY_SUBSCR    
              980  STORE_FAST               't'

 L. 483       982  LOAD_GLOBAL              len
              984  LOAD_FAST                't'
              986  CALL_FUNCTION_1       1  '1 positional argument'
              988  LOAD_CONST               1
              990  COMPARE_OP               ==
          992_994  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 484       996  LOAD_FAST                't'
              998  LOAD_CONST               0
             1000  BINARY_SUBSCR    
             1002  LOAD_GLOBAL              Vocabulary
             1004  LOAD_ATTR                QUANTIFIER
             1006  COMPARE_OP               !=
         1008_1010  POP_JUMP_IF_FALSE  1064  'to 1064'
             1012  LOAD_FAST                't'
             1014  LOAD_CONST               0
             1016  BINARY_SUBSCR    
             1018  LOAD_GLOBAL              Vocabulary
             1020  LOAD_ATTR                UNIT
             1022  COMPARE_OP               !=
         1024_1026  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 485      1028  LOAD_FAST                'v'
             1030  LOAD_STR                 'lemma'
             1032  BINARY_SUBSCR    
             1034  STORE_FAST               'l'

 L. 486      1036  LOAD_FAST                'l'
             1038  LOAD_CONST               None
             1040  COMPARE_OP               is-not
         1042_1044  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 487      1046  LOAD_FAST                'l'
             1048  LOAD_CONST               0
             1050  BINARY_SUBSCR    
             1052  LOAD_FAST                'self'
             1054  LOAD_ATTR                _words
             1056  LOAD_FAST                'i'
             1058  BINARY_SUBSCR    
             1060  LOAD_STR                 'word'
             1062  STORE_SUBSCR     
           1064_0  COME_FROM          1042  '1042'
           1064_1  COME_FROM          1024  '1024'
           1064_2  COME_FROM          1008  '1008'
           1064_3  COME_FROM           992  '992'

 L. 488      1064  CONTINUE_LOOP        22  'to 22'
             1066  POP_BLOCK        
             1068  JUMP_FORWARD       1082  'to 1082'
           1070_0  COME_FROM_EXCEPT    964  '964'

 L. 489      1070  POP_TOP          
             1072  POP_TOP          
             1074  POP_TOP          

 L. 489      1076  POP_EXCEPT       
             1078  JUMP_FORWARD       1082  'to 1082'
             1080  END_FINALLY      
           1082_0  COME_FROM          1078  '1078'
           1082_1  COME_FROM          1068  '1068'

 L. 491      1082  LOAD_FAST                'l'
             1084  LOAD_CONST               4
             1086  COMPARE_OP               >
         1088_1090  POP_JUMP_IF_FALSE  1698  'to 1698'

 L. 493      1092  LOAD_FAST                'word'
             1094  LOAD_METHOD              endswith
             1096  LOAD_STR                 'dden'
             1098  CALL_METHOD_1         1  '1 positional argument'
         1100_1102  POP_JUMP_IF_TRUE   1128  'to 1128'
             1104  LOAD_FAST                'word'
             1106  LOAD_METHOD              endswith
             1108  LOAD_STR                 'tten'
             1110  CALL_METHOD_1         1  '1 positional argument'
         1112_1114  POP_JUMP_IF_TRUE   1128  'to 1128'
             1116  LOAD_FAST                'word'
             1118  LOAD_METHOD              endswith
             1120  LOAD_STR                 'nned'
             1122  CALL_METHOD_1         1  '1 positional argument'
         1124_1126  POP_JUMP_IF_FALSE  1196  'to 1196'
           1128_0  COME_FROM          1112  '1112'
           1128_1  COME_FROM          1100  '1100'

 L. 494      1128  LOAD_FAST                'word'
             1130  LOAD_CONST               -5
             1132  BINARY_SUBSCR    
             1134  LOAD_STR                 'i'
             1136  COMPARE_OP               ==
         1138_1140  POP_JUMP_IF_FALSE  1170  'to 1170'

 L. 495      1142  LOAD_FAST                'word'
             1144  LOAD_CONST               0
             1146  LOAD_CONST               -3
             1148  BUILD_SLICE_2         2 
             1150  BINARY_SUBSCR    
             1152  LOAD_STR                 'e'
             1154  BINARY_ADD       
             1156  LOAD_FAST                'self'
             1158  LOAD_ATTR                _words
             1160  LOAD_FAST                'i'
             1162  BINARY_SUBSCR    
             1164  LOAD_STR                 'word'
             1166  STORE_SUBSCR     
             1168  JUMP_FORWARD       1698  'to 1698'
           1170_0  COME_FROM          1138  '1138'

 L. 497      1170  LOAD_FAST                'word'
             1172  LOAD_CONST               0
             1174  LOAD_CONST               -3
             1176  BUILD_SLICE_2         2 
             1178  BINARY_SUBSCR    
             1180  LOAD_FAST                'self'
             1182  LOAD_ATTR                _words
             1184  LOAD_FAST                'i'
             1186  BINARY_SUBSCR    
             1188  LOAD_STR                 'word'
             1190  STORE_SUBSCR     
         1192_1194  JUMP_FORWARD       1698  'to 1698'
           1196_0  COME_FROM          1124  '1124'

 L. 498      1196  LOAD_FAST                'l'
             1198  LOAD_CONST               6
             1200  COMPARE_OP               >
         1202_1204  POP_JUMP_IF_FALSE  1244  'to 1244'
             1206  LOAD_FAST                'word'
             1208  LOAD_METHOD              endswith
             1210  LOAD_STR                 'lled'
             1212  CALL_METHOD_1         1  '1 positional argument'
         1214_1216  POP_JUMP_IF_FALSE  1244  'to 1244'

 L. 499      1218  LOAD_FAST                'word'
             1220  LOAD_CONST               0
             1222  LOAD_CONST               -3
             1224  BUILD_SLICE_2         2 
             1226  BINARY_SUBSCR    
             1228  LOAD_FAST                'self'
             1230  LOAD_ATTR                _words
             1232  LOAD_FAST                'i'
             1234  BINARY_SUBSCR    
             1236  LOAD_STR                 'word'
             1238  STORE_SUBSCR     
         1240_1242  JUMP_FORWARD       1698  'to 1698'
           1244_0  COME_FROM          1214  '1214'
           1244_1  COME_FROM          1202  '1202'

 L. 500      1244  LOAD_FAST                'word'
             1246  LOAD_METHOD              endswith
             1248  LOAD_STR                 'tred'
             1250  CALL_METHOD_1         1  '1 positional argument'
         1252_1254  POP_JUMP_IF_TRUE   1304  'to 1304'
             1256  LOAD_FAST                'word'
             1258  LOAD_METHOD              endswith
             1260  LOAD_STR                 'nced'
             1262  CALL_METHOD_1         1  '1 positional argument'
         1264_1266  POP_JUMP_IF_TRUE   1304  'to 1304'
             1268  LOAD_FAST                'word'
             1270  LOAD_METHOD              endswith
             1272  LOAD_STR                 'psed'
             1274  CALL_METHOD_1         1  '1 positional argument'
         1276_1278  POP_JUMP_IF_TRUE   1304  'to 1304'
             1280  LOAD_FAST                'word'
             1282  LOAD_METHOD              endswith
             1284  LOAD_STR                 'ysed'
             1286  CALL_METHOD_1         1  '1 positional argument'
         1288_1290  POP_JUMP_IF_TRUE   1304  'to 1304'
             1292  LOAD_FAST                'word'
             1294  LOAD_METHOD              endswith
             1296  LOAD_STR                 'yzed'
             1298  CALL_METHOD_1         1  '1 positional argument'
         1300_1302  POP_JUMP_IF_FALSE  1330  'to 1330'
           1304_0  COME_FROM          1288  '1288'
           1304_1  COME_FROM          1276  '1276'
           1304_2  COME_FROM          1264  '1264'
           1304_3  COME_FROM          1252  '1252'

 L. 501      1304  LOAD_FAST                'word'
             1306  LOAD_CONST               0
             1308  LOAD_CONST               -1
             1310  BUILD_SLICE_2         2 
             1312  BINARY_SUBSCR    
             1314  LOAD_FAST                'self'
             1316  LOAD_ATTR                _words
             1318  LOAD_FAST                'i'
             1320  BINARY_SUBSCR    
             1322  LOAD_STR                 'word'
             1324  STORE_SUBSCR     
         1326_1328  JUMP_FORWARD       1698  'to 1698'
           1330_0  COME_FROM          1300  '1300'

 L. 502      1330  LOAD_FAST                'word'
             1332  LOAD_METHOD              endswith
             1334  LOAD_STR                 'mmed'
             1336  CALL_METHOD_1         1  '1 positional argument'
         1338_1340  POP_JUMP_IF_FALSE  1368  'to 1368'

 L. 503      1342  LOAD_FAST                'word'
             1344  LOAD_CONST               0
             1346  LOAD_CONST               -3
             1348  BUILD_SLICE_2         2 
             1350  BINARY_SUBSCR    
             1352  LOAD_FAST                'self'
             1354  LOAD_ATTR                _words
             1356  LOAD_FAST                'i'
             1358  BINARY_SUBSCR    
             1360  LOAD_STR                 'word'
             1362  STORE_SUBSCR     
         1364_1366  JUMP_FORWARD       1698  'to 1698'
           1368_0  COME_FROM          1338  '1338'

 L. 504      1368  LOAD_FAST                'word'
             1370  LOAD_METHOD              endswith
             1372  LOAD_STR                 'ied'
             1374  CALL_METHOD_1         1  '1 positional argument'
         1376_1378  POP_JUMP_IF_FALSE  1410  'to 1410'

 L. 505      1380  LOAD_FAST                'word'
             1382  LOAD_CONST               0
             1384  LOAD_CONST               -3
             1386  BUILD_SLICE_2         2 
             1388  BINARY_SUBSCR    
             1390  LOAD_STR                 'y'
             1392  BINARY_ADD       
             1394  LOAD_FAST                'self'
             1396  LOAD_ATTR                _words
             1398  LOAD_FAST                'i'
             1400  BINARY_SUBSCR    
             1402  LOAD_STR                 'word'
             1404  STORE_SUBSCR     
         1406_1408  JUMP_FORWARD       1698  'to 1698'
           1410_0  COME_FROM          1376  '1376'

 L. 506      1410  LOAD_FAST                'word'
             1412  LOAD_METHOD              endswith
             1414  LOAD_STR                 'zed'
             1416  CALL_METHOD_1         1  '1 positional argument'
         1418_1420  POP_JUMP_IF_TRUE   1434  'to 1434'
             1422  LOAD_FAST                'word'
             1424  LOAD_METHOD              endswith
             1426  LOAD_STR                 'ved'
             1428  CALL_METHOD_1         1  '1 positional argument'
         1430_1432  POP_JUMP_IF_FALSE  1458  'to 1458'
           1434_0  COME_FROM          1418  '1418'

 L. 507      1434  LOAD_FAST                'word'
             1436  LOAD_CONST               0
             1438  LOAD_CONST               -1
             1440  BUILD_SLICE_2         2 
             1442  BINARY_SUBSCR    
             1444  LOAD_FAST                'self'
             1446  LOAD_ATTR                _words
             1448  LOAD_FAST                'i'
             1450  BINARY_SUBSCR    
             1452  LOAD_STR                 'word'
             1454  STORE_SUBSCR     
             1456  JUMP_FORWARD       1698  'to 1698'
           1458_0  COME_FROM          1430  '1430'

 L. 508      1458  LOAD_FAST                'word'
             1460  LOAD_METHOD              endswith
             1462  LOAD_STR                 'eed'
             1464  CALL_METHOD_1         1  '1 positional argument'
         1466_1468  POP_JUMP_IF_FALSE  1474  'to 1474'

 L. 509      1470  CONTINUE             22  'to 22'
             1472  JUMP_FORWARD       1698  'to 1698'
           1474_0  COME_FROM          1466  '1466'

 L. 510      1474  LOAD_FAST                'word'
             1476  LOAD_METHOD              endswith
             1478  LOAD_STR                 'ed'
             1480  CALL_METHOD_1         1  '1 positional argument'
         1482_1484  POP_JUMP_IF_FALSE  1510  'to 1510'

 L. 511      1486  LOAD_FAST                'word'
             1488  LOAD_CONST               0
             1490  LOAD_CONST               -2
             1492  BUILD_SLICE_2         2 
             1494  BINARY_SUBSCR    
             1496  LOAD_FAST                'self'
             1498  LOAD_ATTR                _words
             1500  LOAD_FAST                'i'
             1502  BINARY_SUBSCR    
             1504  LOAD_STR                 'word'
             1506  STORE_SUBSCR     
             1508  JUMP_FORWARD       1698  'to 1698'
           1510_0  COME_FROM          1482  '1482'

 L. 514      1510  LOAD_FAST                'word'
             1512  LOAD_METHOD              endswith
             1514  LOAD_STR                 'ther'
             1516  CALL_METHOD_1         1  '1 positional argument'
             1518  POP_JUMP_IF_TRUE     22  'to 22'
             1520  LOAD_FAST                'word'
             1522  LOAD_METHOD              endswith
             1524  LOAD_STR                 'ever'
             1526  CALL_METHOD_1         1  '1 positional argument'
         1528_1530  POP_JUMP_IF_FALSE  1536  'to 1536'

 L. 515      1532  CONTINUE             22  'to 22'
             1534  JUMP_FORWARD       1698  'to 1698'
           1536_0  COME_FROM          1528  '1528'

 L. 516      1536  LOAD_FAST                'word'
             1538  LOAD_METHOD              endswith
             1540  LOAD_STR                 'mber'
             1542  CALL_METHOD_1         1  '1 positional argument'
         1544_1546  POP_JUMP_IF_FALSE  1552  'to 1552'

 L. 517      1548  CONTINUE             22  'to 22'
             1550  JUMP_FORWARD       1698  'to 1698'
           1552_0  COME_FROM          1544  '1544'

 L. 518      1552  LOAD_FAST                'word'
             1554  LOAD_METHOD              endswith
             1556  LOAD_STR                 'ncer'
             1558  CALL_METHOD_1         1  '1 positional argument'
         1560_1562  POP_JUMP_IF_FALSE  1588  'to 1588'

 L. 519      1564  LOAD_FAST                'word'
             1566  LOAD_CONST               0
             1568  LOAD_CONST               -1
             1570  BUILD_SLICE_2         2 
             1572  BINARY_SUBSCR    
             1574  LOAD_FAST                'self'
             1576  LOAD_ATTR                _words
             1578  LOAD_FAST                'i'
             1580  BINARY_SUBSCR    
             1582  LOAD_STR                 'word'
             1584  STORE_SUBSCR     
             1586  JUMP_FORWARD       1698  'to 1698'
           1588_0  COME_FROM          1560  '1560'

 L. 520      1588  LOAD_FAST                'word'
             1590  LOAD_METHOD              endswith
             1592  LOAD_STR                 'ier'
             1594  CALL_METHOD_1         1  '1 positional argument'
         1596_1598  POP_JUMP_IF_FALSE  1628  'to 1628'

 L. 521      1600  LOAD_FAST                'word'
             1602  LOAD_CONST               0
             1604  LOAD_CONST               -3
             1606  BUILD_SLICE_2         2 
             1608  BINARY_SUBSCR    
             1610  LOAD_STR                 'y'
             1612  BINARY_ADD       
             1614  LOAD_FAST                'self'
             1616  LOAD_ATTR                _words
             1618  LOAD_FAST                'i'
             1620  BINARY_SUBSCR    
             1622  LOAD_STR                 'word'
             1624  STORE_SUBSCR     
             1626  JUMP_FORWARD       1698  'to 1698'
           1628_0  COME_FROM          1596  '1596'

 L. 522      1628  LOAD_FAST                'word'
             1630  LOAD_METHOD              endswith
             1632  LOAD_STR                 'der'
             1634  CALL_METHOD_1         1  '1 positional argument'
         1636_1638  POP_JUMP_IF_FALSE  1664  'to 1664'

 L. 523      1640  LOAD_FAST                'word'
             1642  LOAD_CONST               0
             1644  LOAD_CONST               -1
             1646  BUILD_SLICE_2         2 
             1648  BINARY_SUBSCR    
             1650  LOAD_FAST                'self'
             1652  LOAD_ATTR                _words
             1654  LOAD_FAST                'i'
             1656  BINARY_SUBSCR    
             1658  LOAD_STR                 'word'
             1660  STORE_SUBSCR     
             1662  JUMP_FORWARD       1698  'to 1698'
           1664_0  COME_FROM          1636  '1636'

 L. 524      1664  LOAD_FAST                'word'
             1666  LOAD_METHOD              endswith
             1668  LOAD_STR                 'er'
             1670  CALL_METHOD_1         1  '1 positional argument'
           1672_0  COME_FROM          1168  '1168'
         1672_1674  POP_JUMP_IF_FALSE  1698  'to 1698'

 L. 525      1676  LOAD_FAST                'word'
             1678  LOAD_CONST               0
             1680  LOAD_CONST               -2
             1682  BUILD_SLICE_2         2 
             1684  BINARY_SUBSCR    
             1686  LOAD_FAST                'self'
             1688  LOAD_ATTR                _words
             1690  LOAD_FAST                'i'
             1692  BINARY_SUBSCR    
             1694  LOAD_STR                 'word'
             1696  STORE_SUBSCR     
           1698_0  COME_FROM          1672  '1672'
           1698_1  COME_FROM          1662  '1662'
           1698_2  COME_FROM          1626  '1626'
           1698_3  COME_FROM          1586  '1586'
           1698_4  COME_FROM          1550  '1550'
           1698_5  COME_FROM          1534  '1534'
           1698_6  COME_FROM          1508  '1508'
           1698_7  COME_FROM          1472  '1472'
           1698_8  COME_FROM          1456  '1456'
           1698_9  COME_FROM          1406  '1406'
          1698_10  COME_FROM          1364  '1364'
          1698_11  COME_FROM          1326  '1326'
          1698_12  COME_FROM          1240  '1240'
          1698_13  COME_FROM          1192  '1192'
          1698_14  COME_FROM          1088  '1088'

 L. 527      1698  LOAD_FAST                'l'
             1700  LOAD_CONST               5
             1702  COMPARE_OP               >
         1704_1706  POP_JUMP_IF_FALSE  1782  'to 1782'

 L. 529      1708  LOAD_FAST                'word'
             1710  LOAD_METHOD              endswith
             1712  LOAD_STR                 'iest'
             1714  CALL_METHOD_1         1  '1 positional argument'
         1716_1718  POP_JUMP_IF_FALSE  1748  'to 1748'

 L. 530      1720  LOAD_FAST                'word'
             1722  LOAD_CONST               0
             1724  LOAD_CONST               -4
             1726  BUILD_SLICE_2         2 
             1728  BINARY_SUBSCR    
             1730  LOAD_STR                 'y'
             1732  BINARY_ADD       
             1734  LOAD_FAST                'self'
             1736  LOAD_ATTR                _words
             1738  LOAD_FAST                'i'
             1740  BINARY_SUBSCR    
             1742  LOAD_STR                 'word'
             1744  STORE_SUBSCR     
             1746  JUMP_FORWARD       1782  'to 1782'
           1748_0  COME_FROM          1716  '1716'

 L. 531      1748  LOAD_FAST                'word'
             1750  LOAD_METHOD              endswith
             1752  LOAD_STR                 'est'
             1754  CALL_METHOD_1         1  '1 positional argument'
         1756_1758  POP_JUMP_IF_FALSE  1782  'to 1782'

 L. 532      1760  LOAD_FAST                'word'
             1762  LOAD_CONST               0
             1764  LOAD_CONST               -3
             1766  BUILD_SLICE_2         2 
             1768  BINARY_SUBSCR    
             1770  LOAD_FAST                'self'
             1772  LOAD_ATTR                _words
             1774  LOAD_FAST                'i'
             1776  BINARY_SUBSCR    
             1778  LOAD_STR                 'word'
             1780  STORE_SUBSCR     
           1782_0  COME_FROM          1756  '1756'
           1782_1  COME_FROM          1746  '1746'
           1782_2  COME_FROM          1704  '1704'

 L. 534      1782  LOAD_FAST                'self'
             1784  LOAD_ATTR                _words
             1786  LOAD_FAST                'i'
             1788  BINARY_SUBSCR    
             1790  LOAD_STR                 'word'
             1792  BINARY_SUBSCR    
             1794  STORE_FAST               'word'

 L. 535      1796  LOAD_GLOBAL              len
             1798  LOAD_FAST                'word'
             1800  CALL_FUNCTION_1       1  '1 positional argument'
             1802  STORE_FAST               'l'

 L. 536      1804  LOAD_FAST                'l'
             1806  LOAD_CONST               5
             1808  COMPARE_OP               >
         1810_1812  POP_JUMP_IF_FALSE  1888  'to 1888'

 L. 538      1814  LOAD_FAST                'word'
             1816  LOAD_METHOD              endswith
             1818  LOAD_STR                 'ily'
             1820  CALL_METHOD_1         1  '1 positional argument'
         1822_1824  POP_JUMP_IF_FALSE  1854  'to 1854'

 L. 539      1826  LOAD_FAST                'word'
             1828  LOAD_CONST               0
             1830  LOAD_CONST               -3
             1832  BUILD_SLICE_2         2 
             1834  BINARY_SUBSCR    
             1836  LOAD_STR                 'y'
             1838  BINARY_ADD       
             1840  LOAD_FAST                'self'
             1842  LOAD_ATTR                _words
             1844  LOAD_FAST                'i'
             1846  BINARY_SUBSCR    
             1848  LOAD_STR                 'word'
             1850  STORE_SUBSCR     
             1852  JUMP_FORWARD       1888  'to 1888'
           1854_0  COME_FROM          1822  '1822'

 L. 540      1854  LOAD_FAST                'word'
             1856  LOAD_METHOD              endswith
             1858  LOAD_STR                 'ly'
             1860  CALL_METHOD_1         1  '1 positional argument'
         1862_1864  POP_JUMP_IF_FALSE  1888  'to 1888'

 L. 541      1866  LOAD_FAST                'word'
             1868  LOAD_CONST               0
             1870  LOAD_CONST               -2
             1872  BUILD_SLICE_2         2 
             1874  BINARY_SUBSCR    
             1876  LOAD_FAST                'self'
             1878  LOAD_ATTR                _words
             1880  LOAD_FAST                'i'
             1882  BINARY_SUBSCR    
             1884  LOAD_STR                 'word'
             1886  STORE_SUBSCR     
           1888_0  COME_FROM          1862  '1862'
           1888_1  COME_FROM          1852  '1852'
           1888_2  COME_FROM          1810  '1810'

 L. 544      1888  SETUP_EXCEPT       1994  'to 1994'

 L. 545      1890  LOAD_GLOBAL              vocab
             1892  LOAD_FAST                'word'
             1894  BINARY_SUBSCR    
             1896  STORE_FAST               'v'

 L. 546      1898  LOAD_FAST                'v'
             1900  LOAD_STR                 'tag'
             1902  BINARY_SUBSCR    
             1904  STORE_FAST               't'

 L. 547      1906  LOAD_GLOBAL              len
             1908  LOAD_FAST                't'
             1910  CALL_FUNCTION_1       1  '1 positional argument'
             1912  LOAD_CONST               1
             1914  COMPARE_OP               ==
         1916_1918  POP_JUMP_IF_FALSE  1988  'to 1988'

 L. 548      1920  LOAD_FAST                't'
             1922  LOAD_CONST               0
             1924  BINARY_SUBSCR    
             1926  LOAD_GLOBAL              Vocabulary
             1928  LOAD_ATTR                QUANTIFIER
             1930  COMPARE_OP               !=
         1932_1934  POP_JUMP_IF_FALSE  1988  'to 1988'
             1936  LOAD_FAST                't'
             1938  LOAD_CONST               0
             1940  BINARY_SUBSCR    
             1942  LOAD_GLOBAL              Vocabulary
             1944  LOAD_ATTR                UNIT
             1946  COMPARE_OP               !=
         1948_1950  POP_JUMP_IF_FALSE  1988  'to 1988'

 L. 549      1952  LOAD_FAST                'v'
             1954  LOAD_STR                 'lemma'
             1956  BINARY_SUBSCR    
             1958  STORE_FAST               'l'

 L. 550      1960  LOAD_FAST                'l'
             1962  LOAD_CONST               None
             1964  COMPARE_OP               is-not
         1966_1968  POP_JUMP_IF_FALSE  1988  'to 1988'

 L. 551      1970  LOAD_FAST                'l'
             1972  LOAD_CONST               0
             1974  BINARY_SUBSCR    
             1976  LOAD_FAST                'self'
             1978  LOAD_ATTR                _words
             1980  LOAD_FAST                'i'
             1982  BINARY_SUBSCR    
             1984  LOAD_STR                 'word'
             1986  STORE_SUBSCR     
           1988_0  COME_FROM          1966  '1966'
           1988_1  COME_FROM          1948  '1948'
           1988_2  COME_FROM          1932  '1932'
           1988_3  COME_FROM          1916  '1916'

 L. 552      1988  CONTINUE_LOOP        22  'to 22'
             1990  POP_BLOCK        
             1992  JUMP_FORWARD       2006  'to 2006'
           1994_0  COME_FROM_EXCEPT   1888  '1888'

 L. 553      1994  POP_TOP          
             1996  POP_TOP          
             1998  POP_TOP          

 L. 553      2000  POP_EXCEPT       
             2002  JUMP_FORWARD       2006  'to 2006'
             2004  END_FINALLY      
           2006_0  COME_FROM          2002  '2002'
           2006_1  COME_FROM          1992  '1992'

 L. 556      2006  LOAD_FAST                'l'
             2008  LOAD_CONST               5
             2010  COMPARE_OP               >
             2012  POP_JUMP_IF_FALSE    22  'to 22'

 L. 557      2014  LOAD_FAST                'word'
             2016  LOAD_METHOD              endswith
             2018  LOAD_STR                 'ise'
             2020  CALL_METHOD_1         1  '1 positional argument'
         2022_2024  POP_JUMP_IF_TRUE   2038  'to 2038'
             2026  LOAD_FAST                'word'
             2028  LOAD_METHOD              endswith
             2030  LOAD_STR                 'ize'
             2032  CALL_METHOD_1         1  '1 positional argument'
         2034_2036  POP_JUMP_IF_FALSE  2062  'to 2062'
           2038_0  COME_FROM          2022  '2022'

 L. 558      2038  LOAD_FAST                'word'
             2040  LOAD_CONST               0
             2042  LOAD_CONST               -3
             2044  BUILD_SLICE_2         2 
             2046  BINARY_SUBSCR    
             2048  LOAD_FAST                'self'
             2050  LOAD_ATTR                _words
             2052  LOAD_FAST                'i'
             2054  BINARY_SUBSCR    
             2056  LOAD_STR                 'word'
             2058  STORE_SUBSCR     
             2060  JUMP_BACK            22  'to 22'
           2062_0  COME_FROM          2034  '2034'

 L. 559      2062  LOAD_FAST                'word'
             2064  LOAD_METHOD              endswith
             2066  LOAD_STR                 'ify'
             2068  CALL_METHOD_1         1  '1 positional argument'
         2070_2072  POP_JUMP_IF_FALSE  2102  'to 2102'

 L. 560      2074  LOAD_FAST                'word'
             2076  LOAD_CONST               0
             2078  LOAD_CONST               -3
             2080  BUILD_SLICE_2         2 
             2082  BINARY_SUBSCR    
             2084  LOAD_STR                 'y'
             2086  BINARY_ADD       
             2088  LOAD_FAST                'self'
             2090  LOAD_ATTR                _words
             2092  LOAD_FAST                'i'
             2094  BINARY_SUBSCR    
             2096  LOAD_STR                 'word'
             2098  STORE_SUBSCR     
             2100  JUMP_BACK            22  'to 22'
           2102_0  COME_FROM          2070  '2070'

 L. 561      2102  LOAD_FAST                'word'
             2104  LOAD_METHOD              endswith
             2106  LOAD_STR                 'fy'
             2108  CALL_METHOD_1         1  '1 positional argument'
         2110_2112  POP_JUMP_IF_FALSE  2138  'to 2138'

 L. 562      2114  LOAD_FAST                'word'
             2116  LOAD_CONST               0
             2118  LOAD_CONST               -2
             2120  BUILD_SLICE_2         2 
             2122  BINARY_SUBSCR    
             2124  LOAD_FAST                'self'
             2126  LOAD_ATTR                _words
             2128  LOAD_FAST                'i'
             2130  BINARY_SUBSCR    
             2132  LOAD_STR                 'word'
             2134  STORE_SUBSCR     
             2136  JUMP_BACK            22  'to 22'
           2138_0  COME_FROM          2110  '2110'

 L. 563      2138  LOAD_FAST                'word'
             2140  LOAD_METHOD              endswith
             2142  LOAD_STR                 'iful'
             2144  CALL_METHOD_1         1  '1 positional argument'
         2146_2148  POP_JUMP_IF_FALSE  2178  'to 2178'

 L. 564      2150  LOAD_FAST                'word'
             2152  LOAD_CONST               0
             2154  LOAD_CONST               -4
             2156  BUILD_SLICE_2         2 
             2158  BINARY_SUBSCR    
             2160  LOAD_STR                 'y'
             2162  BINARY_ADD       
             2164  LOAD_FAST                'self'
             2166  LOAD_ATTR                _words
             2168  LOAD_FAST                'i'
             2170  BINARY_SUBSCR    
             2172  LOAD_STR                 'word'
             2174  STORE_SUBSCR     
             2176  JUMP_BACK            22  'to 22'
           2178_0  COME_FROM          2146  '2146'

 L. 565      2178  LOAD_FAST                'word'
             2180  LOAD_METHOD              endswith
             2182  LOAD_STR                 'ful'
             2184  CALL_METHOD_1         1  '1 positional argument'
         2186_2188  POP_JUMP_IF_FALSE  2214  'to 2214'

 L. 566      2190  LOAD_FAST                'word'
             2192  LOAD_CONST               0
             2194  LOAD_CONST               -3
             2196  BUILD_SLICE_2         2 
             2198  BINARY_SUBSCR    
             2200  LOAD_FAST                'self'
             2202  LOAD_ATTR                _words
             2204  LOAD_FAST                'i'
             2206  BINARY_SUBSCR    
             2208  LOAD_STR                 'word'
             2210  STORE_SUBSCR     
             2212  JUMP_BACK            22  'to 22'
           2214_0  COME_FROM          2186  '2186'

 L. 567      2214  LOAD_FAST                'word'
             2216  LOAD_METHOD              endswith
             2218  LOAD_STR                 'iness'
             2220  CALL_METHOD_1         1  '1 positional argument'
         2222_2224  POP_JUMP_IF_FALSE  2254  'to 2254'

 L. 568      2226  LOAD_FAST                'word'
             2228  LOAD_CONST               0
             2230  LOAD_CONST               -5
             2232  BUILD_SLICE_2         2 
             2234  BINARY_SUBSCR    
             2236  LOAD_STR                 'y'
             2238  BINARY_ADD       
             2240  LOAD_FAST                'self'
             2242  LOAD_ATTR                _words
             2244  LOAD_FAST                'i'
             2246  BINARY_SUBSCR    
             2248  LOAD_STR                 'word'
             2250  STORE_SUBSCR     
             2252  JUMP_BACK            22  'to 22'
           2254_0  COME_FROM          2222  '2222'

 L. 569      2254  LOAD_FAST                'word'
             2256  LOAD_METHOD              endswith
             2258  LOAD_STR                 'ness'
             2260  CALL_METHOD_1         1  '1 positional argument'
         2262_2264  POP_JUMP_IF_FALSE  2290  'to 2290'

 L. 570      2266  LOAD_FAST                'word'
             2268  LOAD_CONST               0
             2270  LOAD_CONST               -4
             2272  BUILD_SLICE_2         2 
             2274  BINARY_SUBSCR    
             2276  LOAD_FAST                'self'
             2278  LOAD_ATTR                _words
             2280  LOAD_FAST                'i'
             2282  BINARY_SUBSCR    
             2284  LOAD_STR                 'word'
             2286  STORE_SUBSCR     
             2288  JUMP_BACK            22  'to 22'
           2290_0  COME_FROM          2262  '2262'

 L. 571      2290  LOAD_FAST                'word'
             2292  LOAD_METHOD              endswith
             2294  LOAD_STR                 'able'
             2296  CALL_METHOD_1         1  '1 positional argument'
             2298  POP_JUMP_IF_FALSE    22  'to 22'

 L. 572      2300  LOAD_FAST                'word'
             2302  LOAD_CONST               0
             2304  LOAD_CONST               -4
             2306  BUILD_SLICE_2         2 
             2308  BINARY_SUBSCR    
             2310  LOAD_FAST                'self'
             2312  LOAD_ATTR                _words
             2314  LOAD_FAST                'i'
             2316  BINARY_SUBSCR    
             2318  LOAD_STR                 'word'
             2320  STORE_SUBSCR     
             2322  JUMP_BACK            22  'to 22'
             2324  POP_BLOCK        
           2326_0  COME_FROM_LOOP       10  '10'

Parse error at or near `JUMP_FORWARD' instruction at offset 406

    def _nltkStemmer(self, name):
        """ NLTK Stemmer """
        if name == 'porter':
            stemmer = PorterStemmer()
        else:
            if name == 'snowball':
                stemmer = SnowballStemmer('english')
            else:
                if name == 'lancaster':
                    stemmer = LancasterStemmer()
                else:
                    return
        length = len(self._words)
        for i in range(length):
            word = self._words[i]['word']
            l = len(word)
            if not l < 4:
                if self._words[i]['tag'] != Vocabulary.UNTAG:
                    continue
                self._words[i]['word'] = stemmer.stem(self._words[i]['word'])

    def _lemma(self):
        """ NLTK Lemmatizer """
        lemma = WordNetLemmatizer()
        length = len(self._words)
        for i in range(length):
            self._words[i]['word'] = lemma.lemmatize(self._words[i]['word'])

    def _stopwords--- This code section failed: ---

 L. 606         0  BUILD_LIST_0          0 
                2  STORE_FAST               'words'

 L. 607         4  LOAD_GLOBAL              len
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _words
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  STORE_FAST               'nwords'

 L. 608        14  LOAD_CONST               0
               16  STORE_FAST               'skip'

 L. 609        18  LOAD_CONST               False
               20  STORE_FAST               'measurement'

 L. 610     22_24  SETUP_LOOP         2756  'to 2756'
               26  LOAD_GLOBAL              range
               28  LOAD_FAST                'nwords'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  GET_ITER         
             34_0  COME_FROM          2732  '2732'
             34_1  COME_FROM          1070  '1070'
             34_2  COME_FROM           902  '902'
             34_3  COME_FROM           726  '726'
             34_4  COME_FROM           652  '652'
             34_5  COME_FROM           440  '440'
             34_6  COME_FROM           376  '376'
             34_7  COME_FROM           314  '314'
            34_36  FOR_ITER           2754  'to 2754'
               38  STORE_FAST               'i'

 L. 612        40  LOAD_FAST                'skip'
               42  LOAD_CONST               0
               44  COMPARE_OP               >
               46  POP_JUMP_IF_FALSE    58  'to 58'

 L. 613        48  LOAD_FAST                'skip'
               50  LOAD_CONST               1
               52  INPLACE_SUBTRACT 
               54  STORE_FAST               'skip'

 L. 614        56  CONTINUE             34  'to 34'
             58_0  COME_FROM            46  '46'

 L. 617        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _words
               62  LOAD_FAST                'i'
               64  BINARY_SUBSCR    
               66  LOAD_STR                 'tag'
               68  BINARY_SUBSCR    
               70  LOAD_GLOBAL              Vocabulary
               72  LOAD_ATTR                NAME
               74  LOAD_GLOBAL              Vocabulary
               76  LOAD_ATTR                TITLE
               78  BUILD_LIST_2          2 
               80  COMPARE_OP               in
               82  POP_JUMP_IF_FALSE    96  'to 96'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _name
               88  LOAD_CONST               False
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE    96  'to 96'

 L. 618        94  CONTINUE             34  'to 34'
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            82  '82'

 L. 620        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _words
              100  LOAD_FAST                'i'
              102  BINARY_SUBSCR    
              104  LOAD_STR                 'word'
              106  BINARY_SUBSCR    
              108  STORE_FAST               'word'

 L. 622       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _words
              114  LOAD_FAST                'i'
              116  BINARY_SUBSCR    
              118  LOAD_STR                 'tag'
              120  BINARY_SUBSCR    
              122  LOAD_GLOBAL              Vocabulary
              124  LOAD_ATTR                PUNCT
              126  LOAD_GLOBAL              Vocabulary
              128  LOAD_ATTR                SYMBOL
              130  BUILD_LIST_2          2 
              132  COMPARE_OP               not-in
          134_136  POP_JUMP_IF_FALSE  2724  'to 2724'

 L. 624       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _isDate
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _words
              146  LOAD_FAST                'i'
              148  CALL_METHOD_2         2  '2 positional arguments'
              150  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST               'w'
              154  STORE_FAST               'n'

 L. 625       156  LOAD_FAST                'w'
              158  LOAD_CONST               None
              160  COMPARE_OP               is-not
          162_164  POP_JUMP_IF_FALSE   336  'to 336'

 L. 626       166  LOAD_FAST                'n'
              168  STORE_FAST               'skip'

 L. 627       170  LOAD_GLOBAL              len
              172  LOAD_FAST                'words'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  LOAD_CONST               0
              178  COMPARE_OP               >
              180  POP_JUMP_IF_FALSE   226  'to 226'
              182  LOAD_FAST                'words'
              184  LOAD_CONST               -1
              186  BINARY_SUBSCR    
              188  LOAD_STR                 'word'
              190  BINARY_SUBSCR    
              192  LOAD_CONST               ('birth', 'birthdate', 'birthday', 'DOB', 'dob')
              194  COMPARE_OP               in
              196  POP_JUMP_IF_FALSE   226  'to 226'

 L. 628       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _dob
              202  LOAD_CONST               True
              204  COMPARE_OP               is
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L. 629       208  LOAD_FAST                'w'
              210  LOAD_GLOBAL              Vocabulary
              212  LOAD_ATTR                DOB
              214  LOAD_CONST               ('word', 'tag')
              216  BUILD_CONST_KEY_MAP_2     2 
              218  LOAD_FAST                'words'
              220  LOAD_CONST               -1
              222  STORE_SUBSCR     
            224_0  COME_FROM           206  '206'
              224  JUMP_BACK            34  'to 34'
            226_0  COME_FROM           196  '196'
            226_1  COME_FROM           180  '180'

 L. 630       226  LOAD_GLOBAL              len
              228  LOAD_FAST                'words'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  LOAD_CONST               1
              234  COMPARE_OP               >
          236_238  POP_JUMP_IF_FALSE   306  'to 306'
              240  LOAD_FAST                'words'
              242  LOAD_CONST               -1
              244  BINARY_SUBSCR    
              246  LOAD_STR                 'word'
              248  BINARY_SUBSCR    
              250  LOAD_STR                 'date'
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   306  'to 306'
              258  LOAD_FAST                'words'
              260  LOAD_CONST               -2
              262  BINARY_SUBSCR    
              264  LOAD_STR                 'word'
              266  BINARY_SUBSCR    
              268  LOAD_STR                 'birth'
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   306  'to 306'

 L. 631       276  LOAD_FAST                'self'
              278  LOAD_ATTR                _dob
              280  LOAD_CONST               True
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_FALSE   334  'to 334'

 L. 632       288  LOAD_FAST                'w'
              290  LOAD_GLOBAL              Vocabulary
              292  LOAD_ATTR                DOB
              294  LOAD_CONST               ('word', 'tag')
              296  BUILD_CONST_KEY_MAP_2     2 
              298  LOAD_FAST                'words'
              300  LOAD_CONST               -1
              302  STORE_SUBSCR     
              304  JUMP_BACK            34  'to 34'
            306_0  COME_FROM           272  '272'
            306_1  COME_FROM           254  '254'
            306_2  COME_FROM           236  '236'

 L. 633       306  LOAD_FAST                'self'
              308  LOAD_ATTR                _date
              310  LOAD_CONST               True
              312  COMPARE_OP               is
              314  POP_JUMP_IF_FALSE    34  'to 34'

 L. 634       316  LOAD_FAST                'words'
              318  LOAD_METHOD              append
              320  LOAD_FAST                'w'
              322  LOAD_GLOBAL              Vocabulary
              324  LOAD_ATTR                DATE
              326  LOAD_CONST               ('word', 'tag')
              328  BUILD_CONST_KEY_MAP_2     2 
              330  CALL_METHOD_1         1  '1 positional argument'
              332  POP_TOP          
            334_0  COME_FROM           284  '284'

 L. 635       334  CONTINUE             34  'to 34'
            336_0  COME_FROM           162  '162'

 L. 638       336  LOAD_FAST                'self'
              338  LOAD_METHOD              _isSSN
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                _words
              344  LOAD_FAST                'i'
              346  CALL_METHOD_2         2  '2 positional arguments'
              348  UNPACK_SEQUENCE_2     2 
              350  STORE_FAST               'w'
              352  STORE_FAST               'n'

 L. 639       354  LOAD_FAST                'w'
              356  LOAD_CONST               None
              358  COMPARE_OP               is-not
          360_362  POP_JUMP_IF_FALSE   398  'to 398'

 L. 640       364  LOAD_FAST                'n'
              366  STORE_FAST               'skip'

 L. 641       368  LOAD_FAST                'self'
              370  LOAD_ATTR                _ssn
              372  LOAD_CONST               True
              374  COMPARE_OP               is
              376  POP_JUMP_IF_FALSE    34  'to 34'

 L. 642       378  LOAD_FAST                'words'
              380  LOAD_METHOD              append
              382  LOAD_FAST                'w'
              384  LOAD_GLOBAL              Vocabulary
              386  LOAD_ATTR                SSN
              388  LOAD_CONST               ('word', 'tag')
              390  BUILD_CONST_KEY_MAP_2     2 
              392  CALL_METHOD_1         1  '1 positional argument'
              394  POP_TOP          

 L. 643       396  CONTINUE             34  'to 34'
            398_0  COME_FROM           360  '360'

 L. 646       398  LOAD_FAST                'self'
              400  LOAD_METHOD              _isTele
              402  LOAD_FAST                'self'
              404  LOAD_ATTR                _words
              406  LOAD_FAST                'i'
              408  CALL_METHOD_2         2  '2 positional arguments'
              410  UNPACK_SEQUENCE_3     3 
              412  STORE_FAST               'w'
              414  STORE_FAST               'n'
              416  STORE_FAST               'tag'

 L. 647       418  LOAD_FAST                'w'
              420  LOAD_CONST               None
              422  COMPARE_OP               is-not
          424_426  POP_JUMP_IF_FALSE   460  'to 460'

 L. 648       428  LOAD_FAST                'n'
              430  STORE_FAST               'skip'

 L. 649       432  LOAD_FAST                'self'
              434  LOAD_ATTR                _telephone
              436  LOAD_CONST               True
              438  COMPARE_OP               is
              440  POP_JUMP_IF_FALSE    34  'to 34'

 L. 650       442  LOAD_FAST                'words'
              444  LOAD_METHOD              append
              446  LOAD_FAST                'w'
              448  LOAD_FAST                'tag'
              450  LOAD_CONST               ('word', 'tag')
              452  BUILD_CONST_KEY_MAP_2     2 
              454  CALL_METHOD_1         1  '1 positional argument'
              456  POP_TOP          

 L. 651       458  CONTINUE             34  'to 34'
            460_0  COME_FROM           424  '424'

 L. 654       460  LOAD_FAST                'self'
              462  LOAD_METHOD              _isAddr
              464  LOAD_FAST                'self'
              466  LOAD_ATTR                _words
              468  LOAD_FAST                'i'
              470  CALL_METHOD_2         2  '2 positional arguments'
              472  STORE_FAST               'n'

 L. 655       474  LOAD_FAST                'n'
              476  LOAD_CONST               0
              478  COMPARE_OP               >
          480_482  POP_JUMP_IF_FALSE   612  'to 612'

 L. 656       484  LOAD_FAST                'n'
              486  STORE_FAST               'skip'

 L. 657       488  LOAD_FAST                'self'
              490  LOAD_ATTR                _address
              492  LOAD_CONST               True
              494  COMPARE_OP               is
          496_498  POP_JUMP_IF_FALSE   602  'to 602'

 L. 658       500  SETUP_LOOP          602  'to 602'
              502  LOAD_GLOBAL              range
              504  LOAD_FAST                'i'
              506  LOAD_FAST                'i'
              508  LOAD_FAST                'skip'
              510  BINARY_ADD       
              512  CALL_FUNCTION_2       2  '2 positional arguments'
              514  GET_ITER         
            516_0  COME_FROM           576  '576'
              516  FOR_ITER            600  'to 600'
              518  STORE_FAST               '_x'

 L. 659       520  LOAD_FAST                'self'
              522  LOAD_ATTR                _words
              524  LOAD_FAST                '_x'
              526  BINARY_SUBSCR    
              528  LOAD_STR                 'tag'
              530  BINARY_SUBSCR    
              532  LOAD_GLOBAL              Vocabulary
              534  LOAD_ATTR                STREET_NUM
              536  LOAD_GLOBAL              Vocabulary
              538  LOAD_ATTR                STREET_DIR

 L. 660       540  LOAD_GLOBAL              Vocabulary
              542  LOAD_ATTR                STREET_NAME
              544  LOAD_GLOBAL              Vocabulary
              546  LOAD_ATTR                STREET_TYPE

 L. 661       548  LOAD_GLOBAL              Vocabulary
              550  LOAD_ATTR                POB
              552  LOAD_GLOBAL              Vocabulary
              554  LOAD_ATTR                SAC

 L. 662       556  LOAD_GLOBAL              Vocabulary
              558  LOAD_ATTR                CITY
              560  LOAD_GLOBAL              Vocabulary
              562  LOAD_ATTR                STATE
              564  LOAD_GLOBAL              Vocabulary
              566  LOAD_ATTR                POSTAL

 L. 663       568  LOAD_GLOBAL              Vocabulary
              570  LOAD_ATTR                STATION
              572  BUILD_LIST_10        10 
              574  COMPARE_OP               in
          576_578  POP_JUMP_IF_FALSE   516  'to 516'

 L. 664       580  LOAD_FAST                'words'
              582  LOAD_METHOD              append
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                _words
              588  LOAD_FAST                '_x'
              590  BINARY_SUBSCR    
              592  CALL_METHOD_1         1  '1 positional argument'
              594  POP_TOP          
          596_598  JUMP_BACK           516  'to 516'
              600  POP_BLOCK        
            602_0  COME_FROM_LOOP      500  '500'
            602_1  COME_FROM           496  '496'

 L. 665       602  LOAD_FAST                'skip'
              604  LOAD_CONST               1
              606  INPLACE_SUBTRACT 
              608  STORE_FAST               'skip'

 L. 666       610  CONTINUE             34  'to 34'
            612_0  COME_FROM           480  '480'

 L. 669       612  LOAD_FAST                'self'
              614  LOAD_METHOD              _isAge
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                _words
              620  LOAD_FAST                'i'
              622  CALL_METHOD_2         2  '2 positional arguments'
              624  UNPACK_SEQUENCE_2     2 
              626  STORE_FAST               'w'
              628  STORE_FAST               'n'

 L. 670       630  LOAD_FAST                'w'
              632  LOAD_CONST               None
              634  COMPARE_OP               is-not
          636_638  POP_JUMP_IF_FALSE   674  'to 674'

 L. 671       640  LOAD_FAST                'n'
              642  STORE_FAST               'skip'

 L. 672       644  LOAD_FAST                'self'
              646  LOAD_ATTR                _age
              648  LOAD_CONST               True
              650  COMPARE_OP               is
              652  POP_JUMP_IF_FALSE    34  'to 34'

 L. 673       654  LOAD_FAST                'words'
              656  LOAD_METHOD              append
              658  LOAD_FAST                'w'
              660  LOAD_GLOBAL              Vocabulary
              662  LOAD_ATTR                AGE
              664  LOAD_CONST               ('word', 'tag')
              666  BUILD_CONST_KEY_MAP_2     2 
              668  CALL_METHOD_1         1  '1 positional argument'
              670  POP_TOP          

 L. 674       672  CONTINUE             34  'to 34'
            674_0  COME_FROM           636  '636'

 L. 677       674  LOAD_FAST                'self'
              676  LOAD_METHOD              _isNumber
              678  LOAD_FAST                'self'
              680  LOAD_ATTR                _words
              682  LOAD_FAST                'i'
              684  CALL_METHOD_2         2  '2 positional arguments'
              686  UNPACK_SEQUENCE_2     2 
              688  STORE_FAST               'w'
              690  STORE_FAST               'n'

 L. 678       692  LOAD_FAST                'w'
              694  LOAD_CONST               None
              696  COMPARE_OP               is-not
          698_700  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 679       702  LOAD_FAST                'n'
              704  STORE_FAST               'skip'

 L. 680       706  LOAD_FAST                'self'
              708  LOAD_ATTR                _number
              710  LOAD_CONST               True
              712  COMPARE_OP               is
          714_716  POP_JUMP_IF_TRUE    728  'to 728'
              718  LOAD_FAST                'self'
              720  LOAD_ATTR                _unit
              722  LOAD_CONST               True
              724  COMPARE_OP               is
              726  POP_JUMP_IF_FALSE    34  'to 34'
            728_0  COME_FROM           714  '714'

 L. 681       728  SETUP_EXCEPT        832  'to 832'

 L. 682       730  LOAD_GLOBAL              vocab
              732  LOAD_FAST                'word'
              734  BINARY_SUBSCR    
              736  LOAD_STR                 'tag'
              738  BINARY_SUBSCR    
              740  STORE_FAST               'tag'

 L. 684       742  LOAD_GLOBAL              Vocabulary
              744  LOAD_ATTR                UNIT
              746  LOAD_FAST                'tag'
              748  COMPARE_OP               in
          750_752  POP_JUMP_IF_FALSE   828  'to 828'
              754  LOAD_FAST                'words'
              756  BUILD_LIST_0          0 
              758  COMPARE_OP               !=
          760_762  POP_JUMP_IF_FALSE   828  'to 828'

 L. 685       764  LOAD_FAST                'words'
              766  LOAD_CONST               -1
              768  BINARY_SUBSCR    
              770  LOAD_STR                 'tag'
              772  BINARY_SUBSCR    
              774  LOAD_GLOBAL              Vocabulary
              776  LOAD_ATTR                NUMBER
              778  COMPARE_OP               ==
          780_782  POP_JUMP_IF_FALSE   828  'to 828'

 L. 686       784  LOAD_FAST                'tag'
              786  LOAD_METHOD              index
              788  LOAD_GLOBAL              Vocabulary
              790  LOAD_ATTR                UNIT
              792  CALL_METHOD_1         1  '1 positional argument'
              794  STORE_FAST               'itag'

 L. 687       796  LOAD_FAST                'words'
              798  LOAD_METHOD              append
              800  LOAD_GLOBAL              vocab
              802  LOAD_FAST                'word'
              804  BINARY_SUBSCR    
              806  LOAD_STR                 'lemma'
              808  BINARY_SUBSCR    
              810  LOAD_FAST                'itag'
              812  BINARY_SUBSCR    
              814  LOAD_GLOBAL              Vocabulary
              816  LOAD_ATTR                UNIT
              818  LOAD_CONST               ('word', 'tag')
              820  BUILD_CONST_KEY_MAP_2     2 
              822  CALL_METHOD_1         1  '1 positional argument'
              824  POP_TOP          

 L. 688       826  CONTINUE_LOOP        34  'to 34'
            828_0  COME_FROM           780  '780'
            828_1  COME_FROM           760  '760'
            828_2  COME_FROM           750  '750'
              828  POP_BLOCK        
              830  JUMP_FORWARD        844  'to 844'
            832_0  COME_FROM_EXCEPT    728  '728'

 L. 689       832  POP_TOP          
              834  POP_TOP          
              836  POP_TOP          

 L. 689       838  POP_EXCEPT       
              840  JUMP_FORWARD        844  'to 844'
              842  END_FINALLY      
            844_0  COME_FROM           840  '840'
            844_1  COME_FROM           830  '830'

 L. 691       844  LOAD_FAST                'w'
              846  LOAD_METHOD              replace
              848  LOAD_FAST                'self'
              850  LOAD_ATTR                THOUSANDS
              852  LOAD_STR                 ''
              854  CALL_METHOD_2         2  '2 positional arguments'
              856  STORE_FAST               'word'

 L. 693       858  LOAD_FAST                'self'
              860  LOAD_ATTR                DECIMAL
              862  LOAD_STR                 ','
              864  COMPARE_OP               ==
          866_868  POP_JUMP_IF_FALSE   882  'to 882'

 L. 694       870  LOAD_FAST                'word'
              872  LOAD_METHOD              replace
              874  LOAD_STR                 ','
              876  LOAD_STR                 '.'
              878  CALL_METHOD_2         2  '2 positional arguments'
              880  STORE_FAST               'word'
            882_0  COME_FROM           866  '866'

 L. 695       882  LOAD_FAST                'words'
              884  LOAD_METHOD              append
              886  LOAD_FAST                'word'
              888  LOAD_GLOBAL              Vocabulary
              890  LOAD_ATTR                NUMBER
              892  LOAD_CONST               ('word', 'tag')
              894  BUILD_CONST_KEY_MAP_2     2 
              896  CALL_METHOD_1         1  '1 positional argument'
              898  POP_TOP          

 L. 697       900  LOAD_FAST                'measurement'
              902  POP_JUMP_IF_FALSE    34  'to 34'

 L. 698       904  LOAD_FAST                'i'
              906  LOAD_CONST               1
              908  BINARY_ADD       
              910  LOAD_FAST                'nwords'
              912  COMPARE_OP               <
          914_916  POP_JUMP_IF_FALSE  1022  'to 1022'

 L. 699       918  LOAD_FAST                'self'
              920  LOAD_ATTR                _words
              922  LOAD_FAST                'i'
              924  LOAD_CONST               1
              926  BINARY_ADD       
              928  BINARY_SUBSCR    
              930  LOAD_STR                 'word'
              932  BINARY_SUBSCR    
              934  LOAD_STR                 "'"
              936  COMPARE_OP               ==
          938_940  POP_JUMP_IF_FALSE   970  'to 970'

 L. 700       942  LOAD_FAST                'words'
              944  LOAD_METHOD              append
              946  LOAD_STR                 'foot'
              948  LOAD_GLOBAL              Vocabulary
              950  LOAD_ATTR                UNIT
              952  LOAD_CONST               ('word', 'tag')
              954  BUILD_CONST_KEY_MAP_2     2 
              956  CALL_METHOD_1         1  '1 positional argument'
              958  POP_TOP          

 L. 701       960  LOAD_FAST                'i'
              962  LOAD_CONST               1
              964  INPLACE_ADD      
              966  STORE_FAST               'i'

 L. 702       968  CONTINUE             34  'to 34'
            970_0  COME_FROM           938  '938'

 L. 703       970  LOAD_FAST                'self'
              972  LOAD_ATTR                _words
              974  LOAD_FAST                'i'
              976  LOAD_CONST               1
              978  BINARY_ADD       
              980  BINARY_SUBSCR    
              982  LOAD_STR                 'word'
              984  BINARY_SUBSCR    
              986  LOAD_STR                 '"'
              988  COMPARE_OP               ==
          990_992  POP_JUMP_IF_FALSE  1022  'to 1022'

 L. 704       994  LOAD_FAST                'words'
              996  LOAD_METHOD              append
              998  LOAD_STR                 'inch'
             1000  LOAD_GLOBAL              Vocabulary
             1002  LOAD_ATTR                UNIT
             1004  LOAD_CONST               ('word', 'tag')
             1006  BUILD_CONST_KEY_MAP_2     2 
             1008  CALL_METHOD_1         1  '1 positional argument'
             1010  POP_TOP          

 L. 705      1012  LOAD_FAST                'i'
             1014  LOAD_CONST               1
             1016  INPLACE_ADD      
             1018  STORE_FAST               'i'

 L. 706      1020  CONTINUE             34  'to 34'
           1022_0  COME_FROM           990  '990'
           1022_1  COME_FROM           914  '914'

 L. 707      1022  LOAD_CONST               False
             1024  STORE_FAST               'measurement'

 L. 708      1026  CONTINUE             34  'to 34'
           1028_0  COME_FROM           698  '698'

 L. 711      1028  LOAD_FAST                'self'
             1030  LOAD_METHOD              _isGender
             1032  LOAD_FAST                'self'
             1034  LOAD_ATTR                _words
             1036  LOAD_FAST                'i'
             1038  CALL_METHOD_2         2  '2 positional arguments'
             1040  UNPACK_SEQUENCE_3     3 
             1042  STORE_FAST               'w'
             1044  STORE_FAST               'n'
             1046  STORE_FAST               't'

 L. 712      1048  LOAD_FAST                'w'
             1050  LOAD_CONST               None
             1052  COMPARE_OP               is-not
         1054_1056  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 713      1058  LOAD_FAST                'n'
             1060  STORE_FAST               'skip'

 L. 714      1062  LOAD_FAST                'self'
             1064  LOAD_ATTR                _gender
             1066  LOAD_CONST               True
             1068  COMPARE_OP               is
             1070  POP_JUMP_IF_FALSE    34  'to 34'

 L. 715      1072  LOAD_FAST                'words'
             1074  LOAD_METHOD              append
             1076  LOAD_FAST                'w'
             1078  LOAD_FAST                't'
             1080  LOAD_CONST               ('word', 'tag')
             1082  BUILD_CONST_KEY_MAP_2     2 
             1084  CALL_METHOD_1         1  '1 positional argument'
             1086  POP_TOP          

 L. 716      1088  CONTINUE             34  'to 34'
           1090_0  COME_FROM          1054  '1054'

 L. 718      1090  LOAD_FAST                'self'
             1092  LOAD_ATTR                _words
             1094  LOAD_FAST                'i'
             1096  BINARY_SUBSCR    
             1098  LOAD_STR                 'tag'
             1100  BINARY_SUBSCR    
             1102  LOAD_GLOBAL              Vocabulary
             1104  LOAD_ATTR                ACRONYM
             1106  LOAD_GLOBAL              Vocabulary
             1108  LOAD_ATTR                NAME
             1110  LOAD_GLOBAL              Vocabulary
             1112  LOAD_ATTR                TITLE
             1114  LOAD_GLOBAL              Vocabulary
             1116  LOAD_ATTR                ABBR
             1118  BUILD_LIST_4          4 
             1120  COMPARE_OP               in
         1122_1124  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 719      1126  LOAD_FAST                'words'
             1128  LOAD_METHOD              append
             1130  LOAD_FAST                'self'
             1132  LOAD_ATTR                _words
             1134  LOAD_FAST                'i'
             1136  BINARY_SUBSCR    
             1138  CALL_METHOD_1         1  '1 positional argument'
             1140  POP_TOP          

 L. 720      1142  CONTINUE             34  'to 34'
           1144_0  COME_FROM          1122  '1122'

 L. 722      1144  LOAD_GLOBAL              Vocabulary
             1146  LOAD_ATTR                UNTAG
             1148  BUILD_LIST_1          1 
             1150  STORE_FAST               'tag'

 L. 723  1152_1154  SETUP_EXCEPT       2690  'to 2690'

 L. 724      1156  LOAD_GLOBAL              vocab
             1158  LOAD_FAST                'word'
             1160  BINARY_SUBSCR    
             1162  LOAD_STR                 'tag'
             1164  BINARY_SUBSCR    
             1166  STORE_FAST               'tag'

 L. 727      1168  LOAD_GLOBAL              Vocabulary
             1170  LOAD_ATTR                UNIT
             1172  LOAD_FAST                'tag'
             1174  COMPARE_OP               in
         1176_1178  POP_JUMP_IF_FALSE  1482  'to 1482'
             1180  LOAD_FAST                'words'
             1182  BUILD_LIST_0          0 
             1184  COMPARE_OP               !=
         1186_1188  POP_JUMP_IF_FALSE  1482  'to 1482'

 L. 728      1190  LOAD_FAST                'i'
             1192  LOAD_CONST               2
             1194  BINARY_ADD       
             1196  LOAD_FAST                'nwords'
             1198  COMPARE_OP               <
         1200_1202  POP_JUMP_IF_FALSE  1278  'to 1278'

 L. 730      1204  LOAD_FAST                'self'
             1206  LOAD_ATTR                _words
             1208  LOAD_FAST                'i'
             1210  LOAD_CONST               1
             1212  BINARY_ADD       
             1214  BINARY_SUBSCR    
             1216  LOAD_STR                 'word'
             1218  BINARY_SUBSCR    
             1220  LOAD_STR                 '/'
             1222  COMPARE_OP               ==
         1224_1226  POP_JUMP_IF_FALSE  1278  'to 1278'
             1228  LOAD_FAST                'self'
             1230  LOAD_ATTR                _words
             1232  LOAD_FAST                'i'
             1234  LOAD_CONST               2
             1236  BINARY_ADD       
             1238  BINARY_SUBSCR    
             1240  LOAD_STR                 'word'
             1242  BINARY_SUBSCR    
             1244  LOAD_CONST               ('h', 's')
             1246  COMPARE_OP               in
         1248_1250  POP_JUMP_IF_FALSE  1278  'to 1278'

 L. 731      1252  LOAD_FAST                'word'
             1254  LOAD_FAST                'self'
             1256  LOAD_ATTR                _words
             1258  LOAD_FAST                'i'
             1260  LOAD_CONST               2
             1262  BINARY_ADD       
             1264  BINARY_SUBSCR    
             1266  LOAD_STR                 'word'
             1268  BINARY_SUBSCR    
             1270  INPLACE_ADD      
             1272  STORE_FAST               'word'

 L. 732      1274  LOAD_CONST               2
             1276  STORE_FAST               'skip'
           1278_0  COME_FROM          1248  '1248'
           1278_1  COME_FROM          1224  '1224'
           1278_2  COME_FROM          1200  '1200'

 L. 733      1278  LOAD_FAST                'words'
             1280  LOAD_CONST               -1
             1282  BINARY_SUBSCR    
             1284  LOAD_STR                 'tag'
             1286  BINARY_SUBSCR    
             1288  LOAD_GLOBAL              Vocabulary
             1290  LOAD_ATTR                NUMBER
             1292  COMPARE_OP               ==
         1294_1296  POP_JUMP_IF_FALSE  1344  'to 1344'

 L. 734      1298  LOAD_FAST                'tag'
             1300  LOAD_METHOD              index
             1302  LOAD_GLOBAL              Vocabulary
             1304  LOAD_ATTR                UNIT
             1306  CALL_METHOD_1         1  '1 positional argument'
             1308  STORE_FAST               'itag'

 L. 735      1310  LOAD_FAST                'words'
             1312  LOAD_METHOD              append
             1314  LOAD_GLOBAL              vocab
             1316  LOAD_FAST                'word'
             1318  BINARY_SUBSCR    
             1320  LOAD_STR                 'lemma'
             1322  BINARY_SUBSCR    
             1324  LOAD_FAST                'itag'
             1326  BINARY_SUBSCR    
             1328  LOAD_GLOBAL              Vocabulary
             1330  LOAD_ATTR                UNIT
             1332  LOAD_CONST               ('word', 'tag')
             1334  BUILD_CONST_KEY_MAP_2     2 
             1336  CALL_METHOD_1         1  '1 positional argument'
             1338  POP_TOP          

 L. 736      1340  CONTINUE_LOOP        34  'to 34'
             1342  JUMP_FORWARD       1482  'to 1482'
           1344_0  COME_FROM          1294  '1294'

 L. 738      1344  LOAD_FAST                'words'
             1346  LOAD_CONST               -1
             1348  BINARY_SUBSCR    
             1350  LOAD_STR                 'tag'
             1352  BINARY_SUBSCR    
             1354  LOAD_GLOBAL              Vocabulary
             1356  LOAD_ATTR                UNIT
             1358  COMPARE_OP               ==
         1360_1362  POP_JUMP_IF_FALSE  1426  'to 1426'
             1364  LOAD_FAST                'words'
             1366  LOAD_CONST               -1
             1368  BINARY_SUBSCR    
             1370  LOAD_STR                 'word'
             1372  BINARY_SUBSCR    
             1374  LOAD_STR                 'square'
             1376  COMPARE_OP               ==
         1378_1380  POP_JUMP_IF_FALSE  1426  'to 1426'

 L. 739      1382  LOAD_FAST                'tag'
             1384  LOAD_METHOD              index
             1386  LOAD_GLOBAL              Vocabulary
             1388  LOAD_ATTR                UNIT
             1390  CALL_METHOD_1         1  '1 positional argument'
             1392  STORE_FAST               'itag'

 L. 740      1394  LOAD_STR                 'square '
             1396  LOAD_GLOBAL              vocab
             1398  LOAD_FAST                'word'
             1400  BINARY_SUBSCR    
             1402  LOAD_STR                 'lemma'
             1404  BINARY_SUBSCR    
             1406  LOAD_FAST                'itag'
             1408  BINARY_SUBSCR    
             1410  BINARY_ADD       
             1412  LOAD_FAST                'words'
             1414  LOAD_CONST               -1
             1416  BINARY_SUBSCR    
             1418  LOAD_STR                 'word'
             1420  STORE_SUBSCR     

 L. 741      1422  CONTINUE_LOOP        34  'to 34'
             1424  JUMP_FORWARD       1482  'to 1482'
           1426_0  COME_FROM          1378  '1378'
           1426_1  COME_FROM          1360  '1360'

 L. 743      1426  LOAD_GLOBAL              Vocabulary
             1428  LOAD_ATTR                ABBR
             1430  LOAD_FAST                'tag'
             1432  COMPARE_OP               in
         1434_1436  POP_JUMP_IF_FALSE  1482  'to 1482'

 L. 744      1438  LOAD_FAST                'tag'
             1440  LOAD_METHOD              index
             1442  LOAD_GLOBAL              Vocabulary
             1444  LOAD_ATTR                ABBR
             1446  CALL_METHOD_1         1  '1 positional argument'
             1448  STORE_FAST               'itag'

 L. 745      1450  LOAD_FAST                'words'
             1452  LOAD_METHOD              append
             1454  LOAD_GLOBAL              vocab
             1456  LOAD_FAST                'word'
             1458  BINARY_SUBSCR    
             1460  LOAD_STR                 'lemma'
             1462  BINARY_SUBSCR    
             1464  LOAD_FAST                'itag'
             1466  BINARY_SUBSCR    
             1468  LOAD_GLOBAL              Vocabulary
             1470  LOAD_ATTR                ABBR
             1472  LOAD_CONST               ('word', 'tag')
             1474  BUILD_CONST_KEY_MAP_2     2 
             1476  CALL_METHOD_1         1  '1 positional argument'
             1478  POP_TOP          

 L. 746      1480  CONTINUE_LOOP        34  'to 34'
           1482_0  COME_FROM          1434  '1434'
           1482_1  COME_FROM          1424  '1424'
           1482_2  COME_FROM          1342  '1342'
           1482_3  COME_FROM          1186  '1186'
           1482_4  COME_FROM          1176  '1176'

 L. 748      1482  LOAD_GLOBAL              Vocabulary
             1484  LOAD_ATTR                QUANTIFIER
             1486  LOAD_FAST                'tag'
             1488  COMPARE_OP               in
         1490_1492  POP_JUMP_IF_FALSE  1578  'to 1578'

 L. 749      1494  LOAD_FAST                'self'
             1496  LOAD_ATTR                _quantifier
             1498  LOAD_CONST               True
             1500  COMPARE_OP               ==
         1502_1504  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 750      1506  LOAD_GLOBAL              vocab
             1508  LOAD_FAST                'word'
             1510  BINARY_SUBSCR    
             1512  LOAD_STR                 'lemma'
             1514  BINARY_SUBSCR    
             1516  LOAD_CONST               None
             1518  COMPARE_OP               is-not
         1520_1522  POP_JUMP_IF_FALSE  1556  'to 1556'

 L. 751      1524  LOAD_FAST                'words'
             1526  LOAD_METHOD              append
             1528  LOAD_GLOBAL              vocab
             1530  LOAD_FAST                'word'
             1532  BINARY_SUBSCR    
             1534  LOAD_STR                 'lemma'
             1536  BINARY_SUBSCR    
             1538  LOAD_CONST               0
             1540  BINARY_SUBSCR    
             1542  LOAD_GLOBAL              Vocabulary
             1544  LOAD_ATTR                QUANTIFIER
             1546  LOAD_CONST               ('word', 'tag')
             1548  BUILD_CONST_KEY_MAP_2     2 
             1550  CALL_METHOD_1         1  '1 positional argument'
             1552  POP_TOP          
             1554  JUMP_FORWARD       2684  'to 2684'
           1556_0  COME_FROM          1520  '1520'

 L. 753      1556  LOAD_FAST                'words'
             1558  LOAD_METHOD              append
             1560  LOAD_FAST                'word'
             1562  LOAD_GLOBAL              Vocabulary
             1564  LOAD_ATTR                QUANTIFIER
             1566  LOAD_CONST               ('word', 'tag')
             1568  BUILD_CONST_KEY_MAP_2     2 
             1570  CALL_METHOD_1         1  '1 positional argument'
             1572  POP_TOP          
         1574_1576  JUMP_FORWARD       2684  'to 2684'
           1578_0  COME_FROM          1490  '1490'

 L. 754      1578  LOAD_GLOBAL              Vocabulary
             1580  LOAD_ATTR                CONJUNCTION
             1582  LOAD_FAST                'tag'
             1584  COMPARE_OP               in
         1586_1588  POP_JUMP_IF_FALSE  1624  'to 1624'

 L. 755      1590  LOAD_FAST                'self'
             1592  LOAD_ATTR                _conjunction
             1594  LOAD_CONST               True
             1596  COMPARE_OP               ==
         1598_1600  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 756      1602  LOAD_FAST                'words'
             1604  LOAD_METHOD              append
             1606  LOAD_FAST                'word'
             1608  LOAD_GLOBAL              Vocabulary
             1610  LOAD_ATTR                CONJUNCTION
             1612  LOAD_CONST               ('word', 'tag')
             1614  BUILD_CONST_KEY_MAP_2     2 
             1616  CALL_METHOD_1         1  '1 positional argument'
             1618  POP_TOP          
         1620_1622  JUMP_FORWARD       2684  'to 2684'
           1624_0  COME_FROM          1586  '1586'

 L. 757      1624  LOAD_GLOBAL              Vocabulary
             1626  LOAD_ATTR                ARTICLE
             1628  LOAD_FAST                'tag'
             1630  COMPARE_OP               in
         1632_1634  POP_JUMP_IF_FALSE  1670  'to 1670'

 L. 758      1636  LOAD_FAST                'self'
             1638  LOAD_ATTR                _article
             1640  LOAD_CONST               True
             1642  COMPARE_OP               ==
         1644_1646  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 759      1648  LOAD_FAST                'words'
             1650  LOAD_METHOD              append
             1652  LOAD_FAST                'word'
             1654  LOAD_GLOBAL              Vocabulary
             1656  LOAD_ATTR                ARTICLE
             1658  LOAD_CONST               ('word', 'tag')
             1660  BUILD_CONST_KEY_MAP_2     2 
             1662  CALL_METHOD_1         1  '1 positional argument'
             1664  POP_TOP          
         1666_1668  JUMP_FORWARD       2684  'to 2684'
           1670_0  COME_FROM          1632  '1632'

 L. 760      1670  LOAD_GLOBAL              Vocabulary
             1672  LOAD_ATTR                DEMONSTRATIVE
             1674  LOAD_FAST                'tag'
             1676  COMPARE_OP               in
         1678_1680  POP_JUMP_IF_FALSE  1716  'to 1716'

 L. 761      1682  LOAD_FAST                'self'
             1684  LOAD_ATTR                _demonstrative
             1686  LOAD_CONST               True
             1688  COMPARE_OP               ==
         1690_1692  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 762      1694  LOAD_FAST                'words'
             1696  LOAD_METHOD              append
             1698  LOAD_FAST                'word'
             1700  LOAD_GLOBAL              Vocabulary
             1702  LOAD_ATTR                DEMONSTRATIVE
             1704  LOAD_CONST               ('word', 'tag')
             1706  BUILD_CONST_KEY_MAP_2     2 
             1708  CALL_METHOD_1         1  '1 positional argument'
             1710  POP_TOP          
         1712_1714  JUMP_FORWARD       2684  'to 2684'
           1716_0  COME_FROM          1678  '1678'

 L. 763      1716  LOAD_GLOBAL              Vocabulary
             1718  LOAD_ATTR                PREPOSITION
             1720  LOAD_FAST                'tag'
             1722  COMPARE_OP               in
         1724_1726  POP_JUMP_IF_FALSE  1762  'to 1762'

 L. 764      1728  LOAD_FAST                'self'
             1730  LOAD_ATTR                _preposition
             1732  LOAD_CONST               True
             1734  COMPARE_OP               ==
         1736_1738  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 765      1740  LOAD_FAST                'words'
             1742  LOAD_METHOD              append
             1744  LOAD_FAST                'word'
             1746  LOAD_GLOBAL              Vocabulary
             1748  LOAD_ATTR                PREPOSITION
             1750  LOAD_CONST               ('word', 'tag')
             1752  BUILD_CONST_KEY_MAP_2     2 
             1754  CALL_METHOD_1         1  '1 positional argument'
             1756  POP_TOP          
         1758_1760  JUMP_FORWARD       2684  'to 2684'
           1762_0  COME_FROM          1724  '1724'

 L. 766      1762  LOAD_GLOBAL              Vocabulary
             1764  LOAD_ATTR                PRONOUN
             1766  LOAD_FAST                'tag'
             1768  COMPARE_OP               in
         1770_1772  POP_JUMP_IF_FALSE  1808  'to 1808'

 L. 767      1774  LOAD_FAST                'self'
             1776  LOAD_ATTR                _pronoun
             1778  LOAD_CONST               True
             1780  COMPARE_OP               ==
         1782_1784  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 768      1786  LOAD_FAST                'words'
             1788  LOAD_METHOD              append
             1790  LOAD_FAST                'word'
             1792  LOAD_GLOBAL              Vocabulary
             1794  LOAD_ATTR                PRONOUN
             1796  LOAD_CONST               ('word', 'tag')
             1798  BUILD_CONST_KEY_MAP_2     2 
             1800  CALL_METHOD_1         1  '1 positional argument'
             1802  POP_TOP          
         1804_1806  JUMP_FORWARD       2684  'to 2684'
           1808_0  COME_FROM          1770  '1770'

 L. 769      1808  LOAD_GLOBAL              Vocabulary
             1810  LOAD_ATTR                QUESTION
             1812  LOAD_FAST                'tag'
             1814  COMPARE_OP               in
         1816_1818  POP_JUMP_IF_FALSE  1854  'to 1854'

 L. 770      1820  LOAD_FAST                'self'
             1822  LOAD_ATTR                _question
             1824  LOAD_CONST               True
             1826  COMPARE_OP               ==
         1828_1830  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 771      1832  LOAD_FAST                'words'
             1834  LOAD_METHOD              append
             1836  LOAD_FAST                'word'
             1838  LOAD_GLOBAL              Vocabulary
             1840  LOAD_ATTR                QUESTION
             1842  LOAD_CONST               ('word', 'tag')
             1844  BUILD_CONST_KEY_MAP_2     2 
             1846  CALL_METHOD_1         1  '1 positional argument'
             1848  POP_TOP          
         1850_1852  JUMP_FORWARD       2684  'to 2684'
           1854_0  COME_FROM          1816  '1816'

 L. 772      1854  LOAD_GLOBAL              Vocabulary
             1856  LOAD_ATTR                NAME
             1858  LOAD_FAST                'tag'
             1860  COMPARE_OP               in
         1862_1864  POP_JUMP_IF_FALSE  1900  'to 1900'

 L. 773      1866  LOAD_FAST                'self'
             1868  LOAD_ATTR                _name
             1870  LOAD_CONST               True
             1872  COMPARE_OP               ==
         1874_1876  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 774      1878  LOAD_FAST                'words'
             1880  LOAD_METHOD              append
             1882  LOAD_FAST                'word'
             1884  LOAD_GLOBAL              Vocabulary
             1886  LOAD_ATTR                NAME
             1888  LOAD_CONST               ('word', 'tag')
             1890  BUILD_CONST_KEY_MAP_2     2 
             1892  CALL_METHOD_1         1  '1 positional argument'
             1894  POP_TOP          
         1896_1898  JUMP_FORWARD       2684  'to 2684'
           1900_0  COME_FROM          1862  '1862'

 L. 775      1900  LOAD_GLOBAL              Vocabulary
             1902  LOAD_ATTR                TITLE
             1904  LOAD_FAST                'tag'
             1906  COMPARE_OP               in
         1908_1910  POP_JUMP_IF_FALSE  2008  'to 2008'

 L. 776      1912  LOAD_FAST                'self'
             1914  LOAD_ATTR                _name
             1916  LOAD_CONST               True
             1918  COMPARE_OP               ==
         1920_1922  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 777      1924  LOAD_GLOBAL              vocab
             1926  LOAD_FAST                'word'
             1928  BINARY_SUBSCR    
             1930  LOAD_STR                 'lemma'
             1932  BINARY_SUBSCR    
             1934  LOAD_CONST               None
             1936  COMPARE_OP               is-not
         1938_1940  POP_JUMP_IF_FALSE  1986  'to 1986'

 L. 778      1942  LOAD_FAST                'tag'
             1944  LOAD_METHOD              index
             1946  LOAD_GLOBAL              Vocabulary
             1948  LOAD_ATTR                TITLE
             1950  CALL_METHOD_1         1  '1 positional argument'
             1952  STORE_FAST               'itag'

 L. 779      1954  LOAD_FAST                'words'
             1956  LOAD_METHOD              append
             1958  LOAD_GLOBAL              vocab
             1960  LOAD_FAST                'word'
             1962  BINARY_SUBSCR    
             1964  LOAD_STR                 'lemma'
             1966  BINARY_SUBSCR    
             1968  LOAD_FAST                'itag'
             1970  BINARY_SUBSCR    
             1972  LOAD_GLOBAL              Vocabulary
             1974  LOAD_ATTR                TITLE
             1976  LOAD_CONST               ('word', 'tag')
             1978  BUILD_CONST_KEY_MAP_2     2 
             1980  CALL_METHOD_1         1  '1 positional argument'
             1982  POP_TOP          
             1984  JUMP_FORWARD       2684  'to 2684'
           1986_0  COME_FROM          1938  '1938'

 L. 781      1986  LOAD_FAST                'words'
             1988  LOAD_METHOD              append
             1990  LOAD_FAST                'word'
             1992  LOAD_GLOBAL              Vocabulary
             1994  LOAD_ATTR                TITLE
             1996  LOAD_CONST               ('word', 'tag')
             1998  BUILD_CONST_KEY_MAP_2     2 
             2000  CALL_METHOD_1         1  '1 positional argument'
             2002  POP_TOP          
         2004_2006  JUMP_FORWARD       2684  'to 2684'
           2008_0  COME_FROM          1908  '1908'

 L. 782      2008  LOAD_FAST                'tag'
             2010  LOAD_CONST               0
             2012  BINARY_SUBSCR    
             2014  LOAD_GLOBAL              Vocabulary
             2016  LOAD_ATTR                MALE
             2018  LOAD_GLOBAL              Vocabulary
             2020  LOAD_ATTR                FEMALE
             2022  LOAD_GLOBAL              Vocabulary
             2024  LOAD_ATTR                TRANSGENDER
             2026  BUILD_LIST_3          3 
             2028  COMPARE_OP               in
         2030_2032  POP_JUMP_IF_FALSE  2070  'to 2070'

 L. 783      2034  LOAD_FAST                'self'
             2036  LOAD_ATTR                _gender
             2038  LOAD_CONST               True
             2040  COMPARE_OP               ==
         2042_2044  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 784      2046  LOAD_FAST                'words'
             2048  LOAD_METHOD              append
             2050  LOAD_FAST                'word'
             2052  LOAD_FAST                'tag'
             2054  LOAD_CONST               0
             2056  BINARY_SUBSCR    
             2058  LOAD_CONST               ('word', 'tag')
             2060  BUILD_CONST_KEY_MAP_2     2 
             2062  CALL_METHOD_1         1  '1 positional argument'
             2064  POP_TOP          
         2066_2068  JUMP_FORWARD       2684  'to 2684'
           2070_0  COME_FROM          2030  '2030'

 L. 785      2070  LOAD_FAST                'tag'
             2072  LOAD_CONST               0
             2074  BINARY_SUBSCR    
             2076  LOAD_GLOBAL              Vocabulary
             2078  LOAD_ATTR                POSITIVE
             2080  COMPARE_OP               ==
         2082_2084  POP_JUMP_IF_FALSE  2154  'to 2154'

 L. 786      2086  LOAD_FAST                'self'
             2088  LOAD_ATTR                _sentiment
             2090  LOAD_CONST               True
             2092  COMPARE_OP               ==
         2094_2096  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 788      2098  LOAD_GLOBAL              len
             2100  LOAD_FAST                'words'
             2102  CALL_FUNCTION_1       1  '1 positional argument'
             2104  LOAD_CONST               0
             2106  COMPARE_OP               ==
         2108_2110  POP_JUMP_IF_TRUE   2132  'to 2132'
             2112  LOAD_FAST                'words'
             2114  LOAD_CONST               -1
             2116  BINARY_SUBSCR    
             2118  LOAD_STR                 'tag'
             2120  BINARY_SUBSCR    
             2122  LOAD_GLOBAL              Vocabulary
             2124  LOAD_ATTR                NEGATIVE
             2126  COMPARE_OP               !=
         2128_2130  POP_JUMP_IF_FALSE  2684  'to 2684'
           2132_0  COME_FROM          2108  '2108'

 L. 789      2132  LOAD_FAST                'words'
             2134  LOAD_METHOD              append
             2136  LOAD_FAST                'word'
             2138  LOAD_GLOBAL              Vocabulary
             2140  LOAD_ATTR                POSITIVE
             2142  LOAD_CONST               ('word', 'tag')
             2144  BUILD_CONST_KEY_MAP_2     2 
             2146  CALL_METHOD_1         1  '1 positional argument'
             2148  POP_TOP          
         2150_2152  JUMP_FORWARD       2684  'to 2684'
           2154_0  COME_FROM          2082  '2082'

 L. 790      2154  LOAD_FAST                'tag'
             2156  LOAD_CONST               0
             2158  BINARY_SUBSCR    
             2160  LOAD_GLOBAL              Vocabulary
             2162  LOAD_ATTR                NEGATIVE
             2164  COMPARE_OP               ==
         2166_2168  POP_JUMP_IF_FALSE  2278  'to 2278'

 L. 791      2170  LOAD_FAST                'self'
             2172  LOAD_ATTR                _sentiment
             2174  LOAD_CONST               True
             2176  COMPARE_OP               ==
         2178_2180  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 793      2182  LOAD_GLOBAL              len
             2184  LOAD_FAST                'words'
             2186  CALL_FUNCTION_1       1  '1 positional argument'
             2188  LOAD_CONST               0
             2190  COMPARE_OP               >
         2192_2194  POP_JUMP_IF_FALSE  2256  'to 2256'
             2196  LOAD_FAST                'words'
             2198  LOAD_CONST               -1
             2200  BINARY_SUBSCR    
             2202  LOAD_STR                 'tag'
             2204  BINARY_SUBSCR    
             2206  LOAD_GLOBAL              Vocabulary
             2208  LOAD_ATTR                NEGATIVE
             2210  COMPARE_OP               ==
         2212_2214  POP_JUMP_IF_FALSE  2256  'to 2256'

 L. 794      2216  LOAD_FAST                'self'
             2218  LOAD_ATTR                _words
             2220  LOAD_FAST                'i'
             2222  LOAD_CONST               1
             2224  BINARY_SUBTRACT  
             2226  BINARY_SUBSCR    
             2228  LOAD_STR                 'word'
             2230  BINARY_SUBSCR    
             2232  LOAD_STR                 'and'
             2234  COMPARE_OP               !=
         2236_2238  POP_JUMP_IF_FALSE  2274  'to 2274'

 L. 795      2240  LOAD_GLOBAL              Vocabulary
             2242  LOAD_ATTR                POSITIVE
             2244  LOAD_FAST                'words'
             2246  LOAD_CONST               -1
             2248  BINARY_SUBSCR    
             2250  LOAD_STR                 'tag'
             2252  STORE_SUBSCR     
             2254  JUMP_FORWARD       2684  'to 2684'
           2256_0  COME_FROM          2212  '2212'
           2256_1  COME_FROM          2192  '2192'

 L. 797      2256  LOAD_FAST                'words'
             2258  LOAD_METHOD              append
             2260  LOAD_FAST                'word'
             2262  LOAD_GLOBAL              Vocabulary
             2264  LOAD_ATTR                NEGATIVE
             2266  LOAD_CONST               ('word', 'tag')
             2268  BUILD_CONST_KEY_MAP_2     2 
             2270  CALL_METHOD_1         1  '1 positional argument'
             2272  POP_TOP          
           2274_0  COME_FROM          2236  '2236'
         2274_2276  JUMP_FORWARD       2684  'to 2684'
           2278_0  COME_FROM          2166  '2166'

 L. 798      2278  LOAD_FAST                'tag'
             2280  LOAD_CONST               0
             2282  BINARY_SUBSCR    
             2284  LOAD_GLOBAL              Vocabulary
             2286  LOAD_ATTR                UNIT
             2288  COMPARE_OP               ==
         2290_2292  POP_JUMP_IF_FALSE  2374  'to 2374'

 L. 799      2294  LOAD_FAST                'self'
             2296  LOAD_ATTR                _unit
             2298  LOAD_CONST               True
             2300  COMPARE_OP               ==
         2302_2304  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 800      2306  LOAD_GLOBAL              len
             2308  LOAD_FAST                'word'
             2310  CALL_FUNCTION_1       1  '1 positional argument'
             2312  LOAD_CONST               1
             2314  COMPARE_OP               >
         2316_2318  POP_JUMP_IF_FALSE  2352  'to 2352'

 L. 801      2320  LOAD_FAST                'words'
             2322  LOAD_METHOD              append
             2324  LOAD_GLOBAL              vocab
             2326  LOAD_FAST                'word'
             2328  BINARY_SUBSCR    
             2330  LOAD_STR                 'lemma'
             2332  BINARY_SUBSCR    
             2334  LOAD_CONST               0
             2336  BINARY_SUBSCR    
             2338  LOAD_GLOBAL              Vocabulary
             2340  LOAD_ATTR                UNIT
             2342  LOAD_CONST               ('word', 'tag')
             2344  BUILD_CONST_KEY_MAP_2     2 
             2346  CALL_METHOD_1         1  '1 positional argument'
             2348  POP_TOP          
             2350  JUMP_FORWARD       2684  'to 2684'
           2352_0  COME_FROM          2316  '2316'

 L. 803      2352  LOAD_FAST                'words'
             2354  LOAD_METHOD              append
             2356  LOAD_FAST                'word'
             2358  LOAD_GLOBAL              Vocabulary
             2360  LOAD_ATTR                UNTAG
             2362  LOAD_CONST               ('word', 'tag')
             2364  BUILD_CONST_KEY_MAP_2     2 
             2366  CALL_METHOD_1         1  '1 positional argument'
             2368  POP_TOP          
         2370_2372  JUMP_FORWARD       2684  'to 2684'
           2374_0  COME_FROM          2290  '2290'

 L. 804      2374  LOAD_FAST                'tag'
             2376  LOAD_CONST               0
             2378  BINARY_SUBSCR    
             2380  LOAD_GLOBAL              Vocabulary
             2382  LOAD_ATTR                MEASUREMENT
             2384  COMPARE_OP               ==
         2386_2388  POP_JUMP_IF_FALSE  2472  'to 2472'

 L. 805      2390  LOAD_FAST                'self'
             2392  LOAD_ATTR                _unit
             2394  LOAD_CONST               True
             2396  COMPARE_OP               ==
         2398_2400  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 806      2402  LOAD_GLOBAL              len
             2404  LOAD_FAST                'word'
             2406  CALL_FUNCTION_1       1  '1 positional argument'
             2408  LOAD_CONST               1
             2410  COMPARE_OP               >
         2412_2414  POP_JUMP_IF_FALSE  2452  'to 2452'

 L. 807      2416  LOAD_FAST                'words'
             2418  LOAD_METHOD              append
             2420  LOAD_GLOBAL              vocab
             2422  LOAD_FAST                'word'
             2424  BINARY_SUBSCR    
             2426  LOAD_STR                 'lemma'
             2428  BINARY_SUBSCR    
             2430  LOAD_CONST               0
             2432  BINARY_SUBSCR    
             2434  LOAD_GLOBAL              Vocabulary
             2436  LOAD_ATTR                MEASUREMENT
             2438  LOAD_CONST               ('word', 'tag')
             2440  BUILD_CONST_KEY_MAP_2     2 
             2442  CALL_METHOD_1         1  '1 positional argument'
             2444  POP_TOP          

 L. 808      2446  LOAD_CONST               True
             2448  STORE_FAST               'measurement'
             2450  JUMP_FORWARD       2470  'to 2470'
           2452_0  COME_FROM          2412  '2412'

 L. 810      2452  LOAD_FAST                'words'
             2454  LOAD_METHOD              append
             2456  LOAD_FAST                'word'
             2458  LOAD_GLOBAL              Vocabulary
             2460  LOAD_ATTR                UNTAG
             2462  LOAD_CONST               ('word', 'tag')
             2464  BUILD_CONST_KEY_MAP_2     2 
             2466  CALL_METHOD_1         1  '1 positional argument'
             2468  POP_TOP          
           2470_0  COME_FROM          2450  '2450'
             2470  JUMP_FORWARD       2684  'to 2684'
           2472_0  COME_FROM          2386  '2386'

 L. 811      2472  LOAD_FAST                'tag'
             2474  LOAD_CONST               0
             2476  BINARY_SUBSCR    
             2478  LOAD_GLOBAL              Vocabulary
             2480  LOAD_ATTR                NUMBER
             2482  COMPARE_OP               ==
         2484_2486  POP_JUMP_IF_FALSE  2544  'to 2544'

 L. 812      2488  LOAD_FAST                'self'
             2490  LOAD_ATTR                _number
             2492  LOAD_CONST               True
             2494  COMPARE_OP               ==
         2496_2498  POP_JUMP_IF_TRUE   2512  'to 2512'
             2500  LOAD_FAST                'self'
             2502  LOAD_ATTR                _unit
             2504  LOAD_CONST               True
             2506  COMPARE_OP               ==
         2508_2510  POP_JUMP_IF_FALSE  2684  'to 2684'
           2512_0  COME_FROM          2496  '2496'

 L. 813      2512  LOAD_FAST                'words'
             2514  LOAD_METHOD              append
             2516  LOAD_GLOBAL              vocab
             2518  LOAD_FAST                'word'
             2520  BINARY_SUBSCR    
             2522  LOAD_STR                 'lemma'
             2524  BINARY_SUBSCR    
             2526  LOAD_CONST               0
             2528  BINARY_SUBSCR    
             2530  LOAD_GLOBAL              Vocabulary
             2532  LOAD_ATTR                NUMBER
             2534  LOAD_CONST               ('word', 'tag')
             2536  BUILD_CONST_KEY_MAP_2     2 
             2538  CALL_METHOD_1         1  '1 positional argument'
             2540  POP_TOP          
             2542  JUMP_FORWARD       2684  'to 2684'
           2544_0  COME_FROM          2484  '2484'

 L. 814      2544  LOAD_FAST                'tag'
             2546  LOAD_CONST               0
             2548  BINARY_SUBSCR    
             2550  LOAD_GLOBAL              Vocabulary
             2552  LOAD_ATTR                PORTER
             2554  COMPARE_OP               ==
         2556_2558  POP_JUMP_IF_FALSE  2592  'to 2592'

 L. 815      2560  LOAD_FAST                'self'
             2562  LOAD_ATTR                _porter
             2564  LOAD_CONST               True
             2566  COMPARE_OP               ==
         2568_2570  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 816      2572  LOAD_FAST                'words'
             2574  LOAD_METHOD              append
             2576  LOAD_FAST                'word'
             2578  LOAD_GLOBAL              Vocabulary
             2580  LOAD_ATTR                PORTER
             2582  LOAD_CONST               ('word', 'tag')
             2584  BUILD_CONST_KEY_MAP_2     2 
             2586  CALL_METHOD_1         1  '1 positional argument'
             2588  POP_TOP          
             2590  JUMP_FORWARD       2684  'to 2684'
           2592_0  COME_FROM          2556  '2556'

 L. 817      2592  LOAD_FAST                'tag'
             2594  LOAD_CONST               0
             2596  BINARY_SUBSCR    
             2598  LOAD_GLOBAL              Vocabulary
             2600  LOAD_ATTR                ADDRESS
             2602  LOAD_GLOBAL              Vocabulary
             2604  LOAD_ATTR                STREET_TYPE
             2606  LOAD_GLOBAL              Vocabulary
             2608  LOAD_ATTR                SAC
             2610  BUILD_LIST_3          3 
             2612  COMPARE_OP               in
         2614_2616  POP_JUMP_IF_FALSE  2638  'to 2638'

 L. 819      2618  LOAD_FAST                'words'
             2620  LOAD_METHOD              append
             2622  LOAD_FAST                'word'
             2624  LOAD_GLOBAL              Vocabulary
             2626  LOAD_ATTR                UNTAG
             2628  LOAD_CONST               ('word', 'tag')
             2630  BUILD_CONST_KEY_MAP_2     2 
             2632  CALL_METHOD_1         1  '1 positional argument'
             2634  POP_TOP          
             2636  JUMP_FORWARD       2684  'to 2684'
           2638_0  COME_FROM          2614  '2614'

 L. 820      2638  LOAD_FAST                'tag'
             2640  LOAD_CONST               0
             2642  BINARY_SUBSCR    
             2644  LOAD_GLOBAL              Vocabulary
             2646  LOAD_ATTR                UNTAG
             2648  COMPARE_OP               ==
         2650_2652  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 821      2654  LOAD_FAST                'words'
             2656  LOAD_METHOD              append
             2658  LOAD_GLOBAL              vocab
             2660  LOAD_FAST                'word'
           2662_0  COME_FROM          2350  '2350'
           2662_1  COME_FROM          2254  '2254'
           2662_2  COME_FROM          1984  '1984'
           2662_3  COME_FROM          1554  '1554'
             2662  BINARY_SUBSCR    
             2664  LOAD_STR                 'lemma'
             2666  BINARY_SUBSCR    
             2668  LOAD_CONST               0
             2670  BINARY_SUBSCR    
             2672  LOAD_GLOBAL              Vocabulary
             2674  LOAD_ATTR                UNTAG
             2676  LOAD_CONST               ('word', 'tag')
             2678  BUILD_CONST_KEY_MAP_2     2 
             2680  CALL_METHOD_1         1  '1 positional argument'
             2682  POP_TOP          
           2684_0  COME_FROM          2650  '2650'
           2684_1  COME_FROM          2636  '2636'
           2684_2  COME_FROM          2590  '2590'
           2684_3  COME_FROM          2568  '2568'
           2684_4  COME_FROM          2542  '2542'
           2684_5  COME_FROM          2508  '2508'
           2684_6  COME_FROM          2470  '2470'
           2684_7  COME_FROM          2398  '2398'
           2684_8  COME_FROM          2370  '2370'
           2684_9  COME_FROM          2302  '2302'
          2684_10  COME_FROM          2274  '2274'
          2684_11  COME_FROM          2178  '2178'
          2684_12  COME_FROM          2150  '2150'
          2684_13  COME_FROM          2128  '2128'
          2684_14  COME_FROM          2094  '2094'
          2684_15  COME_FROM          2066  '2066'
          2684_16  COME_FROM          2042  '2042'
          2684_17  COME_FROM          2004  '2004'
          2684_18  COME_FROM          1920  '1920'
          2684_19  COME_FROM          1896  '1896'
          2684_20  COME_FROM          1874  '1874'
          2684_21  COME_FROM          1850  '1850'
          2684_22  COME_FROM          1828  '1828'
          2684_23  COME_FROM          1804  '1804'
          2684_24  COME_FROM          1782  '1782'
          2684_25  COME_FROM          1758  '1758'
          2684_26  COME_FROM          1736  '1736'
          2684_27  COME_FROM          1712  '1712'
          2684_28  COME_FROM          1690  '1690'
          2684_29  COME_FROM          1666  '1666'
          2684_30  COME_FROM          1644  '1644'
          2684_31  COME_FROM          1620  '1620'
          2684_32  COME_FROM          1598  '1598'
          2684_33  COME_FROM          1574  '1574'
          2684_34  COME_FROM          1502  '1502'

 L. 822      2684  CONTINUE_LOOP        34  'to 34'
             2686  POP_BLOCK        
             2688  JUMP_FORWARD       2722  'to 2722'
           2690_0  COME_FROM_EXCEPT   1152  '1152'

 L. 823      2690  POP_TOP          
             2692  POP_TOP          
             2694  POP_TOP          

 L. 824      2696  LOAD_FAST                'words'
             2698  LOAD_METHOD              append
             2700  LOAD_FAST                'word'
             2702  LOAD_FAST                'tag'
             2704  LOAD_CONST               0
             2706  BINARY_SUBSCR    
             2708  LOAD_CONST               ('word', 'tag')
             2710  BUILD_CONST_KEY_MAP_2     2 
             2712  CALL_METHOD_1         1  '1 positional argument'
             2714  POP_TOP          
             2716  POP_EXCEPT       
             2718  JUMP_FORWARD       2722  'to 2722'
             2720  END_FINALLY      
           2722_0  COME_FROM          2718  '2718'
           2722_1  COME_FROM          2688  '2688'
             2722  JUMP_BACK            34  'to 34'
           2724_0  COME_FROM           134  '134'

 L. 826      2724  LOAD_FAST                'self'
             2726  LOAD_ATTR                _punct
             2728  LOAD_CONST               False
             2730  COMPARE_OP               !=
             2732  POP_JUMP_IF_FALSE    34  'to 34'

 L. 827      2734  LOAD_FAST                'words'
             2736  LOAD_METHOD              append
             2738  LOAD_FAST                'self'
             2740  LOAD_ATTR                _words
             2742  LOAD_FAST                'i'
             2744  BINARY_SUBSCR    
             2746  CALL_METHOD_1         1  '1 positional argument'
             2748  POP_TOP          

 L. 828      2750  CONTINUE             34  'to 34'
             2752  JUMP_BACK            34  'to 34'
             2754  POP_BLOCK        
           2756_0  COME_FROM_LOOP       22  '22'

 L. 830      2756  LOAD_FAST                'words'
             2758  LOAD_FAST                'self'
             2760  STORE_ATTR               _words

Parse error at or near `COME_FROM' instruction at offset 2662_0

    def _isNumber(self, words, index):
        """ Check if word sequence is a number """
        word = words[index]['word']
        try:
            tag = vocab[word]['tag']
            if Vocabulary.NUMBER in tag:
                word = vocab[word]['lemma'][0]
        except:
            pass

        hex = False
        start = 0
        if word[0] == '+':
            word = word[1:]
        else:
            if word[0] == '-':
                start = 1
            elif start >= len(word):
                return (None, 0)
                if word[start] == self.DECIMAL:
                    word = word[0:start] + '0' + word[start:]
                    start += 2
                else:
                    if word.startswith('0x'):
                        hex = True
                        word = word[2:]
                digit = False
                dpt = False
                exp = False
                nom = False
                end = len(word)
                for i in range(start, end):
                    if word[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        digit = True
                    elif hex and word[i] in ('a', 'b', 'c', 'd', 'e', 'f'):
                        digit = True
                    elif digit:
                        if not dpt:
                            if word[i] == self.DECIMAL:
                                digit = False
                                dpt = True
                        else:
                            if digit:
                                if word[i] == self.THOUSANDS:
                                    digit = False
                            if digit:
                                if not exp:
                                    if word[i] == 'e':
                                        exp = True
                            if exp and word[i] == '-':
                                continue
                        if digit and word[i] == '/':
                            nom = i
                    else:
                        if digit:
                            if word[(i - 1)] == '1':
                                if word[i:] == 'st':
                                    return (
                                     word[0:i], 0)
                            elif word[(i - 1)] == '2':
                                if word[i:] == 'nd':
                                    return (
                                     word[0:i], 0)
                            elif word[(i - 1)] == '3':
                                if word[i:] == 'rd':
                                    return (
                                     word[0:i], 0)
                            elif word[i:] == 'th':
                                return (
                                 word[0:i], 0)
                            return (None, 0)
                        return (None, 0)

                if hex:
                    try:
                        word = str(int(word, 16))
                    except:
                        return (None, 0)

            else:
                if nom is not False:
                    try:
                        word = str(int(word[0:nom]) / int(word[nom + 1:]))
                    except:
                        pass

                length = len(words)
                if index + 1 < length:
                    try:
                        tags = vocab[words[(index + 1)]['word']]['tag']
                        if Vocabulary.MUNIT in tags:
                            if Vocabulary.NUMBER in tags:
                                if self.DECIMAL in word:
                                    word = str(int(float(word) * int(vocab[words[(index + 1)]['word']]['lemma'][0])))
                                else:
                                    word = str(int(word) * int(vocab[words[(index + 1)]['word']]['lemma'][0]))
                                return (
                                 word, 1)
                    except:
                        pass

            return (
             word, 0)

    def _isDate(self, words, index):
        """ Check if word sequence is a date """
        length = len(words)
        if words[index]['word'] in ('jan', 'january', 'feb', 'february', 'mar', 'march',
                                    'apr', 'april', 'may', 'jun', 'june', 'jul',
                                    'july', 'aug', 'august', 'sep', 'september',
                                    'oct', 'october', 'nov', 'november', 'dec', 'december'):
            if index + 2 >= length:
                return (None, 0)
                day = words[(index + 1)]['word']
                if not day.isdigit():
                    return (None, 0)
                if int(day) < 10:
                    day = '0' + day
                elif words[(index + 2)]['word'] == ',':
                    if index + 3 == length:
                        return (None, 0)
                    year = words[(index + 3)]['word']
                    n = 3
                else:
                    year = words[(index + 2)]['word']
                    n = 2
                if not year.isdigit():
                    return (None, 0)
            else:
                if len(year) == 2:
                    year = '20' + year
                else:
                    months = {'jan':'01', 
                     'jan.':'01',  'january':'01',  'feb':'02', 
                     'feb.':'02',  'february':'02',  'mar':'03', 
                     'mar.':'03',  'march':'03',  'apr':'04', 
                     'apr.':'04',  'april':'04',  'may':'05', 
                     'jun':'06', 
                     'jun.':'06',  'june':'06',  'jul':'07', 
                     'jul.':'07',  'july':'07',  'aug':'08', 
                     'aug.':'08',  'august':'08',  'sep':'09', 
                     'sep.':'09',  'september':'09',  'oct':'10', 
                     'oct.':'10',  'october':'10',  'nov':'11', 
                     'nov.':'11',  'november':'11',  'dec':'12', 
                     'dec.':'12',  'december':'12'}
                    return (
                     year + '-' + months[words[index]['word']] + '-' + day, n)
                    if '/' in words[index]['word']:
                        terms = words[index]['word'].split('/')
                        if len(terms) != 3:
                            return (None, 0)
                        else:
                            month = terms[0]
                            if not month.isdigit():
                                return (None, 0)
                                mm = int(month)
                                day = terms[1]
                                if not day.isdigit():
                                    return (None, 0)
                                else:
                                    dd = int(day)
                                    year = terms[2]
                                    if not year.isdigit():
                                        return (None, 0)
                                        if mm < 1 or mm > 12:
                                            return (None, 0)
                                        elif not dd < 1:
                                            if dd > 31:
                                                return (None, 0)
                                            if len(year) == 2:
                                                yyyy = '20' + year
                                        elif len(year) == 4:
                                            yyyy = year
                                        else:
                                            return (None, 0)
                                        if mm < 10:
                                            mm = '0' + str(mm)
                                    else:
                                        mm = str(mm)
                                if dd < 10:
                                    dd = '0' + str(dd)
                            else:
                                dd = str(dd)
                        return (
                         yyyy + '-' + mm + '-' + dd, 1)
                    first = words[index]['word']
                    if not first.isdigit():
                        return (None, 0)
                    index += 2
                    if index >= length:
                        return (None, 0)
                    if words[(index - 1)]['word'] != '-':
                        return (None, 0)
                    second = words[index]['word']
                    return second.isdigit() or (None, 0)
                index += 2
                if index >= length:
                    return (None, 0)
                if words[(index - 1)]['word'] != '-':
                    return (None, 0)
                third = words[index]['word']
                return second.isdigit() or (None, 0)
            if len(first) == 4:
                yyyy = first
                mm = int(second)
                if mm < 1 or mm > 12:
                    return (None, 0)
                dd = int(third)
                if dd < 1 or dd > 31:
                    return (None, 0)
        else:
            mm = int(first)
            if mm < 1 or mm > 12:
                return (None, 0)
            dd = int(second)
        if not dd < 1:
            if dd > 31:
                return (None, 0)
            if len(third) == 2:
                yyyy = '20' + third
            else:
                if len(third) == 4:
                    yyyy = third
                else:
                    return (None, 0)
        else:
            if mm < 10:
                mm = '0' + str(mm)
            else:
                mm = str(mm)
            if dd < 10:
                dd = '0' + str(dd)
            else:
                dd = str(dd)
        return (
         yyyy + '-' + mm + '-' + dd, 5)

    def _isSSN(self, words, index):
        """ Check if sequence of words is a SSN """
        length = len(words)
        start = index
        if words[index]['word'] == 'ssn':
            index += 1
        else:
            if words[index]['word'] in ('social', 'soc'):
                index += 1
                if index == length:
                    return (None, 0)
                if words[index]['word'] == '.':
                    index += 1
                    if index == length:
                        return (None, 0)
                if words[index]['word'] not in ('security', 'sec'):
                    return (None, 0)
                index += 1
                if index == length:
                    return (None, 0)
                if words[index]['word'] == '.':
                    index += 1
                    if index == length:
                        return (None, 0)
                if words[index]['word'] in ('number', 'num', 'no'):
                    index += 1
                    if words[index]['word'] == '.':
                        index += 1
                        if index == length:
                            return (None, 0)
                        else:
                            return (None, 0)
            else:
                if index == length:
                    return (None, 0)
                while words[index]['tag'] in [Vocabulary.PUNCT, Vocabulary.SYMBOL] or words[index]['word'] in ('is',
                                                                                                               'of'):
                    index += 1
                    if index == length:
                        return (None, 0)

                if len(words[index]['word']) == 9 and words[index]['word'].isdigit():
                    return (
                     words[index]['word'], index - start)
            if len(words[index]['word']) == 3:
                ssn = words[index]['word']
                index += 1
                if index == length:
                    return (None, 0)
                if words[index]['word'] == '-':
                    index += 1
                    if index == length:
                        return (None, 0)
                if len(words[index]['word']) != 2:
                    return (None, 0)
                ssn += words[index]['word']
                index += 1
                if index == length:
                    return (None, 0)
                if words[index]['word'] == '-':
                    index += 1
                if len(words[index]['word']) != 4:
                    return (None, 0)
                ssn += words[index]['word']
                return (
                 ssn, index - start)
            return (None, 0)

    def _isTele(self, words, index):
        """ Check if sequence of words is a USA/CA Telephone """
        tag = Vocabulary.TELEPHONE
        length = len(words)
        start = index
        if words[index]['word'] in ('phone', 'tel', 'tele', 'telephone', 'home', 'work',
                                    'office', 'cell', 'mobile', 'fax', 'contact',
                                    'support'):
            if words[index]['word'] == 'home':
                tag = Vocabulary.TELEPHONE_HOME
            else:
                if words[index]['word'] in ('work', 'office'):
                    tag = Vocabulary.TELEPHONE_WORK
                else:
                    if words[index]['word'] in ('cell', 'mobile'):
                        tag = Vocabulary.TELEPHONE_CELL
                    else:
                        if words[index]['word'] in ('fax', ):
                            tag = Vocabulary.TELEPHONE_FAX
                        else:
                            index += 1
                            if index == length:
                                return (None, 0, 0)
                            if words[index]['word'] in ('number', 'no', 'num'):
                                index += 1
                                if index == length:
                                    return (None, 0, 0)
                        while words[index]['tag'] in [Vocabulary.PUNCT, Vocabulary.SYMBOL] or words[index]['word'] in ('is',
                                                                                                                       'of'):
                            index += 1
                            if index == length:
                                return (None, 0, 0)

                        prefix = True
        else:
            prefix = False
        tele = ''
        if prefix == True:
            if len(words[index]['word']) == 10:
                if words[index]['word'].isdigit():
                    return (
                     words[index]['word'], index - start, tag)
        if prefix == True:
            if len(words[index]['word']) == 11:
                if words[index]['word'].isdigit():
                    if words[index]['word'][0] == '1':
                        return (
                         words[index]['word'], index - start, tag)
        if '.' in words[index]['word']:
            toks = words[index]['word'].split('.')
            if len(toks) == 3:
                for i in range(3):
                    if not toks[i].isdigit():
                        return (None, 0, 0)
                        tele += toks[i]

                return (
                 tele, index - start, tag)
            if len(toks) == 4:
                tele = '1'
                if toks[0] != '1':
                    return (None, 0, 0)
                for i in range(1, 4):
                    if not toks[i].isdigit():
                        return (None, 0, 0)
                        tele += toks[i]

                return (
                 tele, index - start, tag)
        if len(words[index]['word']) == 1:
            if words[index]['word'] == '1':
                tele = '1'
                index += 1
                if index == length:
                    return (None, 0, 0)
                if words[index]['word'] in ('-', '.'):
                    index += 1
                    if index == length:
                        return (None, 0, 0)
        if words[index]['word'] == '(':
            index += 1
            if index == length:
                return (None, 0, 0)
        if len(words[index]['word']) == 3:
            if words[index]['word'].isdigit():
                tele += words[index]['word']
                index += 1
                if index == length:
                    return (None, 0, 0)
                if words[index]['word'] in ('-', '.', ')'):
                    index += 1
                    if index == length:
                        return (None, 0, 0)
                if len(words[index]['word']) == 7:
                    tele += words[index]['word']
                    return (tele, index - start, tag)
                if len(words[index]['word']) != 3:
                    return (None, 0, 0)
                tele += words[index]['word']
                index += 1
                if index == length:
                    return (None, 0, 0)
                if words[index]['word'] in ('-', '.'):
                    index += 1
                    if index == length:
                        return (None, 0, 0)
                if len(words[index]['word']) != 4:
                    return (None, 0, 0)
                tele += words[index]['word']
                return (
                 tele, index - start, tag)
        return (None, 0, 0)

    def _isAddr(self, words, index):
        """ Check if sequence of words is a USA/CA Address """
        start = index
        addr = Address(words, index)
        if addr.is_addr():
            return addr.index - start
        return 0

    def _isGender(self, words, index):
        """ Check if sequence is Gender reference """
        length = len(words)
        start = index
        if words[index]['word'] in ('sex', 'gender'):
            index += 1
            if index == length:
                return (
                 None, 0, Vocabulary.UNTAG)
            while words[index]['tag'] in [Vocabulary.PUNCT, Vocabulary.SYMBOL]:
                index += 1
                if index == length:
                    return (
                     None, 0, Vocabulary.UNTAG)

        else:
            return (
             None, 0, Vocabulary.UNTAG)
        if words[index]['word'] in ('m', 'male'):
            words[index]['tag'] = Vocabulary.MALE
            return ('male', index - start, Vocabulary.MALE)
        if words[index]['word'] in ('f', 'female'):
            words[index]['tag'] = Vocabulary.FEMALE
            return ('female', index - start, Vocabulary.FEMALE)
        if words[index]['word'] in ('t', 'trans', 'tg', 'transgender'):
            words[index]['tag'] = Vocabulary.TRANSGENDER
            return ('transgender', index - start, Vocabulary.TRANSGENDER)
        return (None, 0, Vocabulary.UNTAG)

    def _isAge(self, words, index):
        """ Check if sequence is age reference """
        start = index
        length = len(words)
        if words[index]['word'] == 'age':
            index += 1
            if index == length:
                return (None, 0)
                if words[index]['word'] == ':':
                    index += 1
                    if index == length:
                        return (None, 0)
                age_key = True
            else:
                age_key = False
        else:
            return words[index]['word'].isdigit() or (None, 0)
        age = words[index]['word']
        index += 1
        if index < length:
            if words[index]['word'] in ('yr', 'yrs', 'year', 'years'):
                age_key = True
                index += 1
                if index < length:
                    if words[index]['word'] == 'old':
                        index += 1
        if age_key:
            return (
             age, index - start - 1)
        return (None, 0)

    def _conversion--- This code section failed: ---

 L.1346         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _standard
                4  POP_JUMP_IF_TRUE     16  'to 16'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _metric
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L.1347        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'
             16_1  COME_FROM             4  '4'

 L.1349        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _words
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  STORE_FAST               'l'

 L.1350     26_28  SETUP_LOOP         1902  'to 1902'
               30  LOAD_GLOBAL              range
               32  LOAD_CONST               1
               34  LOAD_FAST                'l'
               36  CALL_FUNCTION_2       2  '2 positional arguments'
               38  GET_ITER         
             40_0  COME_FROM          1852  '1852'
             40_1  COME_FROM          1060  '1060'
             40_2  COME_FROM            92  '92'
             40_3  COME_FROM            68  '68'
            40_42  FOR_ITER           1900  'to 1900'
               44  STORE_FAST               'i'

 L.1351        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _words
               50  LOAD_FAST                'i'
               52  BINARY_SUBSCR    
               54  LOAD_STR                 'tag'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'tag'

 L.1352        60  LOAD_FAST                'tag'
               62  LOAD_GLOBAL              Vocabulary
               64  LOAD_ATTR                UNIT
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    40  'to 40'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _words
               74  LOAD_FAST                'i'
               76  LOAD_CONST               1
               78  BINARY_SUBTRACT  
               80  BINARY_SUBSCR    
               82  LOAD_STR                 'tag'
               84  BINARY_SUBSCR    
               86  LOAD_GLOBAL              Vocabulary
               88  LOAD_ATTR                NUMBER
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE    40  'to 40'

 L.1353        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _words
               98  LOAD_FAST                'i'
              100  BINARY_SUBSCR    
              102  LOAD_STR                 'word'
              104  BINARY_SUBSCR    
              106  STORE_FAST               'unit'

 L.1354       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _words
              112  LOAD_FAST                'i'
              114  LOAD_CONST               1
              116  BINARY_SUBTRACT  
              118  BINARY_SUBSCR    
              120  LOAD_STR                 'word'
              122  BINARY_SUBSCR    
              124  STORE_FAST               'numb'

 L.1355       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _standard
              130  LOAD_CONST               True
              132  COMPARE_OP               ==
          134_136  POP_JUMP_IF_FALSE  1052  'to 1052'

 L.1356       138  LOAD_FAST                'unit'
              140  LOAD_STR                 'millimeter'
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   194  'to 194'

 L.1357       146  LOAD_GLOBAL              str
              148  LOAD_GLOBAL              float
              150  LOAD_FAST                'numb'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  LOAD_CONST               0.0393701
              156  BINARY_MULTIPLY  
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                _words
              164  LOAD_FAST                'i'
              166  LOAD_CONST               1
              168  BINARY_SUBTRACT  
              170  BINARY_SUBSCR    
              172  LOAD_STR                 'word'
              174  STORE_SUBSCR     

 L.1358       176  LOAD_STR                 'inch'
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                _words
              182  LOAD_FAST                'i'
              184  BINARY_SUBSCR    
              186  LOAD_STR                 'word'
              188  STORE_SUBSCR     
          190_192  JUMP_ABSOLUTE      1898  'to 1898'
            194_0  COME_FROM           144  '144'

 L.1359       194  LOAD_FAST                'unit'
              196  LOAD_STR                 'centimeter'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   250  'to 250'

 L.1360       202  LOAD_GLOBAL              str
              204  LOAD_GLOBAL              float
              206  LOAD_FAST                'numb'
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  LOAD_CONST               0.393701
              212  BINARY_MULTIPLY  
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                _words
              220  LOAD_FAST                'i'
              222  LOAD_CONST               1
              224  BINARY_SUBTRACT  
              226  BINARY_SUBSCR    
              228  LOAD_STR                 'word'
              230  STORE_SUBSCR     

 L.1361       232  LOAD_STR                 'inch'
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                _words
              238  LOAD_FAST                'i'
              240  BINARY_SUBSCR    
              242  LOAD_STR                 'word'
              244  STORE_SUBSCR     
          246_248  JUMP_ABSOLUTE      1898  'to 1898'
            250_0  COME_FROM           200  '200'

 L.1362       250  LOAD_FAST                'unit'
              252  LOAD_STR                 'meter'
              254  COMPARE_OP               ==
          256_258  POP_JUMP_IF_FALSE   308  'to 308'

 L.1363       260  LOAD_GLOBAL              str
              262  LOAD_GLOBAL              float
              264  LOAD_FAST                'numb'
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  LOAD_CONST               3.28084
              270  BINARY_MULTIPLY  
              272  CALL_FUNCTION_1       1  '1 positional argument'
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                _words
              278  LOAD_FAST                'i'
              280  LOAD_CONST               1
              282  BINARY_SUBTRACT  
              284  BINARY_SUBSCR    
              286  LOAD_STR                 'word'
              288  STORE_SUBSCR     

 L.1364       290  LOAD_STR                 'feet'
              292  LOAD_FAST                'self'
              294  LOAD_ATTR                _words
              296  LOAD_FAST                'i'
              298  BINARY_SUBSCR    
              300  LOAD_STR                 'word'
              302  STORE_SUBSCR     
          304_306  JUMP_ABSOLUTE      1898  'to 1898'
            308_0  COME_FROM           256  '256'

 L.1365       308  LOAD_FAST                'unit'
              310  LOAD_STR                 'kilometer'
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   366  'to 366'

 L.1366       318  LOAD_GLOBAL              str
              320  LOAD_GLOBAL              float
              322  LOAD_FAST                'numb'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  LOAD_CONST               0.621371
              328  BINARY_MULTIPLY  
              330  CALL_FUNCTION_1       1  '1 positional argument'
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                _words
              336  LOAD_FAST                'i'
              338  LOAD_CONST               1
              340  BINARY_SUBTRACT  
              342  BINARY_SUBSCR    
              344  LOAD_STR                 'word'
              346  STORE_SUBSCR     

 L.1367       348  LOAD_STR                 'mile'
              350  LOAD_FAST                'self'
              352  LOAD_ATTR                _words
              354  LOAD_FAST                'i'
              356  BINARY_SUBSCR    
              358  LOAD_STR                 'word'
              360  STORE_SUBSCR     
          362_364  JUMP_ABSOLUTE      1898  'to 1898'
            366_0  COME_FROM           314  '314'

 L.1368       366  LOAD_FAST                'unit'
              368  LOAD_STR                 'milliliter'
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   424  'to 424'

 L.1369       376  LOAD_GLOBAL              str
              378  LOAD_GLOBAL              float
              380  LOAD_FAST                'numb'
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  LOAD_CONST               0.033814
              386  BINARY_MULTIPLY  
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  LOAD_FAST                'self'
              392  LOAD_ATTR                _words
              394  LOAD_FAST                'i'
              396  LOAD_CONST               1
              398  BINARY_SUBTRACT  
              400  BINARY_SUBSCR    
              402  LOAD_STR                 'word'
              404  STORE_SUBSCR     

 L.1370       406  LOAD_STR                 'ounce'
              408  LOAD_FAST                'self'
              410  LOAD_ATTR                _words
              412  LOAD_FAST                'i'
              414  BINARY_SUBSCR    
              416  LOAD_STR                 'word'
              418  STORE_SUBSCR     
          420_422  JUMP_ABSOLUTE      1898  'to 1898'
            424_0  COME_FROM           372  '372'

 L.1371       424  LOAD_FAST                'unit'
              426  LOAD_STR                 'liter'
              428  COMPARE_OP               ==
          430_432  POP_JUMP_IF_FALSE   482  'to 482'

 L.1372       434  LOAD_GLOBAL              str
              436  LOAD_GLOBAL              float
              438  LOAD_FAST                'numb'
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  LOAD_CONST               0.264172
              444  BINARY_MULTIPLY  
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                _words
              452  LOAD_FAST                'i'
              454  LOAD_CONST               1
              456  BINARY_SUBTRACT  
              458  BINARY_SUBSCR    
              460  LOAD_STR                 'word'
              462  STORE_SUBSCR     

 L.1373       464  LOAD_STR                 'gallon'
              466  LOAD_FAST                'self'
              468  LOAD_ATTR                _words
              470  LOAD_FAST                'i'
              472  BINARY_SUBSCR    
              474  LOAD_STR                 'word'
              476  STORE_SUBSCR     
          478_480  JUMP_ABSOLUTE      1898  'to 1898'
            482_0  COME_FROM           430  '430'

 L.1374       482  LOAD_FAST                'unit'
              484  LOAD_STR                 'kiloliter'
              486  COMPARE_OP               ==
          488_490  POP_JUMP_IF_FALSE   540  'to 540'

 L.1375       492  LOAD_GLOBAL              str
              494  LOAD_GLOBAL              float
              496  LOAD_FAST                'numb'
              498  CALL_FUNCTION_1       1  '1 positional argument'
              500  LOAD_CONST               264.172
              502  BINARY_MULTIPLY  
              504  CALL_FUNCTION_1       1  '1 positional argument'
              506  LOAD_FAST                'self'
              508  LOAD_ATTR                _words
              510  LOAD_FAST                'i'
              512  LOAD_CONST               1
              514  BINARY_SUBTRACT  
              516  BINARY_SUBSCR    
              518  LOAD_STR                 'word'
              520  STORE_SUBSCR     

 L.1376       522  LOAD_STR                 'gallon'
              524  LOAD_FAST                'self'
              526  LOAD_ATTR                _words
              528  LOAD_FAST                'i'
              530  BINARY_SUBSCR    
              532  LOAD_STR                 'word'
              534  STORE_SUBSCR     
          536_538  JUMP_ABSOLUTE      1898  'to 1898'
            540_0  COME_FROM           488  '488'

 L.1377       540  LOAD_FAST                'unit'
              542  LOAD_STR                 'milligram'
              544  COMPARE_OP               ==
          546_548  POP_JUMP_IF_FALSE   598  'to 598'

 L.1378       550  LOAD_GLOBAL              str
              552  LOAD_GLOBAL              float
              554  LOAD_FAST                'numb'
              556  CALL_FUNCTION_1       1  '1 positional argument'
              558  LOAD_CONST               3.5274e-05
              560  BINARY_MULTIPLY  
              562  CALL_FUNCTION_1       1  '1 positional argument'
              564  LOAD_FAST                'self'
              566  LOAD_ATTR                _words
              568  LOAD_FAST                'i'
              570  LOAD_CONST               1
              572  BINARY_SUBTRACT  
              574  BINARY_SUBSCR    
              576  LOAD_STR                 'word'
              578  STORE_SUBSCR     

 L.1379       580  LOAD_STR                 'ounce'
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                _words
              586  LOAD_FAST                'i'
              588  BINARY_SUBSCR    
              590  LOAD_STR                 'word'
              592  STORE_SUBSCR     
          594_596  JUMP_ABSOLUTE      1898  'to 1898'
            598_0  COME_FROM           546  '546'

 L.1380       598  LOAD_FAST                'unit'
              600  LOAD_STR                 'gram'
              602  COMPARE_OP               ==
          604_606  POP_JUMP_IF_FALSE   656  'to 656'

 L.1381       608  LOAD_GLOBAL              str
              610  LOAD_GLOBAL              float
              612  LOAD_FAST                'numb'
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  LOAD_CONST               0.035274
              618  BINARY_MULTIPLY  
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  LOAD_FAST                'self'
              624  LOAD_ATTR                _words
              626  LOAD_FAST                'i'
              628  LOAD_CONST               1
              630  BINARY_SUBTRACT  
              632  BINARY_SUBSCR    
              634  LOAD_STR                 'word'
              636  STORE_SUBSCR     

 L.1382       638  LOAD_STR                 'ounce'
              640  LOAD_FAST                'self'
              642  LOAD_ATTR                _words
              644  LOAD_FAST                'i'
              646  BINARY_SUBSCR    
              648  LOAD_STR                 'word'
              650  STORE_SUBSCR     
          652_654  JUMP_ABSOLUTE      1898  'to 1898'
            656_0  COME_FROM           604  '604'

 L.1383       656  LOAD_FAST                'unit'
              658  LOAD_STR                 'kilogram'
              660  COMPARE_OP               ==
          662_664  POP_JUMP_IF_FALSE   714  'to 714'

 L.1384       666  LOAD_GLOBAL              str
              668  LOAD_GLOBAL              float
              670  LOAD_FAST                'numb'
              672  CALL_FUNCTION_1       1  '1 positional argument'
              674  LOAD_CONST               2.20462
              676  BINARY_MULTIPLY  
              678  CALL_FUNCTION_1       1  '1 positional argument'
              680  LOAD_FAST                'self'
              682  LOAD_ATTR                _words
              684  LOAD_FAST                'i'
              686  LOAD_CONST               1
              688  BINARY_SUBTRACT  
              690  BINARY_SUBSCR    
              692  LOAD_STR                 'word'
              694  STORE_SUBSCR     

 L.1385       696  LOAD_STR                 'pound'
              698  LOAD_FAST                'self'
              700  LOAD_ATTR                _words
              702  LOAD_FAST                'i'
              704  BINARY_SUBSCR    
              706  LOAD_STR                 'word'
              708  STORE_SUBSCR     
          710_712  JUMP_ABSOLUTE      1898  'to 1898'
            714_0  COME_FROM           662  '662'

 L.1386       714  LOAD_FAST                'unit'
              716  LOAD_STR                 'square meter'
              718  COMPARE_OP               ==
          720_722  POP_JUMP_IF_FALSE   772  'to 772'

 L.1387       724  LOAD_GLOBAL              str
              726  LOAD_GLOBAL              float
              728  LOAD_FAST                'numb'
              730  CALL_FUNCTION_1       1  '1 positional argument'
              732  LOAD_CONST               10.7639
              734  BINARY_MULTIPLY  
              736  CALL_FUNCTION_1       1  '1 positional argument'
              738  LOAD_FAST                'self'
              740  LOAD_ATTR                _words
              742  LOAD_FAST                'i'
              744  LOAD_CONST               1
              746  BINARY_SUBTRACT  
              748  BINARY_SUBSCR    
              750  LOAD_STR                 'word'
              752  STORE_SUBSCR     

 L.1388       754  LOAD_STR                 'square foot'
              756  LOAD_FAST                'self'
              758  LOAD_ATTR                _words
              760  LOAD_FAST                'i'
              762  BINARY_SUBSCR    
              764  LOAD_STR                 'word'
              766  STORE_SUBSCR     
          768_770  JUMP_ABSOLUTE      1898  'to 1898'
            772_0  COME_FROM           720  '720'

 L.1389       772  LOAD_FAST                'unit'
              774  LOAD_STR                 'kilometer per hour'
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   828  'to 828'

 L.1390       782  LOAD_GLOBAL              str
              784  LOAD_GLOBAL              float
              786  LOAD_FAST                'numb'
              788  CALL_FUNCTION_1       1  '1 positional argument'
              790  LOAD_CONST               0.621371
              792  BINARY_MULTIPLY  
              794  CALL_FUNCTION_1       1  '1 positional argument'
              796  LOAD_FAST                'self'
              798  LOAD_ATTR                _words
              800  LOAD_FAST                'i'
              802  LOAD_CONST               1
              804  BINARY_SUBTRACT  
              806  BINARY_SUBSCR    
              808  LOAD_STR                 'word'
              810  STORE_SUBSCR     

 L.1391       812  LOAD_STR                 'mile per hour'
              814  LOAD_FAST                'self'
              816  LOAD_ATTR                _words
              818  LOAD_FAST                'i'
              820  BINARY_SUBSCR    
              822  LOAD_STR                 'word'
              824  STORE_SUBSCR     
              826  JUMP_FORWARD       1050  'to 1050'
            828_0  COME_FROM           778  '778'

 L.1392       828  LOAD_FAST                'unit'
              830  LOAD_STR                 'hectera'
              832  COMPARE_OP               ==
          834_836  POP_JUMP_IF_FALSE   884  'to 884'

 L.1393       838  LOAD_GLOBAL              str
              840  LOAD_GLOBAL              float
              842  LOAD_FAST                'numb'
              844  CALL_FUNCTION_1       1  '1 positional argument'
              846  LOAD_CONST               2.47105
              848  BINARY_MULTIPLY  
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  LOAD_FAST                'self'
              854  LOAD_ATTR                _words
              856  LOAD_FAST                'i'
              858  LOAD_CONST               1
              860  BINARY_SUBTRACT  
              862  BINARY_SUBSCR    
              864  LOAD_STR                 'word'
              866  STORE_SUBSCR     

 L.1394       868  LOAD_STR                 'acre'
              870  LOAD_FAST                'self'
              872  LOAD_ATTR                _words
              874  LOAD_FAST                'i'
              876  BINARY_SUBSCR    
              878  LOAD_STR                 'word'
              880  STORE_SUBSCR     
              882  JUMP_FORWARD       1050  'to 1050'
            884_0  COME_FROM           834  '834'

 L.1395       884  LOAD_FAST                'unit'
              886  LOAD_STR                 'tonne'
              888  COMPARE_OP               ==
          890_892  POP_JUMP_IF_FALSE   940  'to 940'

 L.1396       894  LOAD_GLOBAL              str
              896  LOAD_GLOBAL              float
              898  LOAD_FAST                'numb'
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  LOAD_CONST               1.10231
              904  BINARY_MULTIPLY  
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  LOAD_FAST                'self'
              910  LOAD_ATTR                _words
              912  LOAD_FAST                'i'
              914  LOAD_CONST               1
              916  BINARY_SUBTRACT  
              918  BINARY_SUBSCR    
              920  LOAD_STR                 'word'
              922  STORE_SUBSCR     

 L.1397       924  LOAD_STR                 'ton'
              926  LOAD_FAST                'self'
              928  LOAD_ATTR                _words
              930  LOAD_FAST                'i'
              932  BINARY_SUBSCR    
              934  LOAD_STR                 'word'
              936  STORE_SUBSCR     
              938  JUMP_FORWARD       1050  'to 1050'
            940_0  COME_FROM           890  '890'

 L.1398       940  LOAD_FAST                'unit'
              942  LOAD_STR                 'cubic meter'
              944  COMPARE_OP               ==
          946_948  POP_JUMP_IF_FALSE   996  'to 996'

 L.1399       950  LOAD_GLOBAL              str
              952  LOAD_GLOBAL              float
              954  LOAD_FAST                'numb'
              956  CALL_FUNCTION_1       1  '1 positional argument'
              958  LOAD_CONST               35.3147
              960  BINARY_MULTIPLY  
              962  CALL_FUNCTION_1       1  '1 positional argument'
              964  LOAD_FAST                'self'
              966  LOAD_ATTR                _words
              968  LOAD_FAST                'i'
              970  LOAD_CONST               1
              972  BINARY_SUBTRACT  
              974  BINARY_SUBSCR    
              976  LOAD_STR                 'word'
              978  STORE_SUBSCR     

 L.1400       980  LOAD_STR                 'cubic foot'
              982  LOAD_FAST                'self'
              984  LOAD_ATTR                _words
              986  LOAD_FAST                'i'
              988  BINARY_SUBSCR    
              990  LOAD_STR                 'word'
              992  STORE_SUBSCR     
              994  JUMP_FORWARD       1050  'to 1050'
            996_0  COME_FROM           946  '946'

 L.1401       996  LOAD_FAST                'unit'
              998  LOAD_STR                 'square kilometer'
             1000  COMPARE_OP               ==
         1002_1004  POP_JUMP_IF_FALSE  1898  'to 1898'

 L.1402      1006  LOAD_GLOBAL              str
             1008  LOAD_GLOBAL              float
             1010  LOAD_FAST                'numb'
             1012  CALL_FUNCTION_1       1  '1 positional argument'
             1014  LOAD_CONST               0.386102
             1016  BINARY_MULTIPLY  
             1018  CALL_FUNCTION_1       1  '1 positional argument'
             1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                _words
             1024  LOAD_FAST                'i'
             1026  LOAD_CONST               1
             1028  BINARY_SUBTRACT  
             1030  BINARY_SUBSCR    
             1032  LOAD_STR                 'word'
             1034  STORE_SUBSCR     

 L.1403      1036  LOAD_STR                 'square mile'
             1038  LOAD_FAST                'self'
             1040  LOAD_ATTR                _words
             1042  LOAD_FAST                'i'
             1044  BINARY_SUBSCR    
             1046  LOAD_STR                 'word'
             1048  STORE_SUBSCR     
           1050_0  COME_FROM           994  '994'
           1050_1  COME_FROM           938  '938'
           1050_2  COME_FROM           882  '882'
           1050_3  COME_FROM           826  '826'
             1050  JUMP_BACK            40  'to 40'
           1052_0  COME_FROM           134  '134'

 L.1404      1052  LOAD_FAST                'self'
             1054  LOAD_ATTR                _metric
             1056  LOAD_CONST               True
             1058  COMPARE_OP               ==
             1060  POP_JUMP_IF_FALSE    40  'to 40'

 L.1405      1062  LOAD_FAST                'unit'
             1064  LOAD_STR                 'inch'
             1066  COMPARE_OP               ==
         1068_1070  POP_JUMP_IF_FALSE  1118  'to 1118'

 L.1406      1072  LOAD_GLOBAL              str
             1074  LOAD_GLOBAL              float
             1076  LOAD_FAST                'numb'
             1078  CALL_FUNCTION_1       1  '1 positional argument'
             1080  LOAD_CONST               2.54
             1082  BINARY_MULTIPLY  
             1084  CALL_FUNCTION_1       1  '1 positional argument'
             1086  LOAD_FAST                'self'
             1088  LOAD_ATTR                _words
             1090  LOAD_FAST                'i'
             1092  LOAD_CONST               1
             1094  BINARY_SUBTRACT  
             1096  BINARY_SUBSCR    
             1098  LOAD_STR                 'word'
             1100  STORE_SUBSCR     

 L.1407      1102  LOAD_STR                 'centimeter'
             1104  LOAD_FAST                'self'
             1106  LOAD_ATTR                _words
             1108  LOAD_FAST                'i'
             1110  BINARY_SUBSCR    
             1112  LOAD_STR                 'word'
             1114  STORE_SUBSCR     
             1116  JUMP_BACK            40  'to 40'
           1118_0  COME_FROM          1068  '1068'

 L.1408      1118  LOAD_FAST                'unit'
             1120  LOAD_STR                 'foot'
             1122  COMPARE_OP               ==
         1124_1126  POP_JUMP_IF_FALSE  1174  'to 1174'

 L.1409      1128  LOAD_GLOBAL              str
             1130  LOAD_GLOBAL              float
             1132  LOAD_FAST                'numb'
             1134  CALL_FUNCTION_1       1  '1 positional argument'
             1136  LOAD_CONST               0.3048
             1138  BINARY_MULTIPLY  
             1140  CALL_FUNCTION_1       1  '1 positional argument'
             1142  LOAD_FAST                'self'
             1144  LOAD_ATTR                _words
             1146  LOAD_FAST                'i'
             1148  LOAD_CONST               1
             1150  BINARY_SUBTRACT  
             1152  BINARY_SUBSCR    
             1154  LOAD_STR                 'word'
             1156  STORE_SUBSCR     

 L.1410      1158  LOAD_STR                 'meter'
             1160  LOAD_FAST                'self'
             1162  LOAD_ATTR                _words
             1164  LOAD_FAST                'i'
             1166  BINARY_SUBSCR    
             1168  LOAD_STR                 'word'
             1170  STORE_SUBSCR     
             1172  JUMP_BACK            40  'to 40'
           1174_0  COME_FROM          1124  '1124'

 L.1411      1174  LOAD_FAST                'unit'
             1176  LOAD_STR                 'yard'
             1178  COMPARE_OP               ==
         1180_1182  POP_JUMP_IF_FALSE  1230  'to 1230'

 L.1412      1184  LOAD_GLOBAL              str
             1186  LOAD_GLOBAL              float
             1188  LOAD_FAST                'numb'
             1190  CALL_FUNCTION_1       1  '1 positional argument'
             1192  LOAD_CONST               0.9144
             1194  BINARY_MULTIPLY  
             1196  CALL_FUNCTION_1       1  '1 positional argument'
             1198  LOAD_FAST                'self'
             1200  LOAD_ATTR                _words
             1202  LOAD_FAST                'i'
             1204  LOAD_CONST               1
             1206  BINARY_SUBTRACT  
             1208  BINARY_SUBSCR    
             1210  LOAD_STR                 'word'
             1212  STORE_SUBSCR     

 L.1413      1214  LOAD_STR                 'meter'
             1216  LOAD_FAST                'self'
             1218  LOAD_ATTR                _words
             1220  LOAD_FAST                'i'
             1222  BINARY_SUBSCR    
             1224  LOAD_STR                 'word'
             1226  STORE_SUBSCR     
             1228  JUMP_BACK            40  'to 40'
           1230_0  COME_FROM          1180  '1180'

 L.1414      1230  LOAD_FAST                'unit'
             1232  LOAD_STR                 'mile'
             1234  COMPARE_OP               ==
         1236_1238  POP_JUMP_IF_FALSE  1286  'to 1286'

 L.1415      1240  LOAD_GLOBAL              str
             1242  LOAD_GLOBAL              float
             1244  LOAD_FAST                'numb'
             1246  CALL_FUNCTION_1       1  '1 positional argument'
             1248  LOAD_CONST               1.60934
             1250  BINARY_MULTIPLY  
             1252  CALL_FUNCTION_1       1  '1 positional argument'
             1254  LOAD_FAST                'self'
             1256  LOAD_ATTR                _words
             1258  LOAD_FAST                'i'
             1260  LOAD_CONST               1
             1262  BINARY_SUBTRACT  
             1264  BINARY_SUBSCR    
             1266  LOAD_STR                 'word'
             1268  STORE_SUBSCR     

 L.1416      1270  LOAD_STR                 'kilometer'
             1272  LOAD_FAST                'self'
             1274  LOAD_ATTR                _words
             1276  LOAD_FAST                'i'
             1278  BINARY_SUBSCR    
             1280  LOAD_STR                 'word'
             1282  STORE_SUBSCR     
             1284  JUMP_BACK            40  'to 40'
           1286_0  COME_FROM          1236  '1236'

 L.1417      1286  LOAD_FAST                'unit'
             1288  LOAD_STR                 'ounce'
             1290  COMPARE_OP               ==
         1292_1294  POP_JUMP_IF_FALSE  1342  'to 1342'

 L.1418      1296  LOAD_GLOBAL              str
             1298  LOAD_GLOBAL              float
             1300  LOAD_FAST                'numb'
             1302  CALL_FUNCTION_1       1  '1 positional argument'
             1304  LOAD_CONST               0.0295735
             1306  BINARY_MULTIPLY  
             1308  CALL_FUNCTION_1       1  '1 positional argument'
             1310  LOAD_FAST                'self'
             1312  LOAD_ATTR                _words
             1314  LOAD_FAST                'i'
             1316  LOAD_CONST               1
             1318  BINARY_SUBTRACT  
             1320  BINARY_SUBSCR    
             1322  LOAD_STR                 'word'
             1324  STORE_SUBSCR     

 L.1419      1326  LOAD_STR                 'liter'
             1328  LOAD_FAST                'self'
             1330  LOAD_ATTR                _words
             1332  LOAD_FAST                'i'
             1334  BINARY_SUBSCR    
             1336  LOAD_STR                 'word'
             1338  STORE_SUBSCR     
             1340  JUMP_BACK            40  'to 40'
           1342_0  COME_FROM          1292  '1292'

 L.1420      1342  LOAD_FAST                'unit'
             1344  LOAD_STR                 'cup'
             1346  COMPARE_OP               ==
         1348_1350  POP_JUMP_IF_FALSE  1398  'to 1398'

 L.1421      1352  LOAD_GLOBAL              str
             1354  LOAD_GLOBAL              float
             1356  LOAD_FAST                'numb'
             1358  CALL_FUNCTION_1       1  '1 positional argument'
             1360  LOAD_CONST               0.236588
             1362  BINARY_MULTIPLY  
             1364  CALL_FUNCTION_1       1  '1 positional argument'
             1366  LOAD_FAST                'self'
             1368  LOAD_ATTR                _words
             1370  LOAD_FAST                'i'
             1372  LOAD_CONST               1
             1374  BINARY_SUBTRACT  
             1376  BINARY_SUBSCR    
             1378  LOAD_STR                 'word'
             1380  STORE_SUBSCR     

 L.1422      1382  LOAD_STR                 'liter'
             1384  LOAD_FAST                'self'
             1386  LOAD_ATTR                _words
             1388  LOAD_FAST                'i'
             1390  BINARY_SUBSCR    
             1392  LOAD_STR                 'word'
             1394  STORE_SUBSCR     
             1396  JUMP_BACK            40  'to 40'
           1398_0  COME_FROM          1348  '1348'

 L.1423      1398  LOAD_FAST                'unit'
             1400  LOAD_STR                 'pint'
             1402  COMPARE_OP               ==
         1404_1406  POP_JUMP_IF_FALSE  1454  'to 1454'

 L.1424      1408  LOAD_GLOBAL              str
             1410  LOAD_GLOBAL              float
             1412  LOAD_FAST                'numb'
             1414  CALL_FUNCTION_1       1  '1 positional argument'
             1416  LOAD_CONST               0.473176
             1418  BINARY_MULTIPLY  
             1420  CALL_FUNCTION_1       1  '1 positional argument'
             1422  LOAD_FAST                'self'
             1424  LOAD_ATTR                _words
             1426  LOAD_FAST                'i'
             1428  LOAD_CONST               1
             1430  BINARY_SUBTRACT  
             1432  BINARY_SUBSCR    
             1434  LOAD_STR                 'word'
             1436  STORE_SUBSCR     

 L.1425      1438  LOAD_STR                 'liter'
             1440  LOAD_FAST                'self'
             1442  LOAD_ATTR                _words
             1444  LOAD_FAST                'i'
             1446  BINARY_SUBSCR    
             1448  LOAD_STR                 'word'
             1450  STORE_SUBSCR     
             1452  JUMP_BACK            40  'to 40'
           1454_0  COME_FROM          1404  '1404'

 L.1426      1454  LOAD_FAST                'unit'
             1456  LOAD_STR                 'gallon'
             1458  COMPARE_OP               ==
         1460_1462  POP_JUMP_IF_FALSE  1510  'to 1510'

 L.1427      1464  LOAD_GLOBAL              str
             1466  LOAD_GLOBAL              float
             1468  LOAD_FAST                'numb'
             1470  CALL_FUNCTION_1       1  '1 positional argument'
             1472  LOAD_CONST               3.78541
             1474  BINARY_MULTIPLY  
             1476  CALL_FUNCTION_1       1  '1 positional argument'
             1478  LOAD_FAST                'self'
             1480  LOAD_ATTR                _words
             1482  LOAD_FAST                'i'
             1484  LOAD_CONST               1
             1486  BINARY_SUBTRACT  
             1488  BINARY_SUBSCR    
             1490  LOAD_STR                 'word'
             1492  STORE_SUBSCR     

 L.1428      1494  LOAD_STR                 'liter'
             1496  LOAD_FAST                'self'
             1498  LOAD_ATTR                _words
             1500  LOAD_FAST                'i'
             1502  BINARY_SUBSCR    
             1504  LOAD_STR                 'word'
             1506  STORE_SUBSCR     
             1508  JUMP_BACK            40  'to 40'
           1510_0  COME_FROM          1460  '1460'

 L.1429      1510  LOAD_FAST                'unit'
             1512  LOAD_STR                 'pound'
             1514  COMPARE_OP               ==
         1516_1518  POP_JUMP_IF_FALSE  1566  'to 1566'

 L.1430      1520  LOAD_GLOBAL              str
             1522  LOAD_GLOBAL              float
             1524  LOAD_FAST                'numb'
             1526  CALL_FUNCTION_1       1  '1 positional argument'
             1528  LOAD_CONST               0.453592
             1530  BINARY_MULTIPLY  
             1532  CALL_FUNCTION_1       1  '1 positional argument'
             1534  LOAD_FAST                'self'
             1536  LOAD_ATTR                _words
             1538  LOAD_FAST                'i'
             1540  LOAD_CONST               1
             1542  BINARY_SUBTRACT  
             1544  BINARY_SUBSCR    
             1546  LOAD_STR                 'word'
             1548  STORE_SUBSCR     

 L.1431      1550  LOAD_STR                 'kilogram'
             1552  LOAD_FAST                'self'
             1554  LOAD_ATTR                _words
             1556  LOAD_FAST                'i'
             1558  BINARY_SUBSCR    
             1560  LOAD_STR                 'word'
             1562  STORE_SUBSCR     
             1564  JUMP_BACK            40  'to 40'
           1566_0  COME_FROM          1516  '1516'

 L.1432      1566  LOAD_FAST                'unit'
             1568  LOAD_STR                 'ton'
             1570  COMPARE_OP               ==
         1572_1574  POP_JUMP_IF_FALSE  1622  'to 1622'

 L.1433      1576  LOAD_GLOBAL              str
             1578  LOAD_GLOBAL              float
             1580  LOAD_FAST                'numb'
             1582  CALL_FUNCTION_1       1  '1 positional argument'
             1584  LOAD_CONST               0.907185
             1586  BINARY_MULTIPLY  
             1588  CALL_FUNCTION_1       1  '1 positional argument'
             1590  LOAD_FAST                'self'
             1592  LOAD_ATTR                _words
             1594  LOAD_FAST                'i'
             1596  LOAD_CONST               1
             1598  BINARY_SUBTRACT  
             1600  BINARY_SUBSCR    
             1602  LOAD_STR                 'word'
             1604  STORE_SUBSCR     

 L.1434      1606  LOAD_STR                 'tonne'
             1608  LOAD_FAST                'self'
             1610  LOAD_ATTR                _words
             1612  LOAD_FAST                'i'
             1614  BINARY_SUBSCR    
             1616  LOAD_STR                 'word'
             1618  STORE_SUBSCR     
             1620  JUMP_BACK            40  'to 40'
           1622_0  COME_FROM          1572  '1572'

 L.1435      1622  LOAD_FAST                'unit'
             1624  LOAD_STR                 'square foot'
             1626  COMPARE_OP               ==
         1628_1630  POP_JUMP_IF_FALSE  1678  'to 1678'

 L.1436      1632  LOAD_GLOBAL              str
             1634  LOAD_GLOBAL              float
             1636  LOAD_FAST                'numb'
             1638  CALL_FUNCTION_1       1  '1 positional argument'
             1640  LOAD_CONST               0.092903
             1642  BINARY_MULTIPLY  
             1644  CALL_FUNCTION_1       1  '1 positional argument'
             1646  LOAD_FAST                'self'
             1648  LOAD_ATTR                _words
             1650  LOAD_FAST                'i'
             1652  LOAD_CONST               1
             1654  BINARY_SUBTRACT  
             1656  BINARY_SUBSCR    
             1658  LOAD_STR                 'word'
             1660  STORE_SUBSCR     

 L.1437      1662  LOAD_STR                 'square meter'
             1664  LOAD_FAST                'self'
             1666  LOAD_ATTR                _words
             1668  LOAD_FAST                'i'
             1670  BINARY_SUBSCR    
             1672  LOAD_STR                 'word'
             1674  STORE_SUBSCR     
             1676  JUMP_BACK            40  'to 40'
           1678_0  COME_FROM          1628  '1628'

 L.1438      1678  LOAD_FAST                'unit'
             1680  LOAD_STR                 'square mile'
             1682  COMPARE_OP               ==
         1684_1686  POP_JUMP_IF_FALSE  1734  'to 1734'

 L.1439      1688  LOAD_GLOBAL              str
             1690  LOAD_GLOBAL              float
             1692  LOAD_FAST                'numb'
             1694  CALL_FUNCTION_1       1  '1 positional argument'
             1696  LOAD_CONST               2.58999
             1698  BINARY_MULTIPLY  
             1700  CALL_FUNCTION_1       1  '1 positional argument'
             1702  LOAD_FAST                'self'
             1704  LOAD_ATTR                _words
             1706  LOAD_FAST                'i'
             1708  LOAD_CONST               1
             1710  BINARY_SUBTRACT  
             1712  BINARY_SUBSCR    
             1714  LOAD_STR                 'word'
             1716  STORE_SUBSCR     

 L.1440      1718  LOAD_STR                 'square kilometer'
             1720  LOAD_FAST                'self'
             1722  LOAD_ATTR                _words
             1724  LOAD_FAST                'i'
             1726  BINARY_SUBSCR    
             1728  LOAD_STR                 'word'
             1730  STORE_SUBSCR     
             1732  JUMP_BACK            40  'to 40'
           1734_0  COME_FROM          1684  '1684'

 L.1441      1734  LOAD_FAST                'unit'
             1736  LOAD_STR                 'acre'
             1738  COMPARE_OP               ==
         1740_1742  POP_JUMP_IF_FALSE  1790  'to 1790'

 L.1442      1744  LOAD_GLOBAL              str
             1746  LOAD_GLOBAL              float
             1748  LOAD_FAST                'numb'
             1750  CALL_FUNCTION_1       1  '1 positional argument'
             1752  LOAD_CONST               0.404686
             1754  BINARY_MULTIPLY  
             1756  CALL_FUNCTION_1       1  '1 positional argument'
             1758  LOAD_FAST                'self'
             1760  LOAD_ATTR                _words
             1762  LOAD_FAST                'i'
             1764  LOAD_CONST               1
             1766  BINARY_SUBTRACT  
             1768  BINARY_SUBSCR    
             1770  LOAD_STR                 'word'
             1772  STORE_SUBSCR     

 L.1443      1774  LOAD_STR                 'hectera'
             1776  LOAD_FAST                'self'
             1778  LOAD_ATTR                _words
             1780  LOAD_FAST                'i'
             1782  BINARY_SUBSCR    
             1784  LOAD_STR                 'word'
             1786  STORE_SUBSCR     
             1788  JUMP_BACK            40  'to 40'
           1790_0  COME_FROM          1740  '1740'

 L.1444      1790  LOAD_FAST                'unit'
             1792  LOAD_STR                 'mile per hour'
             1794  COMPARE_OP               ==
         1796_1798  POP_JUMP_IF_FALSE  1846  'to 1846'

 L.1445      1800  LOAD_GLOBAL              str
             1802  LOAD_GLOBAL              float
             1804  LOAD_FAST                'numb'
             1806  CALL_FUNCTION_1       1  '1 positional argument'
             1808  LOAD_CONST               1.60934
             1810  BINARY_MULTIPLY  
             1812  CALL_FUNCTION_1       1  '1 positional argument'
             1814  LOAD_FAST                'self'
             1816  LOAD_ATTR                _words
             1818  LOAD_FAST                'i'
             1820  LOAD_CONST               1
             1822  BINARY_SUBTRACT  
             1824  BINARY_SUBSCR    
             1826  LOAD_STR                 'word'
             1828  STORE_SUBSCR     

 L.1446      1830  LOAD_STR                 'kilometer per hour'
             1832  LOAD_FAST                'self'
             1834  LOAD_ATTR                _words
             1836  LOAD_FAST                'i'
             1838  BINARY_SUBSCR    
             1840  LOAD_STR                 'word'
             1842  STORE_SUBSCR     
             1844  JUMP_BACK            40  'to 40'
           1846_0  COME_FROM          1796  '1796'

 L.1447      1846  LOAD_FAST                'unit'
             1848  LOAD_STR                 'knot'
             1850  COMPARE_OP               ==
             1852  POP_JUMP_IF_FALSE    40  'to 40'

 L.1448      1854  LOAD_GLOBAL              str
             1856  LOAD_GLOBAL              float
             1858  LOAD_FAST                'numb'
             1860  CALL_FUNCTION_1       1  '1 positional argument'
             1862  LOAD_CONST               1.852
             1864  BINARY_MULTIPLY  
             1866  CALL_FUNCTION_1       1  '1 positional argument'
             1868  LOAD_FAST                'self'
             1870  LOAD_ATTR                _words
             1872  LOAD_FAST                'i'
             1874  LOAD_CONST               1
             1876  BINARY_SUBTRACT  
             1878  BINARY_SUBSCR    
             1880  LOAD_STR                 'word'
             1882  STORE_SUBSCR     

 L.1449      1884  LOAD_STR                 'kilometer per hour'
             1886  LOAD_FAST                'self'
             1888  LOAD_ATTR                _words
             1890  LOAD_FAST                'i'
             1892  BINARY_SUBSCR    
             1894  LOAD_STR                 'word'
             1896  STORE_SUBSCR     
           1898_0  COME_FROM          1002  '1002'
             1898  JUMP_BACK            40  'to 40'
             1900  POP_BLOCK        
           1902_0  COME_FROM_LOOP       26  '26'

Parse error at or near `POP_BLOCK' instruction at offset 1900

    def _partsofspeech(self):
        """ Do Parts of Speech Tagging """
        l = len(self._words)
        for i in range(l):
            self._words[i]['pos'] = pos_tag([self._words[i]['word']])[0][1]

    @property
    def bagOfWords(self):
        """ Generate/return Bag of Words """
        if self._bow is None:
            self._bow = {}
            for word in self._words:
                if word['word'] in self._bow:
                    self._bow[word['word']] += 1
                else:
                    self._bow[word['word']] = 1

        return self._bow

    @property
    def freqDist(self):
        """ Generate / return frequency distribution """
        if self._freq is None:
            self._freq = sorted((self.bagOfWords.items()), key=(lambda x: x[1]), reverse=True)
        return self._freq

    @property
    def termFreq(self):
        """ Generate / return term frequencies """
        if self._tf is None:
            nwords = len(self)
            self._tf = []
            for t in self.freqDist:
                self._tf.append((t[0], t[1] / nwords))

        return self._tf

    def __len__(self):
        """ Override the len() operator - get the number of tokenized words """
        if self._words is None:
            return 0
        return len(self._words)

    def __iadd__(self, words):
        """ Override the += operator """
        if words is None:
            return self
        elif isinstance(words, str):
            pass
        elif isinstance(words, list):
            if self._words is None:
                self._words = words
            else:
                self._words += words
        else:
            raise TypeError('String or List expected for words')
        return self


import lg.word2int_en as word2int_en
import lg.word2int_fr as word2int_fr
import lg.word2int_es as word2int_es
import lg.word2int_it as word2int_it
import lg.word2int_de as word2int_de

class Norvig(object):
    __doc__ = ' \n    https://norvig.com/spell-correct.html\n    \n    Enhanced version of the Norvig spell checker. Enhancements designed by Andrew Ferlitsch and coded by David Molina.\n    In the original Norvig spell checker, guess of what would be the next character replacement to try was in alphabetical order.\n    In this enhancement, the next character is based on the QWERTY keyboard layout and the likelihood that the hand shifted one key.\n    '

    def __init__(self, lang='en'):
        global word2int_de
        global word2int_en
        global word2int_es
        global word2int_fr
        global word2int_it
        if lang == 'en':
            self.word2int = word2int_en
        else:
            if lang == 'es':
                self.word2int = word2int_es
            else:
                if lang == 'fr':
                    self.word2int = word2int_fr
                else:
                    if lang == 'it':
                        self.word2int = word2int_it
                    else:
                        if lang == 'de':
                            self.word2int = word2int_de

    def known(self, words):
        """The subset of `words` that appear in the dictionary of WORDS."""
        return set((w for w in words if w in self.word2int))

    def edits1(self, word):
        """All edits that are one edit away from `word`."""
        letters = {'a':'asqzbcdefghijklmnoprtuvwxy', 
         'b':'bnvghacdefijklmopqrstuwxyz', 
         'c':'cvxdfabeghijklmnopqrstuwyz', 
         'd':'dfsexcabghijklmnopqrtuvwyz', 
         'e':'erwsdabcfghijklmnopqtuvxyz', 
         'f':'fgdrcvabehijklmnopqstuwxyz', 
         'g':'ghftvbacdeijklmnopqrsuwxyz', 
         'h':'hjgybnacdefiklmopqrstuvwxz', 
         'i':'ioujkabcdefghlmnpqrstvwxyz', 
         'j':'jkhunmabcdefgilopqrstvwxyz', 
         'k':'kljimabcdefghnopqrstuvwxyz', 
         'l':'lkoabcdefghijmnpqrstuvwxyz', 
         'm':'mnjkabcdefghilopqrstuvwxyz', 
         'n':'nmbhjacdefgiklopqrstuvwxyz', 
         'o':'opiklabcdefghjmnqrstuvwxyz', 
         'p':'polabcdefghijkmnqrstuvwxyz', 
         'q':'qwabcdefghijklmnoprstuvxyz', 
         'r':'rtedfabcghijklmnopqsuvwxyz', 
         's':'sdawzxbcefghijklmnopqrtuvy', 
         't':'tyrfgabcdehijklmnopqsuvwxz', 
         'u':'uiyhjabcdefgklmnopqrstvwxz', 
         'v':'vbcfgadehijklmnopqrstuwxyz', 
         'w':'weqasbcdfghijklmnoprtuvxyz', 
         'x':'xczsdabefghijklmnopqrtuvwy', 
         'y':'yutghabcdefijklmnopqrsvwxz', 
         'z':'zxasbcdefghijklmnopqrtuvwy'}
        splits = [(word[:i], word[i:]) for i in range(1, len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters[R[0]]]
        inserts = [L + c + R for L, R in splits if R for c in letters[R[0]]]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """All edits that are two edits away from `word`."""
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def candidates(self, word):
        """Generate possible spelling corrections for word."""
        return self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word]

    def correction(self, word):
        k = self.candidates(word)
        return k.pop()

    def encode(self, word):
        k = self.candidates(word)
        word = k.pop()
        try:
            intval = self.word2int[word]
            return (word, intval)
        except:
            return (
             '<OUT>', self.word2int['<OUT>'])