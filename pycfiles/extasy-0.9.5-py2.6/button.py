# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\extasy\step_definitions\button.py
# Compiled at: 2010-11-20 06:10:24
import extasy
from extasy import *

def _getxpath(label):
    return "(%(scope_xpath)s//input[(@value='%(label)s') and (@type='button' or @type='submit')])|(%(scope_xpath)s//button[.='%(label)s'])" % {'scope_xpath': extasy.scope.get_xpath(), 
       'label': label}


@Given('I click on "$label" button')
@When('I click on "$label" button')
@Then('I click on "$label" button')
def click(context, label):
    xpath = 'xpath=%s' % _getxpath(label=label)
    if not extasy.selenium.getDriver().is_element_visible(xpath):
        message = '"%s" button should exists and be visible' % label
        raise StepFailure(message)
    extasy.selenium.getDriver().click_element(xpath)