# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\extasy\step_definitions\combo.py
# Compiled at: 2010-11-20 06:10:24
import extasy
from extasy import *

def _get_open_button_xpath(label):
    return "(%(scope_xpath)s//img[contains(concat(' ',@class, ' '),' x-form-arrow-trigger ')]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]/descendant::label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%(label)s'])[last()]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]//img[contains(concat(' ',@class, ' '),' x-form-arrow-trigger ')]" % {'scope_xpath': extasy.scope.get_xpath(), 
       'label': label}


def _get_xpath(label):
    return "(%(scope_xpath)s//img[contains(concat(' ',@class, ' '),' x-form-arrow-trigger ')]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]/descendant::label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%(label)s'])[last()]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]/descendant::input[contains(concat(' ',@class, ' '),' x-form-field ')]" % {'scope_xpath': extasy.scope.get_xpath(), 
       'label': label}


def _get_options_xpath(comboId):
    script = "(function( comboId ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        if( !combo.list ) return '';\n        return combo.list.dom.id;\n    })( '%s' )" % comboId
    comboListId = extasy.selenium.getDriver().exec_js(script)
    return "//div[@id='%s']//div[contains(concat(' ',@class, ' '),' x-combo-list-item ')]" % comboListId


def _assert_is_visible(label):
    combo_xpath = 'xpath=' + _get_xpath(label)
    if not extasy.selenium.getDriver().is_element_visible(combo_xpath):
        raise StepFailure('"%s" combo should exists and be visible' % label)


@Given('I open "$label" combo')
@When('I open "$label" combo')
@Then('I open "$label" combo')
def open(context, label):
    combo_button_xpath = 'xpath=' + _get_open_button_xpath(label)
    combo_xpath = 'xpath=' + _get_xpath(label)
    if not extasy.selenium.getDriver().is_element_visible(combo_xpath):
        raise StepFailure('"%s" combo should exists and be visible' % label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        combo.collapse();\n        return 'ok';\n    })( '%s' )" % comboId
    extasy.selenium.getDriver().exec_js(script)
    extasy.selenium.getDriver().click_element_at(combo_button_xpath, 5, 5)


@Given('I close "$label" combo')
@When('I close "$label" combo')
@Then('I close "$label" combo')
def close(context, label):
    combo_button_xpath = 'xpath=' + _get_open_button_xpath(label)
    combo_xpath = 'xpath=' + _get_xpath(label)
    if not extasy.selenium.getDriver().is_element_visible(combo_xpath):
        raise StepFailure('"%s" combo should exists and be visible' % label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        combo.collapse();\n        return 'ok';\n    })( '%s' )" % comboId
    result = extasy.selenium.getDriver().exec_js(script)


def _options_wait_for_presence(context, label, timeout=None):
    combo_xpath = 'xpath=' + _get_xpath(label)
    if not extasy.selenium.getDriver().is_element_visible(combo_xpath):
        raise StepFailure('"%s" combo should exists and be visible' % label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    options_xpath = 'xpath=' + _get_options_xpath(comboId)
    if not timeout:
        timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
    timeout = int(timeout)
    if not extasy.selenium.getDriver().wait_for_element_present(options_xpath, timeout):
        raise StepFailure('"%s" combo options should be present in %s seconds' % (label, timeout))


@Given('I wait for "$label" combo options to be present')
@When('I wait for "$label" combo options to be present')
@Then('I wait for "$label" combo options to be present')
def options_wait_for_presence(context, label):
    _options_wait_for_presence(context, label)


@Given('I wait for "$label" combo options to be present for $timeout seconds')
@When('I wait for "$label" combo options to be present for $timeout seconds')
@Then('I wait for "$label" combo options to be present for $timeout seconds')
def options_wait_for_presence_timeout(context, label, timeout):
    _options_wait_for_presence(context, label, timeout)


@Given('I select the option with value of "$value" in "$label" combo')
@When('I select the option with value of "$value" in "$label" combo')
@Then('I select the option with value of "$value" in "$label" combo')
def select_by_value(context, label, value):
    combo_xpath = 'xpath=' + _get_xpath(label)
    _assert_is_visible(label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId, value ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        var record = combo.findRecord( combo.valueField, value );\n        if( !record ){\n            return '';\n        }\n        combo.collapse();\n        combo.setValue( record.get( combo.valueField ) );\n        return 'ok';\n    })( '%s', '%s' )" % (comboId, value)
    result = extasy.selenium.getDriver().exec_js(script)
    if not result:
        raise StepFailure('"%s" combo should have an option with value of "%s"' % (label, value))


@Given('I select the option with index of $index in "$label" combo')
@When('I select the option with index of $index in "$label" combo')
@Then('I select the option with index of $index in "$label" combo')
def select_by_index(context, label, index):
    combo_xpath = 'xpath=' + _get_xpath(label)
    index = int(index)
    _assert_is_visible(label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId, index ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        if( index >= combo.getStore().getCount() ) return '';\n        \n        var record = combo.getStore().getAt(index);\n        \n        combo.setValue( record.get( combo.valueField ) );\n        return 'ok';\n    })( '%s', '%s' )" % (comboId, index)
    result = extasy.selenium.getDriver().exec_js(script)
    if not result:
        raise StepFailure('"%s" combo should have an option with index of "%s"' % (label, index))


