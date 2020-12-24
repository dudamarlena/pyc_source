# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\extasy\step_definitions\tab.py
# Compiled at: 2010-11-20 06:10:24
import extasy, extasy.selenium
from extasy import *

def _getxpath(title):
    return "(%(scope_xpath)s//span[contains(concat(' ',@class, ' '),' x-tab-strip-text ') and .='%(title)s'])[last()]/../../.." % {'scope_xpath': extasy.scope.get_xpath(), 
       'title': title}


def _get_close_button_xpath(title):
    return "(%(scope_xpath)s//span[contains(concat(' ',@class, ' '),' x-tab-strip-text  ') and .='%(title)s'])[last()]/../../../../a[contains(concat(' ',@class, ' '),' x-tab-strip-close ')]" % {'scope_xpath': extasy.scope.get_xpath(), 
       'title': title}


def _get_enter_scope_xpath(title):
    tab_xpath = "((%(scope_xpath)s//span[contains(concat(' ',@class, ' '),' x-tab-strip-text ') and .='%(title)s'])[last()]/ancestor::li)[1]" % {'scope_xpath': extasy.scope.get_xpath(), 
       'title': title}
    tabId = extasy.selenium.getDriver().get_element_id('xpath=%s' % tab_xpath)
    script = "(function( tabId ){\n        tabId = tabId.split( '__' )[ 1 ];\n        var tab = selenium.browserbot.getCurrentWindow().Ext.getCmp( tabId );\n        if( !tab.body ) return selenium.browserbot.getCurrentWindow().Ext.id();\n        return tab.body.dom.id;\n    })( '%s' )" % tabId
    tabBodyId = extasy.selenium.getDriver().exec_js(script)
    return "//div[@id='%s']" % tabBodyId


def _wait_for_presence(context, title, timeout=None):
    xpath = 'xpath=%s' % _getxpath(title=title)
    if not timeout:
        timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
    timeout = int(timeout)
    if not extasy.selenium.getDriver().wait_for_element_present(xpath, timeout):
        message = '"%s" tab should appear in %s seconds' % (title, timeout)
        raise StepFailure(message)


@Given('I wait for "$title" tab to disappear')
@When('I wait for "$title" tab to disappear')
@Then('"$title" tab should disappear')
def wait_to_disappear(context, title, timeout=None):
    xpath = 'xpath=%s' % _getxpath(title=title)
    if not extasy.selenium.getDriver().is_element_visible(xpath):
        message = '"%s" tab should exists and be visible' % title
        raise StepFailure(message)
    if not timeout:
        timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
    timeout = int(timeout)
    if not extasy.selenium.getDriver().wait_for_element_to_disappear(xpath, timeout):
        message = '"%s" tab should disappear in %s seconds' % (title, timeout)
        raise StepFailure(message)


@Given('"$title" tab is present')
def is_present(context, title):
    xpath = 'xpath=%s' % _getxpath(title=title)
    if not extasy.selenium.getDriver().is_element_visible(xpath):
        message = '"%s" tab should exists and be visible' % title
        raise StepFailure(message)


@Given('In "$title" tab:')
@When('In "$title" tab:')
@Then('In "$title" tab:')
def enter_scope(context, title):
    scope_xpath = _get_enter_scope_xpath(title=title)
    extasy.scope.enter(scope_xpath, context.indentation_level)


@Given('I click on "$title" tab')
@When('I click on "$title" tab')
@Then('I click on "$title" tab')
def click(context, title):
    xpath = 'xpath=%s' % _getxpath(title=title)
    if not extasy.selenium.getDriver().is_element_visible(xpath):
        message = '"%s" tab should exists and be visible' % title
        raise StepFailure(message)
    extasy.selenium.getDriver().click_element_at(xpath, 5, 5)


@Given('I close "$title" tab')
@When('I close "$title" tab')
@Then('I close "$title" tab')
def close(context, title):
    xpath = 'xpath=%s' % _get_close_button_xpath(title=title)
    if not extasy.selenium.getDriver().is_element_visible(xpath):
        message = '"%s" tab should exists and be closable' % title
        raise StepFailure(message)
    extasy.selenium.getDriver().click_element(xpath)


@Given('I wait for "$title" tab to be present', 'I wait for "$title" tab to be present for $timout seconds')
@When('I wait for "$title" tab to be present', 'I wait for "$title" tab to be present for $timout seconds')
@Then('I wait for "$title" tab to be present', 'I wait for "$title" tab to be present for $timout seconds', 'Tab "$title" should be present')
def wait_for_presence_timeout(context, title, timeout=None):
    return _wait_for_presence(context, title, timeout)