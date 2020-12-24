# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/bibolamazi_gui/helpbrowser.py
# Compiled at: 2015-05-11 05:40:29
import sys, logging, bibolamazi.init
from bibolamazi.core import main as bibolamazimain
from bibolamazi.core import blogger
from bibolamazi.core.blogger import logger
from bibolamazi.core import butils
from bibolamazi.core import argparseactions
from bibolamazi.core.bibfilter import factory as filters_factory
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from . import filterinstanceeditor
from . import settingswidget
from .qtauto.ui_helpbrowser import Ui_HelpBrowser
logger = logging.getLogger(__name__)
_HOME_TAB_STYLESHEET = '\nQWidget {\n}\n\n#wFilters {\n    padding: 10px 50px 10px 50px;\n    background-color: white;\n}\n\n\nQPushButton {\n    color: rgba(255,255,255,255);\n    padding: 8px 2px;\n}\nQPushButton {\n    /* light blue */\n    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 113, 188, 255), stop:0.9 rgba(64, 91, 110, 255));\n}\nQPushButton[bibolamaziHelpButtonType="filter"] {\n    /* bordeau */\n    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(158, 0, 93, 255), stop:0.9 rgba(82, 55, 71, 255));\n}\nQPushButton[bibolamaziHelpButtonType="intro"] {\n    /* dark blue */\n\tbackground-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(27, 20, 100, 255), stop:0.9 rgba(77, 75, 99, 255));\n}\n'

