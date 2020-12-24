# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jace/Dropbox/projects/hasgeek/baseframe/baseframe/deprecated.py
# Compiled at: 2015-01-17 04:11:58
"""
Deprecated declarations. Will be removed in Baseframe 0.3.0
"""
from __future__ import absolute_import
from webassets import Bundle
jquery_js = Bundle('baseframe/js/jquery-1.7.1.js', filters='closure_js', output='js/baseframe-jquery.min.js')
bootstrap_js = Bundle('baseframe/js/bootstrap/bootstrap-alert.js', 'baseframe/js/bootstrap/bootstrap-button.js', 'baseframe/js/bootstrap/bootstrap-dropdown.js', 'baseframe/js/bootstrap/bootstrap-modal.js', 'baseframe/js/bootstrap/bootstrap-tooltip.js', 'baseframe/js/bootstrap/bootstrap-tab.js', 'baseframe/js/bootstrap/bootstrap-transition.js')
extra_js = Bundle('baseframe/js/jquery.form.js', 'baseframe/js/tiny_mce/jquery.tinymce.js', 'baseframe/js/bootstrap-datepicker.js', 'baseframe/js/jquery.timepicker.js', 'baseframe/js/select2.js')
networkbar_js = Bundle('baseframe/js/networkbar.js')
baseframe_js = Bundle(bootstrap_js, extra_js, networkbar_js, 'baseframe/js/baseframe.js', debug=False, filters='closure_js', output='js/baseframe-packed.js')
mousetrap_js = Bundle('baseframe/js/mousetrap.js')
toastr_js = Bundle('baseframe/js/toastr.js')
expander_js = Bundle('baseframe/js/jquery.expander.js')
cookie_js = Bundle('baseframe/js/jquery.cookie.js')
timezone_js = Bundle('baseframe/js/detect_timezone.js')
socialite_js = Bundle('baseframe/js/socialite.js')
swfobject_js = Bundle('baseframe/js/swfobject.js')
parsley_js = Bundle('baseframe/js/parsley.js')
parsley_extend_js = Bundle('baseframe/js/parsley.extend.js')
networkbar_css = Bundle('baseframe/css/networkbar.css')
baseframe_css = Bundle('baseframe/css/bootstrap.css', 'baseframe/css/responsive.css', 'baseframe/css/select2.css', 'baseframe/css/jquery.timepicker.css', 'baseframe/css/baseframe.css', networkbar_css, filters='cssmin', output='css/baseframe-packed.css')
toastr_css = Bundle('baseframe/css/toastr.css')
animate_css = Bundle('baseframe/css/animate.css')