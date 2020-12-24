# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/SMS/utils/LaTeX.py
# Compiled at: 2015-08-11 04:57:39
import logging, sys
if float(sys.version[:3]) < 3.0:
    import ConfigParser
else:
    import configparser as ConfigParser
from pkg_resources import resource_filename
from os.path import dirname, join

class LaTeX:

    def __init__(self, serie):
        """initialization stuff"""
        smsConfig = ConfigParser.SafeConfigParser()
        smsConfig.read([join(resource_filename(__name__, 'data'), 'lecture.cfg'), 'lecture.cfg'])
        self.__name = smsConfig.get('Lecture', 'name')
        self.__lecturer = smsConfig.get('Lecture', 'lecturer')
        self.__year = smsConfig.get('Lecture', 'year')
        self.__exercisetext = smsConfig.get('Lecture', 'exercisetext')
        self.__solutiontext = smsConfig.get('Lecture', 'solutiontext')
        self.__contenttext = smsConfig.get('Lecture', 'contenttext')
        self.__headertitle = smsConfig.get('Lecture', 'headertitle')
        self.__bibtex = smsConfig.get('Lecture', 'bibtex')
        self.__noCiteList = smsConfig.get('Lecture', 'nocite').split(',')
        self.__unilogo = smsConfig.get('Logo', 'unilogo')
        self.__groupelogo = smsConfig.get('Logo', 'groupelogo')
        self.__pdfkeyword = smsConfig.get('PDF', 'pdfkeyword')
        self.__pdftitle = smsConfig.get('PDF', 'pdftitle')
        self.__pdfauthor = smsConfig.get('PDF', 'pdfauthor')
        self.__serie = serie
        self.__log = logging.getLogger('seriesManagementSystem')

    def createHeader(self, _file, titles, isSolution=False):
        _file.write('\\documentclass[francais,a4paper]{article}' + '\n')
        _file.write('\\usepackage{sms}\n')
        _file.write('\\newcommand{\\compilationpath}{./}' + '\n')
        _file.write('\\newcommand{\\prof}{' + self.__lecturer + '}' + '\n')
        _file.write('\\newcommand{\\course}{' + self.__name + '}' + '\n')
        _file.write('\\newcommand{\\theyear}{' + self.__year + '}' + '\n')
        _file.write('\\newcommand{\\exercisetext}{' + self.__exercisetext + '}' + '\n')
        if isSolution:
            solutionText = self.__solutiontext
        else:
            solutionText = ''
        _file.write('\\newcommand{\\solutiontext}{' + solutionText + '}' + '\n')
        _file.write('\\newcommand{\\thecontent} {\\sffamily\\bfseries ' + self.__contenttext + ':}' + '\n')
        _file.write('\\newcommand{\\theheadertitle}{' + self.__headertitle + '}' + '\n')
        _file.write('\\newcommand{\\unilogo}{' + self.__unilogo + '}' + '\n')
        _file.write('\\newcommand{\\groupelogo}{' + self.__groupelogo + '}' + '\n')
        _file.write('% Number of the serie' + '\n')
        _file.write('\\newcommand{\\exercisenb}{' + str(self.__serie) + '}' + '\n')
        _file.write('\\newcommand{\\includepath}{\\compilationpath}' + '\n')
        _file.write('\\hypersetup{pdftitle={' + self.__pdftitle + '},pdfauthor={' + self.__pdfauthor + '},pdfkeywords={' + self.__pdfkeyword + '}}\n')
        _file.write('\\begin{document}\n')
        _file.write('\\input{\\compilationpath/captionnames}' + '\n')
        _file.write('% Header of the exercise:' + '\n')
        _file.write('\\exheader\n')
        if len(titles) != 0:
            _file.write('% Content of the exercise, topics' + '\n')
            _file.write('\\content{\n')
            _file.write('\\begin{itemize}\n')
            for title in titles:
                _file.write('\\item ' + title + '\n')

            _file.write('\\end{itemize}\n')
            _file.write('}\n')

    def createFooter(self, _file):
        for bib in self.__noCiteList:
            _file.write('\\nocite{' + bib + '}\n')

        _file.write('\\bibliography{bibdb}' + '\n')
        _file.write('\\bibliographystyle{plain}' + '\n')
        _file.write('\\end{document}\n')

    def makeWorkBookTitlePageHeader(self, _file):
        _file.write('\\documentclass[francais,a4paper]{article}' + '\n')
        _file.write('\\newcommand{\\compilationpath}{./}' + '\n')
        _file.write('\\newcommand{\\groupelogo}{' + self.__groupelogo + '}' + '\n')
        _file.write('\\usepackage{graphicx}' + '\n')
        _file.write('\\usepackage{palatino}' + '\n')
        _file.write('%\\usepackage[french]{babel}' + '\n')
        _file.write('\\usepackage[utf8]{inputenc}' + '\n')
        _file.write('\\usepackage{ae, pslatex}    % Joli output en PDF' + '\n')
        _file.write('%\\usepackage{graphics}          % Manipulation de boîtes et importation de graphismes.' + '\n')
        _file.write('%\\usepackage[dvips]{graphicx}   %' + '\n')
        _file.write('\\usepackage[T1]{fontenc}' + '\n')
        _file.write('\\begin{document}\n')
        _file.write('\\pagestyle{empty}\n')
        _file.write('\\vspace{-1cm}\n')
        _file.write('\\begin{center}\n')
        _file.write('\\begin{Huge}\n')
        _file.write('{\\sf ' + self.__name + ' }' + '\n')
        _file.write('\\end{Huge}\n')
        _file.write('\\vspace{0.4cm}%\n')
        _file.write('\\begin{huge}\n')
        _file.write('Workbook (' + self.__year + ')' + '\n')
        _file.write('\\end{huge}\n')
        _file.write('\\end{center}\n')
        _file.write('\\rule{\\linewidth}{1pt}' + '\n')
        _file.write('\\vspace{1cm}\n')

    def printWorkBookTitlePageFooter(self, _file):
        _file.write('%\\end{itemize}\n')
        _file.write('\\rule{\\linewidth}{1pt}' + '\n')
        _file.write('\\vfill\n')
        _file.write('\\centering\n')
        _file.write('\\includegraphics[height=1.65cm]{\\compilationpath/logos/\\groupelogo}' + '\n')
        _file.write('\\end{document}\n')