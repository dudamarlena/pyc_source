# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gapml/splitter.py
# Compiled at: 2018-08-31 14:33:57
# Size of source mod 2**32: 30726 bytes
""" Splitter Module for Processing PDF Documents
Copyright, 2018(c), Andrew Ferlitsch
"""
version = '0.9.2'
import os.path, re, threading, time, shutil, glob, sys, json, shutil
from .segment import Segment
from .syntax import Words, Vocabulary, Norvig
from .pdf_res import PDFResource
import lg.word2int_en as word2int_en
import lg.word2int_fr as word2int_fr
import lg.word2int_es as word2int_es
import lg.word2int_it as word2int_it
import lg.word2int_de as word2int_de
if shutil.which('gswin64c'):
    GHOSTSCRIPT = 'gswin64c'
else:
    if shutil.which('gswin32c'):
        GHOSTSCRIPT = 'gswin32c'
    else:
        if shutil.which('gs'):
            GHOSTSCRIPT = 'gs'
        else:
            GHOSTSCRIPT = 'gs'
TESSERACT = 'tesseract'
MAGICK = 'magick'

class Document(object):
    __doc__ = ' Base (super) Class for Classifying a Document '
    RESOLUTION = 300
    SCANCHECK = 20
    WORDDICT = 'norvig'

    def __init__(self, document=None, dir='./', ehandler=None, config=None):
        """ Constructor for document object
        document - - path to the document
        dir - directory where to store extracted pages and text
        """
        self._document = document
        self._name = None
        self._label = None
        self._pages = []
        self._dir = dir
        self._type = None
        self._size = 0
        self._ehandler = ehandler
        self._time = 0
        self._scanned = False
        self._quality = 0
        self._segment = False
        self._bow = None
        self._freq = None
        self._tf = None
        self._lang = 'en'
        if dir is not None:
            if isinstance(dir, str) == False:
                raise TypeError('String expected for page directory path')
        if config is not None:
            if isinstance(config, list) == False:
                raise TypeError('List expected for config settings')
        else:
            if config is not None:
                for setting in config:
                    if isinstance(setting, str) == False:
                        raise TypeError('String expected for each config setting')
                    if setting == 'bare':
                        Page.BARE = True
                    elif setting == 'pos':
                        Page.POS = True
                    elif setting == 'roman':
                        Page.ROMAN = True
                    elif setting == 'segment':
                        self._segment = True
                    elif setting.startswith('stem'):
                        vals = setting.split('=')
                        if len(vals) == 2:
                            if vals[1] in ('gap', 'porter', 'snowball', 'lancaster',
                                           'lemma'):
                                Page.STEM = vals[1]
                            else:
                                raise AttributeError('Setting stem set to an invalid value: ' + vals[1])
                        else:
                            raise AttributeError('Setting stem not assigned to a value')
                    elif setting.startswith('spell'):
                        vals = setting.split('=')
                        if len(vals) == 2:
                            if vals[1] in ('norvig', ):
                                Page.SPELL = vals[1]
                            else:
                                raise AttributeError('Setting spell set to an invalid value: ' + vals[1])
                        else:
                            raise AttributeError('Setting spell not assigned to a value')
                    else:
                        raise AttributeError('Setting is not recognized: ' + setting)

            if self._document is not None:
                self._exist()
                if ehandler is None:
                    self._collate(dir)
                else:
                    t = threading.Thread(target=(self._async), args=(dir,))
                    t.start()

    def _async(self, dir):
        """ Asynchronous processing of the document """
        self._collate(dir)
        self._ehandler(self)

    def _exist(self):
        """ Check if document exists """
        if isinstance(self._document, str) == False:
            raise TypeError('String expected for document name')
        else:
            if os.path.isfile(self._document) == False:
                raise FileNotFoundError(self._document)
            basename = os.path.splitext(os.path.basename(self._document))
            self._name = basename[0]
            self._type = basename[1][1:].lower()
            self._size = os.path.getsize(self._document)
            if self._size == 0:
                raise IOError('The document is an empty file')
            if self._type == 'pdf' and self._size < 100:
                raise IOError('The document is too small for a PDF document')

    def _collate(self, dir='./'):
        """ split document into pages and extract text
        dir - the directory where to store the split pages (defaults to current directory)
        """
        start = time.time()
        if dir.endswith('/') == False:
            dir += '/'
        else:
            self._dir = dir
            if dir != './':
                if os.path.isdir(dir) == False:
                    os.mkdir(dir)
            if self._type == 'txt':
                text_file = dir + self._name + '1.txt'
                with open((self._document), 'r', encoding='utf-8') as (f):
                    text = f.read()
                with open(text_file, 'w', encoding='utf-8') as (f):
                    f.write(text)
                if self._segment:
                    segment = Segment(text)
                    text = segment.segments
                page = Page(text_file, text, 1)
                self.__iadd__(page)
                json_file = dir + self._name + '1.json'
                page.store(json_file)
            else:
                if self._type == 'png' or self._type == 'jpg':
                    img_file = dir + self._name + '1.' + self._type
                    shutil.copy2(self._document, img_file)
                    text_file = dir + self._name + '1.txt'
                    os.system(TESSERACT + ' ' + img_file + ' ' + dir + self._name + '1' + ' >nul 2>&1')
                    with open(text_file, 'r', encoding='utf-8') as (f):
                        text = f.read()
                    if self._segment:
                        segment = Segment(text)
                        text = segment.segments
                    page = Page(img_file, text, 1)
                    self.__iadd__(page)
                    json_file = dir + self._name + '1.json'
                    page.store(json_file)
                    self._scanned = True
                else:
                    if self._type == 'pdf':
                        os.system(GHOSTSCRIPT + ' -dBATCH -q -dNODISPLAY -c "("' + self.document + '") (r) file runpdfbegin pdfpagecount = quit" >tmp.tmp')
                        with open('tmp.tmp', 'r') as (f):
                            npages = int(f.read())
                        os.remove('tmp.tmp')
                        for n in range(npages):
                            pdf_file = dir + self._name + str(n + 1) + '.pdf'
                            os.system(GHOSTSCRIPT + ' -dBATCH -dNOPAUSE -sOutputFile=' + pdf_file + ' -sPageList=' + str(n + 1) + ' -sDEVICE=pdfwrite ' + self.document + ' >nul')
                            if n == 0:
                                res = PDFResource(pdf_file)
                                if res.image == True:
                                    if res.text == False:
                                        self._scanned = True
                            else:
                                text_file = dir + self._name + str(n + 1) + '.txt'
                                if self._scanned == True:
                                    image_file = dir + self._name + str(n + 1) + '.png'
                                    os.system(GHOSTSCRIPT + ' -dBATCH -dNOPAUSE -sOutputFile=' + image_file + ' -sPageList=1 -sDEVICE=pnggray -r' + str(self.RESOLUTION) + ' ' + dir + self._name + str(n + 1) + '.pdf >nul')
                                    os.system(TESSERACT + ' ' + image_file + ' ' + dir + self._name + str(n + 1) + ' >nul 2>&1')
                                else:
                                    os.system(GHOSTSCRIPT + ' -dBATCH -dNOPAUSE -sOutputFile=' + text_file + ' -sPageList=1 -sDEVICE=txtwrite ' + dir + self._name + str(n + 1) + '.pdf >nul')
                            with open(text_file, 'r', encoding='utf-8') as (f):
                                text = f.read()
                                if self._segment:
                                    segment = Segment(text)
                                    text = segment.segments
                                page = Page(pdf_file, text, n + 1)
                                json_file = dir + self._name + str(n + 1) + '.json'
                                page.store(json_file)
                                self.__iadd__(page)
                                if n == 0 and self._scanned == False and not self._pages[0].size == 0:
                                    if self._pages[0].text[0] == '\x01':
                                        image_file = dir + self._name + str(n + 1) + '.png'
                                        os.system(GHOSTSCRIPT + ' -dBATCH -dNOPAUSE -sOutputFile=' + image_file + ' -sPageList=1 -sDEVICE=pnggray -r' + str(self.RESOLUTION) + ' ' + dir + self._name + str(n + 1) + '.pdf >nul')
                                        os.system(TESSERACT + ' ' + image_file + ' ' + dir + self._name + str(n + 1) + ' >nul 2>&1')
                                        with open(text_file, 'r', encoding='utf-8') as (f):
                                            self.pages[n] = Page(pdf_file, f.read(), n + 1)
                                            page.store(json_file)
                                        self._scanned = True

                    else:
                        if self._type == 'tif' or self._type == 'tiff':
                            os.system(MAGICK + ' ' + self.document + ' ' + dir + self._name + '%d.tif')
                            files = glob.glob(dir + self._name + '*.tif')
                            npages = 0
                            for file in files:
                                if file.replace('\\', '/') != self._document:
                                    npages += 1

                            for n in range(npages, 0, -1):
                                os.rename(dir + self._name + str(n - 1) + '.tif', dir + self._name + str(n) + '.tif')

                            for n in range(npages):
                                tif_file = dir + self._name + str(n + 1) + '.tif'
                                text_file = dir + self._name + str(n + 1) + '.tif'
                                os.system(TESSERACT + ' ' + tif_file + ' ' + dir + self._name + str(n + 1) + ' >nul 2>&1')
                                with open(text_file, 'r', encoding='utf-8', errors='ignore') as (f):
                                    text = f.read()
                                    if self._segment:
                                        segment = Segment(text)
                                        text = segment.segments
                                    page = Page(tif_file, text, n + 1)
                                    json_file = dir + self._name + str(n + 1) + '.json'
                                    page.store(json_file)
                                    self.__iadd__(page)

                            self._scanned = True
            if len(self.pages) == 1 or len(self.pages[0]) > len(self.pages[1]):
                self._langcheck(self.pages[0].words)
            else:
                self._langcheck(self.pages[1].words)
            if not self._scanned or len(self.pages) == 1 or len(self.pages[0]) > len(self.pages[1]):
                self._scancheck(self.pages[0].words)
            else:
                self._scancheck(self.pages[1].words)
        self._time = time.time() - start

    def _langcheck(self, words):
        """ Use the speller checker to determine which language the document is in """
        english = 0
        spanish = 0
        french = 0
        italian = 0
        german = 0
        lg = {'en':{'dict':word2int_en, 
          'lang':english}, 
         'es':{'dict':word2int_es, 
          'lang':spanish}, 
         'fr':{'dict':word2int_fr, 
          'lang':french}, 
         'it':{'dict':word2int_it, 
          'lang':italian}, 
         'de':{'dict':word2int_de, 
          'lang':german}}
        for _ in range(20):
            try:
                if len(words[_]['word']) == 1:
                    continue
            except:
                continue

            if words[_]['word'].isdigit():
                continue
            else:
                if words[_]['tag'] == Vocabulary.ACRONYM:
                    continue
            for item in lg:
                try:
                    id = lg[item]['dict'][words[_]['word']]
                    lg[item]['lang'] += 1
                except:
                    pass

            if _ >= 11:
                lg_list_val = [lg[item]['lang'] for item in lg]
                if len(set(lg_list_val)) != len(lg_list_val):
                    continue
                else:
                    break

        for i in lg:
            exc_lg = [lg[j]['lang'] for j in lg if i != j]
            verify = all((lg[i]['lang'] > item for item in exc_lg))
            if verify:
                self._lang = i

    def _scancheck(self, words):
        """ Use spell checker to determine the quality of the scan """
        correct = 0
        count = 0
        for _ in range(0, min(len(words), self.SCANCHECK)):
            try:
                if len(words[_]['word']) == 1:
                    continue
            except:
                count += 1
                continue

            if words[_]['word'].isdigit():
                continue
            else:
                if words[_]['tag'] == Vocabulary.ACRONYM:
                    continue
            count += 1
            if self.WORDDICT == 'norvig':
                norvig = Norvig(self._lang)
                if norvig.known(words[_]['word'].lower()):
                    correct += 1

        if count:
            self._quality = correct / count
        else:
            self._quality = 1

    def load(self, document, dir='./'):
        """ """
        self._document = document
        if dir.endswith('/') == False:
            dir += '/'
        self._dir = dir
        basename = os.path.splitext(os.path.basename(self._document))
        self._name = basename[0]
        self._type = basename[1][1:].lower()
        files = glob.glob(dir + self._name + '*.json')
        npages = len(files)
        pageno = 1
        for pageno in range(1, npages + 1):
            page = Page(pageno=pageno)
            page.load(dir + self._name + str(pageno) + '.json')
            self.__iadd__(page)

    @property
    def document(self):
        """ Getter for the document name (path) """
        return self._document

    @document.setter
    def document(self, document):
        """ Setter for the document name (path)
        document - path to the document
        """
        self._document = document
        self._exist()
        self._collate(self._dir)

    @property
    def name(self):
        """ Getter for the document name (path) """
        return self._name

    @property
    def text(self):
        """ Getter for the raw text in the document """
        text = []
        for page in self._pages:
            text.append(page.text)

        return text

    @text.setter
    def text(self, text):
        """ Setter for the raw text in a document """
        self._text = text

    @property
    def dir(self):
        """ Getter for the page directory """
        return self._dir

    @dir.setter
    def dir(self, dir):
        """ Setter for page directory """
        if dir is not None:
            if isinstance(dir, str) == False:
                raise TypeError('String expected for page directory path')
        self._dir = dir

    @property
    def label(self):
        """ Getter for the document classification """
        return self._label

    @label.setter
    def label(self, label):
        """ Setter for document classification """
        if label is not None:
            if isinstance(label, str) == False:
                raise TypeError('String expected for classification (label)')
        self._label = label

    @property
    def pages(self):
        """ Return the list of pages """
        return self._pages

    @property
    def size(self):
        """ Return the byte size of the document """
        return self._size

    @property
    def type(self):
        """ Return the file type of the document """
        return self._type

    @property
    def time(self):
        """ Return the elapse time to do processing """
        return self._time

    @property
    def lang(self):
        """ Return the document language """
        return self._lang

    @property
    def scanned(self):
        """ Return whether document is a scanned (captured) image """
        return (
         self._scanned, self._quality)

    @property
    def bagOfWords(self):
        """ Return  bag of words for the document """
        if self._bow is None:
            self._bow = self[0].bagOfWords
            for i in range(1, len(self)):
                bag = self[i].bagOfWords
                for word, count in bag.items():
                    if word in self._bow:
                        self._bow[word] += count
                    else:
                        self._bow[word] = count

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
        """ Override the len() operator - return the number of pages """
        return len(self._pages)

    def __getitem__(self, index):
        """ Override the [] operator - return a page """
        if index < len(self):
            return self._pages[index]
        return

    def __setitem__(self, index, page):
        """ Override the [] operator - set a page """
        if page is not None:
            if isinstance(page, Page) == False:
                raise TypeError('Page expected for [] set operation')
        self._pages[index] = page

    def __iadd__(self, page):
        """ Override the + operator - add a page """
        self._pages.append(page)
        return self

    def __str__(self):
        """ Override the str() operator - return the document classification """
        return self._label


