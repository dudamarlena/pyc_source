# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/server.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    CGI Server for PDB2PQR\n\n    This module contains the various functions necessary to run PDB2PQR\n    from a web server.\n\n    ----------------------------\n   \n    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of\n    Poisson-Boltzmann electrostatics calculations\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; \n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific \n    Northwest National Laboratory, operated by Battelle Memorial Institute, \n    Pacific Northwest Division for the U.S. Department Energy.; \n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n\tAll rights reserved.\n\n\tRedistribution and use in source and binary forms, with or without modification, \n\tare permitted provided that the following conditions are met:\n\n\t\t* Redistributions of source code must retain the above copyright notice, \n\t\t  this list of conditions and the following disclaimer.\n\t\t* Redistributions in binary form must reproduce the above copyright notice, \n\t\t  this list of conditions and the following disclaimer in the documentation \n\t\t  and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n\tTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND \n\tANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n\tWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. \n\tIN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, \n\tINDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, \n\tBUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, \n\tDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF \n\tLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE \n\tOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED \n\tOF THE POSSIBILITY OF SUCH DAMAGE.\n\n    ----------------------------\n'
__date__ = '4 August 2008'
__author__ = 'Todd Dolinsky, Samir Unni, Yong Huang'
import string, os, sys, time
from aconf import *
SRCPATH = SRCPATH
TMPDIR = 'tmp/'
LIMIT = 500.0
WEBSITE = WEBSITE
WEBNAME = 'index.html'
STYLESHEET = WEBSITE + 'pdb2pqr.css'
REFRESHTIME = 20
LOADPATH = '/proc/loadavg'
LOGPATH = '%s/%s/usage.txt' % (INSTALLDIR, TMPDIR)

def setID(time):
    """
        Given a floating point time.time(), generate an ID.
        Use the tenths of a second to differentiate.

        Parameters
            time:  The current time.time() (float)
        Returns
            id  :  The file id (string)
    """
    strID = '%s' % time
    period = string.find(strID, '.')
    id = '%s%s' % (strID[:period], strID[period + 1:period + 2])
    return id


def cleanTmpdir():
    """
        Clean up the temp directory for CGI.  If the size of the directory
        is greater than LIMIT, delete the older half of the files.  Since
        the files are stored by system time of creation, this is an
        easier task.
    """
    newdir = []
    size = 0.0
    count = 0
    path = INSTALLDIR + TMPDIR
    dir = os.listdir(path)
    for filename in dir:
        size = size + os.path.getsize('%s%s' % (path, filename))
        period = string.find(filename, '.')
        id = filename[:period]
        if id not in newdir:
            newdir.append(id)
            count += 1

    newdir.sort()
    size = size / 1048576.0
    newcount = 0
    if size >= LIMIT:
        for filename in newdir:
            if newcount > count / 2.0:
                break
            try:
                os.remove('%s%s.pqr' % (path, filename))
            except OSError:
                pass

            try:
                os.remove('%s%s.in' % (path, filename))
            except OSError:
                pass

            try:
                os.remove('%s%s.html' % (path, filename))
            except OSError:
                pass

            newcount += 1


