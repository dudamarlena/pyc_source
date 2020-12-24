# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/test/xxx_worldcat.py
# Compiled at: 2009-05-01 11:44:33
"""
Tests for biblio.webquery.worldcat, using nose.
"""

def test_parse_authors():
    test_dict = {'edited by Carol Shoshkes Reiss.': [
                                         'Reiss, Carol Shoshkes'], 
       'by Bill Scott, Theresa Neil.': [
                                      'Scott, Bill', 'Neil, Theresa'], 
       'Leonard Richardson and Sam Ruby.': [
                                          'Richardson, Leonard', 'Ruby, Sam'], 
       'Huntington F. Willard and Geoffrey S. Ginsburg.': [
                                                         'Willard, Huntington F.', 'Ginsburg, Geoffrey S.'], 
       'edited by Steven Laureys, Giulio Tononi.': [
                                                  'Laureys, Steven', 'Tononi, Giulio'], 
       'Jack D. Edinger, Colleen E. Carney.': [
                                             'Edinger, Jack D.', 'Carney, Colleen E.'], 
       'Ann Thomson.': [
                      'Thomson, Ann'], 
       '[John Grossman]': [
                         'Grossman, John'], 
       'Stephen P. Schoenberger, Bali Pulendran, editors.': [
                                                           'Schoenberger, Stephen P.', 'Pulendran, Bali'], 
       'Philip J. Davis, Reuben Hersh ; with an introduction by Gian-Carlo Rota.': [
                                                                                  'Davis, Philip J.', 'Hersh, Reuben'], 
       'Madonna': [
                 'Madonna']}
    for (k, v) in test_dict.iteritems():
        assert worldcat.parse_authors(k) == v