# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/tests/test_htmlframework.py
# Compiled at: 2013-09-20 12:23:25
import os, nose
from ... import htmlframework as dfh

def setUpModule():
    global cheatsheet
    global log
    global pathToInputDataDir
    global pathToInputDir
    global pathToOutputDataDir
    global pathToOutputDir
    global testlog
    import logging, logging.config, yaml
    moduleDirectory = os.path.dirname(__file__) + '/../../tests'
    pathToInputDir = moduleDirectory + '/input/'
    pathToInputDataDir = pathToInputDir + 'data/'
    pathToOutputDir = moduleDirectory + '/output/'
    pathToOutputDataDir = pathToOutputDir + 'data/'
    testlog = open(pathToOutputDir + 'tests.log', 'w')
    loggerConfig = '\n    version: 1\n    formatters:\n        file_style:\n            format: \'* %(asctime)s - %(name)s - %(levelname)s (%(filename)s > %(funcName)s > %(lineno)d) - %(message)s  \'\n            datefmt: \'%Y/%m/%d %H:%M:%S\'\n        console_style:\n            format: \'* %(asctime)s - %(levelname)s: %(filename)s:%(funcName)s:%(lineno)d > %(message)s\'\n            datefmt: \'%H:%M:%S\'\n        html_style:\n            format: \'<div id="row" class="%(levelname)s"><span class="date">%(asctime)s</span>   <span class="label">file:</span><span class="filename">%(filename)s</span>   <span class="label">method:</span><span class="funcName">%(funcName)s</span>   <span class="label">line#:</span><span class="lineno">%(lineno)d</span> <span class="pathname">%(pathname)s</span>  <div class="right"><span class="message">%(message)s</span><span class="levelname">%(levelname)s</span></div></div>\'\n            datefmt: \'%Y-%m-%d <span class= "time">%H:%M <span class= "seconds">%Ss</span></span>\'\n    handlers:\n        console:\n            class: logging.StreamHandler\n            level: DEBUG\n            formatter: console_style\n            stream: ext://sys.stdout\n    root:\n        level: DEBUG\n        handlers: [console]'
    logging.config.dictConfig(yaml.load(loggerConfig))
    log = logging.getLogger(__name__)
    cheatsheet = open(pathToOutputDir + 'dryxPython_htmlframework_cheatsheet.html', 'w')
    return


def tearDownModule():
    """tear down test fixtures"""
    cheatsheet.close()
    testlog.close()
    return


class emptyLogger:
    info = None
    error = None
    debug = None
    critical = None
    warning = None


