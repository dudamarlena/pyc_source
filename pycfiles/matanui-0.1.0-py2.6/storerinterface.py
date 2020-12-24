# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/matanui/storerinterface.py
# Compiled at: 2011-01-18 01:15:35
"""Interfaces to storer back-ends."""
__author__ = 'Guy K. Kloss <Guy.Kloss@aut.ac.nz>'
import re, json
from matanui import config
PRIV_READ = 4
PRIV_WRITE = 2
PRIV_READ_WRITE = PRIV_READ | PRIV_WRITE
WORLD_MASK = PRIV_READ_WRITE
GROUP_SHIFT = 3
GROUP_MASK = WORLD_MASK << GROUP_SHIFT
OWNER_SHIFT = 6
OWNER_MASK = WORLD_MASK << OWNER_SHIFT
PRIV_MAX = 438
PRIV_MASK = 511

class NullStorer(object):
    """
    Null pattern/default implementation of the data-related interface.
    """

    def __init__(self):
        """Constructor."""
        pass

    def get_content(self, filename=None, object_id=None):
        """ 
        Retrieves a file from the storage sub-system. The method requires a file
        name or an object ID to reference the resource.
        
        @param filename: Path/file name of the resource.
        @type filename: C{str}
        @param object_id: Object ID of the resource.
        @type object_id: C{str}
        
        @return: A content object.
        @rtype: L{ContentObject}
        
        @raise MataNuiStorerException: In case of errors from the storage
            sub-system.
        """
        return

    def put_content(self, content_object, query_metadata=None):
        """ 
        Stores a file in the storage sub-system.
        
        @param content_object: Content object for the file to put.
        @type content_object: L{matanui.storerinterface.ContentObject}
        @param query_metadata: Meta-data to be stored, passed along with file
            content object.
        @type query_metadata: C{dict}
        
        @return: Unique object ID of storage system.
        @rtype: C{str}
        
        @raise MataNuiStorerException: In case of errors from the storage
            sub-system.
        """
        return

    def delete_file(self, filename=None, object_id=None):
        """ 
        Deletes a file from the storage sub-system. The method requires a file
        name or an object ID to reference the resource.
        
        @param filename: Path/file name of the resource.
        @type filename: C{str}
        @param object_id: Object ID of the resource.
        @type object_id: C{str}
        
        @return: Object ID of the deleted file.
        @rtype: C{str}
        
        @raise MataNuiStorerException: In case of errors from the storage
            sub-system.
        """
        return

    def get_metadata(self, filename=None, object_id=None):
        """ 
        Retrieves a resource's meta-data from the storage sub-system. The method
        requires a file name or an object ID to reference the resource.
        
        @param filename: Path/file name of the resource.
        @type filename: C{str}
        @param object_id: Object ID of the resource.
        @type object_id: C{str}
        
        @return: Object ID and meta-data object.
        @rtype: C{tupel} of C{str} and L{MetadataObject}
        
        @raise MataNuiStorerException: In case of errors from the storage
            sub-system.
        """
        return

    def set_metadata(self, metadata, filename=None, object_id=None):
        """ 
        Sets a resource's meta-data from the storage sub-system. The method 
        requires a file name or an object ID to reference the resource.
        
        @param metadata: A meta-data object.
        @type metadata: L{MetadataObject}
        @param filename: Path/file name of the resource.
        @type filename: C{str}
        @param object_id: Object ID of the resource.
        @type object_id: C{str}
        
        @return: Object ID of updated resource.
        @rtype: C{str}
        
        @raise MataNuiStorerException: In case of errors from the storage
            sub-system.
        """
        return

    def list_resources(self, query):
        """ 
        Returns a list of resources in the style of a UN*X "ls" shell command
        satisfying the given query.
        
        @param query: Search query, may contain command line wild cards ("*"
            and "?").
        @type query: C{str}
        
        @return: List of resources' listed with meta-data.
        @rtype: L{matanui.storerinterface.MetadataObject}
        
        @raise MataNuiStorerException: In case of errors from the storage
            sub-system.
        """
        return

    def is_access_allowed(self, user, access_mode, filename=None, object_id=None, dir_mode=False):
        """
        Checks whether the requested access mode for a user on a resource in the
        storage system is given. The method requires a file name or an object ID
        to perform the check.
        
        @param user: User name.
        @type user: C{str}
        @param access_mode: UN*X style access mode indicator.
        @type access_mode: C{int}
        @param filename: Path/file name of the file.
        @type filename: C{str}
        @param object_id: Object ID of the resource.
        @type object_id: C{str}
        @param dir_mode: Are we interested in directory level access, e. g. for
            writing a file into the directory or listing it.
        @type dir_mode: C{bool}
        
        @return: C{True} if the desired access is allowed.
        @rtype: C{bool}
        
        @raise @raise matanui.exceptions.MataNuiStorerException: In case of a
            file name mismatch. 
        """
        return False

    def is_file(self, filename=None, object_id=None):
        """
        Checks whether the resource indicated is a file.
        
        @param filename: Path/file name of the resource.
        @type filename: C{str}
        @param object_id: Object ID of the resource.
        @type object_id: C{str}
        
        @return: C{True} if the resource is a file.
        @rtype: C{bool}
        
        @raise @raise matanui.exceptions.MataNuiStorerException: In case of a
            name mismatch. 
        """
        return False

    def is_directory(self, filename=None, object_id=None):
        """
        Checks whether the resource indicated is a directory.
        
        @param filename: Path/file name of the resource.
        @type filename: C{str}
        @param object_id: Object ID of the resource.
        @type object_id: C{str}
        
        @return: C{True} if the resource is a directory.
        @rtype: C{bool}
        
        @raise @raise matanui.exceptions.MataNuiStorerException: In case of a
            name mismatch. 
        """
        return False

    def exists(self, path):
        """
        Checks, whether an entry with the given path exists.
        
        @param path: Path of the resource to check.
        @type path: C{str}
        
        @return: True if it exists.
        @rtype: C{bool}
        """
        return False


