# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/EMS/utils/LaTeX.py
# Compiled at: 2015-08-10 13:01:53
import logging, ConfigParser, time, os

class LaTeX:

    def __init__(self, examConfig, lecturer, lecture, exercisetext, solutiontext, unilogo, grouplogo, pdftitle, pdfauthor, pdfkeyword, nociteList, language):
        """initialization stuff"""
        self.__date = time.strftime('%d.%m.%Y') + ' --- 14h00 / PEII --- G120'
        self.__percentages = '30, 30,30'
        self.__semester = 'Autumn'
        self.__numbers = '1,2,3'
        self.__titles = 'Thérie,Pattern,SimJ'
        if os.path.isfile(examConfig):
            seriesConfig = ConfigParser.SafeConfigParser()
            seriesConfig.read(examConfig)
            self.__titles = seriesConfig.get('Exam', 'titles')
            self.__numbers = seriesConfig.get('Exam', 'exo-numbers')
            self.__semester = seriesConfig.get('Exam', 'semester')
            self.__date = seriesConfig.get('Exam', 'date')
            self.__percentages = seriesConfig.get('Exam', 'percentage')
        self.__lecturer = lecturer
        self.__lecturename = lecture
        self.__exercisetext = exercisetext
        self.__solutiontext = solutiontext
        self.__unilogo = unilogo
        self.__grouplogo = grouplogo
        self.__pdftitle = pdftitle
        self.__pdfauthor = pdfauthor
        self.__pdfkeyword = pdfkeyword
        self.__nociteList = nociteList
        self.__language = language
        self.__log = logging.getLogger('exaManagementSystem')

    def createHeader(self, file, isSolution):
        if isSolution:
            file.write('\\documentclass[' + self.__language + ',a4paper,12pt]{solution}' + '\n')
        else:
            file.write('\\documentclass[' + self.__language + ',a4paper,12pt]{exam-' + self.__language + '}' + '\n')
        file.write('\\newcommand{\\prof}{' + self.__lecturer + '}' + '\n')
        file.write('\\newcommand{\\course}{' + self.__lecturename + '}' + '\n')
        file.write('\\newcommand{\\theyear}{' + self.__date + '}' + '\n')
        file.write('\\newcommand{\\exercisetext}{' + self.__exercisetext + '}' + '\n')
        file.write('\\newcommand{\\solutiontext}{' + self.__solutiontext + '}' + '\n')
        file.write('\\newcommand{\\unilogo}{' + self.__unilogo + '}' + '\n')
        file.write('\\newcommand{\\groupelogo}{' + self.__grouplogo + '}' + '\n')
        file.write('\\hypersetup{pdftitle={' + self.__pdftitle + '},pdfauthor={' + self.__pdfauthor + '},pdfkeywords={' + self.__pdfkeyword + '}}\n')
        file.write('\\begin{document}\n')
        file.write('\\input{\\compilationpath/captionnames}' + '\n')
        file.write('% Header of the exercise:' + '\n')
        if not isSolution:
            per = ''
            counter = 1
            totalper = 0
            for percentage in self.__percentages.split(','):
                per += '&&\\\\\n'
                per += '' + str(counter) + ' & ......... & ' + str(percentage) + '\\\\' + '\n'
                counter += 1
                totalper += int(percentage)

            file.write('\\newcommand{\\custompercentages}{' + per + '}' + '\n')
            file.write('\\newcommand{\\totalpercentage}{' + str(totalper) + '}' + '\n')
            file.write('\\studentheader\n')
            file.write('\\exampreamble\n')

    def createFooter(self, file):
        for bib in self.__nociteList:
            file.write('\\nocite{' + bib + '}\n')

        file.write('\\end{document}\n')

    def makeWorkBookTitlePageHeader(self, _file):
        _file.write('\\documentclass[francais,a4paper]{article}' + '\n')
        _file.write('\\newcommand{\\compilationpath}{./}' + '\n')
        _file.write('\\newcommand{\\groupelogo}{' + self.__grouplogo + '}' + '\n')
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
        _file.write('{\\sf ' + self.__exercisetext + ' }' + '\n')
        _file.write('\\end{Huge}\n')
        _file.write('\\vspace{0.4cm}%\n')
        _file.write('\\begin{huge}\n')
        _file.write('Workbook (' + self.__date + ')' + '\n')
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