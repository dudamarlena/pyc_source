# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/pegasus/kickstart_hdr.py
# Compiled at: 2009-12-08 17:43:30
"""
Kickstart-extracted header placed on another file.
Used by the script nl_pegasus_hdr, and some of the
parser modules.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__rcsid__ = '$Id: kickstart_hdr.py 23923 2009-09-18 22:42:26Z ksb $'
import glob, logging, optparse, os, re, sys
from xml import sax
from netlogger import nllog
HEADER_TAG = '<header'

class WorkflowLabelHandler(sax.handler.ContentHandler):
    """Extract the first workflow label found
    in an <invocation> element.
    """
    ATTR = 'wf-label'

    def startDocument(self):
        self.wflow_value = None
        return

    def startElement(self, name, attrs):
        if self.wflow_value is None and name == 'invocation':
            self.wflow_value = attrs.getValue(self.ATTR)
        return


def addHeader(filename, text):
    """Add text at the beginning of the file 'filename'.
    """
    moved_filename = filename + '.moved'
    os.rename(filename, moved_filename)
    old_file = file(moved_filename)
    new_file = file(filename, 'w')
    new_file.write(text)
    while 1:
        buf = old_file.read(65536)
        if buf == '':
            break
        new_file.write(buf)

    old_file.close()
    os.unlink(moved_filename)


def lineHasHeader(line):
    return line.startswith(HEADER_TAG)


def getHeaderLabel(line):
    m = re.match('%s .*wf-label="([^"]*)"' % HEADER_TAG, line)
    if m and len(m.groups()) == 1:
        label = m.group(1)
    else:
        raise ValueError('Bad header line')
    return label


def getWorkflowLabel(infile):
    """Find the value of the workflow label in the
    first invocation record in the file.

    Returns None if no label found, otherwise
    a string whose value is the label.
    """
    wlh = WorkflowLabelHandler()
    num_inv, lines = 0, []
    for line in infile:
        if '<invocation' in line:
            num_inv += 1
            if num_inv > 1:
                break
        lines.append(line)

    xmlstr = ('').join(lines)
    sax.parseString(xmlstr, wlh)
    return wlh.wflow_value


def makeHeader(label):
    """Make the special header string.
    """
    return '%s wf-label="%s"/>\n' % (HEADER_TAG, label)


def hasHeader(path):
    """Return true if the file has the special header.
    """
    f = file(path)
    line = f.readline().strip()
    return line.startswith(HEADER_TAG)