def createResults(header, input, name, time, missedligands=[]):
    """
        Create the results web page for CGI-based runs

        Parameters
            header: The header of the PQR file (string)
            input:   A flag whether an input file has been created (int)
            tmpdir:  The resulting file directory (string)
            name:    The result file root name, based on local time (string)
            time:    The time taken to run the script (float)
            missedligands: A list of ligand names whose parameters could
                     not be assigned. Optional. (list)
    """
    newheader = string.replace(header, '\n', '<BR>')
    newheader = string.replace(newheader, ' ', '&nbsp;')
    filename = '%s%s%s.html' % (INSTALLDIR, TMPDIR, name)
    file = open(filename, 'w')
    file.write('<html>\n')
    file.write('<head>\n')
    file.write('<title>PDB2PQR Results</title>\n')
    file.write('<link rel="stylesheet" href="%s" type="text/css">\n' % STYLESHEET)
    file.write('</head>\n')
    file.write('<body>\n')
    file.write('<h2>PDB2PQR Results</h2>\n')
    file.write('<P>\n')
    file.write('Here are the results from PDB2PQR.  The files will be available on the ')
    file.write('server for a short period of time if you need to re-access the results.<P>\n')
    file.write('<a href="%s%s%s.pqr">%s.pqr</a><BR>\n' % (WEBSITE, TMPDIR, name, name))
    if input:
        file.write('<a href="%s%s%s.in">%s.in</a><BR>\n' % (WEBSITE, TMPDIR, name, name))
    pkaname = '%s%s%s.propka' % (INSTALLDIR, TMPDIR, name)
    if os.path.isfile(pkaname):
        file.write('<a href="%s%s%s.propka">%s.propka</a><BR>\n' % (WEBSITE, TMPDIR, name, name))
    typename = '%s%s%s-typemap.html' % (INSTALLDIR, TMPDIR, name)
    if os.path.isfile(typename):
        file.write('<a href="%s%s%s-typemap.html">%s-typemap.html</a><BR>\n' % (WEBSITE, TMPDIR, name, name))
    file.write('<P>The header for your PQR file, including any warnings generated, is:<P>\n')
    file.write('<blockquote><code>\n')
    file.write('%s<P>\n' % newheader)
    file.write('</code></blockquote>\n')
    if missedligands != []:
        file.write('The forcefield that you have selected does not have ')
        file.write('parameters for the following ligands in your PDB file.  Please visit ')
        file.write('<a href="http://davapc1.bioch.dundee.ac.uk/programs/prodrg/">PRODRG</a> ')
        file.write('to convert these ligands into MOL2 format.  This ligand can the be ')
        file.write('parameterized in your PDB2PQR calculation using the PEOE_PB methodology via ')
        file.write("the 'Assign charges to the ligand specified in a MOL2 file' checkbox:<P>\n")
        file.write('<blockquote><code>\n')
        for item in missedligands:
            file.write('%s<BR>\n' % item)

        file.write('<P></code></blockquote>\n')
    file.write('If you would like to run PDB2PQR again, please click <a href="%s%s">\n' % (WEBSITE, WEBNAME))
    file.write('here</a>.<P>\n')
    file.write('If you would like to run APBS with these results, please click <a href="%s../apbs/index.py?pdb2pqr-id=%s">here</a>.<P>\n' % (WEBSITE[:-1], name))
    file.write('<P>Thank you for using the PDB2PQR server!<P>\n')
    file.write('<font size="-1"><P>Total time on server: %.2f seconds</font><P>\n' % time)
    file.write('<font size="-1"><CENTER><I>Last Updated %s</I></CENTER></font>\n' % __date__)
    file.write('</body>\n')
    file.write('</html>\n')


def createError(name, details):
    """
        Create an error results page for CGI-based runs

        Parameters
            name:    The result file root name, based on local time (string)
            details: The details of the error (string)
    """
    filename = '%s%s%s.html' % (INSTALLDIR, TMPDIR, name)
    file = open(filename, 'w')
    file.write('<html>\n')
    file.write('<head>\n')
    file.write('<title>PDB2PQR Error</title>\n')
    file.write('<link rel="stylesheet" href="%s" type="text/css">\n' % STYLESHEET)
    file.write('</head>\n')
    file.write('<body>\n')
    file.write('<h2>PDB2PQR Error</h2>\n')
    file.write('<P>\n')
    file.write('An error occurred when attempting to run PDB2PQR:<P>\n')
    file.write('%s<P>\n' % details)
    file.write('If you believe this error is due to a bug, please contact the server administrator.<BR>\n')
    file.write('If you would like to try running PDB2QR again, please click <a href="%s%s">\n' % (WEBSITE, WEBNAME))
    file.write('here</a>.<P>\n')
    file.write('<font size="-1"><CENTER><I>Last Updated %s</I></CENTER></font>\n' % __date__)
    file.write('</body>\n')
    file.write('</html>\n')