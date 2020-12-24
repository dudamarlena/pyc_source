# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/n3p/n3meta.py
# Compiled at: 2008-04-06 11:56:08
"""n3meta - For use with n3p.py."""
import re
branches = {'_:jcOJHCYs16': {',': [',',
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs16'], 
                    '.': [], '}': []}, 
   '_:jcOJHCYs20': {',': [',',
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs20'], 
                    '.': [], '}': []}, 
   '_:jcOJHCYs33': {'.': [], ':': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs16'], 
                    '<': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs16'], 
                    '_': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs16'], 
                    'a': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs16'], 
                    '}': []}, 
   '_:jcOJHCYs36': {'.': [], ':': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs20'], 
                    '<': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs20'], 
                    '_': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs20'], 
                    'a': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#symbol',
                        '_:jcOJHCYs20'], 
                    '}': []}, 
   '_:jcOJHCYs44': {'.': [], '_': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#barename',
                        '_:jcOJHCYs9'], 
                    'a': [
                        'http://www.w3.org/2000/10/swap/grammar/n3#barename',
                        '_:jcOJHCYs9'], 
                    '}': []}, 
   '_:jcOJHCYs9': {',': [',',
                       'http://www.w3.org/2000/10/swap/grammar/n3#barename',
                       '_:jcOJHCYs9'], 
                   '.': [], '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#declaration': {'@keywords': ['@keywords',
                                                                         '_:jcOJHCYs44'], 
                                                             '@prefix': [
                                                                       '@prefix',
                                                                       'http://www.w3.org/2000/10/swap/grammar/n3#qname',
                                                                       'http://www.w3.org/2000/10/swap/grammar/n3#explicituri']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#document': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '(': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '+': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '-': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '0': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          ':': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '<': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '?': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '@EOFDUMMY': [
                                                                      'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                                      'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '@forAll': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                                    'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '@forSome': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                                     'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '@keywords': [
                                                                      'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                                      'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '@prefix': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                                    'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '@this': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                                  'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '[': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '_': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          'a': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof'], 
                                                          '{': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional',
                                                              'http://www.w3.org/2000/10/swap/grammar/bnf#eof']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#dtlang': {'!': [], '"': [], '(': [], ')': [], '+': [], ',': [], '-': [], '.': [], '0': [], ':': [], ';': [], '<': [], '<=': [], '=': [], '=>': [], '?': [], '@': [
                                                            '@',
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#langcode'], 
                                                        '@a': [], '@has': [], '@is': [], '@of': [], '@this': [], '[': [], ']': [], '^': [], '^^': [
                                                             '^^',
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#symbol'], 
                                                        '_': [], 'a': [], '{': [], '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#existential': {'@forSome': ['@forSome',
                                                                        '_:jcOJHCYs36']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#formulacontent': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], '(': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '+': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '-': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '0': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                ':': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '<': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '?': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '@forAll': [
                                                                          'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '@forSome': [
                                                                           'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '@keywords': [
                                                                            'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '@prefix': [
                                                                          'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '@this': [
                                                                        'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '[': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '_': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                'a': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '{': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                                '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#literal': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#string',
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#dtlang']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#node': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#literal'], '(': [
                                                          '(',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathlist',
                                                          ')'], 
                                                      '+': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#numericliteral'], 
                                                      '-': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#numericliteral'], 
                                                      '0': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#numericliteral'], 
                                                      ':': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#symbol'], 
                                                      '<': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#symbol'], 
                                                      '?': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#variable'], 
                                                      '@this': [
                                                              '@this'], 
                                                      '[': [
                                                          '[',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#propertylist',
                                                          ']'], 
                                                      '_': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#symbol'], 
                                                      'a': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#symbol'], 
                                                      '{': [
                                                          '{',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#formulacontent',
                                                          '}']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#object': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#path'], '(': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '+': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '-': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '0': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        ':': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '<': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '?': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '@this': [
                                                                'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '[': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '_': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        'a': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                        '{': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#objecttail': {',': [',',
                                                                'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                'http://www.w3.org/2000/10/swap/grammar/n3#objecttail'], 
                                                            '.': [], ';': [], ']': [], '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#path': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '(': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '+': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '-': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '0': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      ':': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '<': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '?': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '@this': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '[': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '_': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      'a': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail'], 
                                                      '{': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#node',
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#pathtail']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#pathlist': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '(': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          ')': [], '+': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '-': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '0': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          ':': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '<': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '?': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '@this': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '[': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '_': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          'a': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist'], 
                                                          '{': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#pathlist']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#pathtail': {'!': ['!',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                          '"': [], '(': [], ')': [], '+': [], ',': [], '-': [], '.': [], '0': [], ':': [], ';': [], '<': [], '<=': [], '=': [], '=>': [], '?': [], '@a': [], '@has': [], '@is': [], '@of': [], '@this': [], '[': [], ']': [], '^': [
                                                              '^',
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                          '_': [], 'a': [], '{': [], '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#propertylist': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '(': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '+': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '-': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '.': [], '0': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              ':': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '<': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '<=': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '=': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '=>': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '?': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '@a': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '@has': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '@is': [
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                    'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '@this': [
                                                                      'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                      'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                      'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                      'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '[': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              ']': [], '_': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              'a': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '{': [
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#verb',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#object',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#objecttail',
                                                                  'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail'], 
                                                              '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#propertylisttail': {'.': [], ';': [
                                                                      ';',
                                                                      'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                  ']': [], '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '(': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '+': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '-': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '0': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 ':': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '<': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '?': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '@this': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '[': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '_': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 'a': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist'], 
                                                                 '{': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#subject',
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#propertylist']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#statement': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], '(': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '+': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '-': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '0': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           ':': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '<': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '?': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '@forAll': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#universal'], 
                                                           '@forSome': [
                                                                      'http://www.w3.org/2000/10/swap/grammar/n3#existential'], 
                                                           '@keywords': [
                                                                       'http://www.w3.org/2000/10/swap/grammar/n3#declaration'], 
                                                           '@prefix': [
                                                                     'http://www.w3.org/2000/10/swap/grammar/n3#declaration'], 
                                                           '@this': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '[': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '_': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           'a': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement'], 
                                                           '{': [
                                                               'http://www.w3.org/2000/10/swap/grammar/n3#simpleStatement']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#statementlist': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '(': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '+': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '-': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '0': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               ':': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '<': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '?': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '@forAll': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '@forSome': [
                                                                          'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                          'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '@keywords': [
                                                                           'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                           'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '@prefix': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '@this': [
                                                                       'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                       'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '[': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '_': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               'a': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '{': [
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail'], 
                                                               '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '(': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '+': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '-': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '0': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     ':': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '<': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '?': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '@EOFDUMMY': [], '@forAll': [
                                                                               'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                               '.',
                                                                               'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '@forSome': [
                                                                                'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                                '.',
                                                                                'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '@keywords': [
                                                                                 'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                                 '.',
                                                                                 'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '@prefix': [
                                                                               'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                               '.',
                                                                               'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '@this': [
                                                                             'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                             '.',
                                                                             'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '[': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '_': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     'a': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional'], 
                                                                     '{': [
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statement',
                                                                         '.',
                                                                         'http://www.w3.org/2000/10/swap/grammar/n3#statements_optional']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#statementtail': {'.': ['.',
                                                                   'http://www.w3.org/2000/10/swap/grammar/n3#statementlist'], 
                                                               '}': []}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#subject': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#path'], '(': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '+': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '-': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '0': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         ':': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '<': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '?': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '@this': [
                                                                 'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '[': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '_': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         'a': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                         '{': [
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#symbol': {':': ['http://www.w3.org/2000/10/swap/grammar/n3#qname'], '<': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#explicituri'], 
                                                        '_': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#qname'], 
                                                        'a': [
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#qname']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#universal': {'@forAll': ['@forAll',
                                                                     '_:jcOJHCYs33']}, 
   'http://www.w3.org/2000/10/swap/grammar/n3#verb': {'"': ['http://www.w3.org/2000/10/swap/grammar/n3#path'], '(': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '+': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '-': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '0': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      ':': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '<': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '<=': [
                                                           '<='], 
                                                      '=': [
                                                          '='], 
                                                      '=>': [
                                                           '=>'], 
                                                      '?': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '@a': [
                                                           '@a'], 
                                                      '@has': [
                                                             '@has',
                                                             'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '@is': [
                                                            '@is',
                                                            'http://www.w3.org/2000/10/swap/grammar/n3#path',
                                                            '@of'], 
                                                      '@this': [
                                                              'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '[': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '_': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      'a': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path'], 
                                                      '{': [
                                                          'http://www.w3.org/2000/10/swap/grammar/n3#path']}}
regexps = {'http://www.w3.org/2000/10/swap/grammar/n3#barename': re.compile('[a-zA-Z_][a-zA-Z0-9_]*'), 
   'http://www.w3.org/2000/10/swap/grammar/n3#variable': re.compile('\\?[a-zA-Z_][a-zA-Z0-9_]*'), 
   'http://www.w3.org/2000/10/swap/grammar/n3#qname': re.compile('(([a-zA-Z_][a-zA-Z0-9_]*)?:)?([a-zA-Z_][a-zA-Z0-9_-]*)?'), 
   'http://www.w3.org/2000/10/swap/grammar/n3#string': re.compile('("""[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*""")|("[^"\\\\]*(?:\\\\.[^"\\\\]*)*")'), 
   'http://www.w3.org/2000/10/swap/grammar/n3#explicituri': re.compile('<[^>]*>'), 
   'http://www.w3.org/2000/10/swap/grammar/n3#langcode': re.compile('[a-z]+(-[a-z0-9]+)*'), 
   'http://www.w3.org/2000/10/swap/grammar/n3#numericliteral': re.compile('[-+]?[0-9]+(\\.[0-9]+)?(e[-+]?[0-9]+)?')}
if __name__ == '__main__':
    print __doc__