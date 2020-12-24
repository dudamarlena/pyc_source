# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/praat.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 12556 bytes
"""
    pygments.lexers.praat
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for Praat

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, words, bygroups, include
from pygments.token import Name, Text, Comment, Keyword, String, Punctuation, Number, Operator
__all__ = [
 'PraatLexer']

class PraatLexer(RegexLexer):
    __doc__ = '\n    For `Praat <http://www.praat.org>`_ scripts.\n\n    .. versionadded:: 2.1\n    '
    name = 'Praat'
    aliases = ['praat']
    filenames = ['*.praat', '*.proc', '*.psc']
    keywords = ('if', 'then', 'else', 'elsif', 'elif', 'endif', 'fi', 'for', 'from',
                'to', 'endfor', 'endproc', 'while', 'endwhile', 'repeat', 'until',
                'select', 'plus', 'minus', 'demo', 'assert', 'stopwatch', 'nocheck',
                'nowarn', 'noprogress', 'editor', 'endeditor', 'clearinfo')
    functions_string = ('backslashTrigraphsToUnicode', 'chooseDirectory', 'chooseReadFile',
                        'chooseWriteFile', 'date', 'demoKey', 'do', 'environment',
                        'extractLine', 'extractWord', 'fixed', 'info', 'left', 'mid',
                        'percent', 'readFile', 'replace', 'replace_regex', 'right',
                        'selected', 'string', 'unicodeToBackslashTrigraphs')
    functions_numeric = ('abs', 'appendFile', 'appendFileLine', 'appendInfo', 'appendInfoLine',
                         'arccos', 'arccosh', 'arcsin', 'arcsinh', 'arctan', 'arctan2',
                         'arctanh', 'barkToHertz', 'beginPause', 'beginSendPraat',
                         'besselI', 'besselK', 'beta', 'beta2', 'binomialP', 'binomialQ',
                         'boolean', 'ceiling', 'chiSquareP', 'chiSquareQ', 'choice',
                         'comment', 'cos', 'cosh', 'createDirectory', 'deleteFile',
                         'demoClicked', 'demoClickedIn', 'demoCommandKeyPressed',
                         'demoExtraControlKeyPressed', 'demoInput', 'demoKeyPressed',
                         'demoOptionKeyPressed', 'demoShiftKeyPressed', 'demoShow',
                         'demoWaitForInput', 'demoWindowTitle', 'demoX', 'demoY',
                         'differenceLimensToPhon', 'do', 'editor', 'endPause', 'endSendPraat',
                         'endsWith', 'erb', 'erbToHertz', 'erf', 'erfc', 'exitScript',
                         'exp', 'extractNumber', 'fileReadable', 'fisherP', 'fisherQ',
                         'floor', 'gaussP', 'gaussQ', 'hertzToBark', 'hertzToErb',
                         'hertzToMel', 'hertzToSemitones', 'imax', 'imin', 'incompleteBeta',
                         'incompleteGammaP', 'index', 'index_regex', 'invBinomialP',
                         'invBinomialQ', 'invChiSquareQ', 'invFisherQ', 'invGaussQ',
                         'invSigmoid', 'invStudentQ', 'length', 'ln', 'lnBeta', 'lnGamma',
                         'log10', 'log2', 'max', 'melToHertz', 'min', 'minusObject',
                         'natural', 'number', 'numberOfColumns', 'numberOfRows',
                         'numberOfSelected', 'objectsAreIdentical', 'option', 'optionMenu',
                         'pauseScript', 'phonToDifferenceLimens', 'plusObject', 'positive',
                         'randomBinomial', 'randomGauss', 'randomInteger', 'randomPoisson',
                         'randomUniform', 'real', 'readFile', 'removeObject', 'rindex',
                         'rindex_regex', 'round', 'runScript', 'runSystem', 'runSystem_nocheck',
                         'selectObject', 'selected', 'semitonesToHertz', 'sentencetext',
                         'sigmoid', 'sin', 'sinc', 'sincpi', 'sinh', 'soundPressureToPhon',
                         'sqrt', 'startsWith', 'studentP', 'studentQ', 'tan', 'tanh',
                         'variableExists', 'word', 'writeFile', 'writeFileLine',
                         'writeInfo', 'writeInfoLine')
    functions_array = ('linear', 'randomGauss', 'randomInteger', 'randomUniform', 'zero')
    objects = ('Activation', 'AffineTransform', 'AmplitudeTier', 'Art', 'Artword',
               'Autosegment', 'BarkFilter', 'BarkSpectrogram', 'CCA', 'Categories',
               'Cepstrogram', 'Cepstrum', 'Cepstrumc', 'ChebyshevSeries', 'ClassificationTable',
               'Cochleagram', 'Collection', 'ComplexSpectrogram', 'Configuration',
               'Confusion', 'ContingencyTable', 'Corpus', 'Correlation', 'Covariance',
               'CrossCorrelationTable', 'CrossCorrelationTables', 'DTW', 'DataModeler',
               'Diagonalizer', 'Discriminant', 'Dissimilarity', 'Distance', 'Distributions',
               'DurationTier', 'EEG', 'ERP', 'ERPTier', 'EditCostsTable', 'EditDistanceTable',
               'Eigen', 'Excitation', 'Excitations', 'ExperimentMFC', 'FFNet', 'FeatureWeights',
               'FileInMemory', 'FilesInMemory', 'Formant', 'FormantFilter', 'FormantGrid',
               'FormantModeler', 'FormantPoint', 'FormantTier', 'GaussianMixture',
               'HMM', 'HMM_Observation', 'HMM_ObservationSequence', 'HMM_State',
               'HMM_StateSequence', 'Harmonicity', 'ISpline', 'Index', 'Intensity',
               'IntensityTier', 'IntervalTier', 'KNN', 'KlattGrid', 'KlattTable',
               'LFCC', 'LPC', 'Label', 'LegendreSeries', 'LinearRegression', 'LogisticRegression',
               'LongSound', 'Ltas', 'MFCC', 'MSpline', 'ManPages', 'Manipulation',
               'Matrix', 'MelFilter', 'MelSpectrogram', 'MixingMatrix', 'Movie',
               'Network', 'OTGrammar', 'OTHistory', 'OTMulti', 'PCA', 'PairDistribution',
               'ParamCurve', 'Pattern', 'Permutation', 'Photo', 'Pitch', 'PitchModeler',
               'PitchTier', 'PointProcess', 'Polygon', 'Polynomial', 'PowerCepstrogram',
               'PowerCepstrum', 'Procrustes', 'RealPoint', 'RealTier', 'ResultsMFC',
               'Roots', 'SPINET', 'SSCP', 'SVD', 'Salience', 'ScalarProduct', 'Similarity',
               'SimpleString', 'SortedSetOfString', 'Sound', 'Speaker', 'Spectrogram',
               'Spectrum', 'SpectrumTier', 'SpeechSynthesizer', 'SpellingChecker',
               'Strings', 'StringsIndex', 'Table', 'TableOfReal', 'TextGrid', 'TextInterval',
               'TextPoint', 'TextTier', 'Tier', 'Transition', 'VocalTract', 'VocalTractTier',
               'Weight', 'WordList')
    variables_numeric = ('macintosh', 'windows', 'unix', 'praatVersion', 'pi', 'e',
                         'undefined')
    variables_string = ('praatVersion', 'tab', 'shellDirectory', 'homeDirectory', 'preferencesDirectory',
                        'newline', 'temporaryDirectory', 'defaultDirectory')
    tokens = {'root':[
      (
       '(\\s+)(#.*?$)', bygroups(Text, Comment.Single)),
      (
       '^#.*?$', Comment.Single),
      (
       ';[^\\n]*', Comment.Single),
      (
       '\\s+', Text),
      (
       '\\bprocedure\\b', Keyword, 'procedure_definition'),
      (
       '\\bcall\\b', Keyword, 'procedure_call'),
      (
       '@', Name.Function, 'procedure_call'),
      include('function_call'),
      (
       words(keywords, suffix='\\b'), Keyword),
      (
       '(\\bform\\b)(\\s+)([^\\n]+)',
       bygroups(Keyword, Text, String), 'old_form'),
      (
       '(print(?:line|tab)?|echo|exit|asserterror|pause|send(?:praat|socket)|include|execute|system(?:_nocheck)?)(\\s+)',
       bygroups(Keyword, Text), 'string_unquoted'),
      (
       '(goto|label)(\\s+)(\\w+)', bygroups(Keyword, Text, Name.Label)),
      include('variable_name'),
      include('number'),
      (
       '"', String, 'string'),
      (
       words(objects, suffix='(?=\\s+\\S+\\n)'), Name.Class, 'string_unquoted'),
      (
       '\\b[A-Z]', Keyword, 'command'),
      (
       '(\\.{3}|[)(,])', Punctuation)], 
     'command':[
      (
       '( ?[\\w()-]+ ?)', Keyword),
      (
       "'(?=.*')", String.Interpol, 'string_interpolated'),
      (
       '\\.{3}', Keyword, ('#pop', 'old_arguments')),
      (
       ':', Keyword, ('#pop', 'comma_list')),
      (
       '\\s', Text, '#pop')], 
     'procedure_call':[
      (
       '\\s+', Text),
      (
       '([\\w.]+)(:|\\s*\\()',
       bygroups(Name.Function, Text), '#pop'),
      (
       '([\\w.]+)', Name.Function, ('#pop', 'old_arguments'))], 
     'procedure_definition':[
      (
       '\\s', Text),
      (
       '([\\w.]+)(\\s*?[(:])',
       bygroups(Name.Function, Text), '#pop'),
      (
       '([\\w.]+)([^\\n]*)',
       bygroups(Name.Function, Text), '#pop')], 
     'function_call':[
      (
       words(functions_string, suffix='\\$(?=\\s*[:(])'), Name.Function, 'function'),
      (
       words(functions_array, suffix='#(?=\\s*[:(])'), Name.Function, 'function'),
      (
       words(functions_numeric, suffix='(?=\\s*[:(])'), Name.Function, 'function')], 
     'function':[
      (
       '\\s+', Text),
      (
       ':', Punctuation, ('#pop', 'comma_list')),
      (
       '\\s*\\(', Punctuation, ('#pop', 'comma_list'))], 
     'comma_list':[
      (
       '(\\s*\\n\\s*)(\\.{3})', bygroups(Text, Punctuation)),
      (
       '(\\s*[])\\n])', Text, '#pop'),
      (
       '\\s+', Text),
      (
       '"', String, 'string'),
      (
       '\\b(if|then|else|fi|endif)\\b', Keyword),
      include('function_call'),
      include('variable_name'),
      include('operator'),
      include('number'),
      (
       '[()]', Text),
      (
       ',', Punctuation)], 
     'old_arguments':[
      (
       '\\n', Text, '#pop'),
      include('variable_name'),
      include('operator'),
      include('number'),
      (
       '"', String, 'string'),
      (
       '[^\\n]', Text)], 
     'number':[
      (
       '\\n', Text, '#pop'),
      (
       '\\b\\d+(\\.\\d*)?([eE][-+]?\\d+)?%?', Number)], 
     'object_attributes':[
      (
       '\\.?(n(col|row)|[xy]min|[xy]max|[nd][xy])\\b', Name.Builtin, '#pop'),
      (
       '(\\.?(?:col|row)\\$)(\\[)',
       bygroups(Name.Builtin, Text), 'variable_name'),
      (
       '(\\$?)(\\[)',
       bygroups(Name.Builtin, Text), ('#pop', 'comma_list'))], 
     'variable_name':[
      include('operator'),
      include('number'),
      (
       words(variables_string, suffix='\\$'), Name.Variable.Global),
      (
       words(variables_numeric, suffix='\\b'), Name.Variable.Global),
      (
       '\\bObject_\\w+', Name.Builtin, 'object_attributes'),
      (
       words(objects, prefix='\\b', suffix='_\\w+'),
       Name.Builtin, 'object_attributes'),
      (
       "\\b(Object_)(')",
       bygroups(Name.Builtin, String.Interpol),
       ('object_attributes', 'string_interpolated')),
      (
       words(objects, prefix='\\b', suffix="(_)(')"),
       bygroups(Name.Builtin, Name.Builtin, String.Interpol),
       ('object_attributes', 'string_interpolated')),
      (
       '\\.?_?[a-z][\\w.]*(\\$|#)?', Text),
      (
       '[\\[\\]]', Punctuation, 'comma_list'),
      (
       "'(?=.*')", String.Interpol, 'string_interpolated')], 
     'operator':[
      (
       '([+\\/*<>=!-]=?|[&*|][&*|]?|\\^|<>)', Operator),
      (
       '(?<![\\w.])(and|or|not|div|mod)(?![\\w.])', Operator.Word)], 
     'string_interpolated':[
      (
       '\\.?[_a-z][\\w.]*[$#]?(?:\\[[a-zA-Z0-9,]+\\])?(:[0-9]+)?',
       String.Interpol),
      (
       "'", String.Interpol, '#pop')], 
     'string_unquoted':[
      (
       '(\\n\\s*)(\\.{3})', bygroups(Text, Punctuation)),
      (
       '\\n', Text, '#pop'),
      (
       '\\s', Text),
      (
       "'(?=.*')", String.Interpol, 'string_interpolated'),
      (
       "'", String),
      (
       "[^'\\n]+", String)], 
     'string':[
      (
       '(\\n\\s*)(\\.{3})', bygroups(Text, Punctuation)),
      (
       '"', String, '#pop'),
      (
       "'(?=.*')", String.Interpol, 'string_interpolated'),
      (
       "'", String),
      (
       '[^\\\'"\\n]+', String)], 
     'old_form':[
      (
       '\\s+', Text),
      (
       '(optionmenu|choice)([ \\t]+\\S+:[ \\t]+)',
       bygroups(Keyword, Text), 'number'),
      (
       '(option|button)([ \\t]+)',
       bygroups(Keyword, Text), 'string_unquoted'),
      (
       '(sentence|text)([ \\t]+\\S+)',
       bygroups(Keyword, Text), 'string_unquoted'),
      (
       '(word)([ \\t]+\\S+[ \\t]*)(\\S+)?([ \\t]+.*)?',
       bygroups(Keyword, Text, String, Text)),
      (
       '(boolean)(\\s+\\S+\\s*)(0|1|"?(?:yes|no)"?)',
       bygroups(Keyword, Text, Name.Variable)),
      (
       '(real|natural|positive|integer)([ \\t]+\\S+[ \\t]*)([+-]?)(\\d+(?:\\.\\d*)?(?:[eE][-+]?\\d+)?%?)',
       bygroups(Keyword, Text, Operator, Number)),
      (
       '(comment)(\\s+)',
       bygroups(Keyword, Text), 'string_unquoted'),
      (
       '\\bendform\\b', Keyword, '#pop')]}