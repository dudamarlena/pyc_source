# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/json_token_parser.py
# Compiled at: 2012-08-13 04:31:17
__doc__ = '\nSimple global function for parsing JSON queries containing tokens\n'
import json, debug
from botnee import debug
from botnee import errors

def json_token_parser(text, verbose=False, logger=None):
    with debug.Timer(None, None, verbose, logger):
        tokens_dict = {}
        if len(text) == 0:
            return tokens_dict
        try:
            tokens_dict.update(json.loads(text))
        except Exception, e:
            errors.GetRelatedWarning(e.__repr__(), logger)
            return tokens_dict
        else:
            for (key, value) in tokens_dict.items():
                if key[:-1] != 'tokens_':
                    msg = 'Unknown key [%s] in tokens dict' % key
                    errors.GetRelatedWarning(msg, web_logger)
                    return tokens_dict
                ngram = int(key[(-1)])
                if ngram == 1:
                    if all(type(x) == unicode for x in value):
                        tokens_dict[key] = [
                         value]
                    elif all(type(x) == list for x in value):
                        pass
                    else:
                        msg = 'Incorrect type in tokens dict (%d)' % ngram
                        errors.GetRelatedWarning(msg, web_logger)
                        return tokens_dict
                elif all(len(x) == ngram for x in value) and all(type(y) == unicode for x in value for y in x):
                    tokens_dict[key] = [
                     value]
                elif all(len(y) == ngram for x in value for y in x) and all(type(z) == unicode for x in value for y in x):
                    pass
                else:
                    msg = 'Incorrect type in tokens dict (%d)' % ngram
                    errors.GetRelatedWarning(msg, web_logger)
                    return tokens_dict

    return tokens_dict