# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/repository/server/IRDataAccessSwiftMongo.py
# Compiled at: 2012-09-06 11:03:15
"""
This class is to use MongoDB as Image Repository back-end

Create a config file with
    list of mongos: ip/address and port
    list of db names: I would say one per imgType    

MongoDB Databases Info:

    A database with all the info. The problem of the Option 1 is that we need to perform 
                                   a minimum of two queries to get an image
                                  The problem of Option 2 could be that if the db is too big,
                                   we could have performance problems... or not, lets see ;)
        images.fs.chunks (GridFS files)
        images.fs.files  (GridFS metadata)
        images.data      (Image details)
        images.meta        (Image metadata)

REMEBER: imgId will be _id (String) in the data collection, which is also _id (ObjectId) in fs.files. 
               In the first case it is an String and in the second one is an ObjectId
               
"""
__author__ = 'Javier Diaz'
import pymongo
from pymongo import Connection
from pymongo.objectid import ObjectId
import gridfs, bson, os, re, sys, cloudfiles
from datetime import datetime
from futuregrid.image.repository.server.IRDataAccessMongo import ImgStoreMongo
from futuregrid.image.repository.server.IRDataAccessMongo import ImgMetaStoreMongo
from futuregrid.image.repository.server.IRDataAccessMongo import IRUserStoreMongo
from futuregrid.image.repository.server.IRTypes import ImgEntry
from futuregrid.image.repository.server.IRTypes import ImgMeta
from futuregrid.image.repository.server.IRTypes import IRUser

