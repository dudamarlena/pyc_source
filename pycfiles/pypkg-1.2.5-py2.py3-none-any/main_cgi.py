# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: main_cgi.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    Driver for PDB2PQR\n\n    This module takes a PDB file as input and performs optimizations\n    before yielding a new PDB-style file as output.\n\n    Ported to Python by Todd Dolinsky (todd@ccb.wustl.edu)\n    Washington University in St. Louis\n\n    Parsing utilities provided by Nathan A. Baker (Nathan.Baker@pnl.gov)\n    Pacific Northwest National Laboratory\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; \n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific \n    Northwest National Laboratory, operated by Battelle Memorial Institute, \n    Pacific Northwest Division for the U.S. Department Energy.; \n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n\tAll rights reserved.\n\n\tRedistribution and use in source and binary forms, with or without modification, \n\tare permitted provided that the following conditions are met:\n\n\t\t* Redistributions of source code must retain the above copyright notice, \n\t\t  this list of conditions and the following disclaimer.\n\t\t* Redistributions in binary form must reproduce the above copyright notice, \n\t\t  this list of conditions and the following disclaimer in the documentation \n\t\t  and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n\tTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND \n\tANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n\tWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. \n\tIN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, \n\tINDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, \n\tBUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, \n\tDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF \n\tLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE \n\tOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED \n\tOF THE POSSIBILITY OF SUCH DAMAGE.\n\n'
__date__ = '5 April 2010'
__author__ = 'Todd Dolinsky, Nathan Baker, Jens Nielsen, Paul Czodrowski, Jan Jensen, Samir Unni, Yong Huang'
import glob, os, time, re, sys, string
from StringIO import StringIO
from src.pdb import readPDB
from src.definitions import Definition
from src.protein import Protein
from src import utilities
from src.server import setID, createError
from src.aconf import STYLESHEET, WEBSITE, PDB2PQR_OPAL_URL, HAVE_PDB2PQR_OPAL, INSTALLDIR, TMPDIR, MAXATOMS, PDB2PQR_VERSION
import traceback
__version__ = PDB2PQR_VERSION
from main import runPDB2PQR

def printHeader(pagetitle, have_opal=None, jobid=None):
    """
        Function to print html headers
    """
    if jobid:
        if have_opal:
            print 'Location: querystatus.cgi?jobid=%s&typeofjob=opal\n' % jobid
        else:
            print 'Location: querystatus.cgi?jobid=%s&typeofjob=local\n' % jobid
    print '<HTML>'
    print '<HEAD>'
    print '\t<TITLE>%s</TITLE>' % pagetitle
    print '\t<link rel="stylesheet" href="%s" type="text/css">\n' % STYLESHEET
    print '</HEAD>'


def redirector(name, weboptions):
    """
        Prints a page which redirects the user to querystatus.cgi and writes starting time to file
    """
    redirectWait = 3
    utilities.startLogFile(name, 'pdb2pqr_start_time', str(time.time()))
    jobid = int(name)
    analiticsDict = weboptions.getOptions()
    events = {}
    events['submission'] = analiticsDict['pdb'] + '|' + str(os.environ['REMOTE_ADDR'])
    del analiticsDict['pdb']
    events['titration'] = str(analiticsDict.get('ph'))
    if 'ph' in analiticsDict:
        del analiticsDict['ph']
    events['apbsInput'] = str(analiticsDict.get('apbs'))
    del analiticsDict['apbs']
    if 'selectedExtensions' in analiticsDict:
        analiticsDict['selectedExtensions'] = (' ').join(analiticsDict['selectedExtensions'])
    options = (',').join(str(k) + ':' + str(v) for k, v in analiticsDict.iteritems())
    events['options'] = options
    eventsScriptString = ''
    for event in events:
        eventsScriptString += utilities.getEventTrackingString(category='submissionData', action=event, label=events[event])

    redirectURL = ('{website}querystatus.cgi?jobid={jobid}&calctype=pdb2pqr').format(website=WEBSITE, jobid=jobid)
    string = ('\n<html>\n    <head>\n        {trackingscript}\n        <script type="text/javascript">\n            {trackingevents}\n        </script>\n        <meta http-equiv="Refresh" content="{wait}; url={redirectURL}"> \n        <link rel="stylesheet" href="{website}pdb2pqr.css"type="text/css">\n    </head>\n    <body>\n    <center>\n        You are being automatically redirected to a new location.<br />\n        If your browser does not redirect you in {wait} seconds, or you do\n        not wish to wait, <a href="{redirectURL}">click here</a></center>. \n    </body>\n</html>').format(trackingscript=utilities.getTrackingScriptString(jobid=jobid), trackingevents=eventsScriptString, redirectURL=redirectURL, wait=redirectWait, website=WEBSITE)
    return string


