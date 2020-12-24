# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/project/generator.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 3669 bytes
__doc__ = '\nproducti_gestio.project.generator\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nIt generates a simple mini-project.\n'
import os
long_license = '\n# Copyright (c) 2018 The producti-gestio Authors (see AUTHORS)\n#\n# Permission is hereby granted, free of charge, to any person obtaining a copy\n# of this software and associated documentation files (the "Software"), to deal\n# in the Software without restriction, including without limitation the rights\n# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n# copies of the Software, and to permit persons to whom the Software is\n# furnished to do so, subject to the following conditions:\n#\n# The above copyright notice and this permission notice shall\n# be included in all\n# copies or substantial portions of the Software.\n#\n# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n# SOFTWARE.\n'
code: str = long_license + '\nimport producti_gestio\n\n@producti_gestio.Decorator\ndef server_create(*args, **kwargs):\n   """\n   It creates the server and\n   launches it\n   """\n   def handler_function(*args, **kwargs):\n       return ({\n           \'response_code\': 200,\n           \'response\': {\n               \'ok\': True,\n               \'is_meme\': True\n           }\n       })\n\n   return handler_function\n\nif __name__ == \'__main__\':\n   server_create(allow_get=True)\n   while True:\n       pass\n'

def generate_code(name) -> bool:
    """It generates the
    source code in a directory.

    Args:
      name(str): The directory name

    Returns:
      bool: True if all went well.

    """
    global code
    directory = os.getcwd()
    if not os.path.exists(str(directory) + '/' + str(name)):
        print('Generating the directory...')
        os.makedirs(str(directory) + '/' + str(name))
        print('Making code...')
        file = str(directory) + '/' + str(name) + '/handler.py'
        with open(file, 'w') as (code_file):
            code_file.write(code)
        print('Done! Enjoy your product!')
        return True
    raise Exception('The directory you tried to create already exists!')