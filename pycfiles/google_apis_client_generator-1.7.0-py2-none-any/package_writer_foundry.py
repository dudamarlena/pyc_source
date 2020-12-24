# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/filesys/package_writer_foundry.py
# Compiled at: 2019-01-24 16:56:47
"""Foundary for getting a package writer."""
from googleapis.codegen.filesys import filesystem_library_package
from googleapis.codegen.filesys import single_file_library_package
from googleapis.codegen.filesys import tar_library_package
from googleapis.codegen.filesys import zip_library_package

def GetPackageWriter(output_dir=None, output_file=None, output_format='zip'):
    """Get an output writer for a package."""
    if not (output_dir or output_file):
        raise ValueError('GetPackageWriter requires either output_dir or output_file')
    if output_dir and output_file:
        raise ValueError('GetPackageWriter requires only one of output_dir or output_file')
    if output_dir:
        package_writer = filesystem_library_package.FilesystemLibraryPackage(output_dir)
    else:
        out = open(output_file, 'w')
        if output_format == 'tgz':
            package_writer = tar_library_package.TarLibraryPackage(out)
        elif output_format == 'tar':
            package_writer = tar_library_package.TarLibraryPackage(out, compress=False)
        elif output_format == 'txt':
            package_writer = single_file_library_package.SingleFileLibraryPackage(out)
        else:
            package_writer = zip_library_package.ZipLibraryPackage(out)
    return package_writer