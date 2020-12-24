# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/repository/server/IRDataAccessSwiftMysql.py
# Compiled at: 2012-09-06 11:03:15
"""
This class is to use Mysql and Swift (OpenStack Storage Object) as Image Repository back-end 

MySQL Databases Info:

    A database with all the info is called imagesS. It contains two tables
        data      (Image details and URI)
        meta        (Image metadata)

"""
__author__ = 'Javier Diaz'
from datetime import datetime
import os, re, MySQLdb, string, cloudfiles, sys
from futuregrid.image.repository.server.IRDataAccessMysql import ImgStoreMysql
from futuregrid.image.repository.server.IRDataAccessMysql import ImgMetaStoreMysql
from futuregrid.image.repository.server.IRDataAccessMysql import IRUserStoreMysql
from futuregrid.image.repository.server.IRTypes import ImgEntry
from futuregrid.image.repository.server.IRTypes import ImgMeta
from futuregrid.image.repository.server.IRTypes import IRUser
import futuregrid.image.repository.server.IRUtil

class ImgStoreSwiftMysql(ImgStoreMysql):

    def __init__(self, address, userAdmin, configFile, addressS, userAdminS, configFileS, log):
        """
        Initialize object
        
        Keyword parameters:             
        _mongoaddress = mongos addresses and ports separated by commas (optional if config file exits)
        _items = list of imgEntry
        _dbName = name of the database
        
        """
        super(ImgStoreMysql, self).__init__()
        self._dbName = 'imagesS'
        self._tabledata = 'data'
        self._tablemeta = 'meta'
        self._dbConnection = None
        self._mysqlAddress = address
        self._userAdmin = userAdmin
        self._configFile = configFile
        self._log = log
        self._swiftAddress = addressS
        self._userAdminS = userAdminS
        self._configFileS = configFileS
        self._swiftConnection = None
        self._containerName = 'images'
        return

    def getItemUri(self, imgId, userId):
        return 'For now we do not provide this feature with the Swift system as backend.'

    def getItem(self, imgId, userId, admin):
        """
        Get Image file identified by the imgId
        
        keywords:
        imgId: identifies the image
        
        return the image uri
        """
        imgLinks = []
        extension = []
        result = self.queryStore([imgId], imgLinks, userId, admin, extension)
        if result:
            return imgLinks[0]
        else:
            return
            return

    def queryStore(self, imgIds, imgLinks, userId, admin, extension):
        """        
        Query the DB and provide the uri.    
        
        keywords:
        imgIds: this is the list of images that I need
        imgLinks: This is an output parameter. Return the list URIs
        """
        itemsFound = 0
        if self.mysqlConnection() and self.swiftConnection():
            try:
                try:
                    cursor = self._dbConnection.cursor()
                    contain = self._swiftConnection.get_container(self._containerName)
                    for imgId in imgIds:
                        access = False
                        if self.existAndOwner(imgId, userId) or admin:
                            access = True
                        elif self.isPublic(imgId):
                            access = True
                        if access:
                            sql = "SELECT accessCount, extension FROM %s WHERE imgId = '%s' " % (self._tabledata, imgId)
                            cursor.execute(sql)
                            results = cursor.fetchone()
                            if results != None:
                                ext = results[1].strip()
                                imagepath = self._imgStore + '/' + imgId + '' + ext
                                if os.path.isfile(imagepath):
                                    for i in range(1000):
                                        imagepath = self._imgStore + '/' + imgId + '' + ext + '_' + i.__str__()
                                        if not os.path.isfile(imagepath):
                                            break

                                cmd = '$HOME/swift/trunk/bin/st download -q ' + self._containerName + ' ' + imgId + ' -o ' + imagepath + ' -A https://192.168.11.40:8080/auth/v1.0 -U test:tester -K testing'
                                os.system(cmd)
                                imgLinks.append(imagepath)
                                accessCount = int(results[0]) + 1
                                update = "UPDATE %s SET lastAccess='%s', accessCount='%d' WHERE imgId='%s'" % (
                                 self._tabledata, datetime.utcnow(), accessCount, imgId)
                                cursor.execute(update)
                                self._dbConnection.commit()
                                itemsFound += 1

                except MySQLdb.Error, e:
                    self._log.error('Error %d: %s' % (e.args[0], e.args[1]))
                    self._dbConnection.rollback()
                except IOError, (errno, strerror):
                    self._log.error(('I/O error({0}): {1}').format(errno, strerror))
                except TypeError, detail:
                    self._log.error('TypeError in ImgStoreSwiftMysql - queryToStore: ' + format(detail))
                except cloudfiles.errors.NoSuchObject:
                    self._log.error('File not found')
                except:
                    self._log.error('Error in ImgStoreSwiftMysql - queryToStore. ' + str(sys.exc_info()))

            finally:
                self._dbConnection.close()

        else:
            self._log.error('Could not get access to the database. Query failed')
        if itemsFound >= 1:
            return True
        else:
            return False
            return

    def persistToStore(self, items, requestInstance):
        """Copy imgEntry to the DB. 
        
        Keyword arguments:
        items= list of ImgEntrys
                
        return: True if all items are stored successfully, False in any other case
        """
        imgStored = 0
        if self.mysqlConnection():
            try:
                try:
                    cursor = self._dbConnection.cursor()
                    for item in items:
                        s = os.chdir('/tmp')
                        cmd = '$HOME/swift/trunk/bin/st upload -q ' + self._containerName + ' ' + item._imgId + ' -A https://192.168.11.40:8080/auth/v1.0 -U test:tester -K testing'
                        status = os.system(cmd)
                        self._log.debug(' swift upload image status: ' + str(status))
                        if status == 0:
                            loaded = True
                        if loaded:
                            sql = "INSERT INTO %s (imgId, imgMetaData, imgUri, createdDate, lastAccess, accessCount, size, extension)            VALUES ('%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s' )" % (
                             self._tabledata, item._imgId, item._imgId, '', datetime.utcnow(), datetime.utcnow(), 0, item._size, item._extension)
                            cursor.execute(sql)
                            self._dbConnection.commit()
                            imgStored += 1

                except MySQLdb.Error, e:
                    self._log.error('Error %d: %s' % (e.args[0], e.args[1]))
                    self._dbConnection.rollback()
                except IOError:
                    self._log.error('Error in ImgStoreSwiftMysql - persistToStore. ' + str(sys.exc_info()))
                    self._log.error('No such file or directory. Image details: ' + item.__str__())
                except TypeError:
                    self._log.error('TypeError in ImgStoreSwiftMysql - persistToStore ' + str(sys.exc_info()))
                except TypeError, detail:
                    self._log.error('TypeError in ImgStoreSwiftMysql - persistToStore ' + format(detail))
                except:
                    self._log.error('Error in ImgStoreSwiftMysql - persistToStore. ' + str(sys.exc_info()))

            finally:
                self._dbConnection.close()

        else:
            self._log.error('Could not get access to the database. The file has not been stored')
        for item in items:
            if re.search('^/tmp/', item._imgURI):
                cmd = 'rm -f ' + item._imgURI
                os.system(cmd)

        if imgStored == len(items):
            return True
        else:
            return False

    def removeItem(self, userId, imgId, size, admin):
        """
        Remove the Image file and Metainfo if imgId exists and your are the owner.
        
        IMPORTANT: if you want to update both imgEntry and imgMeta, 
                   you have to update first imgMeta and then imgEntry,
                   because imgEntry's update method change the _id of the imgMeta document
                
        keywords:
        imgId : identifies the image (I think that we can remove this)
        imgEntry : new info to update. It HAS TO include the owner in _imgMeta
        
        Return boolean
        """
        removed = False
        if self.mysqlConnection() and self.swiftConnection():
            con = MySQLdb.connect(host=self._mysqlAddress, db=self._dbName, read_default_file=self._configFile, user=self._userAdmin)
            if self.existAndOwner(imgId, userId) or admin:
                try:
                    try:
                        cursor = con.cursor()
                        sql = "SELECT size FROM %s WHERE imgId = '%s' " % (self._tabledata, imgId)
                        cursor.execute(sql)
                        results = cursor.fetchone()
                        size[0] = int(results[0])
                        cmd = '$HOME/swift/trunk/bin/st delete -q ' + self._containerName + ' ' + imgId + ' -A https://192.168.11.40:8080/auth/v1.0 -U test:tester -K testing'
                        status = os.system(cmd)
                        self._log.debug(' swift remove image status: ' + str(status))
                        if status == 0:
                            sql = "DELETE FROM %s WHERE imgId='%s'" % (self._tabledata, imgId)
                            sql1 = "DELETE FROM %s WHERE imgId='%s'" % (self._tablemeta, imgId)
                            cursor.execute(sql)
                            cursor.execute(sql1)
                            con.commit()
                            removed = True
                    except MySQLdb.Error, e:
                        self._log.error('Error %d: %s' % (e.args[0], e.args[1]))
                        con.rollback()
                    except IOError:
                        self._log.error('Error in ImgStoreSwiftMysql - removeItem. ' + str(sys.exc_info()))
                    except TypeError:
                        self._log.error('TypeError in ImgStoreSwiftMysql - removeItem ' + str(sys.exc_info()))
                    except:
                        self._log.error('Error in ImgStoreSwiftMysql - removeItem. ' + str(sys.exc_info()))

                finally:
                    con.close()

            else:
                con.close()
                self._log.error('The Image does not exist or the user is not the owner')
        else:
            self._log.error('Could not get access to the database. The file has not been removed')
        return removed

    def existAndOwner(self, imgId, ownerId):
        """
        To verify if the file exists and I am the owner
        
        keywords:
        imgId: The id of the image
        ownerId: The owner Id
        
        Return: boolean
        """
        exists = False
        owner = False
        try:
            cursor = self._dbConnection.cursor()
            contain = self._swiftConnection.get_container(self._containerName)
            cmd = '$HOME/swift/trunk/bin/st list ' + self._containerName + ' -A https://192.168.11.40:8080/auth/v1.0 -U test:tester -K testing'
            output = os.popen(cmd).read()
            if imgId in output:
                exists = True
            sql = "SELECT owner FROM %s WHERE imgId='%s' and owner='%s'" % (self._tablemeta, imgId, ownerId)
            cursor.execute(sql)
            results = cursor.fetchone()
            if results != None:
                owner = True
        except MySQLdb.Error, e:
            self._log.error('Error %d: %s' % (e.args[0], e.args[1]))
        except IOError:
            self._log.error('Error in ImgStoreSwiftMongo - existandOwner. ' + str(sys.exc_info()))
        except TypeError:
            self._log.error('TypeError in ImgStoreSwiftMongo - existandOwner ' + str(sys.exc_info()))

        if exists and owner:
            return True
        else:
            return False
            return

    def swiftConnection(self):
        """
        Connect with OpenStack swift
        
        """
        connected = False
        idu = self._userAdminS
        pw = self.getPassword(self._configFileS)
        try:
            self._swiftConnection = cloudfiles.get_connection(idu, pw, authurl='https://' + self._swiftAddress + ':8080/auth/v1.0')
            connected = True
        except:
            self._log.error('Error in swift connection. ' + str(sys.exc_info()))

        return connected


class ImgMetaStoreSwiftMysql(ImgMetaStoreMysql):

    def __init__(self, address, userAdmin, configFile, log):
        """
        Initialize object
        
        Keyword parameters:             
        _mongoaddress = mongos addresses and ports separated by commas (optional if config file exits)
        _items = list of imgEntry
        _dbName = name of the database
        
        """
        super(ImgMetaStoreMysql, self).__init__()
        self._dbName = 'imagesS'
        self._tabledata = 'data'
        self._tablemeta = 'meta'
        self._log = log
        self._dbConnection = None
        self._mysqlAddress = address
        self._userAdmin = userAdmin
        self._configFile = configFile
        return


class IRUserStoreSwiftMysql(IRUserStoreMysql):

    def __init__(self, address, userAdmin, configFile, log):
        """
        Initialize object
        
        Keyword parameters:             
        _mongoaddress = mongos addresses and ports separated by commas (optional if config file exits)
        _items = list of imgEntry
        _dbName = name of the database
        
        """
        super(IRUserStoreMysql, self).__init__()
        self._dbName = 'imagesS'
        self._tabledata = 'users'
        self._mysqlAddress = address
        self._userAdmin = userAdmin
        self._configFile = configFile
        self._log = log
        self._dbConnection = None
        return