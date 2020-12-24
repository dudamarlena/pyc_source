# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mozilla/core/manifestparser.py
# Compiled at: 2009-10-10 21:39:57
import silme.io
from silme.core import Package, Structure, Blob
import re

class ManifestParser(object):
    """
  Class for parsing the chrome.manifest files
  """

    @staticmethod
    def get_locales(manifest):
        """
    Get all locales and the path informations specified in the given source
    @param manifest: source of the manifest file
    """
        locales = {}
        lines = manifest.split('\n')
        whitespaceRE = re.compile('\\s+')
        pathRE = re.compile('!/')
        for line in lines:
            line = line.strip()
            if line.startswith('locale'):
                parts = whitespaceRE.split(line)
                if len(parts[2]) > 5:
                    raise Exception('Not a valid locale: ' + parts[2] + ' !')
                if parts[3].startswith('jar:'):
                    paths = parts[3].replace('jar:', '')
                    paths = pathRE.split(paths)
                    try:
                        locales[parts[2]][parts[1]] = {'type': 'jar', 'jarpath': paths[0], 'localepath': paths[1]}
                    except KeyError:
                        locales[parts[2]] = {}
                        locales[parts[2]][parts[1]] = {'type': 'jar', 'jarpath': paths[0], 'localepath': paths[1]}

                else:
                    if parts[3].startswith('file:'):
                        parts[3] = parts[3].replace('file:', '')
                    try:
                        locales[parts[2]][parts[1]] = {'type': 'folder', 'localepath': parts[3]}
                    except KeyError:
                        locales[parts[2]] = {}
                        locales[parts[2]][parts[1]] = {'type': 'folder', 'localepath': parts[3]}

        return locales