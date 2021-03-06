# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/zourite/core/plugin.py
# Compiled at: 2010-04-27 09:42:54
"""
Created on 3 mars 2010

@author: thierry
"""
import logging, os.path, urllib, datetime, gtk, gtk.gdk
from ..common import version
version.getInstance().submitRevision('$Revision: 207 $')
NOT_YET_IMPLEMENTED = 'not yet implemented'
PLUGIN_CONF_INFO = '__info__'
PLUGIN_CONF_WEBBROWSER = '__webbrowser__'
PLUGIN_CONF_STEP = '__step__'

class ZouritePlugin:
    """
    Interface for any network that can be used by zourite
    """

    def run_plugin(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def configure(self, data=None):
        """
        configure the plugin.
        The configuration may be a multiple step process and the data parameter
        contains user provided information. Call this method with no parameter
        to initiate a configuration process. The method return a set of required
        parameter you can pass to a subsequent call as data parameter. And so on.
        When the method return an empty set it means that the configuration process
        is finished.
        
        """
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def get_plugin_id(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getMyConnections(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getMyStatus(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def setMyStatus(self, status):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def clearMyStatus(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getNetworkUpdate(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getShortProfile(self, contactId):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getFullProfile(self, contactId):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getMyShortProfile(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getMyFulllProfile(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getGtkImage(self, shortProfile):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getGdkPixbuf(self, shortProfile):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def getPluginLogoPixbuf(self):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def sendInvitationRequest(self, contactId, subject, body):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def sendMessageRequest(self, contactId, subject, body):
        raise RuntimeError(NOT_YET_IMPLEMENTED)

    def sendMessageToNetwork(self, body):
        raise RuntimeError(NOT_YET_IMPLEMENTED)


class NetworkUpdate:
    """
    base class of any network update
    """
    networkId = ''
    timestamp = None

    def __init__(self, timestamp, networkId):
        self.timestamp = timestamp
        self.networkId = networkId


class NetworkUpdateConnection(NetworkUpdate):
    """
    Network Update of type connection. This is used  when a contact have connected
    to another people
    """
    connection = None
    newConnection = None

    def __init__(self, timestamp, connection, newConnection, networkId):
        NetworkUpdate.__init__(self, timestamp, networkId)
        self.connection = connection
        self.newConnection = newConnection

    def __str__(self):
        return '%s %s is now connected to %s' % (self.connection.firstname, self.connection.lastname, str(self.newConnection))


class NetworkUpdateStatus(NetworkUpdate):
    """
    A connection have update its status
    """
    connection = None
    status = ''

    def __init__(self, timestamp, connection, status, networkId):
        NetworkUpdate.__init__(self, timestamp, networkId)
        self.status = status
        self.connection = connection

    def __str__(self):
        return '%s %s says %s' % (self.connection.firstname, self.connection.lastname, self.status)


class NetworkUpdateSelfConnection(NetworkUpdateConnection):
    """
    The user have made a new connection
    """

    def __init__(self, timestamp, newConn, networkId):
        NetworkUpdateConnection.__init__(self, timestamp, None, newConn, networkId)
        return

    def __str__(self):
        return 'You are now connected to %s' % str(self.newConnection)


class NetworkProfileUpdate(NetworkUpdate):
    """
    This class hold information about a connection that have updated his profile
    """

    def __init__(self, timestamp, connection, networkId):
        NetworkUpdate.__init__(self, timestamp, networkId)
        self.connection = connection

    def __str__(self):
        return '%s %s has update his/her profile' % (self.connection.firstname, self.connection.lastname)


class NetworkJoinGroupUpdate(NetworkUpdate):
    """
    This class hold information about a contact that ha joined a group
    """

    def __init__(self, timestamp, connection, networkId, groupName):
        NetworkUpdate.__init__(self, timestamp, networkId)
        self.connection = connection
        self.groupName = groupName

    def __str__(self):
        return '%s %s has joined %s' % (self.connection.firstname, self.connection.lastname, self.groupName)


class Person:
    """
    Some few data for a connection. This is only some information like firstname, headline and so.
    For more advanced information use Profile instance. 
    """
    id = ''
    networkId = ''
    firstname = ''
    lastname = ''
    headline = ''

    def __init__(self):
        self.id = ''
        self.firstname = ''
        self.lastname = ''
        self.headline = ''
        self.networkId = ''

    def __str__(self):
        return '%s %s as %s' % (self.firstname, self.lastname, self.headline)


class ShortProfile(Person):
    """
    a profile with basic information
    """
    picture = None
    email = None
    phone = None

    def __init__(self):
        Person.__init__(self)
        self.picture = None
        self.email = None
        self.phone = None
        return


class ImageProxy:
    """
    This class can be used to store a  picture attribute for ShortProfile.
    When the plugin is asked for the picture it can retrieve it by this object 
    instead of calling the network API.
    """

    def getGtkImage(self):
        raise RuntimeError('not yet implemented')

    def getGdkPixbuf(self):
        raise RuntimeError('not yet implemented')


class ImageProxyFile(ImageProxy):
    """
    Implementation of ImageProxy that retrieve a picture from file
    These data are stored in the plugin home directory for further use
    """

    def __init__(self, pluginName, filename):
        self.pluginName = pluginName
        self.filename = filename

    def getGtkImage(self):
        file = get_plugin_file_location(self.pluginName, self.filename)
        image = gtk.Image()
        image.set_from_file(file)
        return image

    def getGdkPixbuf(self):
        file = get_plugin_file_location(self.pluginName, self.filename)
        pixbuf = gtk.gdk.pixbuf_new_from_file(file)
        return pixbuf


class ImageProxyNone(ImageProxy):
    """
    This can be used when no image is available
    """

    def getGtkImage(self):
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_LARGE_TOOLBAR)
        return image

    def getGdkPixbuf(self):
        return gtk.gdk.pixbuf_new_from_file('general_default_avatar.png')


class ImageProxyUrl(ImageProxy):
    """
    Implementation of an ImageProxy that retrieve the picture from an url. This 
    is currently used by LinkedIn plugin.
    """
    url = None
    filename = None

    def __init__(self, contactId, pluginName, url):
        """
        plugin : the plugin whom location will be used to store a local cache for
        the picture
        url: the web url of the picture
        """
        self.url = url
        self.filename = contactId
        self.pluginName = pluginName

    def getGtkImage(self):
        file = get_plugin_file_location(self.pluginName, self.filename)
        if os.path.exists(file):
            pass
        else:
            urllib.urlretrieve(self.url, file)
        image = gtk.Image()
        image.set_from_file(file)
        return image

    def getGdkPixbuf(self):
        file = get_plugin_file_location(self.pluginName, self.filename)
        if os.path.exists(file):
            pass
        else:
            urllib.urlretrieve(self.url, file)
        pixbuf = gtk.gdk.pixbuf_new_from_file(file)
        return pixbuf


class FullProfile(ShortProfile):
    """
    a profile with all available information
    """
    summary = ''
    industry = ''
    location = ''
    positions = []

    def __init__(self):
        ShortProfile.__init__(self)
        self.summary = ''
        self.industry = ''
        self.location = ''
        self.positions = []


class Position:
    title = ''
    summary = ''
    company = ''
    dateDebut = None

    def __init__(self, title, company, dateDebut=None):
        self.title = title
        self.company = company
        self.dateDebut = dateDebut
        self.company = ''


def get_plugin_file_location(pluginame, filename):
    """
    return the full path name of a file for a given plugin
    """
    result = os.path.expanduser('~')
    result = os.path.join(result, '.zourite')
    result = os.path.join(result, pluginame)
    result = os.path.join(result, filename)
    return result


def ensure_plugin_config_store_exist(pluginame):
    u"""
    Vérifie que la zone de stockage de la configuration du plugin exist
    et la crée le cas échéant
    """
    storage = os.path.expanduser('~')
    storage = os.path.join(storage, '.zourite')
    storage = os.path.join(storage, pluginame)
    if os.path.exists(storage):
        pass
    else:
        os.makedirs(storage)


class ZouriteException(Exception):
    pass


class UnvailableException(ZouriteException):
    """
    This exception my be thrown by any plugin method that rely on
    a network (I/O) resource or a bandwith limit (like LinkedIn) when
    the method can't be achieve right now. The handler of this exception 
    is suggested to use any cached data.
    """
    pass


class ConfigurationRequiredExeption(ZouriteException):
    """
    Thrown by the plugin when it miss correct configuration to run.
    This exception must be caught by zourite either in a command line interface 
    or g GUI to bring up a wizard to help configuring the plugin.
    """
    pass