class HelpBrowser(QWidget):

    def __init__(self):
        super(HelpBrowser, self).__init__()
        self.ui = Ui_HelpBrowser()
        self.ui.setupUi(self)
        QObject.connect(self.ui.tabs, SIGNAL('tabCloseRequested(int)'), self.closeTab)
        self.filterButtons = []
        self.openTabs = []
        self.ui.lytHomeButtons.setContentsMargins(60, 30, 60, 30)
        vspc1 = QSpacerItem(20, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.lytHomeButtons.addItem(vspc1, 1, 0)
        offsetlineno = 2
        n = 0
        ncols = 2
        for filt in filterinstanceeditor.get_filter_list():
            fbutton = QPushButton('%s' % filt, self)
            fbutton.setProperty('helppath', 'filters/%s' % filt)
            fbutton.setProperty('bibolamaziHelpButtonType', 'filter')
            fbutton.setToolTip(filters_factory.get_filter_class(filt).getHelpDescription())
            self.ui.lytHomeButtons.addWidget(fbutton, offsetlineno + int(n / ncols), n % ncols)
            n += 1
            QObject.connect(fbutton, SIGNAL('clicked()'), self.openHelpTopicBySender)

        newrow = None
        if n % ncols == 0:
            newrow = offsetlineno + n / ncols
        else:
            newrow = offsetlineno + (1 + int(n / ncols))
        vspc3 = QSpacerItem(20, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.lytHomeButtons.addItem(vspc3, newrow, 0)
        self.ui.lytHomeButtons.addWidget(self.ui.btnCmdLineHelp, newrow + 1, 0)
        self.ui.lytHomeButtons.addWidget(self.ui.btnVersion, newrow + 1, 1)
        vspc2 = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.lytHomeButtons.addItem(vspc2, newrow + 2, 0)
        self.vspcButtons = [
         vspc1, vspc2]
        self.ui.tabHome.setStyleSheet(_HOME_TAB_STYLESHEET)
        static_help_btns = [
         self.ui.btnWelcome,
         self.ui.btnVersion,
         self.ui.btnFilterList,
         self.ui.btnCmdLineHelp]
        for btn in static_help_btns:
            QObject.connect(btn, SIGNAL('clicked()'), self.openHelpTopicBySender)

        self.shortcuts = [
         QShortcut(QKeySequence('Ctrl+W'), self, self.closeCurrentTab, self.closeCurrentTab)]
        return

    @pyqtSlot()
    def closeCurrentTab(self):
        index = self.ui.tabs.currentIndex()
        if index == 0:
            self.hide()
            return
        self.closeTab(index)

    @pyqtSlot(int)
    def closeTab(self, index):
        if index == 0:
            return
        del self.openTabs[index - 1]
        self.ui.tabs.removeTab(index)

    @pyqtSlot()
    def openHelpTopicBySender(self):
        sender = self.sender()
        path = str(sender.property('helppath').toString())
        if not path:
            logger.warning('Bad help topic path: %r', path)
            return
        self.openHelpTopic(path)

    @pyqtSlot(QString)
    def openHelpTopic(self, spath):
        path = str(spath)
        pathitems = [ x for x in path.split('/') if x ]
        for tab in self.openTabs:
            if str(tab.property('helppath').toString()) == ('/').join(pathitems):
                self.ui.tabs.setCurrentWidget(tab)
                return

        widget = self.makeHelpTopicTab(pathitems)
        if widget is None:
            return
        else:
            widget.setProperty('helppath', ('/').join(pathitems))
            tabindex = self.ui.tabs.addTab(widget, widget.property('HelpTabTitle').toString())
            self.ui.tabs.setTabToolTip(tabindex, widget.property('HelpTabToolTip').toString())
            self.ui.tabs.setCurrentIndex(tabindex)
            self.openTabs.append(widget)
            return

    def makeHelpTopicTab(self, pathitems):
        if not len(pathitems):
            logger.warning('makeHelpTopicTab(): No Path specified!')
            return
        else:
            font = settingswidget.get_typewriter_font(self)
            if pathitems[0] == 'filters':
                if len(pathitems) < 2:
                    logger.warning('makeHelpTopicTab(): No filter specified!!')
                    return
                filtname = pathitems[1]
                tb = QTextBrowser(self.ui.tabs)
                tb.setFont(font)
                tb.setText(filters_factory.format_filter_help(filtname))
                tb.setProperty('HelpTabTitle', '%s filter' % filtname)
                tb.setProperty('HelpTabToolTip', filters_factory.get_filter_class(filtname).getHelpDescription())
                return tb
            if pathitems[0] == 'general':
                if len(pathitems) < 2:
                    logger.warning('makeHelpTopicTab(): No help topic general page specified!!')
                    return
                tb = QTextBrowser(self.ui.tabs)
                tb.setFont(font)
                if pathitems[1] == 'welcome':
                    tb.setPlainText(HELP_WELCOME)
                    tb.setProperty('HelpTabTitle', 'Welcome')
                elif pathitems[1] == 'version':
                    tb.setPlainText(argparseactions.helptext_prolog())
                    tb.setProperty('HelpTabTitle', 'Version')
                elif pathitems[1] == 'cmdline':
                    tb.setPlainText(argparseactions.helptext_prolog() + bibolamazimain.get_args_parser().format_help())
                    tb.setProperty('HelpTabTitle', 'Command-Line Help')
                elif pathitems[1] == 'filter-list':
                    tb.setPlainText(argparseactions.help_list_filters())
                    tb.setProperty('HelpTabTitle', 'Filter List')
                else:
                    tb.setPlainText('<Unknown help page>')
                    tb.setProperty('HelpTabTitle', '<Unknown>')
                tb.setProperty('HelpTabToolTip', '')
                return tb
            logger.warning('makeHelpTopicTab(): Unknown help topic: %r', ('/').join(pathitems))
            return


HELP_WELCOME = "\n\n======================================================================\nBibolamazi -- Prepare consistent BibTeX files for your LaTeX documents\n======================================================================\n\nBibolamazi lets you prepare consistent and uniform BibTeX files for your LaTeX\ndocuments. It lets you prepare your BibTeX entries as you would like them to\nbe---adding missing or dropping irrelevant information, capitalizing names or\nturning them into initials, converting unicode characters to latex escapes, etc.\n\n\nWhat Bibolamazi Does\n--------------------\n\nBibolamazi works by reading your reference bibtex files---the ``sources'', which\nmight for example have been generated by your favorite bibliography manager or\nprovided by your collaborators---and merging them all into a new file, applying\nspecific rules, or ``filters'', such as turning all the first names into\ninitials or normalizing the way arxiv IDs are presented.\n\nThe Bibolamazi file is this new file, in which all the required bibtex entries\nwill be merged. When you prepare you LaTeX document, you should create a new\nbibolamazi file, and provide that bibolamazi file as the bibtex file for the\nbibliography.\n\nWhen you open a bibolamazi file, you will be prompted to edit its configuration.\nThis is the set of rules which will tell bibolamazi where to look for your\nbibtex entries and how to handle them. You first need to specify all your\nsources, and then all the filters.\n\nThe bibolamazi file is then a valid BibTeX file to include into your LaTeX\ndocument, so if your bibolamazi file is named `main.bibolamazi.bib', you would\ninclude the bibliography in your document with a LaTeX command similar to:\n\n    \\bibliography{main.bibolamazi}\n\n\nThe Bibolamazi Configuration Section\n------------------------------------\n\nIf you open the Bibolamazi application and open your bibolamazi file (or create\na new one), you’ll immediately be prompted to edit its configuration section.\n\nSources are the normal bibtex files from which bibtex entries are read. A source\nis specified using the bibolamazi command\n\n  src: source-file.bib  [ alternative-source-file.bib  ... ]\n\nAlternative source locations can be specified, in case the first file does not\nexist. This is convenient to locate a file which might be in different locations\non different computers. Each source file name can be an absolute path or a\nrelative path (relative to the bibolamazi file). It can also be an HTTP URL\nwhich will be downloaded automatically.\n\nYou can specify several sources by repeating the src: command.\n\n  src: first-source.bib  alternative-first-source.bib\n  src: second-source.bib\n  ...\n\nRemember: the *first* readable source of *each* source command will be read, and\nmerged into the bibolamazi file.\n\nFilters are rules to apply on the whole bibliography database. Their syntax is\n\n  filter: filter_name  <filter-options>\n\nThe filter is usually meant to deal with a particular task, such as for example\nchanging all first names of authors into initials.\n\nFor a list of filters and what they do, please refer the first page of this help\nbrowser.\n\nYou can usually fine-tune the behavior of the filter by providing options. For\na list of options for a particular filter, please refer again to the help page\nof that filter.\n\n\nWhat now?\n---------\n\nWe suggest at this point that you create a new bibolamazi file, and get started\nwith the serious stuff :)\n\nYou might want to have a look at the documentation. It is available at:\n\n  http://bibolamazi.readthedocs.org/en/latest/\n\nIf you want an example, you can have a look at the directory\n\n  https://github.com/phfaist/bibolamazi/tree/master/test\n\nand, in particular the bibolamazi files `testX.bibolamazi.bib`.\n\n\nCommand-line\n------------\n\nPlease note that you can also use bibolamazi in command-line. If you installed\nthe precompiled application, you'll need to install the command-line version\nagain. Go to\n\n  https://github.com/phfaist/bibolamazi\n\nand follow the instructions there.\n\n"