# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gitbranchhealth/manager.py
# Compiled at: 2014-08-29 20:03:05
from git.refs.head import Head
from git.util import join_path
from git.refs.remote import RemoteReference
from git.refs.reference import Reference

class BranchManager:

    def __init__(self, aOptions):
        self.__mOptions = aOptions
        self.__mBranchMap = []

    def getPrefix(self, aRef):
        if type(aRef) == RemoteReference:
            return 'refs/remotes/'
        return 'refs/heads/'

    def getBranchPath(self, aRef):
        branchName = self.getPrefix(aRef)
        branchName = branchName + aRef.name
        return branchName

    def getBranchMap(self, aRefList):
        branchMap = []
        repo = self.__getOptions().getRepo()
        assert repo.bare == False
        gitCmd = repo.git
        for branch in aRefList:
            branchName = self.getBranchPath(branch)
            shouldIgnore = False
            for ignoredBranch in self.__getOptions().getIgnoredBranches():
                if branchName.endswith('/' + ignoredBranch):
                    shouldIgnore = True
                    break

            if shouldIgnore:
                continue
            hasActivity = gitCmd.log('--abbrev-commit', '--date=relative', '-1', branchName)
            hasActivityNonRel = gitCmd.log('--abbrev-commit', '--date=iso', '-1', branchName)
            hasActivityLines = hasActivity.split('\n')
            hasActivityNonRelLines = hasActivityNonRel.split('\n')
            i = 0
            for line in hasActivityLines:
                if 'Date:' in line:
                    lastActivity = line.replace('Date: ', '').strip()
                    lastActivityNonRel = hasActivityNonRelLines[i].replace('Date: ', '').strip()
                    break
                i = i + 1

            branchMap.append((branchName, (lastActivity, lastActivityNonRel)))

        return branchMap

    def getBranchMapFromRemote(self, aRemoteName):
        log = self.__getOptions()
        if not aRemoteName:
            log.warn('Cannot get branches from nameless remote')
            return []
        else:
            repo = self.__getOptions().getRepo()
            assert repo.bare == False
            gitCmd = repo.git
            remoteToUse = None
            for someRemote in repo.remotes:
                if aRemoteName == someRemote.name:
                    remoteToUse = someRemote

            remotePrefix = 'remotes/' + aRemoteName + '/'
            return self.getBranchMap(remoteToUse.refs)

    def getLocalBranches(self):
        repo = self.__mOptions.getRepo()
        heads = [ x.name for x in repo.branches ]
        return heads

    def deleteAllOldBranches(self, aBranchesToDelete):
        log = self.__getOptions().getLog()
        for branchToDelete in aBranchesToDelete:
            branchName, lastActivityRel, branchHealth = branchToDelete
            if branchName.startswith('refs/heads'):
                self.__deleteOldBranch(branchName)
            elif branchName.startswith('remotes'):
                splitName = branchName.split('/')
                remoteName = splitName[(len(splitName) - 2)]
                self.__deleteOldBranch(branchName, remoteName, True)

    def __getOptions(self):
        """
    Retrieve the options object that this BranchManager was instantiated
    with.

    @return The BranchHealthOptions object that this BranchManager was created
            with.
    """
        return self.__mOptions

    def __deleteOldBranch(self, aBranch, aRemote='local', aShouldDeleteLocal=True):
        log = self.__getOptions().getLog()
        repo = self.__getOptions().getRepo()
        if aBranch.split('/')[(-1)] == 'master':
            log.warn('Cowardly refusing to delete master branch')
            return
        if aRemote == 'local':
            log.debug('Going to delete LOCAL branch: ' + aBranch)
            if aBranch.split('/')[(-1)] in repo.heads:
                Head.delete(aBranch.split('/')[(-1)])
        else:
            log.debug('Going to delete REMOTE branch: ' + aBranch)
            branchRef = RemoteReference(repo, join_path('refs', aBranch))
            log.debug('Ready to delete: ' + str(branchRef))
            RemoteReference.delete(repo, branchRef)
            if aShouldDeleteLocal:
                self.deleteOldBranch(branchRef.remote_head)