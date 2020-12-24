# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\user\tablefiles.py
# Compiled at: 2020-05-02 11:41:47
# Size of source mod 2**32: 8323 bytes
"""
filetables - support files endpoints
==============================================================
"""
from os.path import join, exists
from os import mkdir
from os import remove
from uuid import uuid4
from flask import g, current_app, request
from loutilities.user.model import Column, String, Interest
from sqlalchemy.ext.declarative import declared_attr
from .tables import DbCrudApiInterestsRolePermissions
from ..tables import CrudFiles
from loutilities.user.model import db

class ParameterError(Exception):
    pass


debug = False

class FieldUpload(CrudFiles):

    def __init__(self, **kwargs):
        args = dict(filesdirectory=None,
          localinterestmodel=None,
          filesmodel=None,
          fieldname=None)
        args.update(kwargs)
        (super().__init__)(**args)
        if not callable(self.filesdirectory):
            raise ParameterError('filesdirectory required, and must be function')
        if not self.localinterestmodel:
            if not self.filesmodel:
                raise ParameterError('localinterestmodel and filesmodel required')

    def upload(self):
        """
        process post for file upload

        :return: {
            'upload' : {'id': fid },
            'files' : {
                'data' : {
                    fid : {'filename': thisfile.filename}
                },
            },

            NOTE: 'field': fid needs to be added by class which inherits this class
        """
        if debug:
            print('FilesUpload.upload()')
        else:
            thisfile = request.files['upload']
            mimetype = thisfile.mimetype
            if thisfile.filename.split('.')[(-1)] == 'csv':
                mimetype = 'text/csv'
            fid, filepath = self.create_fidfile(g.interest, thisfile.filename, mimetype)
            thisfile.save(filepath)
            thisfile.seek(0)
            returndata = {'upload':{'id': fid}, 
             'files':{'data': {fid: {'filename': thisfile.filename}}}}
            if self.fieldname:
                if callable(self.fieldname):
                    returndata[self.fieldname()] = fid
                else:
                    returndata[self.self.fieldname] = fid
        return returndata

    def list(self):
        if debug:
            print('FieldUpload.list()')
        table = 'data'
        filelist = {table: {}}
        files = self.filesmodel.query.all()
        for file in files:
            filelist[table][file.fileid] = {'filename': file.filename}

        return filelist

    def create_fidfile(self, group, filename, mimetype, fid=None):
        """
        create directory structure for file group
        create a file in the database which has a fileid
        determine pathname for file

        NOTE: while directory structure is created here and filepath is determined, caller must save file

        :param group: files are grouped by "group", to allow separate permissions for separate groups
        :param filename: name of file
        :param mimetype: mimetype for file
        :param fid: optional file id, only used for initial data load
        :return: fid, filepath
        """
        mainfolder = self.filesdirectory()
        if not exists(mainfolder):
            mkdir(mainfolder, mode=504)
        groupfolder = join(mainfolder, group)
        if not exists(groupfolder):
            mkdir(groupfolder, mode=504)
        filename = filename
        if not fid:
            fid = uuid4().hex
        filepath = join(groupfolder, fid)
        interest = Interest.query.filter_by(interest=group).one()
        localinterest = self.localinterestmodel.query.filter_by(interest_id=(interest.id)).one()
        file = self.filesmodel(fileid=fid, filename=filename, interest=localinterest, mimetype=mimetype)
        db.session.add(file)
        db.session.commit()
        return (
         fid, filepath)


class FilesCrud(DbCrudApiInterestsRolePermissions):

    def __init__(self, **kwargs):
        if debug:
            current_app.logger.debug('FilesCrud.__init__()')
        args = dict(filesdirectory=None)
        args.update(kwargs)
        (super().__init__)(**args)
        if not callable(self.filesdirectory):
            raise ParameterError('filesdirectory required, and must be function')

    def deleterow(self, thisid):
        file = self.model.query.filter_by(id=thisid).one()
        fid = file.fileid
        localinterest = self.local_interest_model.query.filter_by(id=(file.interest_id)).one()
        interest = Interest.query.filter_by(id=(localinterest.interest_id)).one()
        groupdir = join(self.filesdirectory(), interest.interest)
        filepath = join(groupdir, fid)
        row = super(FilesCrud, self).deleterow(thisid)
        if exists(filepath):
            remove(filepath)
        return row


FILEID_LEN = 50
FILENAME_LEN = 256
MIMETYPE_LEN = 256

class FilesMixin(object):
    fileid = Column(String(FILEID_LEN))
    filename = Column(String(FILENAME_LEN))
    mimetype = Column(String(MIMETYPE_LEN))