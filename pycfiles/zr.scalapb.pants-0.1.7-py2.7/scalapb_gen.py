# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/trueaccord/pants/scalapb/tasks/scalapb_gen.py
# Compiled at: 2017-06-26 17:11:03
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
import os, subprocess
from collections import OrderedDict
from hashlib import sha1
from twitter.common.collections import OrderedSet
from pants.task.simple_codegen_task import SimpleCodegenTask
from pants.backend.jvm.targets.jar_library import JarLibrary
from pants.backend.jvm.targets.scala_library import ScalaLibrary
from pants.backend.jvm.tasks.jar_import_products import JarImportProducts
from pants.backend.jvm.tasks.nailgun_task import NailgunTask
from pants.base.build_environment import get_buildroot
from pants.base.exceptions import TaskError
from pants.build_graph.address import Address
from pants.fs.archive import ZIP
from trueaccord.pants.scalapb.targets.scalapb_library import ScalaPBLibrary

class ScalaPBGen(SimpleCodegenTask, NailgunTask):

    def __init__(self, *args, **kwargs):
        super(ScalaPBGen, self).__init__(*args, **kwargs)

    @classmethod
    def register_options(cls, register):
        super(ScalaPBGen, cls).register_options(register)
        register(b'--protoc-version', fingerprint=True, help=b'Set a specific protoc version to use.', default=b'330')
        cls.register_jvm_tool(register, b'scalapbc')

    @classmethod
    def product_types(cls):
        return [b'java', b'scala']

    def synthetic_target_type(self, target):
        return ScalaLibrary

    def is_gentarget(self, target):
        return isinstance(target, ScalaPBLibrary)

    def execute_codegen(self, target, target_workdir):
        sources = target.sources_relative_to_buildroot()
        source_roots = self._calculate_source_roots(target)
        source_roots.update(self._proto_path_imports([target]))
        scalapb_options = []
        if target.payload.java_conversions:
            scalapb_options.append(b'java_conversions')
        if target.payload.grpc:
            scalapb_options.append(b'grpc')
        if target.payload.flat_package:
            scalapb_options.append(b'flat_package')
        if target.payload.single_line_to_string:
            scalapb_options.append(b'single_line_to_string')
        gen_scala = (b'--scala_out={0}:{1}').format((b',').join(scalapb_options), target_workdir)
        args = [
         b'-v%s' % self.get_options().protoc_version, gen_scala]
        if target.payload.java_conversions:
            args.append((b'--java_out={0}').format(target_workdir))
        for source_root in source_roots:
            args.append((b'--proto_path={0}').format(source_root))

        classpath = self.tool_classpath(b'scalapbc')
        args.extend(sources)
        main = b'com.trueaccord.scalapb.ScalaPBC'
        result = self.runjava(classpath=classpath, main=main, args=args, workunit_name=b'scalapb-gen')
        if result != 0:
            raise TaskError((b'scalapb-gen ... exited non-zero ({})').format(result))

    def _calculate_source_roots(self, target):
        source_roots = OrderedSet()

        def add_to_source_roots(target):
            if self.is_gentarget(target):
                source_roots.add(target.source_root)

        self.context.build_graph.walk_transitive_dependency_graph([
         target.address], add_to_source_roots, postorder=True)
        return source_roots

    def _jars_to_directories(self, target):
        """Extracts and maps jars to directories containing their contents.

    :returns: a set of filepaths to directories containing the contents of jar.
    """
        files = set()
        jar_import_products = self.context.products.get_data(JarImportProducts)
        imports = jar_import_products.imports(target)
        for coordinate, jar in imports:
            files.add(self._extract_jar(coordinate, jar))

        return files

    def _extract_jar(self, coordinate, jar_path):
        """Extracts the jar to a subfolder of workdir/extracted and returns the path to it."""
        with open(jar_path, b'rb') as (f):
            outdir = os.path.join(self.workdir, b'extracted', sha1(f.read()).hexdigest())
        if not os.path.exists(outdir):
            ZIP.extract(jar_path, outdir)
            self.context.log.debug((b'Extracting jar {jar} at {jar_path}.').format(jar=coordinate, jar_path=jar_path))
        else:
            self.context.log.debug((b'Jar {jar} already extracted at {jar_path}.').format(jar=coordinate, jar_path=jar_path))
        return outdir

    def _proto_path_imports(self, proto_targets):
        for target in proto_targets:
            for path in self._jars_to_directories(target):
                yield os.path.relpath(path, get_buildroot)

    def _copy_target_attributes(self):
        """Propagate the provides attribute to the synthetic java_library() target for publishing."""
        return [b'provides']