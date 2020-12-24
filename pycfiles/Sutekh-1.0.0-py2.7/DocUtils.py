# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/docs/DocUtils.py
# Compiled at: 2019-12-11 16:37:52
"""Useful utilities for generating HTML documentation"""
from __future__ import print_function
import os, glob, re, textile
try:
    import tidy
except ImportError:
    tidy = None

HTML_HEADER = '\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n    <title>%(title)s</title>\n</head>\n<body>\n'
HTML_FOOTER = '\n</body>\n</html>\n'
FILTER_USAGE = 'h2(#usage). Usage\n\nFilter elements and values for the filters can be dragged from the right\nhand pane to the filter to add them to the filter, and dragged from the filter\nto the right hand pane to remove them from the filter. Disabled filter\nelements or filter elements with no values set are ignored.\n'
FILTER_NAVIGATION = 'h2(#navigation). Keyboard Navigation\n\nYou can switch between the different filter lists using\n*&lt;Alt&gt;--&lt;Left&gt;* and *&lt;Alt&gt;--&lt;Right&gt;*.\n*&lt;Ctrl&gt;--&lt;Enter&gt;* will paste the currently selected list of values\ninto the filter.  *&lt;Del&gt;* will delete a value or filter part from the\nfilter *&lt;Ctrl&gt;--&lt;Space&gt;* will disable a filter part, while\n*&lt;Alt&gt;--&lt;Space&gt;* will negate it.\n'
FILTER_ELEMENTS = "h2(#elements). Filter Elements\n\nThe available filtering options are listed below.  The first line of each item\nshows the description you'll see in the filter editor in bold.  The rest of the\ndescription describes the arguments the filter takes and the results it\nproduces.\n"

def _make_link(sName):
    """Helper function to generate a sensible html link
       from the menu name."""
    sLinkTag = sName.lower()
    for sChar in [',', '(', ')', ' ', '-']:
        sLinkTag = sLinkTag.replace(sChar, '')

    return sLinkTag


class FilterGroup(object):
    """Fake filter for Filter Group help."""
    description = 'Filter Group'
    keyword = 'filter_group'
    helptext = "A list of other filter elements.\nFilter element with holds other filter elements. The result of the filter group is  the combination of all the filter elements as specified by the Filter Group type.\n\nThe 4 Group types are:\n\n* _All of_: This filter matches only if every filter in the group matches.\n* _Any of_: This filter matches if at least one of the filters in the group matches.\n* _Not all of_: This filter matches if at least one of the filters in the group doesn't match.\n* _Not any of_: This filter matches only if none of the filters in the group match.\n"


def textile2html(sText, dContext, fProcessText):
    """Convert a Textile markup string to an HTML file."""
    sHtml = ('').join([HTML_HEADER % dContext,
     textile.textile(fProcessText(sText)),
     HTML_FOOTER % dContext])
    sHtml = sHtml.replace('<br />', ' ')
    return sHtml


def textile2markdown(aLines, fProcessText):
    """Convert textile content to markdown.

       This is rule-based, and doesn't cover the full textile syntax.
       We aim to convert to the markdown variant supported by the
       sourceforge wiki."""
    HEADER = re.compile('h([0-9])\\(#(.*)\\)\\. (.*)$')
    NUM_LINK = re.compile('^(#*) "([^:]*)":(#.*)$')
    LINK_TEXT = re.compile('"([^"]*)":([^ ]*)\\b')
    LIST_ITEM = re.compile('^(\\*+)([^\\*]+$|[^\\*]+\\*[^\\*]+\\*[^\\*]*)+$')
    EMP_ITEM = re.compile('\\*([^\\*]+)\\*')
    aOutput = []
    for sLine in aLines:
        sLine = fProcessText(sLine).strip()
        if not sLine:
            sLine = '\n\n'
        elif sLine.startswith('h1.'):
            sLine = sLine.replace('h1.', '#')
        elif sLine.startswith('h2.'):
            sLine = sLine.replace('h2.', '##')
        elif sLine.startswith('h3.'):
            sLine = sLine.replace('h3.', '###')
        elif sLine.startswith('h4.'):
            sLine = sLine.replace('h4.', '####')
        else:
            oMatch = HEADER.search(sLine)
            if oMatch:
                sDepth, sLabel, sHeader = oMatch.groups()
                sLine = '%s <a name="%s"></a> %s' % ('#' * int(sDepth),
                 sLabel, sHeader)
            oMatch = NUM_LINK.search(sLine)
            if oMatch:
                sHash, sText, sLink = oMatch.groups()
                sIndent = '  ' * len(sHash)
                sLine = '%s 1. [%s](%s)\n' % (sIndent, sText, sLink)
            sLine = re.sub(LINK_TEXT, '[\\1](\\2)', sLine)
            oMatch = LIST_ITEM.search(sLine)
            if oMatch:
                sIndent = '    ' * (len(oMatch.groups()[0]) - 1) + '-\\2'
                sLine = re.sub(LIST_ITEM, sIndent, sLine)
                sLine += '\n'
            sLine = re.sub(EMP_ITEM, '**\\1**', sLine)
        if not sLine.endswith('\n'):
            sLine += ' '
        aOutput.append(sLine)

    return ('').join(aOutput)


