from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.sdist import sdist as _sdist

import sys
from os import path

from buildhelpers import rebuild_c_shaders

# always recreate the compiled in C shader files immediately
rebuild_c_shaders()

pyx_sources = [path.join(".", "cyrasterize", "glrasterizer.pyx")]
cythonized_sources = [path.join(".", "cyrasterize", "glrasterizer.cpp")]

# files to compile from glrasterizer
glrasterizer_sources = ["glrasterizer.cpp", "glr.cpp", "glrglfw.cpp"]
external_sources = [path.join(".", "cyrasterize", "cpp", s) for s in
                    glrasterizer_sources]


# kwargs to be provided to distutils
ext_kwargs = {
    'language': 'c++'
}

# unfortunately, linking requirements differ on OS X vs Linux
if sys.platform.startswith('linux'):
    ext_kwargs['libraries'] = ['m', 'GLEW', 'GL', 'GLU', 'glfw']
elif sys.platform == 'darwin':
    ext_kwargs['libraries'] = ['m', 'GLEW', 'glfw3']
    # TODO why does it compile without these on OS X?!
    #c_ext.extra_compile_args += ['-framework OpenGL',
    #                             '-framework Cocoa', '-framework IOKit',
    #                             '-framework CoreVideo']

ext_name = 'cyrasterize.glrasterizer'


# cythonize the .pyx file returning a suitable Extension
def ext_from_source():
    from Cython.Build import cythonize
    return cythonize([
        Extension(ext_name, pyx_sources + external_sources, **ext_kwargs)
    ])


# build an extension directly from the cythonized source - no need for Cython
def ext_from_cythonized():
    return [Extension(ext_name, cythonized_sources + external_sources,
                      **ext_kwargs)]


try:
    # If Cython is available, build the extension module from the Cython source
    extensions = ext_from_source()
except ImportError:
    # No Cython! Let's check if the cythonized file is already present
    # (NB: file is not in git but needs to be included in distributions)
    from os.path import exists
    if not all([exists(f) for f in cythonized_sources]):
        raise ImportError("Installing from source requires Cython")
    # good, we have the file. Just build a good old-fashioned extension
    extensions = ext_from_cythonized()

# either way, by now, extensions is correctly set.

# Subclass sdist to ensure Cython is run when a new distribution is built
class sdist(_sdist):

    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        ext_from_source()
        _sdist.run(self)

cmdclass = {'sdist': sdist}


# http://stackoverflow.com/a/21621689/2691632
# In the case where the user did not have NumPy, build_ext will be run and
# numpy will not yet be available. This class delays the use of NumPy until
# after installation of the setup_requires dependencies and ensures that NumPy
# thinks it is fully installed to allow us to proceed.
class build_ext(_build_ext):

    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process
        __builtins__.__NUMPY_SETUP__ = False
        print 'build_ext: including numpy files'
        import numpy
        self.include_dirs.append(numpy.get_include())

cmdclass['build_ext'] = build_ext


setup(name='cyrasterize',
      version='0.1.5',
      description='Simple fast OpenGL offscreen rasterizing in Python',
      author='James Booth',
      author_email='james.booth08@imperial.ac.uk',
      url='https://github.com/menpo/cyrasterize/',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: C',
          'Programming Language :: Cython',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
      ],
      ext_modules=extensions,
      packages=find_packages(),
      package_data={'cyrasterize': ['*.pyx', 'cpp/*.h', 'shaders/*.vert',
                                    'shaders/*.frag']},
      cmdclass=cmdclass,
      setup_requires=['numpy>=1.8.0'],
      install_requires=['numpy>=1.8.0']
      )
