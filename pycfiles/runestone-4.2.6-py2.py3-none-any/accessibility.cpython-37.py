# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/accessibility/accessibility.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 1602 bytes
"""This extension adds an accessibiligy stylesheet.

By the 'accessibility_style' config value (in conf.py of 
an interactive book project) you can select what accessibility stylesheet
you want to add ('normal', 'light', 'darkest' or 'none')

An accessibility stylesheet overs:

-Change of nav bar to color code based on Users using either mouse or
keyboard to navigate the menu
-Adjusting bootstrap buttons to invert color on active and on focus for
accessibility for users
-Changing default bootstrap buttons to follow WCAG 2.0 guidlines

acessibility.css reflects WCAG 2.0 AA compliance
acessibilitydarkest.css reflects WCAG 2.0 AAA compliance
accessibilitylight.css doesn't change bootstrap colors but adds
inversion

Personally we prefered WCAG 2.0 AA compliance, so accessibility.css
reflects ideal changes

http://imgur.com/a/TSDNf
This shows the different CSS files from most compliance (left) to least
compliance (right)
"""

def setup(app):
    app.add_config_value('accessibility_style', 'normal', 'html')
    acc_style = app.config._raw_config.get('accessibility_style', 'normal')
    if acc_style == 'normal':
        app.add_autoversioned_stylesheet('accessibility.css')
    else:
        if acc_style == 'light':
            app.add_autoversioned_stylesheet('accessibilitylight.css')
        else:
            if acc_style == 'darkest':
                app.add_autoversioned_stylesheet('accessibilitydarkest.css')