# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/outputprocessor.py
# Compiled at: 2016-08-21 13:36:44
# Size of source mod 2**32: 3457 bytes
__doc__ = '\nThis module implements output processing class.\n'
import os, sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from bprc.utils import vlog
from bprc.utils import errlog
from bprc.utils import verboseprint
from bprc.utils import printstepcolophon
from bprc.utils import printhttprequest
from bprc.utils import printheaders
from bprc.utils import printbody
from bprc.utils import printhttpresponse
import bprc.cli, json
from json import JSONDecodeError
from pprint import pprint
import logging

class OutputProcessor:
    """OutputProcessor"""

    def __init__(self, *, step, id, req):
        """Instantiates the Output Processor Object"""
        self.step = step
        self.id = id
        self.req = req

    def writeOutput(self, *, writeformat, writefile, req):
        """Writes the output to the writefile in the format specified"""
        vlog('Generating output of step: ' + str(self.id) + ' ' + self.step.name + '. Format=' + writeformat)
        if writeformat == 'json':
            formatted_json = json.dumps(self.step.response.body, indent=4, sort_keys=True)
            if sys.stdout.isatty():
                from pygments import highlight, lexers, formatters
                colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
                print(colorful_json, file=writefile)
            else:
                print(formatted_json, file=writefile)
        else:
            printstepcolophon(self.step, id=self.id, file=writefile)
            if bprc.cli.args.nocolor:
                colourful = False
            else:
                colourful = sys.stdout.isatty()
            if writeformat == 'raw-all':
                print('-- Request --', file=writefile)
                printhttprequest(self.step, id=self.id, file=writefile, colourful=colourful)
                printheaders(self.step, id=self.id, file=writefile, http_part='request', colourful=colourful)
                logging.debug('PRINTING REQUEST HEADERS')
                if self.step.request.body:
                    logging.debug('Req.body==' + req.body)
                    try:
                        self.step.request.body = json.loads(req.body)
                    except JSONDecodeError as e:
                        self.step.request.body = req.body

                    printbody(self.step, id=self.id, file=writefile, http_part='request', colourful=colourful)
                print('-- Response --', file=writefile)
            printhttpresponse(self.step, id=self.id, file=writefile, colourful=colourful)
            printheaders(self.step, id=self.id, file=writefile, http_part='response', colourful=colourful)
        if self.step.response.body:
            printbody(self.step, id=self.id, file=writefile, http_part='response', colourful=colourful)