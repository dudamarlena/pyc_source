# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/setuptools/setuptools/command/build_clib.py
# Compiled at: 2020-04-16 14:32:33
# Size of source mod 2**32: 4415 bytes
import distutils.command.build_clib as orig
from distutils.errors import DistutilsSetupError
from distutils import log
from setuptools.dep_util import newer_pairwise_group

class build_clib(orig.build_clib):
    __doc__ = "\n    Override the default build_clib behaviour to do the following:\n\n    1. Implement a rudimentary timestamp-based dependency system\n       so 'compile()' doesn't run every time.\n    2. Add more keys to the 'build_info' dictionary:\n        * obj_deps - specify dependencies for each object compiled.\n                     this should be a dictionary mapping a key\n                     with the source filename to a list of\n                     dependencies. Use an empty string for global\n                     dependencies.\n        * cflags   - specify a list of additional flags to pass to\n                     the compiler.\n    "

    def build_libraries(self, libraries):
        for lib_name, build_info in libraries:
            sources = build_info.get('sources')
            if not sources is None:
                if not isinstance(sources, (list, tuple)):
                    raise DistutilsSetupError("in 'libraries' option (library '%s'), 'sources' must be present and must be a list of source filenames" % lib_name)
                sources = list(sources)
                log.info("building '%s' library", lib_name)
                obj_deps = build_info.get('obj_deps', dict())
                if not isinstance(obj_deps, dict):
                    raise DistutilsSetupError("in 'libraries' option (library '%s'), 'obj_deps' must be a dictionary of type 'source: list'" % lib_name)
                dependencies = []
                global_deps = obj_deps.get('', list())
                if not isinstance(global_deps, (list, tuple)):
                    raise DistutilsSetupError("in 'libraries' option (library '%s'), 'obj_deps' must be a dictionary of type 'source: list'" % lib_name)
                for source in sources:
                    src_deps = [
                     source]
                    src_deps.extend(global_deps)
                    extra_deps = obj_deps.get(source, list())
                    if not isinstance(extra_deps, (list, tuple)):
                        raise DistutilsSetupError("in 'libraries' option (library '%s'), 'obj_deps' must be a dictionary of type 'source: list'" % lib_name)
                    src_deps.extend(extra_deps)
                    dependencies.append(src_deps)

                expected_objects = self.compiler.object_filenames(sources,
                  output_dir=(self.build_temp))
                if newer_pairwise_group(dependencies, expected_objects) != ([], []):
                    macros = build_info.get('macros')
                    include_dirs = build_info.get('include_dirs')
                    cflags = build_info.get('cflags')
                    self.compiler.compile(sources,
                      output_dir=(self.build_temp),
                      macros=macros,
                      include_dirs=include_dirs,
                      extra_postargs=cflags,
                      debug=(self.debug))
                self.compiler.create_static_lib(expected_objects,
                  lib_name,
                  output_dir=(self.build_clib),
                  debug=(self.debug))