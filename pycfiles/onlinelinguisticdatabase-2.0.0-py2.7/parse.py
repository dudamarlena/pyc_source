# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/lib/parse.py
# Compiled at: 2016-09-19 13:27:02
"""Basic command-line interface to a configured, compiled and exported OLD parser.

Usage:

    $ ./parse.py wordi (wordj ... wordn)

This script is intended to be included in the .zip archive returned by an OLD application
when GET /morphologicalparsers/id/export is requested on the fully generated and 
compiled morphological parser with id ``id``.  It expects all requisite files for the parser
and its sub-objects (e.g., the compiled morphophonology foma script, the pickled LM Trie, the
lexicon and dictionary pickle files, if needed, etc.) as well as a configuration pickle file
(i.e., config.pickle) to be present in the current working directory.

The code for the parser functionality is all located in ``parser.py``, which is the same as 
that used by an OLD web application.

Note that the included simplelm module is a somewhat modified version from that available at
<<URL>>.

"""
import os, sys, cPickle
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)
import parser
if 'PhonologyFST' not in dir(parser):
    import imp
    parser_module_path = os.path.join(script_dir, 'parser.py')
    parser = imp.load_source(os.path.dirname(__file__), parser_module_path)
config_file = 'config.pickle'
config_path = os.path.join(script_dir, config_file)
config = cPickle.load(open(config_path, 'rb'))
cache_file = 'cache.pickle'
cache_path = os.path.join(script_dir, cache_file)
phonology = parser.PhonologyFST(parent_directory=script_dir, word_boundary_symbol=config['phonology']['word_boundary_symbol'])
morphology = parser.MorphologyFST(parent_directory=script_dir, word_boundary_symbol=config['morphology']['word_boundary_symbol'], rare_delimiter=config['morphology']['rare_delimiter'], rich_upper=config['morphology']['rich_upper'], rich_lower=config['morphology']['rich_lower'], rules_generated=config['morphology']['rules_generated'])
language_model = parser.LanguageModel(parent_directory=script_dir, rare_delimiter=config['language_model']['rare_delimiter'], start_symbol=config['language_model']['start_symbol'], end_symbol=config['language_model']['end_symbol'], categorial=config['language_model']['categorial'])
parser = parser.MorphologicalParser(parent_directory=script_dir, word_boundary_symbol=config['parser']['word_boundary_symbol'], morpheme_delimiters=config['parser']['morpheme_delimiters'], phonology=phonology, morphology=morphology, language_model=language_model, cache=parser.Cache(path=cache_path))
if __name__ == '__main__':
    inputs = sys.argv[1:]
    for input_ in inputs:
        parse = parser.pretty_parse(input_)[input_]
        if parse:
            print '%s %s' % (input_, (' ').join(parse))
        else:
            print '%s No parse' % input_