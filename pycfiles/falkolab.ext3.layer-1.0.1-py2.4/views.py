# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/ext3/layer/views.py
# Compiled at: 2009-09-30 04:55:34
"""
Created on 05.06.2009

@author: falko

$Id$
"""
from zope.viewlet import viewlet
ExtAllCSS = viewlet.CSSViewlet('ext-3/resources/css/ext-all.css')
ExtStandaloneBundleViewlet = viewlet.JavaScriptBundleViewlet(('ext-3/adapter/ext/ext-base.js',
                                                              'ext-3/ext-all.js'))
ExtStandaloneDebugBundleViewlet = viewlet.JavaScriptBundleViewlet(('ext-3/adapter/ext/ext-base-debug.js',
                                                                   'ext-3/ext-all-debug.js'))
ExtJQueryBundleViewlet = viewlet.JavaScriptBundleViewlet(('ext-3/adapter/jquery/ext-jquery-adapter.js',
                                                          'ext-3/ext-all.js'))
ExtJQueryDebugBundleViewlet = viewlet.JavaScriptBundleViewlet(('ext-3/adapter/jquery/ext-jquery-adapter-debug.js',
                                                               'ext-3/ext-all-debug.js'))
ExtPrototypeBundleViewlet = viewlet.JavaScriptBundleViewlet(('ext-3/adapter/prototype/ext-prototype-adapter.js',
                                                             'ext-3/ext-all.js'))
ExtPrototypeDebugBundleViewlet = viewlet.JavaScriptBundleViewlet(('ext-3/adapter/prototype/ext-prototype-adapter-debug.js',
                                                                  'ext-3/ext-all-debug.js'))
ExtYUIBundleViewlet = viewlet.JavaScriptBundleViewlet(('ext-3/adapter/yui/ext-yui-adapter.js',
                                                       'ext-3/ext-all.js'))
ExtYUIDebugBundleViewlet = viewlet.JavaScriptBundleViewlet(('ext-3/adapter/yui/ext-yui-adapter-debug.js',
                                                            'ext-3/ext-all-debug.js'))