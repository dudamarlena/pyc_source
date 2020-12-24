# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/test/contexts/XhtmlComplexTables.py
# Compiled at: 2009-09-30 05:37:25
xhtmlInput = '\n<p>\n<table class="plain">\n<thead>\n<tr>\n<th class="align-right" align="right">Title column one<br /></th>\n<th>title column two</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td class="align-right" align="right">Hi with a <a class="generated" href="http://easi.wallonie.be">http://easi.wallonie.be</a> <br /></td>\n<td>fdff</td>\n</tr>\n<tr>\n<td class="align-right" align="right"><br /></td>\n<td><br /></td>\n</tr>\n<tr>\n<td class="align-right" align="left">Some text here<br />\n<ul><li>Bullet One</li><li>Bullet Two</li>\n<ul><li>Sub-bullet A</li><li>Sub-bullet B</li>\n<ul><li>Subsubboulette<br /></li></ul>\n</ul>\n</ul>\n</td>\n<td>\n<table>\n<tbody>\n<tr>\n<td>SubTable</td>\n<td>Columns 2<br /></td>\n</tr>\n</tbody>\n</table>\n</td>\n</tr>\n</tbody>\n</table>\n<br /></p>\n'
xhtmlInput2 = '\n<ul><li>\n<p>a</p>\n</li><li>\n<p>b</p>\n</li><li>\n<p>c</p>\n</li>\n<ul>\n  <li><p>SUB</p>\n  </li>\n</ul>\n</ul>\n'