@Given('I select the option with text of "$text" in "$label" combo')
@When('I select the option with text of "$text" in "$label" combo')
@Then('I select the option with text of "$text" in "$label" combo')
def select_by_text(context, label, text):
    combo_xpath = 'xpath=' + _get_xpath(label)
    _assert_is_visible(label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId, value ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        var record = combo.findRecord( combo.displayField, value );\n        if( !record ){\n            return '';\n        }\n        combo.setValue( record.get( combo.valueField ) );\n        return 'ok';\n    })( '%s', '%s' )" % (comboId, text)
    result = extasy.selenium.getDriver().exec_js(script)
    if not result:
        raise StepFailure('"%s" combo should have an option with text of "%s"' % (label, text))


def _contains_option_with_text(context, label, text):
    combo_xpath = 'xpath=' + _get_xpath(label)
    _assert_is_visible(label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId, value ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        var record = combo.findRecord( combo.displayField, value );\n        if( !record ){\n            return '';\n        }\n        return 'ok';\n    })( '%s', '%s' )" % (comboId, text)
    found = extasy.selenium.getDriver().exec_js(script)
    return found


@Given('I see "$label" combo contains an option with text of "$text"')
@When('I see "$label" combo contains an option with text of "$text"')
@Then('I see "$label" combo contains an option with text of "$text"')
def contains_option_with_text(context, label, text):
    found = _contains_option_with_text(context, label, text)
    if not found:
        raise StepFailure('"%s" combo should have an option with text of "%s"' % (label, text))


@Given('I see "$label" combo does not contain an option with text of "$text"')
@When('I see "$label" combo does not contain an option with text of "$text"')
@Then('I see "$label" combo does not contain an option with text of "$text"')
def does_not_contain_option_with_text(context, label, text):
    found = _contains_option_with_text(context, label, text)
    if found:
        raise StepFailure('"%s" combo should not have an option with text of "%s"' % (label, text))


def _contains_option_with_value(context, label, value):
    combo_xpath = 'xpath=' + _get_xpath(label)
    _assert_is_visible(label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId, value ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        var record = combo.findRecord( combo.valueField, value );\n        if( !record ){\n            return '';\n        }\n        return 'ok';\n    })( '%s', '%s' )" % (comboId, value)
    found = extasy.selenium.getDriver().exec_js(script)
    return found


@Given('I see "$label" combo contains an option with value of "$value"')
@When('I see "$label" combo contains an option with value of "$value"')
@Then('I see "$label" combo contains an option with value of "$value"')
def contains_option_with_value(context, label, value):
    found = _contains_option_with_value(context, label, value)
    if not found:
        raise StepFailure('"%s" combo should have an option with value of "%s"' % (label, value))


@Given('I see "$label" combo does not contain an option with value of "$value"')
@When('I see "$label" combo does not contain an option with value of "$value"')
@Then('I see "$label" combo does not contain an option with value of "$value"')
def does_not_contain_option_with_value(context, label, value):
    found = _contains_option_with_value(context, label, value)
    if found:
        raise StepFailure('"%s" combo should not have an option with value of "%s"' % (label, value))


def _has_selected_value(context, label, value):
    combo_xpath = 'xpath=' + _get_xpath(label)
    _assert_is_visible(label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId, value ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        if( !combo.getValue() ){\n            return '';\n        }\n        \n        var selectedValue = combo.findRecord( combo.valueField, combo.getValue() ).get( combo.valueField );\n        if( selectedValue != value ){\n            return '';\n        }\n        \n        return 'ok';\n    })( '%s', '%s' )" % (comboId, value)
    found = extasy.selenium.getDriver().exec_js(script)
    return found


def _has_selected_text(context, label, text):
    combo_xpath = 'xpath=' + _get_xpath(label)
    _assert_is_visible(label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId, value ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        if( combo.selectedIndex == -1 ){\n            return '';\n        }\n        \n        var selectedValue = combo.findRecord( combo.valueField, combo.getValue() ).get( combo.displayField );\n        if( selectedValue != value ){\n            return '';\n        }\n        \n        return 'ok';\n    })( '%s', '%s' )" % (comboId, text)
    found = extasy.selenium.getDriver().exec_js(script)
    return found


@Given('I see "$label" combo has selected value of "$value"')
@When('I see "$label" combo has selected value of "$value"')
@Then('I see "$label" combo has selected value of "$value"')
def has_selected_value(context, label, value):
    found = _has_selected_value(context, label, value)
    if not found:
        raise StepFailure('"%s" combo should have selected value of "%s"' % (label, value))


@Given('I see "$label" combo has selected text of "$text"')
@When('I see "$label" combo has selected text of "$text"')
@Then('I see "$label" combo has selected text of "$text"')
def has_selected_text(context, label, text):
    found = _has_selected_text(context, label, text)
    if not found:
        raise StepFailure('"%s" combo should have selected text of "%s"' % (label, text))


@Given('I see "$label" combo does not have a selected option')
@When('I see "$label" combo does not have a selected option')
@Then('I see "$label" combo does not have a selected option')
def does_not_have_selected_option(context, label):
    combo_xpath = 'xpath=' + _get_xpath(label)
    _assert_is_visible(label)
    comboId = extasy.selenium.getDriver().get_element_id(combo_xpath)
    script = "(function( comboId ){\n        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );\n        if( combo.getValue() ){\n            return '';\n        }\n        return 'ok';\n    })( '%s' )" % comboId
    found = extasy.selenium.getDriver().exec_js(script)
    if not found:
        raise StepFailure('"%s" combo should not have a selected option' % label)