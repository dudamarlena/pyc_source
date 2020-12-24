# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\packages\installer.py
# Compiled at: 2010-12-23 17:42:44
import os, sys

class PackageInstaller(object):
    """
    The PackageInstaller allows file system based registration of:
     * packages
     * resource types
     * schemas
     * stylesheets
     * aliases
     * indexes
      
    A package/resourcetype etc. is installed automatically when found the 
    first time, but not if an already existing package was updated to a new
    version. To find out about updated packages and resourcetypes use 
    the getUpdated() method.
    """

    @staticmethod
    def _install_package(env, p):
        if hasattr(p, 'version'):
            version = p.version
        else:
            version = ''
        env.registry.db_registerPackage(p.package_id, version)

    @staticmethod
    def _install_resourcetype(env, rt):
        if hasattr(rt, 'version'):
            version = rt.version
        else:
            version = ''
        if hasattr(rt, 'version_control'):
            version_control = rt.version_control
        else:
            version_control = False
        env.registry.db_registerResourceType(rt.package_id, rt.resourcetype_id, version, version_control)

    @staticmethod
    def _install_pre_registered(env, o):
        package_id = o.package_id
        resourcetype_id = None
        if hasattr(o, 'resourcetype_id'):
            resourcetype_id = o.resourcetype_id
        if hasattr(o, '_registry_schemas'):
            for entry in o._registry_schemas:
                type = entry['type']
                filename = entry['filename']
                name = filename.split(os.sep)[(-1)]
                if env.registry.schemas.get(package_id, resourcetype_id, type):
                    msg = 'Skipping Schema /%s/%s - %s'
                    msg = msg % (package_id, resourcetype_id, filename)
                    env.log.debug(msg)
                    continue
                msg = 'Registering Schema /%s/%s - %s ...'
                env.log.info(msg % (package_id, resourcetype_id, filename))
                try:
                    data = file(filename, 'r').read()
                    env.registry.schemas.register(package_id, resourcetype_id, type, data, name)
                except Exception as e:
                    env.log.warn(e)

        if hasattr(o, '_registry_stylesheets'):
            for entry in o._registry_stylesheets:
                type = entry['type']
                filename = entry['filename']
                name = filename.split(os.sep)[(-1)]
                if env.registry.stylesheets.get(package_id, resourcetype_id, type):
                    msg = 'Skipping Stylesheet /%s/%s - %s'
                    env.log.debug(msg % (package_id, resourcetype_id,
                     filename))
                    continue
                msg = 'Registering Stylesheet /%s/%s - %s ...'
                env.log.info(msg % (package_id, resourcetype_id, filename))
                try:
                    data = file(filename, 'r').read()
                    env.registry.stylesheets.register(package_id, resourcetype_id, type, data, name)
                except Exception as e:
                    env.log.warn(e)

        if hasattr(o, '_registry_aliases'):
            for entry in o._registry_aliases:
                if env.registry.aliases.get(**entry):
                    msg = 'Skipping Alias %s'
                    env.log.debug(msg % entry['uri'])
                    continue
                msg = 'Registering Alias %s ...'
                env.log.info(msg % entry['uri'])
                try:
                    env.registry.aliases.register(**entry)
                except Exception as e:
                    env.log.warn(e)

        if hasattr(o, '_registry_indexes') and resourcetype_id:
            for entry in o._registry_indexes:
                if env.catalog.getIndexes(package_id=package_id, resourcetype_id=resourcetype_id, **entry):
                    msg = 'Skipping XMLIndex /%s/%s - %s'
                    env.log.debug(msg % (package_id, resourcetype_id,
                     entry['xpath']))
                    continue
                msg = 'Registering XMLIndex /%s/%s - %s ...'
                env.log.info(msg % (package_id, resourcetype_id,
                 entry['xpath']))
                try:
                    env.catalog.registerIndex(package_id, resourcetype_id, **entry)
                except Exception as e:
                    env.log.warn(e)

        return

    @staticmethod
    def _pre_register--- This code section failed: ---

 L. 129         0  LOAD_FAST             0  'args'
                3  LOAD_CONST               0
                6  BINARY_SUBSCR    
                7  STORE_FAST            2  'reg'

 L. 131        10  LOAD_GLOBAL           0  'sys'
               13  LOAD_ATTR             1  '_getframe'
               16  LOAD_CONST               2
               19  CALL_FUNCTION_1       1  None
               22  STORE_FAST            3  'frame'

 L. 132        25  LOAD_FAST             3  'frame'
               28  LOAD_ATTR             2  'f_locals'
               31  STORE_FAST            4  'locals_'

 L. 134        34  LOAD_FAST             4  'locals_'
               37  LOAD_FAST             3  'frame'
               40  LOAD_ATTR             3  'f_globals'
               43  COMPARE_OP            9  is-not
               46  POP_JUMP_IF_FALSE    61  'to 61'
               49  LOAD_CONST               '__module__'
               52  LOAD_FAST             4  'locals_'
               55  COMPARE_OP            6  in
             58_0  COME_FROM            46  '46'
               58  POP_JUMP_IF_TRUE     70  'to 70'
               61  LOAD_ASSERT              AssertionError

 L. 135        64  LOAD_CONST               'registerStylesheet() can only be used in a class definition'
               67  RAISE_VARARGS_2       2  None

 L. 136        70  LOAD_FAST             4  'locals_'
               73  LOAD_ATTR             5  'get'
               76  LOAD_CONST               'package_id'
               79  LOAD_CONST               None
               82  CALL_FUNCTION_2       2  None
               85  STORE_FAST            5  'package_id'

 L. 137        88  LOAD_FAST             4  'locals_'
               91  LOAD_ATTR             5  'get'
               94  LOAD_CONST               'resourcetype_id'
               97  LOAD_CONST               None
              100  CALL_FUNCTION_2       2  None
              103  STORE_FAST            6  'resourcetype_id'

 L. 138       106  LOAD_FAST             5  'package_id'
              109  POP_JUMP_IF_TRUE    121  'to 121'
              112  LOAD_ASSERT              AssertionError
              115  LOAD_CONST               'class must provide package_id'
              118  RAISE_VARARGS_2       2  None

 L. 139       121  LOAD_FAST             2  'reg'
              124  LOAD_CONST               ('_schemas', '_indexes')
              127  COMPARE_OP            6  in
              130  POP_JUMP_IF_FALSE   151  'to 151'

 L. 140       133  LOAD_FAST             6  'resourcetype_id'
              136  POP_JUMP_IF_TRUE    151  'to 151'
              139  LOAD_ASSERT              AssertionError
              142  LOAD_CONST               'class must provide resourcetype_id'
              145  RAISE_VARARGS_2       2  None
              148  JUMP_FORWARD          0  'to 151'
            151_0  COME_FROM           148  '148'

 L. 142       151  LOAD_FAST             1  'kwargs'
              154  LOAD_ATTR             5  'get'
              157  LOAD_CONST               'filename'
              160  LOAD_CONST               None
              163  CALL_FUNCTION_2       2  None
              166  STORE_FAST            7  'filename'

 L. 143       169  LOAD_FAST             7  'filename'
              172  POP_JUMP_IF_FALSE   221  'to 221'

 L. 144       175  LOAD_GLOBAL           7  'os'
              178  LOAD_ATTR             8  'path'
              181  LOAD_ATTR             9  'join'
              184  LOAD_GLOBAL           7  'os'
              187  LOAD_ATTR             8  'path'
              190  LOAD_ATTR            10  'dirname'

 L. 145       193  LOAD_FAST             3  'frame'
              196  LOAD_ATTR            11  'f_code'
              199  LOAD_ATTR            12  'co_filename'
              202  CALL_FUNCTION_1       1  None
              205  LOAD_FAST             7  'filename'
              208  CALL_FUNCTION_2       2  None
              211  LOAD_FAST             1  'kwargs'
              214  LOAD_CONST               'filename'
              217  STORE_SUBSCR     
              218  JUMP_FORWARD          0  'to 221'
            221_0  COME_FROM           218  '218'

 L. 146       221  LOAD_FAST             4  'locals_'
              224  LOAD_ATTR            13  'setdefault'
              227  LOAD_CONST               '_registry'
              230  LOAD_FAST             2  'reg'
              233  BINARY_ADD       
              234  BUILD_LIST_0          0 
              237  CALL_FUNCTION_2       2  None
              240  LOAD_ATTR            14  'append'
              243  LOAD_FAST             1  'kwargs'
              246  CALL_FUNCTION_1       1  None
              249  POP_TOP          
              250  LOAD_CONST               None
              253  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 250

    @staticmethod
    def install(env, package_id=None):
        """
        Auto install all known packages.
        
        If package is given, only the specified package will be installed.
        """
        env.log.debug('Installing file system based Components ...')
        if package_id:
            packages = [
             package_id]
        else:
            packages = env.registry.getPackageIds()
            packages.remove('seishub')
            packages.insert(0, 'seishub')
        for p in packages:
            fs_package = env.registry.getPackage(p)
            db_packages = env.registry.db_getPackages(p)
            if len(db_packages) == 0:
                try:
                    PackageInstaller._install_package(env, fs_package)
                except Exception as e:
                    env.log.warn(("Registration of package with id '%s' " + 'failed. (%s)') % (p, e))
                    continue

            PackageInstaller._install_pre_registered(env, fs_package)
            for rt in env.registry.getResourceTypes(p):
                db_rt = env.registry.db_getResourceTypes(p, rt.resourcetype_id)
                if len(db_rt) == 0:
                    try:
                        PackageInstaller._install_resourcetype(env, rt)
                    except Exception as e:
                        env.log.warn(('Registration of resourcetype ' + "with id '%s' in package '%s'" + ' failed. (%s)') % (
                         rt.resourcetype_id, p, e))
                        continue

                PackageInstaller._install_pre_registered(env, rt)

        env.log.info('Components have been updated.')

    @staticmethod
    def cleanup(env):
        """
        Automatically remove unused packages.
        """
        pass


registerSchema = lambda filename, type: PackageInstaller._pre_register('_schemas', type=type, filename=filename)
registerStylesheet = lambda filename, type: PackageInstaller._pre_register('_stylesheets', type=type, filename=filename)
registerAlias = lambda uri, expr: PackageInstaller._pre_register('_aliases', uri=uri, expr=expr)
registerIndex = lambda label, xpath, type='text', options=None: PackageInstaller._pre_register('_indexes', label=label, xpath=xpath, type=type, options=options)