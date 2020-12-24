# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/constants.py
# Compiled at: 2019-08-25 15:15:03
# Size of source mod 2**32: 4722 bytes
import numpy as np
CONLL_COLUMNS = ['i', 'w', 'l', 'x', 'p', 'm', 'g', 'f', 'e', 'o']
COLUMN_NAMES = [
 'file', 's'] + CONLL_COLUMNS
SHORT_TO_LONG_NAME = dict(w='Word',
  l='Lemma',
  p='Part of speech',
  g='Governor index',
  f='Dependency role',
  x='Wordclass',
  i='Token index',
  e='Extra',
  m='Morphological features',
  gw='Governor word',
  gl='Governor lemma',
  gp='Governor POS',
  gg='Governor gov. index',
  gf='Governor dep. role',
  gx='Governor wordclass',
  gi='Governor token index',
  s='Sentence number',
  file='Filename',
  speaker='Speaker',
  d='Depgrep',
  t='TGrep2')
_SHORTER = dict(s='Sent #',
  i='Token #',
  p='POS',
  g='Gov.',
  f='Function',
  x='Class',
  m='Morph')
SHORT_TO_COL_NAME = {**SHORT_TO_LONG_NAME, **_SHORTER}
SHORT_TO_COL_NAME = {k:v.replace('Governor', 'Gov.') for k, v in SHORT_TO_COL_NAME.items()}
DTYPES = dict(i=(np.int32),
  s=(np.int64),
  w='category',
  l='category',
  p='category',
  x='category',
  g=(np.int64),
  parse=object,
  f='category',
  m=str,
  o=str,
  n='category',
  speaker='category',
  year=(np.int64),
  date='category',
  month='category',
  postgroup=(np.float64),
  totalposts=(np.float64),
  postnum=(np.float64),
  _n=(np.int64),
  sent_len=(np.int64),
  line=(np.int64),
  mood='category',
  number='category',
  person=(np.int64),
  tense='category',
  verbform='category',
  definite='category',
  gender='category',
  prontype='category',
  adptype='category',
  puncttype='category',
  numtype='category',
  punctside='category')
LONG_NAMES = dict(file={
 'files'},
  s={
 'sentence', 'sentences'},
  i={
 'index', 'indices'},
  w={
 'word', 'words', 'token', 'tokens'},
  l={
 'lemma', 'lemmas', 'lemmata'},
  x={
 'language_specific', 'localpos', 'class', 'xpos', 'wordclass', 'wordclasses'},
  p={
 'pos', 'partofspeech', 'tag', 'tags'},
  m={
 'morph', 'morphology'},
  g={
 'governor', 'governors', 'gov', 'govs'},
  f={
 'function', 'funct', 'functions', 'role', 'roles', 'link', 'links'},
  e={
 'extra'},
  o={
 'other'},
  speaker={
 'speaker', 'speakers'},
  text={
 'text', 'texts', 'original'})
LANGUAGES = {'German':'de', 
 'Greek':'el', 
 'English':'en', 
 'Spanish':'es', 
 'French':'fr', 
 'Italian':'it', 
 'Dutch':'nl', 
 'Portuguese':'pt', 
 'Multi-language':'xx', 
 'Afrikaans':'af', 
 'Arabic':'ar', 
 'Bulgarian':'bg', 
 'Bengali':'bn', 
 'Catalan':'ca', 
 'Czech':'cs', 
 'Danish':'da', 
 'Estonian':'et', 
 'Persian':'fa', 
 'Finnish':'fi', 
 'Irish':'ga', 
 'Hebrew':'he', 
 'Hindi':'hi', 
 'Croatian':'hr', 
 'Hungarian':'hu', 
 'Indonesian':'id', 
 'Icelandic':'is', 
 'Japanese':'ja', 
 'Kannada':'kn', 
 'Korean':'ko', 
 'Lithuanian':'lt', 
 'Latvian':'lv', 
 'Marathi':'mr', 
 'Norwegian Bokmål':'nb', 
 'Polish':'pl', 
 'Romanian':'ro', 
 'Serbian':'rs', 
 'Russian':'ru', 
 'Sinhala':'si', 
 'Slovak':'sk', 
 'Slovenian':'sl', 
 'Albanian':'sq', 
 'Swedish':'sv', 
 'Tamil':'ta', 
 'Telugu':'te', 
 'Thai':'th', 
 'Tagalog':'tl', 
 'Turkish':'tr', 
 'Tatar':'tt', 
 'Ukrainian':'uk', 
 'Urdu':'ur', 
 'Vietnamese':'vi', 
 'Chinese':'zh'}
_AVAILABLE_MODELS = {
 'en', 'de', 'it', 'nl', 'el', 'pt', 'fr', 'es'}
SPACY_LANGUAGES = {k:v for k, v in LANGUAGES.items() if v in _AVAILABLE_MODELS if v in _AVAILABLE_MODELS}
MORPH_FIELDS = {'adptype':'adp_type', 
 'definite':'definite', 
 'gender':'gender', 
 'mood':'mood', 
 'number':'number', 
 'numtype':'num_type', 
 'person':'person', 
 'prontype':'pron_type', 
 'punctside':'punct_side', 
 'puncttype':'punct_type'}
QUERYSETS = dict(NOUN={
 'f"acomp" <- (X"VERB" -> ({query} = F/nsubj/))',
 'f"amod" <- {query}',
 'P"NN" -> (F"prep" = w/of/ -> ({query} = F/pobj|nsubj/))',
 'X"NOUN" -> F/cc/ -> ({query} = F"conj")',
 'F"amod" <- (X"NOUN" -> ({query} = F"poss"))',
 'X"NOUN" -> ({query} = F"poss")',
 'F"acomp" <- (F"relcl" <- {query})',
 'F"advmod" <- (X"VERB" -> ({query} = F"nsubj"))'},
  VERB={
 'F"advmod" <- (X"VERB" = {query})'})