class Page(object):
    __doc__ = ' Base (super) class for Page object '
    BARE = False
    STEM = 'gap'
    POS = False
    ROMAN = False
    SPELL = None

    def __init__(self, path=None, text=None, pageno=None):
        """ Constructor for page object
        path - filepath to the page
        text - extracted text
        """
        self._path = path
        self._text = text
        self._pageno = pageno
        self._words = None
        self._label = None
        self._size = 0
        if path is not None:
            if isinstance(path, str) == False:
                raise TypeError('String expected for path parameter')
            if os.path.isfile(path) == False:
                raise FileNotFoundError('Not a valid path for the page')
        elif text is not None:
            if isinstance(text, list):
                self._size = 0
                for segment in text:
                    if isinstance(segment, dict) == False:
                        raise TypeError('Dictionary expected for text segment:', type(segment))
                    if segment['tag'] == Segment.PARAGRAPH:
                        self._size += 2 + len(segment['text'])
                    else:
                        self._size += 1 + len(segment['text'])

        elif isinstance(text, str):
            self._text = text.strip()
            self._size = len(text)
        else:
            raise TypeError('String expected for text parameter:', type(text))

    @property
    def path(self):
        """ Getter for page path """
        return self._path

    @path.setter
    def path(self, path):
        """ Setter for page path """
        if path is not None:
            if isinstance(path, str) == False:
                raise TypeError('string expected for path parameter')
            if os.path.isfile(path) == False:
                raise FileNotFoundError('not a valid path for the page')
        self._path = path

    @property
    def text(self):
        """ Getter for page text content """
        if self._text is None:
            return
        if isinstance(self._text, str):
            return self._text
        text = ''
        for segment in self._text:
            if segment['tag'] == Segment.PARAGRAPH:
                text += '\n\n' + segment['text']
            else:
                text += '\n' + segment['text']

        return text.strip()

    @text.setter
    def text(self, text):
        """ Setter for page text """
        if text is not None:
            if isinstance(text, str) == False:
                raise TypeError('String expected for text parameter:', type(text))
            text = text.strip()
            self._size = len(text)
        else:
            self._size = 0
        self._text = text

    @property
    def size(self):
        """ Getter for byte size of page """
        if self._text is None:
            return 0
        return self._size

    @property
    def label(self):
        """ Getter for the document classification """
        return self._label

    @label.setter
    def label(self, label):
        """ Setter for document classification """
        if label is not None:
            if isinstance(label, str) == False:
                raise TypeError('String expected for classification (label)')
        self._label = label

    @property
    def words(self):
        """ Getter for page words (tokenized) """
        if self._text is None:
            if self._words is None:
                return
        elif self._words is None:
            if isinstance(self._text, str):
                self._words = Words((self._text), bare=(self.BARE), stem=(self.STEM), pos=(self.POS), roman=(self.ROMAN), spell=(self.SPELL))
            else:
                words = []
                for segment in self._text:
                    words.append({'tag':segment['tag'],  'words':Words((segment['text']), bare=(self.BARE), stem=(self.STEM), pos=(self.POS), roman=(self.ROMAN), spell=(self.SPELL)).words})

                self._words = Words()
                self._words._words = words
        return self._words.words

    @property
    def pageno(self):
        """ Getter for the page number """
        return self._pageno

    @property
    def bagOfWords(self):
        """ Getter for bag of words """
        words = self.words
        if isinstance(self._text, str):
            return self._words.bagOfWords
        if len(self._words._words) == 0:
            return
        for segment in self._words._words:
            pass

        return

    @property
    def freqDist(self):
        """ Getter for frequency distribution """
        words = self.words
        return self._words.freqDist

    @property
    def termFreq(self):
        """ Getter for term frequency (TF) distribution """
        words = self.words
        return self._words.termFreq

    def store(self, path):
        """ Store the NLP tokenized string to storage """
        if not isinstance(path, str):
            raise TypeError('Path must be a string')
        with open(path, 'w') as (f):
            json.dump(self.words, f)

    def load(self, path):
        """ Load the NLP tokenized string from storage """
        if not isinstance(path, str):
            raise TypeError('Path must be a string')
        if os.path.isfile(path) == False:
            raise FileNotFoundError('Not a valid path')
        with open(path, 'r', encoding='utf-8') as (f):
            self._words = Words()
            self._words._words = json.load(f)
        path = path.replace('.json', '.txt')
        with open(path, 'r', encoding='utf-8') as (f):
            self._text = f.read()

    def __len__(self):
        """ Override the len() operator - get the number of tokenized words """
        if self._text is None:
            return 0
        if self._words is None:
            self._words = Words((self._text), bare=(self.BARE), stem=(self.STEM), pos=(self.POS), roman=(self.ROMAN), spell=(self.SPELL))
        return len(self._words.words)

    def __str__(self):
        """ Override the str() operator - return the document classification """
        return self._label

    def __iadd__(self, text):
        """ Override the += operator - add text to the page """
        if text is None:
            return self
        if isinstance(text, str) == False:
            raise TypeError('String expected for text')
        else:
            if self._text is None:
                self._text = text
            else:
                self._text += ' ' + text
            if self._words is not None:
                words = Words(text, bare=(self.BARE), stem=(self.STEM), pos=(self.POS), roman=(self.ROMAN), spell=(self.SPELL))
                self._words += words.words
        return self


def towords(words):
    ret = []
    for word in words:
        print(word['word'])


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: document.py document [directory]')
    else:
        if len(sys.argv) == 2:
            d = Document(sys.argv[1])
        else:
            d = Document(sys.argv[1], sys.argv[2])
            p = d[0]
            print(towords(p.words))