def _load_textile(sTextilePath):
    """Load lines from the textile file."""
    fTextile = open(sTextilePath, 'rb')
    aLines = []
    aCurLine = []
    for sLine in fTextile.readlines():
        if sLine.endswith('\\\n'):
            if aCurLine:
                aCurLine.append(sLine[:-2])
            else:
                aCurLine = [
                 sLine[:-2]]
            continue
        elif aCurLine:
            aCurLine.append(sLine)
            aLines.append(('').join(aCurLine))
            aCurLine = []
        else:
            aLines.append(sLine)

    fTextile.close()
    return aLines


def _process_plugins(aLines, aPlugins):
    """Add help text for plugins to the textile data."""
    dTags = {}
    for sLine in aLines:
        if sLine.startswith(':'):
            if ':list:' in sLine or ':numbered:' in sLine or ':text:' in sLine:
                sTag = sLine.split(':', 3)[3].strip()
                if sTag not in dTags:
                    dTags[sTag] = {':list:': [], ':numbered:': [], ':text:': []}
            else:
                print('Unknown Tag type %s' % sLine)

    if dTags:
        for cPlugin in aPlugins:
            sPluginCat = cPlugin.get_help_category()
            if sPluginCat is None:
                continue
            if sPluginCat not in dTags:
                print('%s has unrecognised plugin help category: %s' % (
                 cPlugin, sPluginCat))
                continue
            sName = cPlugin.get_help_menu_entry()
            if not sName:
                print('%s has no Help menu entry - Skipped' % cPlugin)
                continue
            sLinkTag = _make_link(sName)
            sText = cPlugin.get_help_list_text()
            dTags[sPluginCat][':list:'].append('*listlevel* "%s":#%s %s' % (sName, sLinkTag, sText))
            sText = cPlugin.get_help_numbered_text()
            dTags[sPluginCat][':numbered:'].append('#numlevel# "%s":#%s %s' % (sName, sLinkTag, sText))
            sText = cPlugin.get_help_text()
            dTags[sPluginCat][':text:'].append('hlevel(#%s). %s\n\n%s\n\n' % (sLinkTag, sName, sText))

        for iCnt, sLine in enumerate(aLines):
            if sLine.startswith(':') and (':list:' in sLine or ':numbered:' in sLine or ':text:' in sLine):
                _sHead, _sSkipType, sLevel, sTag = sLine.split(':', 3)
                sTag = sTag.strip()
                iLevel = int(sLevel)
                for sType, aData in dTags[sTag].items():
                    sFullTag = '%s%d:%s' % (sType, iLevel, sTag)
                    if sType in sLine:
                        sData = ('\n').join(aData)
                        if sType == ':list:':
                            sData = sData.replace('*listlevel*', '*' * iLevel)
                        elif sType == ':numbered:':
                            sData = sData.replace('#numlevel#', '#' * iLevel)
                        elif sType == ':text:':
                            sData = sData.replace('hlevel(', 'h%d(' % iLevel)
                        aLines[iCnt] = sLine.replace(sFullTag, sData)

                if not aLines[iCnt].strip():
                    aLines[iCnt] = ''
                    print('Unused tag %s' % sTag)

    sText = ('').join(aLines)
    return sText.split('\n')


def convert(sTextileDir, sHtmlDir, cAppInfo, aPlugins, fProcessText):
    """Convert all .txt files in sTextileDir to .html files in sHtmlDir."""
    for sTextilePath in glob.glob(os.path.join(sTextileDir, '*.txt')):
        sBasename = os.path.basename(sTextilePath)
        sFilename, _sExt = os.path.splitext(sBasename)
        sHtmlPath = os.path.join(sHtmlDir, sFilename + '.html')
        dContext = {'title': '%s %s' % (cAppInfo.NAME, sFilename.replace('_', ' '))}
        fHtml = open(sHtmlPath, 'wb')
        aLines = _load_textile(sTextilePath)
        aLines = _process_plugins(aLines, aPlugins)
        fHtml.write(textile2html(('\n').join(aLines), dContext, fProcessText))
        fHtml.close()
        if tidy is not None:
            aErrors = tidy.parse(sHtmlPath).get_errors()
            if aErrors:
                print('tidy reports the following errors for %s' % sHtmlPath)
                print(('\n').join([ x.err for x in aErrors ]))

    return


