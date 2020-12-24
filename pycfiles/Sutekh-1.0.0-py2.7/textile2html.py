# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/docs/textile2html.py
# Compiled at: 2019-12-11 16:37:55
"""
Convert Sutekh textile documentation into HTML pages.
"""
import imp, os
sInfoPath = os.path.join(os.path.dirname(__file__), '..', 'SutekhInfo.py')
SutekhInfo = imp.load_source('SutekhInfo', sInfoPath).SutekhInfo
sModPath = os.path.join(os.path.dirname(__file__), '..', '..')
oFile, sModname, oDescription = imp.find_module('sutekh', [sModPath])
sutekh_package = imp.load_module('sutekh', oFile, sModname, oDescription)
Filters = sutekh_package.core.Filters
FilterParser = sutekh_package.base.core.FilterParser
sDocPath = os.path.join(os.path.dirname(__file__), '..', 'base', 'docs', 'DocUtils.py')
DocUtils = imp.load_source('DocUtils', sDocPath)
sPluginPath = os.path.join(os.path.dirname(__file__), '..', 'gui', 'PluginManager.py')
PluginManager = imp.load_source('sutekh.gui.PluginManager', sPluginPath)

def replace_version(sText):
    """Replace the version marker with the correct text."""
    return sText.replace('!Sutekh Version!', 'Sutekh %s' % SutekhInfo.BASE_VERSION_STR)


def main():
    """Actually run the doc generation"""
    oPluginMngr = PluginManager.PluginManager()
    oPluginMngr.load_plugins()
    aPlugins = oPluginMngr.get_all_plugins()
    DocUtils.make_filter_txt('textile', FilterParser.PARSER_FILTERS)
    DocUtils.convert('textile', 'html', SutekhInfo, aPlugins, replace_version)
    DocUtils.cleanup('textile')


if __name__ == '__main__':
    main()