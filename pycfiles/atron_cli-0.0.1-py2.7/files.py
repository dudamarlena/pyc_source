# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atron_cli/files.py
# Compiled at: 2019-03-27 01:21:27
import ast, textwrap
from ampy.pyboard import PyboardError
BUFFER_SIZE = 32

class DirectoryExistsError(Exception):
    pass


class Files(object):
    """Class to interact with a MicroPython board files over a serial connection.
    Provides functions for listing, uploading, and downloading files from the
    board's filesystem.
    """

    def __init__(self, pyboard):
        """Initialize the MicroPython board files class using the provided pyboard
        instance.  In most cases you should create a Pyboard instance (from
        pyboard.py) which connects to a board over a serial connection and pass
        it in, but you can pass in other objects for testing, etc.
        """
        self._pyboard = pyboard

    def get(self, filename):
        """Retrieve the contents of the specified file and return its contents
        as a byte string.
        """
        command = ("\n            import sys\n            with open('{0}', 'rb') as infile:\n                while True:\n                    result = infile.read({1})\n                    if result == b'':\n                        break\n                    len = sys.stdout.write(result)\n        ").format(filename, BUFFER_SIZE)
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            if ex.args[2].decode('utf-8').find('OSError: [Errno 2] ENOENT') != -1:
                raise RuntimeError(('No such file: {0}').format(filename))
            else:
                raise ex

        self._pyboard.exit_raw_repl()
        return out

    def ls(self, directory='/', long_format=True, recursive=False):
        """List the contents of the specified directory (or root if none is
        specified).  Returns a list of strings with the names of files in the
        specified directory.  If long_format is True then a list of 2-tuples
        with the name and size (in bytes) of the item is returned.  Note that
        it appears the size of directories is not supported by MicroPython and
        will always return 0 (i.e. no recursive size computation).
        """
        if not directory.startswith('/'):
            directory = '/' + directory
        command = '                try:        \n                    import os\n                except ImportError:\n                    import uos as os\n'
        if recursive:
            command += "                def listdir(directory):\n                    result = set()\n\n                    def _listdir(dir_or_file):\n                        try:\n                            # if its a directory, then it should provide some children.\n                            children = os.listdir(dir_or_file)\n                        except OSError:                        \n                            # probably a file. run stat() to confirm.\n                            os.stat(dir_or_file)\n                            result.add(dir_or_file) \n                        else:\n                            # probably a directory, add to result if empty.\n                            if children:\n                                # queue the children to be dealt with in next iteration.\n                                for child in children:\n                                    # create the full path.\n                                    if dir_or_file == '/':\n                                        next = dir_or_file + child\n                                    else:\n                                        next = dir_or_file + '/' + child\n                                    \n                                    _listdir(next)\n                            else:\n                                result.add(dir_or_file)                     \n\n                    _listdir(directory)\n                    return sorted(result)\n"
        else:
            command += "                def listdir(directory):\n                    if directory == '/':                \n                        return sorted([directory + f for f in os.listdir(directory)])\n                    else:\n                        return sorted([directory + '/' + f for f in os.listdir(directory)])\n"
        if long_format:
            command += ("\n                r = []\n                for f in listdir('{0}'):\n                    size = os.stat(f)[6]                    \n                    r.append('{{0}} - {{1}} bytes'.format(f, size))\n                print(r)\n            ").format(directory)
        else:
            command += ("\n                print(listdir('{0}'))\n            ").format(directory)
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            if ex.args[2].decode('utf-8').find('OSError: [Errno 2] ENOENT') != -1:
                raise RuntimeError(('No such directory: {0}').format(directory))
            else:
                raise ex

        self._pyboard.exit_raw_repl()
        return ast.literal_eval(out.decode('utf-8'))

    def mkdir(self, directory, exists_okay=False):
        """Create the specified directory.  Note this cannot create a recursive
        hierarchy of directories, instead each one should be created separately.
        """
        command = ("\n            try:\n                import os\n            except ImportError:\n                import uos as os\n            os.mkdir('{0}')\n        ").format(directory)
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            if ex.args[2].decode('utf-8').find('OSError: [Errno 17] EEXIST') != -1:
                if not exists_okay:
                    raise DirectoryExistsError(('Directory already exists: {0}').format(directory))
            else:
                raise ex

        self._pyboard.exit_raw_repl()

    def put(self, filename, data):
        """Create or update the specified file with the provided data.
        """
        self._pyboard.enter_raw_repl()
        self._pyboard.exec_(("f = open('{0}', 'wb')").format(filename))
        size = len(data)
        for i in range(0, size, BUFFER_SIZE):
            chunk_size = min(BUFFER_SIZE, size - i)
            chunk = repr(data[i:i + chunk_size])
            if not chunk.startswith('b'):
                chunk = 'b' + chunk
            self._pyboard.exec_(('f.write({0})').format(chunk))

        self._pyboard.exec_('f.close()')
        self._pyboard.exit_raw_repl()

    def rm(self, filename):
        """Remove the specified file or directory."""
        command = ("\n            try:\n                import os\n            except ImportError:\n                import uos as os\n            os.remove('{0}')\n        ").format(filename)
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            message = ex.args[2].decode('utf-8')
            if message.find('OSError: [Errno 2] ENOENT') != -1:
                raise RuntimeError(('No such file/directory: {0}').format(filename))
            if message.find('OSError: [Errno 13] EACCES') != -1:
                raise RuntimeError(('Directory is not empty: {0}').format(filename))
            else:
                raise ex

        self._pyboard.exit_raw_repl()

    def rmdir(self, directory, missing_okay=False):
        """Forcefully remove the specified directory and all its children."""
        command = ("\n            try:\n                import os\n            except ImportError:\n                import uos as os\n            def rmdir(directory):\n                os.chdir(directory)\n                for f in os.listdir():\n                    try:\n                        os.remove(f)\n                    except OSError:\n                        pass\n                for f in os.listdir():\n                    rmdir(f)\n                os.chdir('..')\n                os.rmdir(directory)\n            rmdir('{0}')\n        ").format(directory)
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            message = ex.args[2].decode('utf-8')
            if message.find('OSError: [Errno 2] ENOENT') != -1:
                if not missing_okay:
                    raise RuntimeError(('No such directory: {0}').format(directory))
            else:
                raise ex

        self._pyboard.exit_raw_repl()

    def run(self, filename, wait_output=True):
        """Run the provided script and return its output.  If wait_output is True
        (default) then wait for the script to finish and then print its output,
        otherwise just run the script and don't wait for any output.
        """
        self._pyboard.enter_raw_repl()
        out = None
        if wait_output:
            out = self._pyboard.execfile(filename)
        else:
            with open(filename, 'rb') as (infile):
                self._pyboard.exec_raw_no_follow(infile.read())
        self._pyboard.exit_raw_repl()
        return out