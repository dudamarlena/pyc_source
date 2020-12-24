# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vanessa/Documents/Dropbox/Code/share/containershare-python/containershare/utils.py
# Compiled at: 2018-07-30 07:30:19
# Size of source mod 2**32: 6599 bytes
__doc__ = '\nutils.py: part of containershare package\n\nCopyright (c) 2018, Vanessa Sochat\nAll rights reserved.\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are met:\n\n* Redistributions of source code must retain the above copyright notice, this\n  list of conditions and the following disclaimer.\n\n* Redistributions in binary form must reproduce the above copyright notice,\n  this list of conditions and the following disclaimer in the documentation\n  and/or other materials provided with the distribution.\n\n* Neither the name of the copyright holder nor the names of its\n  contributors may be used to endorse or promote products derived from\n  this software without specific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"\nAND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\nIMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\nDISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE\nFOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\nDAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR\nSERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER\nCAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,\nOR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\nOF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\n'
import errno
from subprocess import Popen, PIPE, STDOUT
from containershare.logger import bot
import shutil, json, tempfile, sys, os, re

def get_installdir():
    return os.path.dirname(os.path.abspath(__file__))


def find_subdirectories(basepath):
    """
    Return directories (and sub) starting from a base
    """
    directories = []
    for root, dirnames, filenames in os.walk(basepath):
        new_directories = [d for d in dirnames if d not in directories]
        directories = directories + new_directories

    return directories


def find_directories(root, fullpath=True):
    """
    Return directories at one level specified by user
    (not recursive)
    """
    directories = []
    for item in os.listdir(root):
        if not re.match('^[.]', item):
            if os.path.isdir(os.path.join(root, item)):
                if fullpath:
                    directories.append(os.path.abspath(os.path.join(root, item)))
                else:
                    directories.append(item)

    return directories


def copy_directory(src, dest, force=False):
    """ Copy an entire directory recursively
    """
    if os.path.exists(dest):
        if force is True:
            shutil.rmtree(dest)
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            bot.error('Directory not copied. Error: %s' % e)
            sys.exit(1)


def mkdir_p(path):
    """mkdir_p attempts to get the same functionality as mkdir -p
    :param path: the path to create.
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            if os.path.isdir(path):
                pass
        else:
            bot.error('Error creating path %s, exiting.' % path)
            sys.exit(1)


def clone(url, tmpdir=None):
    """clone a repository from Github"""
    if tmpdir is None:
        tmpdir = tempfile.mkdtemp()
    name = os.path.basename(url).replace('.git', '')
    dest = '%s/%s' % (tmpdir, name)
    return_code = os.system('git clone %s %s' % (url, dest))
    if return_code == 0:
        return dest
    bot.error('Error cloning repo.')
    sys.exit(return_code)


def run_command(cmd):
    """run_command uses subprocess to send a command to the terminal.
    :param cmd: the command to send, should be a list for subprocess
    """
    output = Popen(cmd, stderr=STDOUT, stdout=PIPE)
    t = (output.communicate()[0], output.returncode)
    output = {'message':t[0],  'return_code':t[1]}
    return output


def read_json(filename, mode='r'):
    with open(filename, mode) as (filey):
        data = json.load(filey)
    return data


def write_json(json_obj, filename, mode='w'):
    with open(filename, mode) as (filey):
        filey.write(json.dumps(json_obj, sort_keys=True, indent=4, separators=(',',
                                                                               ': ')))
    return filename


def read_file(filename, mode='r'):
    with open(filename, mode) as (filey):
        data = filey.read()
    return data


def write_file(filename, content, mode='w'):
    with open(filename, mode) as (filey):
        filey.writelines(content)
    return filename


def get_post_fields(request):
    """parse through a request, and return fields from post in a dictionary
    """
    fields = dict()
    for field, value in request.form.items():
        fields[field] = value

    return fields


def convert2boolean(arg):
    """convert2boolean is used for environmental variables
    that must be returned as boolean"""
    if not isinstance(arg, bool):
        return arg.lower() in ('yes', 'true', 't', '1', 'y')
    else:
        return arg


def getenv(variable_key, default=None, required=False, silent=True):
    """getenv will attempt to get an environment variable. If the variable
    is not found, None is returned.
    :param variable_key: the variable name
    :param required: exit with error if not found
    :param silent: Do not print debugging information for variable
    """
    variable = os.environ.get(variable_key, default)
    if variable is None:
        if required:
            bot.error('Cannot find environment variable %s, exiting.' % variable_key)
            sys.exit(1)
        if silent or variable is not None:
            bot.verbose2('%s found as %s' % (variable_key, variable))
    else:
        bot.verbose2('%s not defined (None)' % variable_key)
    return variable