# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilDebugFile.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 6338 bytes
"""Debug tool for copying files contained in a toil jobStore.
"""
from __future__ import absolute_import
import logging, fnmatch, os.path
from toil.lib.bioio import getBasicOptionParser
from toil.lib.bioio import parseBasicOptions
from toil.common import Toil, jobStoreLocatorHelp, Config
from toil.version import version
logger = logging.getLogger(__name__)

def recursiveGlob(directoryname, glob_pattern):
    """
    Walks through a directory and its subdirectories looking for files matching
    the glob_pattern and returns a list=[].

    :param directoryname: Any accessible folder name on the filesystem.
    :param glob_pattern: A string like "*.txt", which would find all text files.
    :return: A list=[] of absolute filepaths matching the glob pattern.
    """
    directoryname = os.path.abspath(directoryname)
    matches = []
    for root, dirnames, filenames in os.walk(directoryname):
        for filename in fnmatch.filter(filenames, glob_pattern):
            absolute_filepath = os.path.join(root, filename)
            matches.append(absolute_filepath)

    return matches


def fetchJobStoreFiles(jobStore, options):
    """
    Takes a list of file names as glob patterns, searches for these within a
    given directory, and attempts to take all of the files found and copy them
    into options.localFilePath.

    :param jobStore: A fileJobStore object.
    :param options.fetch: List of file glob patterns to search
        for in the jobStore and copy into options.localFilePath.
    :param options.localFilePath: Local directory to copy files into.
    :param options.jobStore: The path to the jobStore directory.
    """
    for jobStoreFile in options.fetch:
        jobStoreHits = recursiveGlob(directoryname=(options.jobStore), glob_pattern=jobStoreFile)
        for jobStoreFileID in jobStoreHits:
            logger.debug('Copying job store file: %s to %s', jobStoreFileID, options.localFilePath[0])
            jobStore.readFile(jobStoreFileID, (os.path.join(options.localFilePath[0], os.path.basename(jobStoreFileID))),
              symlink=(options.useSymlinks))


def printContentsOfJobStore(jobStorePath, nameOfJob=None):
    """
    Fetch a list of all files contained in the jobStore directory input if
    nameOfJob is not declared, otherwise it only prints out the names of files
    for that specific job for which it can find a match.  Also creates a logFile
    containing this same record of job files in the working directory.

    :param jobStorePath: Directory path to recursively look for files.
    :param nameOfJob: Default is None, which prints out all files in the jobStore.
    If specified, it will print all jobStore files that have been written to the
    jobStore by that job.
    """
    if nameOfJob:
        glob = '*' + nameOfJob + '*'
        logFile = nameOfJob + '_fileset.txt'
    else:
        glob = '*'
        logFile = 'jobstore_files.txt'
        nameOfJob = ''
    list_of_files = recursiveGlob(directoryname=jobStorePath, glob_pattern=glob)
    if os.path.exists(logFile):
        os.remove(logFile)
    for gfile in sorted(list_of_files):
        if not gfile.endswith('.new'):
            logger.debug(nameOfJob + 'File: %s', os.path.basename(gfile))
            with open(logFile, 'a+') as (f):
                f.write(os.path.basename(gfile))
                f.write('\n')


def main():
    parser = getBasicOptionParser()
    parser.add_argument('jobStore', type=str,
      help=('The location of the job store used by the workflow.' + jobStoreLocatorHelp))
    parser.add_argument('--localFilePath', nargs=1,
      help='Location to which to copy job store files.')
    parser.add_argument('--fetch', nargs='+',
      help="List of job-store files to be copied locally.Use either explicit names (i.e. 'data.txt'), or specify glob patterns (i.e. '*.txt')")
    parser.add_argument('--listFilesInJobStore', help='Prints a list of the current files in the jobStore.')
    parser.add_argument('--fetchEntireJobStore', help='Copy all job store files into a local directory.')
    parser.add_argument('--useSymlinks', help="Creates symlink 'shortcuts' of files in the localFilePath instead of hardlinking or copying, where possible.  If this is not possible, it will copy the files (shutil.copyfile()).")
    parser.add_argument('--version', action='version', version=version)
    options = parseBasicOptions(parser)
    config = Config()
    config.setOptions(options)
    jobStore = Toil.resumeJobStore(config.jobStore)
    logger.debug('Connected to job store: %s', config.jobStore)
    if options.fetch:
        logger.debug('Fetching local files: %s', options.fetch)
        fetchJobStoreFiles(jobStore=jobStore, options=options)
    else:
        if options.fetchEntireJobStore:
            logger.debug('Fetching all local files.')
            options.fetch = '*'
            fetchJobStoreFiles(jobStore=jobStore, options=options)
    if options.listFilesInJobStore:
        printContentsOfJobStore(jobStorePath=(options.jobStore))


if __name__ == '__main__':
    main()