class ImgStoreSwiftMongo(ImgStoreMongo):

    def __init__(self, address, userAdmin, configFile, addressS, userAdminS, configFileS, imgStore, log):
        """
        Initialize object
        
        Keyword parameters:             
        _mongoaddress = mongos addresses and ports separated by commas (optional if config file exits)
        _items = list of imgEntry
        _dbName = name of the database
        
        """
        super(ImgStoreMongo, self).__init__()
        self._dbName = 'imagesS'
        self._datacollection = 'data'
        self._metacollection = 'meta'
        self._dbConnection = None
        self._log = log
        self._mongoAddress = address
        self._userAdmin = userAdmin
        self._configFile = configFile
        self._imgStore = imgStore
        self._swiftAddress = addressS
        self._userAdminS = userAdminS
        self._configFileS = configFileS
        self._swiftConnection = None
        self._containerName = 'imagesMongo'
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
        self._log.debug(imgLinks[0])
        if result:
            return imgLinks[0]
        else:
            return
            return

    def queryStore(self, imgIds, imgLinks, userId, admin, extension):
        """        
        Query the DB and provide a generator object of the Images to create them with strean method.    
        
        keywords:
        imgIds: this is the list of images that I need
        imgEntries: This is an output parameter. Return the list of GridOut objects
                      To read the file it is needed to use the read() method    
        """
        del imgLinks[:]
        itemsFound = 0
        if self.mongoConnection():
            try:
                try:
                    dbLink = self._dbConnection[self._dbName]
                    collection = dbLink[self._datacollection]
                    for imgId in imgIds:
                        access = False
                        if self.existAndOwner(imgId, userId) or admin:
                            access = True
                        elif self.isPublic(imgId):
                            access = True
                        if access:
                            ext = collection.find_one({'_id': imgId})['extension']
                            imagepath = self._imgStore + '/' + imgId + '' + ext.strip()
                            if os.path.isfile(imagepath):
                                for i in range(1000):
                                    imagepath = self._imgStore + '/' + imgId + '' + ext.strip() + '_' + i.__str__()
                                    if not os.path.isfile(imagepath):
                                        break

                            cmd = '$HOME/swift/trunk/bin/st download -q ' + self._containerName + ' ' + imgId + ' -o ' + imagepath + ' -A https://192.168.11.40:8080/auth/v1.0 -U test:tester -K testing'
                            os.system(cmd)
                            self._log.debug(imagepath)
                            imgLinks.append(imagepath)
                            collection.update({'_id': imgId}, {'$inc': {'accessCount': 1}}, safe=True)
                            collection.update({'_id': imgId}, {'$set': {'lastAccess': datetime.utcnow()}}, safe=True)
                            itemsFound += 1

                except pymongo.errors.AutoReconnect:
                    self._log.warning('Autoreconnected in ImgStoreSwiftMongo - queryStore.')
                except pymongo.errors.ConnectionFailure:
                    self._log.error('Connection failure: the query cannot be performed.')
                except TypeError, detail:
                    self._log.error('TypeError in ImgStoreSwiftMongo - queryStore')
                except bson.errors.InvalidId:
                    self._log.error('There is no Image with such Id. (ImgStoreSwiftMongo - queryStore)')
                except gridfs.errors.NoFile:
                    self._log.error('File not found')
                except cloudfiles.errors.NoSuchObject:
                    self._log.error('File not found')
                except:
                    self._log.error('Error in ImgStoreSwiftMongo - queryToStore. ' + str(sys.exc_info()))

            finally:
                self._dbConnection.disconnect()

        else:
            self._log.error('Could not get access to the database. The file has not been stored')
        if itemsFound >= 1:
            return True
        else:
            return False

    def persistToStore(self, items, requestInstance):
        """Copy imgEntry and imgMeta to the DB. It first store the imgEntry to get the file Id
        
        Keyword arguments:
        items= list of ImgEntrys
                
        return: True if all items are stored successfully, False in any other case
        """
        self._dbConnection = self.mongoConnection()
        imgStored = 0
        if self.mongoConnection():
            try:
                try:
                    dbLink = self._dbConnection[self._dbName]
                    collection = dbLink[self._datacollection]
                    collectionMeta = dbLink[self._metacollection]
                    for item in items:
                        s = os.chdir(self._imgStore)
                        cmd = '$HOME/swift/trunk/bin/st upload -q ' + self._containerName + ' ' + item._imgId + ' -A https://192.168.11.40:8080/auth/v1.0 -U test:tester -K testing'
                        status = os.system(cmd)
                        self._log.debug(' swift upload image status: ' + str(status))
                        if status == 0:
                            loaded = True
                        if loaded:
                            tags = item._imgMeta._tag.split(',')
                            tags_list = [ x.strip() for x in tags ]
                            meta = {'_id': item._imgId, 'os': item._imgMeta._os, 
                               'arch': item._imgMeta._arch, 
                               'owner': item._imgMeta._owner, 
                               'description': item._imgMeta._description, 
                               'tag': tags_list, 
                               'vmType': item._imgMeta._vmType, 
                               'imgType': item._imgMeta._imgType, 
                               'permission': item._imgMeta._permission, 
                               'imgStatus': item._imgMeta._imgStatus}
                            data = {'_id': item._imgId, 'createdDate': datetime.utcnow(), 
                               'lastAccess': datetime.utcnow(), 
                               'accessCount': 0, 
                               'size': item._size, 
                               'extension': item._extension}
                            collectionMeta.insert(meta, safe=True)
                            collection.insert(data, safe=True)
                            imgStored += 1

                except pymongo.errors.AutoReconnect:
                    self._log.warning('Autoreconnected.')
                except pymongo.errors.ConnectionFailure:
                    self._log.error('Connection failure. The file has not been stored. Image details: ' + item.__str__() + '\n')
                except IOError:
                    self._log.error('Error in ImgStoreSwiftMongo - persistToStore. ' + str(sys.exc_info()))
                    self._log.error('No such file or directory. Image details: ' + item.__str__())
                except TypeError:
                    self._log.error('TypeError in ImgStoreSwiftMongo - persistToStore ' + str(sys.exc_info()))
                except pymongo.errors.OperationFailure:
                    self._log.error('Operation Failure in ImgStoreSwiftMongo - persistenToStore')
                except:
                    self._log.error('Error in ImgStoreSwiftMongo - persistToStore. ' + str(sys.exc_info()))

            finally:
                self._dbConnection.disconnect()

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
        size: Size of the img deleted.
        
        Return boolean
        """
        removed = False
        if self.mongoConnection():
            if self.existAndOwner(imgId, userId) or admin:
                try:
                    try:
                        dbLink = self._dbConnection[self._dbName]
                        collection = dbLink[self._datacollection]
                        collectionMeta = dbLink[self._metacollection]
                        cmd = '$HOME/swift/trunk/bin/st delete -q ' + self._containerName + ' ' + imgId + ' -A https://192.168.11.40:8080/auth/v1.0 -U test:tester -K testing'
                        status = os.system(cmd)
                        self._log.debug(' swift remove image status: ' + str(status))
                        if status == 0:
                            aux = collection.find_one({'_id': imgId})
                            size[0] = aux['size']
                            collection.remove({'_id': imgId}, safe=True)
                            collectionMeta.remove({'_id': imgId}, safe=True)
                            removed = True
                    except pymongo.errors.AutoReconnect:
                        self._log.warning('Autoreconnected.')
                    except pymongo.errors.ConnectionFailure:
                        self._log.error('Connection failure. The file has not been updated')
                    except IOError:
                        self._log.error('Error in ImgStoreSwiftMongo - removeItem. ' + str(sys.exc_info()))
                    except TypeError:
                        self._log.error('TypeError in ImgStoreSwiftMongo - removeItem ' + str(sys.exc_info()))
                    except pymongo.errors.OperationFailure:
                        self._log.error('Operation Failure in ImgStoreSwiftMongo - RemoveItem')
                    except:
                        self._log.error('Error in ImgStoreSwiftMongo - removeItem. ' + str(sys.exc_info()))

                finally:
                    self._dbConnection.disconnect()

            else:
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
        isOwner = False
        try:
            dbLink = self._dbConnection[self._dbName]
            collection = dbLink[self._metacollection]
            cmd = '$HOME/swift/trunk/bin/st list ' + self._containerName + ' -A https://192.168.11.40:8080/auth/v1.0 -U test:tester -K testing'
            output = os.popen(cmd).read()
            if imgId in output:
                exists = True
            aux = collection.find_one({'_id': imgId, 'owner': ownerId})
            if aux == None:
                isOwner = False
            else:
                isOwner = True
        except pymongo.errors.AutoReconnect:
            self._log.warning('Autoreconnected.')
        except pymongo.errors.ConnectionFailure:
            self._log.error('Connection failure')
        except TypeError, detail:
            self._log.error('TypeError in ImgStoreMongo - existAndOwner')
        except bson.errors.InvalidId:
            self._log.error('Error, not a valid ObjectId in ImgStoreMongo - existAndOwner')
        except gridfs.errors.NoFile:
            self._log.error('File not found')

        if exists and isOwner:
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


class ImgMetaStoreSwiftMongo(ImgMetaStoreMongo):

    def __init__(self, address, userAdmin, configFile, log):
        """
        Initialize object
        
        Keyword parameters:             
        _mongoaddress = mongos addresses and ports separated by commas (optional if config file exits)
        _items = list of imgEntry
        _dbName = name of the database
        
        """
        super(ImgMetaStoreMongo, self).__init__()
        self._dbName = 'imagesS'
        self._datacollection = 'data'
        self._metacollection = 'meta'
        self._dbConnection = None
        self._log = log
        self._mongoAddress = address
        self._userAdmin = userAdmin
        self._configFile = configFile
        return


class IRUserStoreSwiftMongo(IRUserStoreMongo):

    def __init__(self, address, userAdmin, configFile, log):
        """
        Initialize object
        
        Keyword parameters:             
        _mongoaddress = mongos addresses and ports separated by commas (optional if config file exits)
        _items = list of imgEntry
        _dbName = name of the database
        
        """
        super(IRUserStoreMongo, self).__init__()
        self._dbName = 'imagesS'
        self._usercollection = 'users'
        self._dbConnection = None
        self._log = log
        self._mongoAddress = address
        self._userAdmin = userAdmin
        self._configFile = configFile
        return