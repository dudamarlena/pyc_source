# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/test/contexts/XhtmlTables.py
# Compiled at: 2009-09-30 05:37:25
xhtmlInput = '\n<p>Table test.</p>\n<p>\n<table class="plain">\n<tbody>\n<tr>\n<td>Table 1 <br /></td>\n<td colspan="2">aaaaa<br /></td>\n</tr>\n<tr>\n<td>zzz <br /></td>\n<td>\n  <table>\n    <tr>\n      <td>SubTableA</td>\n      <td>SubTableB</td>\n    </tr>\n    <tr>\n      <td>SubTableC</td>\n      <td>SubTableD</td>\n    </tr>\n  </table>\n</td>\n<td><b>Hello</b> blabla<table><tr><td>SubTableOneRowOneColumn</td></tr></table></td>\n</tr>\n<tr>\n<td><p>Within a <b>para</b>graph</p></td>\n<td><b>Hello</b> non bold</td>\n<td>Hello <b>bold</b> not bold</td>\n</tr>\n</tbody>\n</table>\n</p>\n<br />'