def sanitizeFileName(fileName):
    fileName = re.split('[/\\\\]', fileName)[(-1)]
    fileName = fileName.replace(' ', '_')
    fileName = fileName.replace('-', '_')
    return fileName


class WebOptionsError(Exception):
    pass


class WebOptions(object):
    """Helper class for gathering and querying options selected by the user"""

    def __init__(self, form):
        """Gleans all information about the user selected options and uploaded files.
        Also validates the user input. Raises WebOptionsError if there is any problems."""
        self.runoptions = {}
        self.otheroptions = {}
        self.runoptions['debump'] = form.has_key('DEBUMP')
        self.runoptions['opt'] = form.has_key('OPT')
        if form.has_key('FF'):
            self.ff = form['FF'].value.lower()
        else:
            raise WebOptionsError('Force field type missing from form.')
        if form.has_key('PDBID') and form['PDBID'].value and form['PDBSOURCE'].value == 'ID':
            self.pdbfile = utilities.getPDBFile(form['PDBID'].value)
            if self.pdbfile is None:
                raise WebOptionsError('The pdb ID provided is invalid.')
            self.pdbfilestring = self.pdbfile.read()
            self.pdbfile = StringIO(self.pdbfilestring)
            self.pdbfilename = form['PDBID'].value
        elif form.has_key('PDB') and form['PDB'].filename and form['PDBSOURCE'].value == 'UPLOAD':
            self.pdbfilestring = form['PDB'].value
            self.pdbfile = StringIO(self.pdbfilestring)
            self.pdbfilename = sanitizeFileName(form['PDB'].filename)
        else:
            raise WebOptionsError('You need to specify a pdb ID or upload a pdb file.')
        if form.has_key('PKACALCMETHOD'):
            if form['PKACALCMETHOD'].value != 'none':
                if not form.has_key('PH'):
                    raise WebOptionsError('Please provide a pH value.')
                phHelp = 'Please choose a pH between 0.0 and 14.0.'
                try:
                    ph = float(form['PH'].value)
                except ValueError:
                    raise WebOptionsError('The pH value provided must be a number!  ' + phHelp)

                if ph < 0.0 or ph > 14.0:
                    text = 'The entered pH of %.2f is invalid!  ' % ph
                    text += phHelp
                    raise WebOptionsError(text)
                self.runoptions['ph'] = ph
                if form['PKACALCMETHOD'].value == 'propka':
                    self.runoptions['ph_calc_method'] = 'propka'
                    self.runoptions['ph_calc_options'] = utilities.createPropkaOptions(ph, False)
                if form['PKACALCMETHOD'].value == 'pdb2pka':
                    self.runoptions['ph_calc_method'] = 'pdb2pka'
                    self.runoptions['ph_calc_options'] = {'output_dir': 'pdb2pka_output', 'clean_output': True, 
                       'pdie': 8, 
                       'sdie': 80, 
                       'pairene': 1.0}
        self.otheroptions['apbs'] = form.has_key('INPUT')
        self.otheroptions['whitespace'] = form.has_key('WHITESPACE')
        if self.ff == 'user':
            if form.has_key('USERFF') and form['USERFF'].filename:
                self.userfffilename = sanitizeFileName(form['USERFF'].filename)
                self.userffstring = form['USERFF'].value
                self.runoptions['userff'] = StringIO(form['USERFF'].value)
            else:
                text = 'A force field file must be provided if using a user created force field.'
                raise WebOptionsError(text)
            if form.has_key('USERNAMES') and form['USERNAMES'].filename:
                self.usernamesfilename = sanitizeFileName(form['USERNAMES'].filename)
                self.usernamesstring = form['USERNAMES'].value
                self.runoptions['usernames'] = StringIO(form['USERNAMES'].value)
            else:
                text = 'A names file must be provided if using a user created force field.'
                raise WebOptionsError(text)
        if form.has_key('FFOUT') and form['FFOUT'].value != 'internal':
            self.runoptions['ffout'] = form['FFOUT'].value
        self.runoptions['chain'] = form.has_key('CHAIN')
        self.runoptions['typemap'] = form.has_key('TYPEMAP')
        self.runoptions['neutraln'] = form.has_key('NEUTRALN')
        self.runoptions['neutralc'] = form.has_key('NEUTRALC')
        self.runoptions['drop_water'] = form.has_key('DROPWATER')
        if (self.runoptions['neutraln'] or self.runoptions['neutraln']) and self.ff != 'parse':
            raise WebOptionsError('Neutral N-terminus and C-terminus require the PARSE forcefield.')
        if form.has_key('LIGAND') and form['LIGAND'].filename:
            self.ligandfilename = sanitizeFileName(form['LIGAND'].filename)
            ligandfilestring = form['LIGAND'].value
            ligandfilestring = ligandfilestring.replace('\r\n', '\n')
            self.ligandfilestring = ligandfilestring.replace('\r', '\n')
            self.runoptions['ligand'] = StringIO(self.ligandfilestring)
        if self.pdbfilename[-4:] == '.pdb':
            self.pqrfilename = '%s.pqr' % self.pdbfilename[:-4]
        else:
            self.pqrfilename = '%s.pqr' % self.pdbfilename
        self.runoptions['verbose'] = True
        self.runoptions['selectedExtensions'] = ['summary']
        return

    def getLoggingList(self):
        """Returns a list of options the user has turned on.
        Used for logging jobs later in usage.txt"""
        results = []
        for key in self:
            if self[key]:
                results.append(key)

        return results

    def getRunArguments(self):
        """Returns argument suitable for runPDB2PQR"""
        return self.runoptions.copy()

    def getOptions(self):
        """Returns all options for reporting to Google analytics"""
        options = self.runoptions.copy()
        options.update(self.otheroptions)
        options['ff'] = self.ff
        options['pdb'] = self.pdbfilename
        if options.has_key('ph_calc_options'):
            del options['ph_calc_options']
        if options.has_key('ligand'):
            options['ligand'] = self.ligandfilename
        if options.has_key('userff'):
            options['userff'] = self.userfffilename
        if options.has_key('usernames'):
            options['usernames'] = self.usernamesfilename
        return options

    def getCommandLine(self):
        commandLine = []
        if not self.runoptions['debump']:
            commandLine.append('--nodebump')
        if not self.runoptions['opt']:
            commandLine.append('--noopt')
        if 'ph' in self.runoptions:
            commandLine.append('--with-ph=%s' % self.runoptions['ph'])
        if 'ph_calc_method' in self.runoptions:
            commandLine.append('--ph-calc-method=%s' % self.runoptions['ph_calc_method'])
        if self.runoptions['drop_water']:
            commandLine.append('--drop-water')
        if self.otheroptions['apbs']:
            commandLine.append('--apbs-input')
        if self.otheroptions['whitespace']:
            commandLine.append('--whitespace')
        if 'userff' in self.runoptions and self.ff == 'user':
            commandLine.append('--userff=%s' % self.userfffilename)
            commandLine.append('--usernames=%s' % self.usernamesfilename)
        else:
            commandLine.append('--ff=%s' % self.ff)
        if 'ffout' in self.runoptions:
            commandLine.append('--ffout=%s' % self.runoptions['ffout'])
        for o in ('chain', 'typemap', 'neutraln', 'neutralc', 'verbose'):
            if self.runoptions[o]:
                commandLine.append('--' + o)

        if 'ligand' in self.runoptions:
            commandLine.append('--ligand=%s' % self.ligandfilename)
        for ext in self.runoptions.get('selectedExtensions', []):
            commandLine.append('--%s' % ext)

        commandLine.append(self.pdbfilename)
        commandLine.append(self.pqrfilename)
        return (' ').join(commandLine)

    def __contains__(self, item):
        """Helper for checking for the presence of an option"""
        return item in self.runoptions or item in self.otheroptions

    def has_key(self, item):
        """Helper for checking for the presence of an option"""
        return item in self.runoptions or item in self.otheroptions

    def __iter__(self):
        for key in self.runoptions:
            yield key

        for key in self.otheroptions:
            yield key

    def __getitem__(self, key):
        if key in self.runoptions:
            return self.runoptions[key]
        return self.otheroptions[key]


