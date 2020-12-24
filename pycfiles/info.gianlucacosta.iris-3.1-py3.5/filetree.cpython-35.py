# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/info/gianlucacosta/iris/io/filetree.py
# Compiled at: 2017-10-18 20:54:09
# Size of source mod 2**32: 3766 bytes
"""
File-tree utilities

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""
import os, re

class FileTreeProcessor:
    __doc__ = '\n    Applies an action to every file - whose path matches the given pattern - below a given root directory.\n\n    The "onProcessing" field is a function called just before a file path is going to be processed;\n    it must only receive the file path and return a True-like value if the file should be processed.\n    '

    def __init__(self, filePathPattern):
        """
        --filePathPattern: the regex describing the file paths to be processed
        """
        if isinstance(filePathPattern, str):
            self._filePathPattern = re.compile(filePathPattern)
        else:
            self._filePathPattern = filePathPattern
        self.onProcessing = lambda filePath: True

    def applyTo(self, rootDir):
        if not os.path.isdir(rootDir):
            raise ValueError('Root dir must be a directory')
        for dirPath, dirNames, fileNames in os.walk(rootDir):
            for fileName in fileNames:
                filePath = os.path.join(dirPath, fileName)
                if self._filePathPattern.match(filePath) is not None and self.onProcessing(filePath):
                    self._processFile(filePath)

    def _processFile(self, filePath):
        """
        Performs the actual file processing; can return None
        """
        raise NotImplementedError


class DefaultOnProcessingFunctions:
    __doc__ = '\n    Provides default implementations for FileTreeProcessor\'s "onProcessing" field\n    '

    @staticmethod
    def printProcessedFile(filePath):
        """
        Prints out the file path, without interfering with the processing
        """
        print('---> ' + filePath)
        return True


class HeaderRemover(FileTreeProcessor):
    __doc__ = '\n    Removes any file header ending with the "trailingPattern" regex\n    '

    def __init__(self, filePathPattern, trailingPattern):
        super().__init__(filePathPattern)
        if isinstance(trailingPattern, str):
            self._trailingPattern = re.compile(trailingPattern)
        else:
            self._trailingPattern = trailingPattern

    def _processFile(self, filePath):
        with open(filePath, 'r') as (sourceFile):
            fileContent = sourceFile.read()
            trailingMatch = self._trailingPattern.match(fileContent)
        if trailingMatch is not None:
            fileContent = fileContent[trailingMatch.end():]
            with open(filePath, 'w') as (targetFile):
                targetFile.write(fileContent)


class FileTreeLineProcessor(FileTreeProcessor):
    __doc__ = '\n    Adds a granularity level to FileTreeProcessor, by introducing line filtering\n    '

    def _processFile(self, filePath):
        with open(filePath, 'r') as (sourceFile):
            processedLines = [processedLine for processedLine in (self._processLine(sourceLine) for sourceLine in sourceFile) if processedLine is not None]
        with open(filePath, 'w') as (targetFile):
            targetFile.writelines(processedLines)

    def _processLine(self, line):
        """
        Returns the modified version of the line, or None if the line must be skipped
        """
        raise NotImplementedError


class TrailingSpaceRemover(FileTreeLineProcessor):
    __doc__ = "\n    Removes trailing spaces from every line in the given file set, leaving each line's last newline if it's present\n    "

    def _processLine(self, line):
        if line.endswith('\n'):
            return line.rstrip() + '\n'
        else:
            return line.rstrip()