# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/csinsertcopyright.py
# Compiled at: 2007-10-05 20:12:50
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: csinsertcopyright.py,v 1.1 2007/10/06 00:12:50 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    return parser


parser = setOptions()
options, args = parser.parse_args()
verbose = ''
if options.verbose:
    verbose = '-v'
    sys.stdout = sys.stderr
Csys.getoptionsEnvironment(options)
copyrightfmt = "\n%s\n\nCopyright (c) 2000-2007 Celestial Software, LLC\nCopyright (c) 2000-2007 Bill Campbell <bill@celestial.com>\n\nThis software may be copied under the terms of the GPL2 (Gnu\nGeneral Public Licence Version 2).\n\nTHIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED\nWARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF\nMERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.\nIN NO EVENT SHALL THE AUTHORS AND COPYRIGHT HOLDERS AND THEIR CONTRIBUTORS\nBE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,\nOR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF\nSUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS\nINTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN\nCONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)\nARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF\nTHE POSSIBILITY OF SUCH DAMAGE.\n"
copyright = copyrightfmt % Csys.Config.progname
startLinePattern = re.compile('^', re.DOTALL | re.MULTILINE)

def genCopyright(fname):
    base, ext = os.path.splitext(fname)
    sys.stderr.write('base >%s< ext >%s<\n' % (base, ext))
    copyright = copyrightfmt % fname
    if ext == '.py':
        copyright = "\n__copyright__ = ('''\n%s\n''')" % copyright
    elif ext in ('.c', '.cc'):
        copyright = '\n#if 0\n%s\n#endif\n' % copyright
    else:
        copyright = startLinePattern.sub('## ', copyright)
    return copyright


from fileinput import FileInput
fileinput = FileInput(files=args, inplace=True, backup='.bak')
needBlank = True
for line in fileinput:
    line = line[:-1]
    if fileinput.isfirstline():
        needBlank = True
        fname = os.path.basename(fileinput.filename())
        sys.stderr.write('fname: %s\n' % fname)
    if needBlank and not line:
        needBlank = False
        print genCopyright(fname)
    print line