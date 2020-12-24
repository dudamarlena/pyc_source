# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/laureano/desarrollo/eggs/tw/twtools/projects/tw.jsunit/trunk/tw/jsunit/base.py
# Compiled at: 2008-04-25 20:27:53
from tw.api import Widget, JSLink, CSSLink
jsunit_js = JSLink(modname=__name__, filename='static/jsUnitCore.js', javascript=[])
jsunit_version_check_js = JSLink(modname=__name__, filename='static/jsUnitVersionCheck.js', javascript=[])
jsunit_mock_timeout_js = JSLink(modname=__name__, filename='static/jsUnitMockTimeout.js', javascript=[])
jsunit_tracer_js = JSLink(modname=__name__, filename='static/jsUnitTracer.js', javascript=[])
jsunit_test_manager_js = JSLink(modname=__name__, filename='static/jsUnitTestManager.js', javascript=[])
jsunit_test_suite_js = JSLink(modname=__name__, filename='static/jsUnitTestSuite.js', javascript=[])
jsunit_xbdebug_js = JSLink(modname=__name__, filename='static/xbDebug.js', jsvascript=[])
jsunit_css = CSSLink(modname=__name__, filename='static/css/jsUnitStyle.css')