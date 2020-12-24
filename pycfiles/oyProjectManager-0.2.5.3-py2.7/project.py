# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/models/project.py
# Compiled at: 2013-02-05 13:32:42
import os, re, jinja2
from sqlalchemy import Column, Integer, Boolean, String, Float, ForeignKey
from sqlalchemy.ext.declarative import synonym_for
from sqlalchemy.orm import reconstructor, relationship, validates
from oyProjectManager.db import Base
from oyProjectManager import db
from oyProjectManager.models.auth import Client
from oyProjectManager.models.repository import Repository
from oyProjectManager import utils
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Project(Base):
    """Manages project related data.
    
    The Project class is in the center of the Asset Management system.
    Everything starts with the Project instance.
    
    **Creating a Project**
    
    All Projects have their own folder structure in the repository. Creating a
    :class:`~oyProjectManager.models.project.Project` instance is not enough to
    physically create the project folder structure. To make it happen the
    :meth:`~oyProjectManager.models.project.Project.create` should be called to
    finish the creation process. This will both create the project folder and
    the general structure of the project and a ``.metadata.db`` file. Any
    Project, which has a ``.metadata.db`` file (thus a folder with a name of
    ``Project.name``) considered an existing Project and ``Project.exists``
    returns ``True``.
    
    A Project can not be created without a `name` or with a name which is None
    or with an invalid name. For example, a project with name "'^+'^" can not
    be created because the name will become an empty string after the name
    validation process.
    
    The name of the project can freely be changed, but the path of the project
    will not change after the name of the project is changed.
    
    :param name: The name of the project. Should be a string or unicode. Name
      can not be None, a TypeError will be raised when it is given as None,
      can not be an empty string, a ValueError will be raised when it is an
      empty string.
      
      The given project name is validated against the following rules:
      
        * The name can only have a-z, A-Z, 0-9, "_" and "-" characters, all the
          other characters will be filtered out.
        * The name can start with literals, numbers and underscore character.
          No spaces, or any other characters are allowed at the beginning.
    
    :param code: The code of the project. Should be a string or unicode. If
      given as None it will be generated from the
      :attr:`~oyProjectManager.models.project.Project.name` attribute. If it an
      empty string or become an empty string after validation a ValueError will
      be raised.
      
        * The code can only have a-z, A-Z, 0-9, "_" and "-" characters, all the
          other characters will be filtered out.
        * The code can start with literals, numbers and underscore character.
          No spaces, or any other characters are allowed at the beginning.
        
      The :attr:`~oyProjectManager.models.project.Project.code` is a read only
      attribute.
    
    :param int fps: The frame rate in frame per second format. It is an 
      integer. The default value is 25. It can be skipped. If set to None. 
      The default value will be used.
    """
    __tablename__ = 'Projects'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=True)
    name = Column(String(256), unique=True)
    _code = Column(String(256), unique=True)
    description = Column(String)
    shot_number_prefix = Column(String(16))
    shot_number_padding = Column(Integer)
    rev_number_prefix = Column(String(16))
    rev_number_padding = Column(Integer)
    ver_number_prefix = Column(String(16))
    ver_number_padding = Column(Integer)
    fps = Column(Integer, doc='The frames per second setting of this project. The default value\n        is 25   \n        ')
    width = Column(Integer)
    height = Column(Integer)
    pixel_aspect = Column(Float)
    structure = Column(String)
    sequences = relationship('Sequence', primaryjoin='Sequences.c.project_id==Projects.c.id', cascade='all, delete-orphan')
    client_id = Column(Integer, ForeignKey('Clients.id'))
    client = relationship('Client', primaryjoin='Projects.c.client_id==Clients.c.id')

    def __new__(cls, name=None, code=None, client=None):
        """the overridden __new__ method to manage the creation of a Project
        instances.
        
        If the Project is created before then calling Project() for a second
        time, may be in another Python session will return the Project instance
        from the database.
        """
        if name:
            name = Project._condition_name(name)
            if db.session is None:
                logger.debug('db.session is None, setting up a new session')
                db.setup()
            proj_db = Project.query().filter_by(name=name).first()
            if proj_db is not None:
                logger.debug('found the project in the database')
                logger.debug('returning the Project instance from the database')
                proj_db.__skip_init__ = None
                from oyProjectManager import conf
                proj_db.conf = conf
                return proj_db
            logger.debug("Project doesn't exists")
        logger.debug('returning a normal Project instance')
        return super(Project, cls).__new__(cls, name, code, client)

    def __init__(self, name, code=None, client=None):
        if hasattr(self, '__skip_init__'):
            logging.debug('skipping the __init__ on Project')
            return
        else:
            logger.debug('initializing the Project')
            from oyProjectManager import conf
            self.conf = conf
            self.repository = Repository()
            self.name = name
            if code is None:
                code = self.name
            self._code = self._condition_code(code)
            self.shot_number_prefix = self.conf.shot_number_prefix
            self.shot_number_padding = self.conf.shot_number_padding
            self.rev_number_prefix = self.conf.rev_number_prefix
            self.rev_number_padding = self.conf.rev_number_padding
            self.ver_number_prefix = self.conf.ver_number_prefix
            self.ver_number_padding = self.conf.ver_number_padding
            default_resolution_key = conf.default_resolution_preset
            default_resolution = conf.resolution_presets[default_resolution_key]
            self.fps = self.conf.default_fps
            self.width = default_resolution[0]
            self.height = default_resolution[1]
            self.pixel_aspect = default_resolution[2]
            self.structure = self.conf.project_structure
            self.client = client
            return

    @reconstructor
    def __init_on_load__(self):
        """init when loaded from the db
        """
        self.repository = Repository()
        from oyProjectManager import conf
        self.conf = conf
        self._sequenceList = []
        self._exists = None
        return

    def __str__(self):
        """the string representation of the project
        """
        return self.name

    def __eq__(self, other):
        """equality of two projects
        """
        return isinstance(other, Project) and self.name == other.name

    @classmethod
    def _condition_name(cls, name):
        if name is None:
            raise TypeError('The Project.name can not be None')
        if not isinstance(name, (str, unicode)):
            raise TypeError('Project.name should be an instance of string or unicode not %s' % type(name))
        if name is '':
            raise ValueError('The Project.name can not be an empty string')
        name = name.strip()
        name = re.sub('([^a-zA-Z0-9\\s_\\-]+)', '', name)
        name = re.sub('(^[^a-zA-Z0-9_]+)', '', name)
        if name is '':
            raise ValueError('The Project.name is not valid after validation')
        return name

    @classmethod
    def _condition_code(cls, code):
        if code is None:
            raise TypeError('The %s.code can not be None' % cls.__name__)
        if not isinstance(code, (str, unicode)):
            raise TypeError('%s.code should be an instance of string or unicode not %s' % (
             cls.__name__, type(code)))
        if code is '':
            raise ValueError('The %s.code can not be an empty string' % cls.__name__)
        code = code.strip()
        code = re.sub('([^a-zA-Z0-9\\s_\\-]+)', '', code)
        code = re.sub('(^[^a-zA-Z0-9_]+)', '', code)
        code = re.sub('([\\s])+', '_', code)
        if code is '':
            raise ValueError('The Project.code is not valid after validation')
        return code

    @validates('name')
    def _validate_name(self, key, name_in):
        """validates the given name_in value
        """
        name_in = self._condition_name(name_in)
        return name_in

    def _validate_code(self, code):
        """validates the given code_in value
        """
        if code is None:
            code = self.name
        if not isinstance(code, (str, unicode)):
            raise TypeError('Project.code should be an instance of string or unicode not %s' % type(code))
        if code is '':
            raise ValueError('Project.code can not be an empty string')
        code = self._condition_code(code)
        if code is '':
            raise ValueError('Project.code is not valid after validation')
        return code

    def save(self):
        """Saves the Project related information to the database.
        
        If there is no ``.metadata.db`` file it will be created, but be
        careful that the project structure will not be created. The safest way
        to both create the project structure and the .metadata.db file is to
        call the :meth:`~oyProjectManager.models.project.Project.create`
        method.
        """
        logger.debug('saving project settings to %s' % db.database_url)
        if db.session is None:
            logger.debug('there is no session, creating a new one')
            db.setup()
        if self not in db.session:
            db.session.add(self)
        db.session.commit()
        return

    def create(self):
        """Creates the project directory structure and saves the project, thus
        creates the ``.metadata.db`` file in the repository.
        """
        utils.mkdir(self.full_path)
        rendered_structure = jinja2.Template(self.structure).render(project=self)
        folders = rendered_structure.split('\n')
        if len(folders):
            for folder in rendered_structure.split('\n'):
                try:
                    utils.createFolder(folder.strip())
                except OSError:
                    pass

        self._exists = True
        self.save()

    @property
    def path(self):
        """The path of this project instance. Basically it is the same value
        with what $REPO env variable holds
        """
        return self.repository.server_path

    @property
    def full_path(self):
        """The full_path of this project instance.
        """
        return os.path.join(self.path, self.code)

    @synonym_for('_code')
    @property
    def code(self):
        """Returns the code of this Project instance.
        
        The ``code`` attribute is read-only.
        
        :return: str
        """
        return self._code

    @validates('client')
    def _validate_client(self, key, client):
        """validates the given client value
        """
        if client is not None:
            if not isinstance(client, Client):
                raise TypeError('Project.client should be an oyProjectManager.models.auth.Client instance, not %s' % client.__class__.__name__)
        return client

    @property
    def assets(self):
        r"""Returns all the :class:`~oyProjectManager.models.asset.Asset`\ s related to this Project.
        :return: list of :class:`~oyProjectManager.models.asset.Asset`
        """
        from oyProjectManager import Asset
        return Asset.query().filter(Asset.project == self).all()