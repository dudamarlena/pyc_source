# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/repository/server/IRService.py
# Compiled at: 2012-09-06 11:03:15
"""
Service interface in the server side.

"""
__author__ = 'Fugang Wang, Javier Diaz'
import cherrypy
from cherrypy.lib import cptools
import os, sys, os.path, re, string
from datetime import datetime
from futuregrid.image.repository.server.IRTypes import ImgMeta
from futuregrid.image.repository.server.IRTypes import ImgEntry
from futuregrid.image.repository.server.IRTypes import IRUser
from futuregrid.image.repository.server.IRServerConf import IRServerConf
import futuregrid.image.repository.server.IRUtil
from futuregrid.utils.FGTypes import FGCredential
from futuregrid.utils import FGAuth, fgLog

class IRService(object):

    def __init__(self):
        super(IRService, self).__init__()
        self._repoConf = IRServerConf()
        self._repoConf.loadRepoServerConfig()
        self._backend = self._repoConf.getBackend()
        self._address = self._repoConf.getAddress()
        self._userAdmin = self._repoConf.getUserAdmin()
        self._configFile = self._repoConf.getConfigFile()
        self._imgStore = self._repoConf.getImgStore()
        self._addressS = self._repoConf.getAddressS()
        self._userAdminS = self._repoConf.getUserAdminS()
        self._configFileS = self._repoConf.getConfigFileS()
        print '\nReading Configuration file from ' + self._repoConf.getServerConfig() + '\n'
        self._log = fgLog.fgLog(self._repoConf.getLogRepo(), self._repoConf.getLogLevelRepo(), 'Img Repo Server', False)
        if self._backend == 'mongodb':
            from IRDataAccessMongo import ImgStoreMongo
            from IRDataAccessMongo import ImgMetaStoreMongo
            from IRDataAccessMongo import IRUserStoreMongo
            self.metaStore = ImgMetaStoreMongo(self._address, self._userAdmin, self._configFile, self._log)
            self.imgStore = ImgStoreMongo(self._address, self._userAdmin, self._configFile, self._imgStore, self._log)
            self.userStore = IRUserStoreMongo(self._address, self._userAdmin, self._configFile, self._log)
        elif self._backend == 'mysql':
            from IRDataAccessMysql import ImgStoreMysql
            from IRDataAccessMysql import ImgMetaStoreMysql
            from IRDataAccessMysql import IRUserStoreMysql
            self.metaStore = ImgMetaStoreMysql(self._address, self._userAdmin, self._configFile, self._log)
            self.imgStore = ImgStoreMysql(self._address, self._userAdmin, self._configFile, self._imgStore, self._log)
            self.userStore = IRUserStoreMysql(self._address, self._userAdmin, self._configFile, self._log)
        elif self._backend == 'swiftmysql':
            from IRDataAccessSwiftMysql import ImgStoreSwiftMysql
            from IRDataAccessSwiftMysql import ImgMetaStoreSwiftMysql
            from IRDataAccessSwiftMysql import IRUserStoreSwiftMysql
            self.metaStore = ImgMetaStoreSwiftMysql(self._address, self._userAdmin, self._configFile, self._log)
            self.imgStore = ImgStoreSwiftMysql(self._address, self._userAdmin, self._configFile, self._addressS, self._userAdminS, self._configFileS, self._imgStore, self._log)
            self.userStore = IRUserStoreSwiftMysql(self._address, self._userAdmin, self._configFile, self._log)
        elif self._backend == 'swiftmongo':
            from IRDataAccessSwiftMongo import ImgStoreSwiftMongo
            from IRDataAccessSwiftMongo import ImgMetaStoreSwiftMongo
            from IRDataAccessSwiftMongo import IRUserStoreSwiftMongo
            self.metaStore = ImgMetaStoreSwiftMongo(self._address, self._userAdmin, self._configFile, self._log)
            self.imgStore = ImgStoreSwiftMongo(self._address, self._userAdmin, self._configFile, self._addressS, self._userAdminS, self._configFileS, self._imgStore, self._log)
            self.userStore = IRUserStoreSwiftMongo(self._address, self._userAdmin, self._configFile, self._log)
        elif self._backend == 'cumulusmysql':
            from IRDataAccessCumulusMysql import ImgStoreCumulusMysql
            from IRDataAccessCumulusMysql import ImgMetaStoreCumulusMysql
            from IRDataAccessCumulusMysql import IRUserStoreCumulusMysql
            self.metaStore = ImgMetaStoreCumulusMysql(self._address, self._userAdmin, self._configFile, self._log)
            self.imgStore = ImgStoreCumulusMysql(self._address, self._userAdmin, self._configFile, self._addressS, self._userAdminS, self._configFileS, self._imgStore, self._log)
            self.userStore = IRUserStoreCumulusMysql(self._address, self._userAdmin, self._configFile, self._log)
        elif self._backend == 'cumulusmongo':
            from IRDataAccessCumulusMongo import ImgStoreCumulusMongo
            from IRDataAccessCumulusMongo import ImgMetaStoreCumulusMongo
            from IRDataAccessCumulusMongo import IRUserStoreCumulusMongo
            self.metaStore = ImgMetaStoreCumulusMongo(self._address, self._userAdmin, self._configFile, self._log)
            self.imgStore = ImgStoreCumulusMongo(self._address, self._userAdmin, self._configFile, self._addressS, self._userAdminS, self._configFileS, self._imgStore, self._log)
            self.userStore = IRUserStoreCumulusMongo(self._address, self._userAdmin, self._configFile, self._log)
        else:
            print 'Wrong backend'
            sys.exit()

    def getRepoConf(self):
        return self._repoConf

    def genImgId(self):
        """
        return None if it could not get an imgId
        """
        return self.metaStore.genImgId()

    def getLog(self):
        return self._log

    def setLog(self, log):
        self._log = log

    def getAuthorizedUsers(self):
        return self._authorizedUsers

    def getBackend(self):
        return self._backend

    def getImgStore(self):
        return self._imgStore

    def auth(self, userId, userCred, provider):
        """
        Check the status of the user and verify the passwd.        
        
        return True, False, "NoActive", "NoUser"
        """
        cred = FGCredential(provider, userCred)
        status = FGAuth.auth(userId, cred)
        if status:
            userstatus = self.userStore.getUserStatus(userId)
            if userstatus == 'Active':
                self.userStore.updateLastLogin(userId)
            else:
                status = userstatus
        return status

    def isUserAdmin(self, userId):
        self._log.info('user:' + userId + ' command:isUserAdmin args={userId:' + userId + '}')
        return self.userStore.isAdmin(userId)

    def getUserStatus(self, userId):
        """
        This is to verify the status of a user. 
        This method should be called by the auth method.
        return "Active", "NoActive" or "NoUser"
        """
        self._log.info('user:' + userId + ' command:getUserStatus args={userId:' + userId + '}')
        return self.userStore.getUserStatus(userId)

    def uploadValidator(self, userId, size):
        self._log.info('user:' + userId + ' command:uploadValidator args={size:' + str(size) + '}')
        return self.userStore.uploadValidator(userId, size)

    def userAdd(self, userId, username):
        self._log.info('user:' + userId + ' command:userAdd args={userIdtoAdd:' + username + '}')
        user = IRUser(username)
        return self.userStore.userAdd(userId, user)

    def userDel(self, userId, userIdtoDel):
        self._log.info('user:' + userId + ' command:userDel args={userIdtoDel:' + userIdtoDel + '}')
        return self.userStore.userDel(userId, userIdtoDel)

    def userList(self, userId):
        self._log.info('user:' + userId + ' command:userlist')
        return self.userStore.queryStore(userId, None)

    def setUserRole(self, userId, userIdtoModify, role):
        self._log.info('user:' + userId + ' command:setUserRole args={userIdtoModify:' + userIdtoModify + ', role:' + role + '}')
        if role in IRUser.Role:
            return self.userStore.setRole(userId, userIdtoModify, role)
        else:
            self._log.error('Role ' + role + ' is not valid')
            print 'Role not valid. Valid roles are ' + str(IRUser.Role)
            return False

    def setUserQuota(self, userId, userIdtoModify, quota):
        self._log.info('user:' + userId + ' command:setUserQuota args={userIdtoModify:' + userIdtoModify + ', quota:' + str(quota) + '}')
        return self.userStore.setQuota(userId, userIdtoModify, quota)

    def setUserStatus(self, userId, userIdtoModify, status):
        self._log.info('user:' + userId + ' command:setUserStatus args={userIdtoModify:' + userIdtoModify + ', status:' + status + '}')
        if status in IRUser.Status:
            return self.userStore.setUserStatus(userId, userIdtoModify, status)
        else:
            self._log.error('Status ' + status + ' is not valid')
            print 'Status not valid. Status available: ' + str(IRUser.Status)
            return False

    def query(self, userId, queryString):
        self._log.info('user:' + userId + ' command:list args={queryString:' + queryString + '}')
        return self.metaStore.getItems(queryString)

    def get(self, userId, option, imgId):
        self._log.info('user:' + userId + ' command:get args={option:' + option + ', imgId:' + imgId + '}')
        if option == 'img':
            return self.imgStore.getItem(imgId, userId, self.userStore.isAdmin(userId))
        if option == 'uri':
            return self.imgStore.getItemUri(imgId, userId, self.userStore.isAdmin(userId))

    def put(self, userId, imgId, imgFile, attributeString, size, extension):
        """
        Register the file in the database
        
        return imgId or 0 if something fails
        """
        status = False
        statusImg = False
        fileLocation = ''
        aMeta = None
        aImg = None
        if size > 0:
            if type(imgFile) == cherrypy._cpreqbody.Part:
                self._log.info('user:' + userId + ' command:put args={imgId:' + imgId + ', imgFile:' + imgId + ', metadata:' + attributeString + ', size:' + str(size) + ', extension:' + extension + '}')
                aMeta = self._createImgMeta(userId, imgId, attributeString, False)
                aImg = ImgEntry(imgId, aMeta, self._imgStore + '/' + imgId, size, extension)
                statusImg = self.imgStore.addItem(aImg, imgFile)
            else:
                self._log.info('user:' + userId + ' command:put args={imgId:' + imgId + ', imgFile:' + imgFile + ', metadata:' + attributeString + ', size:' + str(size) + ', extension:' + extension + '}')
                fileLocation = self._imgStore + imgId
                if os.path.isfile(fileLocation):
                    aMeta = self._createImgMeta(userId, imgId, attributeString, False)
                    aImg = ImgEntry(imgId, aMeta, fileLocation, size, extension.strip())
                    statusImg = self.imgStore.addItem(aImg, None)
            if statusImg:
                if re.search('mongo', self._backend) == None:
                    statusMeta = self.metaStore.addItem(aMeta)
                else:
                    statusMeta = True
                if statusMeta:
                    statusAcc = self.userStore.updateAccounting(userId, size, 1)
                    if statusAcc:
                        status = True
        else:
            self._log.error('File size must be higher than 0')
        if status:
            return aImg._imgId
        else:
            return 0
            return

    def updateItem(self, userId, imgId, attributeString):
        """
        Update Image Repository
      
        keywords:
        option: 
        img - update only the Image file
        meta - update only the Metadata
        all - update Image file and Metadata
        """
        self._log.info('user:' + userId + ' command:updateItem args={imgId:' + imgId + ',metadata:' + attributeString + '}')
        success = False
        self._log.debug(str(attributeString))
        aMeta = self._createImgMeta(userId, imgId, attributeString, True)
        self._log.debug(str(aMeta))
        success = self.metaStore.updateItem(userId, imgId, aMeta)
        return success

    def remove(self, userId, imgIdList):
        self._log.info('user:' + userId + ' command:remove args={imgId:' + imgIdList + '}')
        notdeletedIds = []
        for imgId in imgIdList.split():
            status = False
            owner = self.imgStore.getOwner(imgId)
            if owner != None:
                size = [
                 0]
                status = self.imgStore.removeItem(userId, imgId, size, self.userStore.isAdmin(userId))
            if status:
                status = self.userStore.updateAccounting(owner, -size[0], -1)
                self._log.info('Image ' + imgId + ' removed')
            else:
                notdeletedIds.append(imgId)
                self._log.info('Image ' + imgId + ' NOT removed')

        if len(notdeletedIds) == 0:
            return True
        else:
            return (' ').join(notdeletedIds)
            return

    def histImg(self, userId, imgId):
        self._log.info('user:' + userId + ' command:histImg args={imgId:' + imgId + '}')
        output = self.imgStore.histImg(imgId)
        if output != None:
            output = re.sub('imgURI=,|size=0,|extension=', '', str(output))
        return output

    def histUser(self, userId, userIdtoSearch):
        self._log.info('user:' + userId + ' command:histImg args={userIdtoSearch:' + userIdtoSearch + '}')
        output = {}
        if userIdtoSearch == 'None':
            userIdtoSearch = None
        users = self.userStore.queryStore(userId, userIdtoSearch)
        if users != None:
            users = re.sub('cred=.*?, ', '', str(users))
        return users

    def _createImgMeta(self, userId, imgId, attributeString, update):
        """
        Create a ImgMeta object from a list of attributes
        
        keywords
        update: if True no default values are added
        """
        args = [
         ''] * 10
        attributes = attributeString.split('&')
        for item in attributes:
            attribute = item.strip()
            tmp = attribute.split('=')
            for i in range(len(tmp)):
                tmp[i] = tmp[i].strip()

            if len(tmp) == 2:
                key = string.lower(tmp[0])
                value = tmp[1]
                if key in ImgMeta.metaArgsIdx.keys():
                    if key == 'vmtype':
                        value = string.lower(value)
                        if value not in ImgMeta.VmType:
                            print 'Wrong value for VmType, please use: ' + str(ImgMeta.VmType)
                            break
                    elif key == 'imgtype':
                        value = string.lower(value)
                        if value not in ImgMeta.ImgType:
                            print 'Wrong value for ImgType, please use: ' + str(ImgMeta.ImgType)
                            break
                    elif key == 'permission':
                        value = string.lower(value)
                        if value not in ImgMeta.Permission:
                            print 'Wrong value for Permission, please use: ' + str(ImgMeta.Permission)
                            break
                    elif key == 'imgstatus':
                        value = string.lower(value)
                        if value not in ImgMeta.ImgStatus:
                            print 'Wrong value for ImgStatus, please use: ' + str(ImgMeta.ImgStatus)
                            break
                    args[ImgMeta.metaArgsIdx[key]] = value

        if not update:
            for x in range(len(args)):
                if args[x] == '':
                    args[x] = ImgMeta.argsDefault[x]

        aMeta = ImgMeta(imgId, args[1], args[2], userId, args[4], args[5], args[6], args[7], args[8], args[9])
        return aMeta