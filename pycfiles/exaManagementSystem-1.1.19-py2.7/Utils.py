# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/EMS/utils/Utils.py
# Compiled at: 2015-10-09 08:47:33
import logging, os, re, subprocess, sys, datetime, shutil
from subprocess import STDOUT
try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

log = logging.getLogger('exaManagementSystem')

def cleanDSStore(dir):

    def cleaner(currdir, dirs, files):
        for item in files:
            if item.find('DS_Store') != -1:
                log.debug('removing ' + currdir + '/' + item)
                os.remove(os.path.join(currdir, item))

    for root, dirs, files in os.walk('./'):
        cleaner(root, dirs, files)


def cleanTempFiles(keepTempFiles):
    if keepTempFiles:
        return
    log.info('Removing temp files')
    tmpfile = os.listdir('/tmp')
    tmpfile.sort()
    for file in tmpfile:
        if file.find('serie') != -1 or file.find('solution') != -1 or file.find('wbtitle') != -1 or file.find('catalog') != -1 or file.find('exam') != -1:
            log.debug('Removing /tmp/' + file)
            os.remove('/tmp/' + file)


def nextUnusedExercice(dir):
    lastExo = 0
    dirs = os.listdir(dir)
    dirs = natsort(dirs)
    for dir in dirs:
        exoNumber = int(dir.partition('ex')[2])
        if exoNumber > lastExo:
            lastExo = exoNumber

    lastExo = int(lastExo) + 1
    return lastExo


def natsort(list_):
    log.debug('Will filter the list ' + str(list_))
    filteredList = [ elem for elem in list_ if not elem.startswith('.') ]
    log.debug('Filtered list: ' + str(filteredList))
    tmp = [ (int(re.search('\\d+', i).group(0)), i) for i in filteredList ]
    log.debug('Tmp list: ' + str(tmp))
    tmp.sort()
    return [ i[1] for i in tmp ]


def doCheckInstall():
    """Verifies if all needed packets are installed"""
    log.info('Checking dependencies')
    missingProgs = list()
    try:
        subprocess.check_call('which gs', shell=True, stdout=open('/dev/null', 'w'))
    except subprocess.CalledProcessError as e:
        log.error('Did not found ghostscript (gs)')
        log.debug(e)
        missingProgs.append('Ghostscript (gs)')

    try:
        subprocess.check_call('which pdflatex', shell=True, stdout=open('/dev/null', 'w'))
    except subprocess.CalledProcessError as e:
        log.error('Did not found pdflatex')
        log.debug(e)
        missingProgs.append('PdfLaTeX')

    try:
        subprocess.check_call('which tar', shell=True, stdout=open('/dev/null', 'w'))
    except subprocess.CalledProcessError as e:
        log.error('Did not found Tar utility')
        log.debug(e)
        missingProgs.append('Tar')

    try:
        if len(missingProgs) != 0:
            raise Exception(missingProgs)
    except Exception as x:
        log.error('Please ensure that the needed utilities (' + x.missing + ') are installed and on the $PATH')
        sys.exit(-1)


def doLatex(texFile, outputDir, doBibTex=False):
    log.info('Running latex in %s on file %s', outputDir, texFile)
    log.debug(('LaTeX command is: latexmk -pdf -silent -outdir={:s} {:s}').format(outputDir, texFile))
    status = subprocess.call(['latexmk', '-pdf', '-silent', '-outdir=' + outputDir, texFile], cwd='./', stdout=DEVNULL, stderr=STDOUT)
    log.info('Compilation succeded ' + texFile)
    tmpfiles = os.listdir(outputDir)
    tmpfiles.sort()
    basename = os.path.split(texFile)[1].split('.')[0]
    for file in tmpfiles:
        if file.find('.pdf') == -1 and file.find(basename) != -1:
            os.remove(os.path.join(outputDir, file))


def doLatex2(texFile, outputDir, doBibTex=False):
    log.info('Running latex in %s on file %s', outputDir, texFile)
    log.debug('LaTeX command is: pdflatex -output-directory=' + outputDir + ' ' + texFile)
    latex_error_messages = ('Type X to quit or <RETURN> to proceed', '! Undefined control sequence.',
                            '? ', 'Type  H <return>  for immediate help.', 'Enter file name: ',
                            'or enter new name. (Default extension: sty)')
    latex_recompile_messages = ('recompile', 're-run', 'undefined references', 'rerun')
    auxFile = os.path.split(texFile)[1].split('.')[0] + '.aux'
    logFile = os.path.split(texFile)[1].split('.')[0] + '.log'
    recompile = True
    counter = 0
    while recompile and counter < 5:
        recompile = False
        counter += 1
        status = subprocess.call(['pdflatex', '-output-directory=' + outputDir, '-halt-on-error', texFile], cwd='./', stdout=open('/dev/null', 'w'))
        if doBibTex:
            bibstatus = subprocess.call(['bibtex', os.path.join(outputDir, auxFile)], cwd='./', stdout=open('/dev/null', 'w'))
        else:
            bibstatus = 0
        if status != 0:
            log.error('Compilation error occured. Try executing by hand pdflatex -output-directory=' + outputDir + ' -halt-on-error ' + texFile)
            exit(1)
        if bibstatus != 0:
            log.error('Compilation error occured. Try executing by hand bibtex ' + os.path.join(outputDir, auxFile))
            exit(1)
        log = open(os.path.join(outputDir, logFile), 'r')
        for line in log:
            for msg in latex_recompile_messages:
                if msg in line:
                    recompile = True
                    log.info('Need to recompile ' + texFile)
                    break

        log.close()

    log.info('Compilation succeded ' + texFile)
    tmpfiles = os.listdir(outputDir)
    tmpfiles.sort()
    basename = os.path.split(texFile)[1].split('.')[0]
    for file in tmpfiles:
        if file.find('.pdf') == -1 and file.find(basename) != -1:
            os.remove(os.path.join(outputDir, file))


def doUpdateBibTex(bibtexfile, noCiteList):
    """Updates the last visited date of the nocite bibtex items"""
    log.info('Updating BibTex Last visited time stamp')
    bibtex = open(bibtexfile, 'r')
    bibtexnew = open(os.path.join('/tmp/', bibtexfile), 'w')
    start = False
    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%b')
    day = datetime.datetime.now().strftime('%d')
    dateExpr = re.compile('\\{\\d*\\}\\{\\w+?\\}\\{\\d*\\}')
    for line in bibtex:
        if line.find('biburl{') != -1 and start:
            partitions = dateExpr.split(line)
            log.debug(partitions)
            bibtexnew.write(partitions[0] + '{' + day + '}{' + month + '}{' + year + '}' + partitions[1])
        else:
            bibtexnew.write(line)
        for cite in noCiteList:
            if line.find(cite) != -1:
                start = True

        if line.find('}') != -1 and line.find('},') == -1:
            start = False

    bibtex.close()
    bibtexnew.close()
    shutil.copy(os.path.join('/tmp/', bibtexfile), bibtexfile)