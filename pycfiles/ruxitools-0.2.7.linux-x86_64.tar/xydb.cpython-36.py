# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lewis/anaconda3/envs/py36/lib/python3.6/site-packages/ruxitools/xydb.py
# Compiled at: 2016-11-07 16:54:13
# Size of source mod 2**32: 5232 bytes
__author__ = 'github.com/ruxi'
__copyright__ = 'Copyright 2016, ruxitools'
__email__ = 'ruxi.github@gmail.com'
__license__ = 'MIT'
__status__ = 'Development'
__version__ = '0.1'
from collections import namedtuple

class XyDB(object):
    __doc__ = 'XyDB is a database-like containers for intermediate data\n\n     The intended usecase of XyDB is to store intermediate data in a database-like\n     container and bind it as an attribute to the source data. It solves the\n     problem of namespace pollution by confining intermediate data forms to\n     the original dataset in a logical and structured manner. The limitation\n     of this object is that it exists in memory only. For more persistent storage\n     solutions, its recommended to use an actual database library such as\n     blaze, mongoDB, or SQLite. Conversely, the advantage is residual information\n     is not left over after a session. \n     \n    \n     Example:\n        Defined a namedtuple for input validation, then assign this function \n        as an attribute of your source data object, usually a pandas dataframe.\n        \n          import XyDB\n          from collections import namedtuple\n          \n          # define input validation schema\n          input_val = namedtuple("data", [\'key\',\'desc\', \'X\', \'y\'])\n\n          # define data\n          myData = pd.DataFrame()\n          \n          # assign class function\n          myData.Xy = XyDB(input_val, verbose = True)  \n          \n          # add data to DB\n          myRecord = dict(key=\'config1\'\n                          , desc=\'dummydata\'\n                          , X=[0,1,0]\n                          , y=[\'a\',\'b\',\'a])\n          myData.Xy.push(**myRecord)\n          \n          # show data\n          myData.Xy.config1.desc       \n\n    '

    def __init__(self, schema=None, verbose=True, welcome=True):
        """
        Arguments:
            schema (default: None | NamedTuple):
                 
                Accepts a NamedTuple subclass with a "key" field
                which is used for input validation when records
                are "push"ed 
            

            verbose (default: True | boolean)
                
                If false, suppresses print commands. Including this message
                
            welcome (default: True | boolean)
            
                Suppresses printing of the docstring upon initialization
        """
        self._db = {}
        self._show = lambda : None
        self._pull = lambda : None
        self._verbose = verbose
        if welcome:
            print(self.__doc__)
        self._schema = False if schema is None else schema
        if self._schema:
            if 'key' not in dir(self._schema):
                raise Exception("namedtuple must have 'key' as a field")

    def push(self, key, *args, **kwargs):
        """Adds records (dict) to database"""
        if not type(key) == str:
            raise Exception('key must be string')
        else:
            if self._schema:
                self._input_validator = self._schema
                record = (self._input_validator)(key, *args, **kwargs)
            else:
                entry_dict = dict(args, key=key, **kwargs)
                self._input_validator = namedtuple('Data', list(entry_dict.keys()))
                record = (self._input_validator)(**entry_dict)
        self._db[record.key] = record
        if self._verbose:
            print('Record added {}'.format(record.key))
        self._update()

    def _update(self):
        """updates dyanamic attribute access for self.show & self.pull"""
        for key in self.keys:
            setattr(self._show, key, self._db[key])
            setattr(self._pull, key, self.db[key]._asdict())

    @property
    def db(self):
        """Intermediate data accessible by keyword. Returns a dict"""
        return self._db

    @property
    def keys(self):
        """
        list configuration keywords
        
        Returns:
            list
        """
        return self.db.keys()

    @property
    def show(self):
        """
        Show record from database. Accessible by attribute via keyname
        
        Returns:
            namedtuple objects  
        Usage: 
            show.<config keyword>.<attribute name>          
        """
        return self._show

    @property
    def pull(self):
        """
        Pull record from database. Accessible by attribute via keyname
           
        Returns:
            dictionary 
        Usage: 
            pull.<config keyword>
        """
        return self._pull