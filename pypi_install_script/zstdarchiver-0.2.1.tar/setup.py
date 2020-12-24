"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/brmmm3/zstdarchiver
"""

import os
import sys
# To use a consistent encoding
from codecs import open
try:
    from setuptools import setup, find_packages
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

PKGNAME = 'zstdarchiver'
PKGVERSION = '0.2.1'
BASEDIR = os.path.dirname(__file__)
PKGDIR = PKGNAME if not BASEDIR else os.path.join(BASEDIR, PKGNAME)
PKGPATH = PKGDIR + "/" + PKGNAME

for filename in os.listdir(PKGDIR):
    for ext in (".cpp", ".c", ".pyx", ".html"):
        if filename.endswith(ext) and os.path.exists(PKGDIR + "/" + filename):
            os.remove(PKGDIR + "/" + filename)

# Get the long description from the README file
with open(os.path.join(BASEDIR, 'README.rst'), encoding='utf-8') as F:
    long_description = F.read()

bAnnotate = "annotate" in sys.argv
bDebug = "debug" in sys.argv
if bDebug:
    sys.argv.remove("debug")
bCythonize = "cython" in sys.argv
if bCythonize:
    sys.argv.remove("cython")

if bCythonize or bAnnotate:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    import Cython.Compiler.Version

    from pyorcy import extract_cython

    # noinspection PyPep8Naming
    class build_ext_subclass(build_ext):

        def run(self):
            build_ext.run(self)

        def build_extensions(self):
            if self.compiler.compiler_type == "msvc":
                for extension in self.extensions:
                    if bDebug:
                        extension.extra_compile_args = ["/Od", "/EHsc", "-Zi", "/D__PYX_FORCE_INIT_THREADS=1"]
                        extension.extra_link_args = ["-debug"]
                    else:
                        extension.extra_compile_args = ["/O2", "/EHsc", "/D__PYX_FORCE_INIT_THREADS=1"]
            else:
                for extension in self.extensions:
                    if bDebug:
                        extension.extra_compile_args = ["-O0", "-g", "-ggdb", "-D__PYX_FORCE_INIT_THREADS=1"]
                        extension.extra_link_args = ["-g"]
                    else:
                        extension.extra_compile_args = ["-O2", "-D__PYX_FORCE_INIT_THREADS=1"]
            build_ext.build_extensions(self)


    if bCythonize:
        print("Building with Cython " + Cython.Compiler.Version.version)
    else:
        print(f"Creating {PKGNAME}.html")
    extract_cython(PKGPATH + ".py")
    MODULES = [PKGDIR + "/" + filename[:-4] for filename in os.listdir(PKGDIR)
               if filename.endswith('.pyx')]
    cythonize(PKGDIR + "/*.pyx", language_level=3, annotate=bAnnotate,
              exclude=["setup.py"])

    if bAnnotate:
        sys.exit(0)

    ext_modules = [
        Extension(PKGNAME,
                  sources=[PKGPATH + ".pyx"],
                  language="c++")
        ]
    cmdclass = {'build_ext': build_ext_subclass}
    install_requires = ['Cython', 'fastthreadpool', 'msgpack', 'zstandard', 'cryptography']
    packages = None
else:
    from setuptools import setup, find_packages

    ext_modules = None
    cmdclass = {}
    install_requires = ['fastthreadpool', 'msgpack', 'zstandard', 'cryptography']
    packages = find_packages()


setup(
    name=PKGNAME,
    version=PKGVERSION,
    description='The Z-Archiver. A fast archiving module.',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    url='https://github.com/brmmm3/' + PKGNAME,
    download_url='https://github.com/brmmm3/%s/releases/download/%s/%s-%s.tar.gz' % (PKGNAME, PKGVERSION, PKGNAME, PKGVERSION),

    author='Martin Bammer',
    author_email='mrbm74@gmail.com',
    license='MIT',

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3.7',
    ],

    keywords='zip archiving',
    include_package_data=True,
    cmdclass=cmdclass,
    install_requires=install_requires,
    ext_modules=ext_modules,
    packages=packages
)
