# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/hydroshare.py
# Compiled at: 2019-10-18 10:13:30
# Size of source mod 2**32: 8456 bytes
from __future__ import print_function
import os, getpass, glob
from hs_restclient import HydroShare, HydroShareAuthBasic, HydroShareAuthOAuth2
from hs_restclient import HydroShareHTTPException
from datetime import datetime as dt
import pickle, shutil, zipfile
from . import threads
from . import resource
from . import utilities
from . import auth
from . import log
from .compat import *
logger = log.logger

class hydroshare:

    def __init__(self, save_dir=None, authfile='~/.hs_auth'):
        """
        save_dir is the location that data will hs resources will be saved.
        """
        self.hs = None
        self.content = {}
        self.authfile = os.path.expanduser(authfile)
        if save_dir is not None:
            self.download_dir = save_dir
        else:
            self.download_dir = os.environ.get('JUPYTER_DOWNLOADS', '.')
        if not os.path.exists(self.download_dir):
            raise Exception("HS resource download directory does not exist! Set this using the 'save_dir' input argument or the JUPYTER_DOWNLOADS environment variable")
        if self.hs is None:
            try:
                self.hs = auth.oauth2_authorization(self.authfile)
            except Exception:
                pass

        if self.hs is None:
            try:
                self.hs = auth.basic_authorization(self.authfile)
            except Exception:
                pass

        if self.hs is None:
            raise Exception(f"Authentication failed using: {self.authfile}")
        self.user_info = self.hs.getUserInfo()

    def close(self):
        """
        closes the connection to HydroShare
        """
        self.hs.session.close()

    def userInfo(self):
        return self.user_info

    def deleteResource(self, resid):
        """Deletes a hydroshare resource

        args:
        -- resid: hydroshare resource id

        returns:
        -- True if successful, else False
        """
        try:
            self.hs.deleteResource(resid)
            logger.info(f"+ successfully removed resource: {resid}")
        except Exception as e:
            try:
                logger.error(f"- failed to remove resource: {resid}")
                raise Exception(e)
            finally:
                e = None
                del e

        return True

    def getResourceMetadata(self, resid):
        """Gets metadata for a specified resource.

        args:
        -- resid: hydroshare resource id

        returns:
        -- resource metadata object
        """
        science_meta = self.hs.getScienceMetadata(resid)
        system_meta = self.hs.getSystemMetadata(resid)
        return resource.ResourceMetadata(system_meta, science_meta)

    def createResource(self, abstract, title, keywords=[], content_files=[]):
        """Creates a hydroshare resource.

        args:
        -- abstract: abstract for resource (str, required)
        -- title: title of resource (str, required)
        -- keywords: list of subject keywords (list, default=>[])
        -- content_files: data to save as resource content (list, default=>[])

        returns:
        -- resource_id
        """
        for f in content_files:
            if not os.path.exists(f):
                raise Exception(f"Could not find file: {f}")

        resid = None
        f = None if len(content_files) == 0 else content_files[0]
        logger.info('+ creating resource')
        resid = self.hs.createResource('CompositeResource', title=title,
          abstract=abstract,
          resource_file=f,
          keywords=keywords)
        try:
            if len(content_files) > 1:
                self.addContentToExistingResource(resid, content_files[1:])
        except Exception as e:
            try:
                logger.error(e)
            finally:
                e = None
                del e

        return resid

    def getResource(self, resourceid):
        """Downloads content of a hydroshare resource.

        args:
        -- resourceid: id of the hydroshare resource (str)

        returns:
        -- None
        """
        dst = self.download_dir
        try:
            logger.info(f"+ downloading resource: {resourceid}")
            self.hs.getResource(resourceid, destination=dst,
              unzip=False)
            logger.info('Successfully downloaded resource %s' % resourceid)
        except Exception as e:
            try:
                logger.error('Failed to retrieve resource content from HydroShare: %s' % e)
                return
            finally:
                e = None
                del e

        archive = f"{os.path.join(dst, resourceid)}.zip"
        with zipfile.ZipFile(archive, 'r') as (zip_ref):
            zip_ref.extractall(f"{os.path.join(dst)}")
            os.remove(archive)
        return os.path.join(dst, resourceid)

    def getResourceFiles(self, resid):
        """
        returns a list of files in a hydroshare resource
        """
        try:
            response = self.hs.resource(resid).files.all()
        except Exception:
            raise Exception(f"Failed to get list of files for resouce {resid}")

        dat = response.json()
        if 'results' in dat.keys():
            return dat['results']
        return []

    def addContentToExistingResource(self, resid, source, target=None):
        """Adds content files to an existing hydroshare resource.

        args:
        -- resid: id of an existing hydroshare resource (str)
        -- source: file paths to be added to resource
        -- target: target path relative to the root directory of the resource

        returns:
        -- None
        """
        if not os.path.exists(source):
            raise Exception(f"Could not find file: {f}")
        logger.info(f"+ adding: {source} -> {target}")
        self.hs.addResourceFile(resid, source, target)
        return resid

    def loadResourceFromLocal(self, resourceid):
        """Loads the contents of a previously downloaded resource.

         args:
         -- resourceid: the id of the resource that has been downloaded (str)

         returns:
         -- {content file name: path}
        """
        resdir = utilities.find_resource_directory(resourceid)
        if resdir is None:
            logger.error(f"Could not find any resource matching the id {resource}")
            return
        search_paths = [
         os.path.join(resdir, f"{resourceid}/data/contents/*"),
         os.path.join(resdir, 'data/contents/*')]
        content = {}
        found_content = False
        for p in search_paths:
            content_files = glob.glob(p)
            if len(content_files) > 0:
                found_content = True
                logger.info(f"Downloaded content is located at: {resdir}")
                logger.info(f"Found {len(content_files)} content file(s)")
            for f in content_files:
                fname = os.path.basename(f)
                content[fname] = f

        if len(content.keys()) == 0:
            logger.error('Did not find any content files for resource id: {resourceid}')
        self.content = content