def handleOpal(weboptions):
    """
        Handle opal based run.
    """
    from AppService_client import AppServiceLocator, launchJobRequest
    from AppService_types import ns0
    inputFiles = []
    if 'userff' in weboptions:
        ffFile = ns0.InputFileType_Def('inputFile')
        ffFile._name = weboptions.userfffilename
        ffFile._contents = weboptions.userffstring
        inputFiles.append(ffFile)
    if 'usernames' in weboptions:
        namesFile = ns0.InputFileType_Def('inputFile')
        namesFile._name = weboptions.usernamesfilename
        namesFile._contents = weboptions.usernamesstring
        inputFiles.append(namesFile)
    if 'ligand' in weboptions:
        ligandFile = ns0.InputFileType_Def('inputFile')
        ligandFile._name = weboptions.ligandfilename
        ligandFile._contents = weboptions.ligandfilestring
        inputFiles.append(ligandFile)
    pdbOpalFile = ns0.InputFileType_Def('inputFile')
    pdbOpalFile._name = weboptions.pdbfilename
    pdbOpalFile._contents = weboptions.pdbfilestring
    inputFiles.append(pdbOpalFile)
    appLocator = AppServiceLocator()
    appServicePort = appLocator.getAppServicePort(PDB2PQR_OPAL_URL)
    req = launchJobRequest()
    req._argList = weboptions.getCommandLine()
    req._inputFile = inputFiles
    try:
        resp = appServicePort.launchJob(req)
    except Exception as e:
        printHeader('PDB2PQR Job Submission - Error')
        print '<BODY>\n<P>'
        print 'There was an error with your job submission<br>'
        print '</P>'
        print '<script type="text/javascript">'
        print 'var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");'
        print 'document.write(unescape("%3Cscript src=\'" + gaJsHost + "google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E"));'
        print '</script>'
        print '<script type="text/javascript">'
        print 'try {'
        print 'var pageTracker = _gat._getTracker("UA-11026338-3");'
        for key in weboptions:
            print 'pageTracker._trackPageview("/main_cgi/has_%s_%s.html");' % (key, weboptions[key])

        print 'pageTracker._trackPageview();'
        print '} catch(err) {}</script>'
        print '</BODY>'
        print '</HTML>'
        sys.exit(2)

    try:
        starttime = time.time()
        name = setID(starttime)
        os.makedirs('%s%s%s' % (INSTALLDIR, TMPDIR, name))
        apbsInputFile = open('%s%s%s/apbs_input' % (INSTALLDIR, TMPDIR, name), 'w')
        apbsInputFile.write(str(weboptions['apbs']))
        apbsInputFile.close()
        typemapInputFile = open('%s%s%s/typemap' % (INSTALLDIR, TMPDIR, name), 'w')
        typemapInputFile.write(str(weboptions['typemap']))
        typemapInputFile.close()
        pdb2pqrOpalJobIDFile = open('%s%s%s/pdb2pqr_opal_job_id' % (INSTALLDIR, TMPDIR, name), 'w')
        pdb2pqrOpalJobIDFile.write(resp._jobID)
        pdb2pqrOpalJobIDFile.close()
        print redirector(name, weboptions)
        pdb2pqrOpalLogFile = open('%s%s%s/pdb2pqr_log' % (INSTALLDIR, TMPDIR, name), 'w')
        pdb2pqrOpalLogFile.write(str(weboptions.getOptions()) + '\n' + str(os.environ['REMOTE_ADDR']))
        pdb2pqrOpalLogFile.close()
    except StandardError as details:
        print details
        createError(name, details)


