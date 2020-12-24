# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/tagger/dispatch_predicates.py
# Compiled at: 2006-11-03 16:09:09
"""
tagger.Tagger depends on a number of string predicates used by
RuleDispatch to determine identity of string arguments. These
predicates have been collected here for cleanliness.
"""
IS_TAG = 'self.is_rdf_type(%s, self.taggedby)'
IS_USER = 'self.is_rdf_type(%s, self.authoredby)'
IS_ITEM = 'self.is_rdf_type(%s, self.annotates)'
ITEM_USER = '%s and %s' % (IS_ITEM, IS_USER)