def convert_to_markdown(sTextileDir, sMarkdownDir, aPlugins, fProcessText):
    """Convert textile files to markdown syntax."""
    for sTextilePath in glob.glob(os.path.join(sTextileDir, '*.txt')):
        sBasename = os.path.basename(sTextilePath)
        sFilename, _sExt = os.path.splitext(sBasename)
        sMarkdownPath = os.path.join(sMarkdownDir, sFilename + '.md')
        fMarkdown = open(sMarkdownPath, 'wb')
        aLines = _load_textile(sTextilePath)
        aLines = _process_plugins(aLines, aPlugins)
        fMarkdown.write(textile2markdown(aLines, fProcessText))
        fMarkdown.close()


def add_single_filter(aOutput, iTocIndex, sKeyword, oFilter):
    """Add a single filter's help text to the file"""
    sDesc = oFilter.description
    sLink = sKeyword.lower()
    aOutput.insert(iTocIndex, '## "%s":#%s\n' % (
     sDesc, sLink))
    iTocIndex += 1
    aOutput.append('h3(#%s). %s\n\n' % (sLink, sDesc))
    try:
        sInput, sRest = oFilter.helptext.split('\n', 1)
        aOutput.append('*Parameters:* %s\n\n' % sInput)
        aOutput.append(sRest)
    except ValueError:
        print('Failed to extract filter details')
        print(oFilter.keyword, oFilter.helptext)

    aOutput.append('\n\n')
    return iTocIndex


def add_filters(aOutput, iTocIndex, dFilters):
    """Add the appropriate list of filters"""
    for sKeyword in sorted(dFilters):
        oFilter = dFilters[sKeyword]
        iTocIndex = add_single_filter(aOutput, iTocIndex, sKeyword, oFilter)

    return iTocIndex


def make_filter_txt(sDir, aFilters):
    """Convert base filters into the approriate textile files"""
    dSections = {'Usage': FILTER_USAGE, 
       'Elements': FILTER_ELEMENTS, 
       'Navigation': FILTER_NAVIGATION}
    dCardSetFilters = {}
    dCardFilters = {}
    for oFilter in aFilters:
        if 'PhysicalCardSet' in oFilter.types:
            dCardSetFilters[oFilter.keyword] = oFilter
        else:
            dCardFilters[oFilter.keyword] = oFilter

    for sTemplatePath in glob.glob(os.path.join(sDir, '*.tmpl')):
        sBasename = os.path.basename(sTemplatePath)
        sFilename, _sExt = os.path.splitext(sBasename)
        sTextilePath = os.path.join(sDir, sFilename + '.txt')
        aOutput = []
        iTocIndex = 0
        fTemplate = open(sTemplatePath, 'rb')
        fTextile = open(sTextilePath, 'wb')
        for sLine in fTemplate.readlines():
            sKeyword = sLine.strip()
            if sKeyword.startswith('!') and sKeyword.endswith('!'):
                sKeyword = sKeyword.replace('!', '')
            else:
                aOutput.append(sLine)
                continue
            if sKeyword == '#toc':
                iTocIndex = len(aOutput)
                continue
            elif sKeyword == 'Filter_Group':
                iTocIndex = add_single_filter(aOutput, iTocIndex, sKeyword, FilterGroup)
            elif sKeyword == 'card_filters_long':
                iTocIndex = add_filters(aOutput, iTocIndex, dCardFilters)
            elif sKeyword == 'card_set_filters_long':
                iTocIndex = add_filters(aOutput, iTocIndex, dCardSetFilters)
            elif sKeyword in dSections:
                sText = dSections[sKeyword]
                sLink = sKeyword.lower()
                sDesc = sText.split('\n', 1)[0]
                sDesc = sDesc.split('). ', 1)[1]
                aOutput.insert(iTocIndex, '# "%s":#%s\n' % (
                 sDesc, sLink))
                iTocIndex += 1
                aOutput.append(sText)
                aOutput.append('\n')
            else:
                print('Unrecognised Keyword in template %s: %s' % (sBasename,
                 sKeyword))

        fTextile.write(('').join(aOutput))


def cleanup(sDir):
    """Remove the autogenerated textile files"""
    for sTemplatePath in glob.glob(os.path.join(sDir, '*.tmpl')):
        sBasename = os.path.basename(sTemplatePath)
        sFilename, _sExt = os.path.splitext(sBasename)
        sTextilePath = os.path.join(sDir, sFilename + '.txt')
        os.remove(sTextilePath)