# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/utils.py
# Compiled at: 2008-10-23 05:55:17
"""
$Id: utils.py 72131 2008-09-18 17:49:28Z glenfant $
"""
__author__ = ''
__docformat__ = 'restructuredtext'
import os, types
from AccessControl import ModuleSecurityInfo
from zope.i18nmessageid import MessageFactory
from Products.Archetypes.Field import ImageField
import config

def getFieldValue(self, name):
    """Returns field value of an object

    @param name: Name of the field
    """
    field = self.getField(name)
    if not field:
        found = False
        fields = [ x for x in self.Schema().fields() if isinstance(x, ImageField) ]
        for field in fields:
            field_name = field.getName()
            names = [ '%s_%s' % (field_name, x) for x in field.getAvailableSizes(self).keys() ]
            if name in names:
                obj = field.getStorage(self).get(name, self)
                found = True
                break

        if not found:
            raise AttributeError(name)
        return obj.__of__(self)
    accessor = field.getAccessor(self)
    if accessor is None:
        return
    return accessor()


FSSMessageFactory = MessageFactory(config.I18N_DOMAIN)
ModuleSecurityInfo('iw.fss.utils').declarePublic('FSSMessageFactory')

def rm_file(path):
    """
    Delete file from a path
    """
    os.remove(path)


def move_file(infile, outfile):
    """
    Move file to another place
    """
    if infile == outfile:
        return
    if os.path.exists(outfile) and infile != outfile:
        os.remove(outfile)
    os.rename(infile, outfile)


def copy_file(infile, outfile):
    """

    Read binary data from infile and write it to outfile. infile and
    outfile my be strings, in which case a file with that name is
    opened, or filehandles, in which case they are accessed directly.

    """
    if type(infile) is types.StringType:
        instream = open(infile, 'rb')
        close_in = 1
    else:
        close_in = 0
        instream = infile
    if type(outfile) is types.StringType:
        outstream = open(outfile, 'wb')
        close_out = 1
    else:
        close_out = 0
        outstream = outfile
    try:
        blocksize = 2 << 16
        block = instream.read(blocksize)
        outstream.write(block)
        while len(block) == blocksize:
            block = instream.read(blocksize)
            outstream.write(block)

        instream.seek(0)
    finally:
        if close_in:
            instream.close()
        if close_out:
            outstream.close()


def create_file(contents_file, target_filepath):
    """
    Creates a physical file on the filesystem at target_filepath.  If
    contents_file is not None, it points to a file whose contents will
    be copied into the target file.  Otherwise, a zero length file
    will be created.  This method will raise an exception if there are
    any problems writing to the target file (or reading
    contents_file).
    """
    if contents_file:
        copy_file(contents_file, target_filepath)
    else:
        touchfile = open(target_filepath, 'wb')
        touchfile.close()


from zope.app.component.hooks import getSite

class NotInstalledComponent(LookupError):
    __module__ = __name__

    def __init__(self, cpt_name):
        self.cpt_name = cpt_name

    def __str__(self):
        msg = "Component '%s' is not installed in this site. You can't run its upgrade steps." % self.cpt_name
        return msg


class IfInstalled(object):
    __module__ = __name__

    def __init__(self, prod_name=config.PROJECTNAME):
        """@param prod_name: as shown in quick installer"""
        self.prod_name = prod_name

    def __call__(self, func):
        """@param func: the decorated function"""

        def wrapper(setuptool):
            qi = getSite().portal_quickinstaller
            installed_ids = [ p['id'] for p in qi.listInstalledProducts() ]
            if self.prod_name not in installed_ids:
                raise NotInstalledComponent(self.prod_name)
            return func(setuptool)

        wrapper.__name__ = func.__name__
        wrapper.__dict__.update(func.__dict__)
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        return wrapper