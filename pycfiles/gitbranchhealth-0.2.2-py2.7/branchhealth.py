# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gitbranchhealth/branchhealth.py
# Compiled at: 2014-08-29 20:03:05
from nicelog.formatters import ColorLineFormatter
import logging, sys, os
from git import *
import argparse, sys
from datetime import *
import dateutil.parser
from colors import red, yellow, green
from config import BranchHealthConfig
from util import hasGitDir
from util import isGitRepo
from util import isoDateComparator
from manager import BranchManager
DEBUG = False
VERBOSE = False
COLOR = True
HEALTHY = 0
AGED = 1
OLD = 2
gLog = None
gParser = None

class BranchHealthOptions:
    """
  Composition of all possible options for a given run of git branchhealth.
  """

    def __init__(self, aRepoPath, aRemoteName, aNumDays, aBadOnly, aNoColor, aDeleteOldBranches, aIgnoredBranches=[
 'master', 'HEAD'], aLog=None):
        """
    Initialize a new BranchHealthOptions object with parameters that were given
    from the command line.
    """
        self.mRepoPath = aRepoPath
        self.mRemoteName = aRemoteName
        self.mNumDays = aNumDays
        self.mBadOnly = aBadOnly
        self.mNoColor = aNoColor
        self.mRepo = Repo(self.mRepoPath)
        self.mLog = aLog
        self.mDeleteOldBranches = aDeleteOldBranches
        self.__mIgnoredBranches = aIgnoredBranches
        self.__setupConfigOptions()

    def shouldDeleteOldBranches(self):
        return self.mDeleteOldBranches

    def getIgnoredBranches(self):
        return self.__mIgnoredBranches

    def getRepo(self):
        return self.mRepo

    def getRepoPath(self):
        return self.mRepoPath

    def getRemoteName(self):
        return self.mRemoteName

    def getHealthyDays(self):
        return int(self.mNumDays)

    def getBadOnly(self):
        return self.mBadOnly

    def shouldHaveColor(self):
        return not self.mNoColor

    def getLog(self):
        return self.mLog

    def setLog(self, aLog):
        self.mLog = aLog

    def __setupConfigOptions(self):
        log = self.getLog()
        config = BranchHealthConfig(self.getRepo())
        self.mNoColor = not config.shouldUseColor() or self.mNoColor
        if not config.shouldIgnoreBranches():
            self.__mIgnoredBranches = []


def showBranchHealth(aOptions):
    global gLog
    branchMap = []
    log = gLog
    remoteName = aOptions.getRemoteName()
    repoPath = aOptions.getRepoPath()
    if log:
        log.debug('Operating on repository in: ' + repoPath)
        log.debug('Operating on remote named: ' + str(remoteName))
    repo = aOptions.getRepo()
    if remoteName:
        manager = BranchManager(aOptions)
        branchMap = manager.getBranchMapFromRemote(remoteName)
    sortedBranches = sortBranchesByHealth(branchMap, aOptions.getHealthyDays())
    printBranchHealthChart(sortedBranches, aOptions)


def sortBranchesByHealth(aBranchMap, aHealthyDays):
    sortedBranchMap = sorted(aBranchMap, cmp=isoDateComparator)
    return markBranchHealth(sortedBranchMap, aHealthyDays)


def markBranchHealth(aBranchList, aHealthyDays):
    finalBranchList = []
    for branchTuple in aBranchList:
        branchName, dateTuple = branchTuple
        humanDate, isoDate = dateTuple
        branchdate = dateutil.parser.parse(isoDate)
        branchLife = date.today() - branchdate.date()
        if branchLife > timedelta(aHealthyDays * 2):
            branchHealth = OLD
        elif branchLife > timedelta(aHealthyDays):
            branchHealth = AGED
        else:
            branchHealth = HEALTHY
        finalBranchList.append((branchName, humanDate, branchHealth))

    return finalBranchList


def printBranchHealthChart(aBranchMap, aOptions):
    badOnly = aOptions.getBadOnly()
    noColor = not aOptions.shouldHaveColor()
    log = gLog
    deleteBucket = []
    for branchTuple in aBranchMap:
        branchName, lastActivityRel, branchHealth = branchTuple
        if branchHealth == OLD:
            deleteBucket.append(branchTuple)
        if badOnly and not branchHealth == OLD:
            continue
        if not noColor:
            if branchHealth == HEALTHY:
                coloredDate = green(lastActivityRel)
            elif branchHealth == AGED:
                coloredDate = yellow(lastActivityRel)
            else:
                coloredDate = red(lastActivityRel)
        else:
            coloredDate = lastActivityRel
        alignedPrintout = ('{0:40} {1}').format(branchName + ':', coloredDate)
        print alignedPrintout

    if aOptions.shouldDeleteOldBranches():
        manager = BranchManager(aOptions)
        manager.deleteAllOldBranches(deleteBucket)


def splitBranchName(aBranchName):
    return aBranchName.split('/')


def createParser():
    parser = argparse.ArgumentParser(description='\n     Show health (time since creation) of git branches, in order.\n  ', add_help=True)
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Output as much as possible')
    parser.add_argument('-r', '--remote', metavar='<remote name>', action='store', help='Operate on specified remote', default=None, dest='remote')
    parser.add_argument('-b', '--bad-only', action='store_true', help='Only show branches that are ready for pruning (i.e. older than numDays * 2)', dest='badOnly')
    parser.add_argument('-d', '--days', action='store', dest='numDays', help="Specify number of days old where a branch is considered to no longer be 'healthy'", default=14)
    parser.add_argument('-n', '--nocolor', action='store_true', help="Don't use ANSI colors to display branch health", dest='noColor')
    parser.add_argument('-R', '--repository', action='store', metavar='repository', help='Path to git repository where branches should be listed', nargs='?', default='.', dest='repo')
    parser.add_argument('-D', '--delete', action='store_true', help='Delete old branches that are considered "unhealthy"', dest='deleteOld')
    parser.add_argument('--no-ignore', action='store_true', help='Do not ignore any branches (by default, "master" and "HEAD" from a given remote are ignored)', dest='noIgnore')
    return parser


def parseArguments():
    global DEBUG
    global VERBOSE
    global gParser
    if not gParser:
        gParser = createParser()
        parsed = gParser.parse_args(sys.argv[1:])
    if parsed.verbose:
        VERBOSE = True
        DEBUG = True
    repo = parsed.repo
    ignoredBranches = [
     'HEAD', 'master']
    if parsed.noIgnore:
        ignoredBranches = []
    return BranchHealthOptions(repo, parsed.remote, parsed.numDays, parsed.badOnly, parsed.noColor, parsed.deleteOld, ignoredBranches)


def setupLog(aOptions):
    global gLog
    gLog = logging.getLogger('git-branchhealth')
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ColorLineFormatter())
    if DEBUG:
        gLog.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    else:
        gLog.setLevel(logging.ERROR)
        handler.setLevel(logging.ERROR)
    gLog.addHandler(handler)
    aOptions.setLog(gLog)


def runMain():
    options = parseArguments()
    setupLog(options)
    if options.getRepoPath() == None:
        gParser.print_help()
        return
    else:
        showBranchHealth(options)
        return


if __name__ == '__main__':
    runMain()