def handleNonOpal(weboptions):
    """
        Handle non opal run.
    """
    pdblist, errlist = readPDB(weboptions.pdbfile)
    dummydef = Definition()
    dummyprot = Protein(pdblist, dummydef)
    if len(pdblist) == 0 and len(errlist) == 0:
        text = 'Unable to find PDB file - Please make sure this is '
        text += 'a valid PDB file ID!'
        print text
        sys.exit(2)
    else:
        if dummyprot.numAtoms() > MAXATOMS and weboptions['opt'] == True:
            text = '<HTML><HEAD>'
            text += '<TITLE>PDB2PQR Error</title>'
            text += '<link rel="stylesheet" href="%s" type="text/css">' % STYLESHEET
            text += '</HEAD><BODY><H2>PDB2PQR Error</H2><P>'
            text += 'Due to server limits, we are currently unable to optimize '
            text += 'proteins of greater than %i atoms on the server (PDB2PQR ' % MAXATOMS
            text += 'found %s atoms in the selected PDB file).  If you ' % dummyprot.numAtoms()
            text += 'want to forgo optimization please try the server again.<P>'
            text += 'Otherwise you may use the standalone version of PDB2PQR that '
            text += 'is available from the <a href="http://pdb2pqr.sourceforge.net">'
            text += 'PDB2PQR SourceForge project page</a>.'
            text += '<script type="text/javascript">'
            text += 'var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");'
            text += 'document.write(unescape("%3Cscript src=\'" + gaJsHost + "google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E"));'
            text += '</script>'
            text += '<script type="text/javascript">'
            text += 'try {'
            text += 'var pageTracker = _gat._getTracker("UA-11026338-3");'
            for key in weboptions:
                text += 'pageTracker._trackPageview("/main_cgi/has_%s_%s.html");' % (key, weboptions[key])

            text += 'pageTracker._trackPageview();'
            text += '} catch(err) {}</script>'
            text += '</BODY></HTML>'
            print text
            sys.exit(2)
        try:
            starttime = time.time()
            name = setID(starttime)
            os.makedirs('%s%s%s' % (INSTALLDIR, TMPDIR, name))
            apbsInputFile = open('%s%s%s/apbs_input' % (INSTALLDIR, TMPDIR, name), 'w')
            apbsInputFile.write(str(weboptions['apbs']))
            apbsInputFile.close()
            typemapInputFile = open('%s%s%s/typemap' % (INSTALLDIR, TMPDIR, name), 'w')
            typemapInputFile.write(str(weboptions['typemap']))
            typemapInputFile.close()
            statusfile = open('%s%s%s/pdb2pqr_status' % (INSTALLDIR, TMPDIR, name), 'w')
            statusfile.write('running')
            statusfile.close()
            pdb2pqrLogFile = open('%s%s%s/pdb2pqr_log' % (INSTALLDIR, TMPDIR, name), 'w')
            pdb2pqrLogFile.write(str(weboptions.getOptions()) + '\n' + str(weboptions.ff) + '\n' + str(os.environ['REMOTE_ADDR']))
            pdb2pqrLogFile.close()
            pid = os.fork()
            if pid:
                print redirector(name, weboptions)
                sys.exit()
            else:
                currentdir = os.getcwd()
                os.chdir('/')
                os.setsid()
                os.umask(0)
                os.chdir(currentdir)
                os.close(1)
                os.close(2)
                pqrpath = '%s%s%s/%s.pqr' % (INSTALLDIR, TMPDIR, name, name)
                orig_stdout = sys.stdout
                orig_stderr = sys.stderr
                sys.stdout = open('%s%s%s/pdb2pqr_stdout.txt' % (INSTALLDIR, TMPDIR, name), 'w')
                sys.stderr = open('%s%s%s/pdb2pqr_stderr.txt' % (INSTALLDIR, TMPDIR, name), 'w')
                run_arguements = weboptions.getRunArguments()
                if weboptions.runoptions.get('ph_calc_method', '') == 'pdb2pka':
                    run_arguements['ph_calc_options']['output_dir'] = '%s%s%s/pdb2pka_output' % (INSTALLDIR, TMPDIR, name)
                header, lines, missedligands = runPDB2PQR(pdblist, weboptions.ff, outname=pqrpath, commandLine=weboptions.getCommandLine(), **weboptions.getRunArguments())
                sys.stdout.close()
                sys.stderr.close()
                sys.stdout = orig_stdout
                sys.stderr = orig_stderr
                endtimefile = open('%s%s%s/pdb2pqr_end_time' % (INSTALLDIR, TMPDIR, name), 'w')
                endtimefile.write(str(time.time()))
                endtimefile.close()
                pqrfile = open(pqrpath, 'w')
                pqrfile.write(header)
                whitespace = weboptions.otheroptions['whitespace']
                for line in lines:
                    if whitespace:
                        if line[0:4] == 'ATOM':
                            newline = line[0:6] + ' ' + line[6:16] + ' ' + line[16:38] + ' ' + line[38:46] + ' ' + line[46:]
                            pqrfile.write('%s\n' % string.strip(newline))
                        elif line[0:6] == 'HETATM':
                            newline = line[0:6] + ' ' + line[6:16] + ' ' + line[16:38] + ' ' + line[38:46] + ' ' + line[46:]
                            pqrfile.write('%s\n' % string.strip(newline))
                    else:
                        pqrfile.write('%s\n' % string.strip(line))

                pqrfile.close()
                if weboptions.otheroptions['apbs']:
                    from src import inputgen
                    from src import psize
                    method = 'mg-auto'
                    size = psize.Psize()
                    size.parseInput(pqrpath)
                    size.runPsize(pqrpath)
                    async = 0
                    myinput = inputgen.Input(pqrpath, size, method, async, potdx=True)
                    myinput.printInputFiles()
                    myinput.dumpPickle()
                endtime = time.time() - starttime
                if 'ligand' in weboptions:
                    outputligandfile = open('%s%s%s/%s.mol2' % (INSTALLDIR, TMPDIR, name, name), 'w')
                    outputligandfile.write(weboptions.ligandfilestring)
                    outputligandfile.close()
                outputpdbfile = open('%s%s%s/%s.pdb' % (INSTALLDIR, TMPDIR, name, name), 'w')
                outputpdbfile.write(weboptions.pdbfilestring)
                outputpdbfile.close()
                statusfile = open('%s%s%s/pdb2pqr_status' % (INSTALLDIR, TMPDIR, name), 'w')
                statusfile.write('complete\n')
                filelist = glob.glob('%s%s%s/%s*' % (INSTALLDIR, TMPDIR, name, name))
                for filename in filelist:
                    statusfile.write(filename + '\n')

                statusfile.close()
        except StandardError as details:
            print traceback.format_exc()
            print sys.exc_info()[0]
            createError(name, details)


def mainCGI():
    """
        Main driver for running PDB2PQR from a web page
    """
    print 'Content-type: text/html\n'
    import cgi, cgitb
    cgitb.enable()
    form = cgi.FieldStorage()
    try:
        weboptions = WebOptions(form)
    except WebOptionsError as error:
        print error
        sys.exit(2)

    if HAVE_PDB2PQR_OPAL:
        handleOpal(weboptions)
    else:
        handleNonOpal(weboptions)