class test_0001_htmlDocument:

    def test_htmlDocument_works_as_expected(self):
        kwargs = {}
        kwargs['relativeUrlBase'] = ''
        kwargs['mainCssFileName'] = 'main.css'
        kwargs['pageTitle'] = ''
        kwargs['extras'] = ''
        headContent = dfh.head(**kwargs)
        kwargs = {}
        kwargs['navBar'] = False
        kwargs['content'] = ''
        kwargs['htmlId'] = ''
        kwargs['extraAttr'] = ''
        kwargs['relativeUrlBase'] = ''
        kwargs['responsive'] = True
        kwargs['googleAnalyticsCode'] = False
        kwargs['jsFileName'] = 'main.js'
        bodyContent = dfh.body(**kwargs)
        kwargs = {}
        kwargs['contentType'] = False
        kwargs['content'] = headContent + bodyContent
        content = dfh.htmlDocument(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_mediaObject:

    def test_mediaObject_works_as_expected(self):
        kwargs = {}
        kwargs['displayType'] = 'div'
        kwargs['img'] = ''
        kwargs['headlineText'] = ''
        kwargs['nestedMediaObjects'] = False
        content = dfh.mediaObject(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_well:

    def test_well_works_as_expected(self):
        kwargs = {}
        kwargs['wellText'] = ''
        wellSize = 'default'
        content = dfh.well(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_closeIcon:

    def test_closeIcon_works_as_expected(self):
        kwargs = {}
        content = dfh.closeIcon(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_get_button:

    def test_get_button_works_as_expected(self):
        kwargs = {}
        kwargs['size'] = 'large'
        kwargs['block'] = False
        kwargs['color'] = 'blue'
        kwargs['text'] = 'button'
        kwargs['htmlId'] = False
        kwargs['htmlClass'] = False
        kwargs['extraAttr'] = False
        kwargs['disabled'] = False
        content = dfh.get_button(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_button:

    def test_button_works_as_expected(self):
        kwargs = {}
        kwargs['buttonText'] = ''
        kwargs['buttonStyle'] = 'default'
        kwargs['buttonSize'] = 'default'
        kwargs['href'] = False
        kwargs['submit'] = False
        kwargs['block'] = False
        kwargs['disable'] = False
        content = dfh.button(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_buttonGroup:

    def test_buttonGroup_works_as_expected(self):
        kwargs = {}
        kwargs['buttonList'] = ''
        kwargs['format'] = 'default'
        content = dfh.buttonGroup(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_code:

    def test_code_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['inline'] = True
        kwargs['scroll'] = False
        content = dfh.code(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_dropdown:

    def test_dropdown_works_as_expected(self):
        kwargs = {}
        kwargs['buttonColor'] = 'default'
        kwargs['buttonSize'] = 'default'
        kwargs['color'] = 'grey'
        kwargs['menuTitle'] = '#'
        kwargs['splitButton'] = False
        kwargs['linkList'] = []
        kwargs['separatedLinkList'] = False
        kwargs['pull'] = False
        kwargs['direction'] = 'down'
        kwargs['onPhone'] = True
        kwargs['onTablet'] = True
        kwargs['onDesktop'] = True
        content = dfh.dropdown(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_searchForm:

    def test_searchForm_works_as_expected(self):
        kwargs = {}
        kwargs['buttonText'] = ''
        kwargs['span'] = 2
        kwargs['inlineHelpText'] = False
        kwargs['blockHelpText'] = False
        kwargs['focusedInputText'] = False
        content = dfh.searchForm(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_form:

    def test_form_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['formType'] = 'inline'
        kwargs['navBarPull'] = False
        content = dfh.form(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_horizontalFormControlGroup:

    def test_horizontalFormControlGroup_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['validationLevel'] = False
        content = dfh.horizontalFormControlGroup(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_horizontalFormControlLabel:

    def test_horizontalFormControlLabel_works_as_expected(self):
        kwargs = {}
        kwargs['labelText'] = ''
        kwargs['forId'] = False
        content = dfh.horizontalFormControlLabel(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_formInput:

    def test_formInput_works_as_expected(self):
        kwargs = {}
        kwargs['ttype'] = 'text'
        kwargs['placeholder'] = ''
        kwargs['span'] = 2
        kwargs['searchBar'] = False
        kwargs['pull'] = False
        kwargs['prepend'] = False
        kwargs['append'] = False
        button1 = False
        button2 = False
        kwargs['prependDropdown'] = False
        kwargs['appendDropdown'] = False
        kwargs['inlineHelpText'] = False
        kwargs['blockHelpText'] = False
        kwargs['focusedInput'] = False
        kwargs['required'] = False
        kwargs['disabled'] = False
        content = dfh.formInput(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_textarea:

    def test_textarea_works_as_expected(self):
        kwargs = {}
        kwargs['rows'] = ''
        kwargs['span'] = 2
        kwargs['inlineHelpText'] = False
        kwargs['blockHelpText'] = False
        kwargs['focusedInputText'] = False
        kwargs['required'] = False
        kwargs['disabled'] = False
        content = dfh.textarea(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_checkbox:

    def test_checkbox_works_as_expected(self):
        kwargs = {}
        kwargs['optionText'] = ''
        kwargs['inline'] = False
        kwargs['optionNumber'] = 1
        kwargs['inlineHelpText'] = False
        kwargs['blockHelpText'] = False
        kwargs['disabled'] = False
        content = dfh.checkbox(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_select:

    def test_select_works_as_expected(self):
        kwargs = {}
        kwargs['optionList'] = []
        kwargs['multiple'] = False
        kwargs['span'] = 2
        kwargs['inlineHelpText'] = False
        kwargs['blockHelpText'] = False
        kwargs['required'] = False
        kwargs['disabled'] = False
        content = dfh.select(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_radio:

    def test_radio_works_as_expected(self):
        kwargs = {}
        kwargs['optionText'] = ''
        kwargs['optionNumber'] = 1
        kwargs['inlineHelpText'] = False
        kwargs['blockHelpText'] = False
        kwargs['disabled'] = False
        content = dfh.radio(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_controlRow:

    def test_controlRow_works_as_expected(self):
        kwargs = {}
        kwargs['inputList'] = []
        content = dfh.controlRow(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_uneditableInput:

    def test_uneditableInput_works_as_expected(self):
        kwargs = {}
        kwargs['placeholder'] = ''
        kwargs['span'] = 2
        kwargs['inlineHelpText'] = False
        kwargs['blockHelpText'] = False
        content = dfh.uneditableInput(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_formActions:

    def test_formActions_works_as_expected(self):
        kwargs = {}
        kwargs['primaryButton'] = ''
        button2 = False
        button3 = False
        button4 = False
        button5 = False
        kwargs['inlineHelpText'] = False
        kwargs['blockHelpText'] = False
        content = dfh.formActions(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_unescape_html:

    def test_unescape_html_works_as_expected(self):
        kwargs = {}
        kwargs['html'] = '&@$^(*^)  123 {}()_+~?><?><'
        content = dfh.unescape_html(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_image:

    def test_image_works_as_expected(self):
        kwargs = {}
        kwargs['src'] = 'http://placehold.it/200x200'
        kwargs['href'] = False
        kwargs['display'] = ('False', )
        kwargs['pull'] = ('left', )
        kwargs['htmlClass'] = False
        kwargs['thumbnail'] = False
        kwargs['width'] = False
        kwargs['onPhone'] = True
        kwargs['onTablet'] = True
        kwargs['onDesktop'] = True
        content = dfh.image(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_thumbnail:

    def test_thumbnail_works_as_expected(self):
        kwargs = {}
        kwargs['htmlContent'] = ''
        content = dfh.thumbnail(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_label:

    def test_label_works_as_expected(self):
        kwargs = {}
        kwargs['text'] = ''
        level = 'default'
        content = dfh.label(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_badge:

    def test_badge_works_as_expected(self):
        kwargs = {}
        kwargs['text'] = ''
        level = 'default'
        content = dfh.badge(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_alert:

    def test_alert_works_as_expected(self):
        kwargs = {}
        kwargs['alertText'] = ''
        kwargs['alertHeading'] = ''
        kwargs['extraPadding'] = False
        kwargs['alertLevel'] = 'warning'
        content = dfh.alert(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_progressBar:

    def test_progressBar_works_as_expected(self):
        kwargs = {}
        kwargs['barStyle'] = 'plain'
        kwargs['precentageWidth'] = '10'
        kwargs['barLevel'] = 'info'
        content = dfh.progressBar(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_stackedProgressBar:

    def test_stackedProgressBar_works_as_expected(self):
        kwargs = {}
        kwargs['barLevel'] = 'info'
        kwargs['barStyle'] = 'plain'
        kwargs['infoWidth'] = '10'
        kwargs['successWidth'] = '10'
        kwargs['warningWidth'] = '10'
        kwargs['errorWidth'] = '10'
        content = dfh.stackedProgressBar(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_responsive_navigation_bar:

    def test_responsive_navigation_bar_works_as_expected(self):
        kwargs = {}
        kwargs['shade'] = 'dark'
        kwargs['brand'] = False
        kwargs['outsideNavList'] = False
        kwargs['insideNavList'] = False
        kwargs['htmlId'] = False
        kwargs['onPhone'] = True
        kwargs['onTablet'] = True
        kwargs['onDesktop'] = True
        content = dfh.responsive_navigation_bar(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_nav_list:

    def test_nav_list_works_as_expected(self):
        kwargs = {}
        kwargs['itemList'] = []
        kwargs['pull'] = False
        kwargs['onPhone'] = True
        kwargs['onTablet'] = True
        kwargs['onDesktop'] = True
        content = dfh.nav_list(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_searchbox:

    def test_searchbox_works_as_expected(self):
        kwargs = {}
        kwargs['size'] = 'medium'
        kwargs['placeHolder'] = False
        kwargs['button'] = False
        kwargs['buttonSize'] = 'small'
        kwargs['buttonColor'] = 'grey'
        kwargs['navBar'] = False
        kwargs['pull'] = False
        content = dfh.searchbox(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_tabbableNavigation:

    def test_tabbableNavigation_works_as_expected(self):
        kwargs = {}
        kwargs['log'] = log
        kwargs['contentDictionary'] = {}
        kwargs['fadeIn'] = True
        kwargs['direction'] = 'top'
        content = dfh.tabbableNavigation(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_navBar:

    def test_navBar_works_as_expected(self):
        kwargs = {}
        kwargs['brand'] = ''
        kwargs['contentDictionary'] = {}
        kwargs['dividers'] = False
        kwargs['fixedOrStatic'] = False
        kwargs['location'] = 'top'
        kwargs['responsive'] = False
        kwargs['dark'] = False
        content = dfh.navBar(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_pagination:

    def test_pagination_works_as_expected(self):
        kwargs = {}
        kwargs['listItems'] = ''
        kwargs['size'] = 'default'
        kwargs['align'] = 'left'
        content = dfh.pagination(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_row:

    def test_row_works_as_expected(self):
        kwargs = {}
        kwargs['responsive'] = True
        kwargs['columns'] = ''
        kwargs['htmlId'] = False
        kwargs['htmlClass'] = False
        kwargs['onPhone'] = True
        kwargs['onTablet'] = True
        kwargs['onDesktop'] = True
        content = dfh.row(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_get_javascript_block:

    def test_get_javascript_block_works_as_expected(self):
        kwargs = {}
        kwargs['jsPath'] = 'test'
        content = dfh.get_javascript_block(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_grid_column:

    def test_grid_column_works_as_expected(self):
        kwargs = {}
        kwargs['log'] = log
        kwargs['span'] = 1
        kwargs['offset'] = 0
        kwargs['content'] = ''
        kwargs['htmlId'] = False
        kwargs['htmlClass'] = False
        kwargs['onPhone'] = True
        kwargs['onTablet'] = True
        kwargs['onDesktop'] = True
        content = dfh.grid_column(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_tr:

    def test_tr_works_as_expected(self):
        kwargs = {}
        kwargs['cellContent'] = ''
        kwargs['color'] = False
        content = dfh.tr(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_th:

    def test_th_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['color'] = False
        content = dfh.th(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_td:

    def test_td_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['color'] = False
        content = dfh.td(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_tableCaption:

    def test_tableCaption_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        content = dfh.tableCaption(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_thead:

    def test_thead_works_as_expected(self):
        kwargs = {}
        kwargs['trContent'] = ''
        content = dfh.thead(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_tbody:

    def test_tbody_works_as_expected(self):
        kwargs = {}
        kwargs['trContent'] = ''
        content = dfh.tbody(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_table:

    def test_table_works_as_expected(self):
        kwargs = {}
        kwargs['caption'] = ''
        kwargs['thead'] = ''
        kwargs['tbody'] = ''
        kwargs['stripped'] = True
        kwargs['bordered'] = False
        kwargs['hover'] = True
        kwargs['condensed'] = False
        content = dfh.table(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_p:

    def test_p_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['lead'] = False
        kwargs['textAlign'] = False
        kwargs['color'] = False
        kwargs['navBar'] = False
        kwargs['onPhone'] = True
        kwargs['onTablet'] = True
        kwargs['onDesktop'] = True
        content = dfh.p(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_emphasizeText:

    def test_emphasizeText_works_as_expected(self):
        kwargs = {}
        kwargs['style'] = 'em'
        kwargs['text'] = ''
        content = dfh.emphasizeText(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_abbr:

    def test_abbr_works_as_expected(self):
        kwargs = {}
        kwargs['abbreviation'] = ''
        kwargs['fullWord'] = ''
        content = dfh.abbr(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_address:

    def test_address_works_as_expected(self):
        kwargs = {}
        kwargs['name'] = False
        addressLine1 = False
        addressLine2 = False
        addressLine3 = False
        kwargs['phone'] = False
        kwargs['email'] = False
        kwargs['twitterHandle'] = False
        content = dfh.address(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_blockquote:

    def test_blockquote_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['source'] = False
        kwargs['pullRight'] = False
        content = dfh.blockquote(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_ul:

    def test_ul_works_as_expected(self):
        kwargs = {}
        kwargs['itemList'] = []
        kwargs['unstyled'] = False
        kwargs['inline'] = False
        kwargs['dropDownMenu'] = False
        kwargs['navStyle'] = False
        kwargs['navPull'] = False
        kwargs['navDirection'] = 'horizontal'
        kwargs['breadcrumb'] = False
        kwargs['pager'] = False
        kwargs['thumbnails'] = False
        kwargs['mediaList'] = False
        content = dfh.ul(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_li:

    def test_li_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['span'] = False
        kwargs['disabled'] = False
        kwargs['submenuTitle'] = False
        kwargs['divider'] = False
        kwargs['navStyle'] = False
        kwargs['navDropDown'] = False
        kwargs['pager'] = False
        content = dfh.li(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_a:

    def test_a_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['href'] = False
        kwargs['tableIndex'] = False
        kwargs['triggerStyle'] = False
        content = dfh.a(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_ol:

    def test_ol_works_as_expected(self):
        kwargs = {}
        kwargs['itemList'] = []
        content = dfh.ol(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_descriptionLists:

    def test_descriptionLists_works_as_expected(self):
        kwargs = {}
        kwargs['orderedDictionary'] = {}
        kwargs['sideBySide'] = False
        content = dfh.descriptionLists(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_code:

    def test_code_works_as_expected(self):
        kwargs = {}
        kwargs['content'] = ''
        kwargs['inline'] = True
        kwargs['scroll'] = False
        content = dfh.code(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_heroUnit:

    def test_heroUnit_works_as_expected(self):
        kwargs = {}
        kwargs['headline'] = ''
        kwargs['tagline'] = ''
        kwargs['buttonStyle'] = 'primary'
        kwargs['buttonText'] = ''
        kwargs['buttonHref'] = '#'
        content = dfh.heroUnit(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return


class test_pageHeader:

    def test_pageHeader_works_as_expected(self):
        kwargs = {}
        kwargs['headline'] = ''
        kwargs['tagline'] = ''
        content = dfh.pageHeader(**kwargs)
        if content is not None:
            cheatsheet.write(content)
        return