class ContentObject(object):
    """
    Interface for passing file/content information back from the storage to
    the service layer.
    """
    data = None
    block_size = 8192
    length = 0
    checksum = ''
    content_type = ''
    last_modified = ''
    filename = ''
    object_id = ''
    metadata = None
    owner = None
    access_mode = config.DEFAULT_PERMISSIONS


class MetadataObject(object):
    """
    Interface for passing meta-data information back from the storage to
    the service layer.
    """
    content = None
    _default = None
    _object_hook = None

    def __init__(self, content=None):
        """
        Constructor.
        
        @param content: Content to initialise object with.
        """
        self.content = content

    @property
    def json_string(self):
        """Content representation in a JSON C{str}."""
        return json.dumps(self.content, default=self._default)

    @json_string.setter
    def json_string(self, a_string):
        self.content = json.loads(a_string, object_hook=self._object_hook)

    def get_json_stream(self, fp):
        """
        Serialisation of the content into a file-like object.
        
        @param fp: File like object (supporting the C{.write()} method(s).
        """
        return json.dump(self.content, fp, default=self._default)

    def set_from_json_stream(self, fp):
        """
        Deserialisation of a file-like object into the content.
        
        @param fp: File like object (supporting the C{.read()} method(s).
        """
        self.content = json.load(fp, object_hook=self._object_hook)


def filter_results(query, entries):
    """
    Filters all entries, and only returns the ones matching the query.
    
    @param query: Search query, may contain command line wild cards ("*"
        and "?").
    @type query: C{str}
    
    @return: List of resources remaining.
    @rtype: C{list} of C{str}
    """
    query_base = query.rsplit('/', 1)[0]
    index = len(query_base) + 1
    left_path_reduced = [ item for item in entries if item.startswith(query[:index])
                        ]
    path_reduced = list(set([ ('/').join([query_base, item[index:].split('/', 1)[0]]) for item in left_path_reduced if item[index:].split('/', 1)[0]
                            ]))
    re_query = shell_to_regex_query(query)
    result = [ item for item in path_reduced if re.search(re_query, item)
             ]
    return result


def shell_to_regex_query(query, close_query=True):
    """
    Convert a UN*X compatible shell query to a regex query.
    
    @param query: Shell like query string (as e. g. used for "ls" command).
    @type query: C{str}
    @param close_query: Shall the query be "closed" (finished with a "$" at the
        end), if appropriate for the query string? (default: True).
    @type close_query: C{bool}
    
    @return: Regular expression query.
    @rtype: C{str}
    """
    re_query = '^%s' % query
    re_query = re_query.replace('.', '\\.')
    re_query = re_query.replace('?', '.')
    re_query = re_query.replace('*', '.*?')
    if close_query and not (re_query.endswith('/') or re_query.endswith('*')):
        re_query = '%s$' % re_query
    return re_query