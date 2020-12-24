#! /usr/bin/python
# -*- coding: future_fstrings -*-

import os
import pkg_resources
import re
from setuptools import setup, find_packages
from setuptools.command.install import install
import site
import sys

VERSION_PATTERN = r'\d+\.\d+[abc]?'
VERSION_REGEX = re.compile(VERSION_PATTERN)

class EnsureBpy(install):
    """
    Ensures that the bpy installation is correct

    Validates the version directory is relative to the scripts directory
    """

    def run(self):
        """
        Ensures the installation of bpy is correct, if bpy is installed

        Searches in the current environment for an installation of the bpy 
        module, if it exists, make sure that the version folder exists sibling 
        to the calling executable. If not, search the python environment's 
        scripts directory for a folder named like a Blender version; if it 
        exists and is a directory, create a symlink from that folder into the 
        sys.executable's parent directory.
        """

        try:

            pkg_resources.get_distribution('bpy')

        except pkg_resources.DistributionNotFound:

            self.announce("Module bpy must be installed prior to running "
                          "ensure_bpy")

        else:

            try:

                import bpy
        
            except ImportError:

                self.announce(f"Version directory must be moved")

                moved = False

                scripts_dir = os.path.join(site.getsitepackages()[0],
                                       '..', '..', 'Scripts')

                for directory_path, sub_directories, files in os.walk(scripts_dir):

                    directory_name = os.path.basename(directory_path)

                    if VERSION_REGEX.match(directory_name):

                        correct_path = os.path.join(os.path.dirname(sys.executable), 
                                                    directory_name)

                        if not os.path.exists(correct_path):

                            os.symlink(directory_path, correct_path)

                            moved = True

                        else:

                            if not os.path.isdir(correct_path):

                                self.warn(f"Cannot create the symlink; "
                                          f"{correct_path} is a file. "
                                          f"Please remove and try again")

                            else:

                                self.warn(f"Weirdly, {correct_path} already "
                                          f"exists as a directory; there may "
                                          f"be something wrong with your "
                                          f"installation")

                        try:

                            import bpy

                        except ImportError:

                            self.warn("For some reason it still doesn't work...")

                        else:

                            self.announce("Successfully imported bpy")

                        break

                if not moved:

                    self.warn("Could not find the Blender version directory")

            else:

                self.announce("Succesfully imported bpy, no need to move the "
                              "version directory")

        super().run()

setup(name='bpy-ensure',
      version='0.0.0.a0',
      packages=find_packages(),
      py_modules=['ensure_bpy'],
      description='Ensures bpy is installed correctly',
      long_description=open("./README.md", 'r').read(),
      long_description_content_type="text/markdown",
      keywords="Blender, 3D, Animation, Renderer, Rendering",
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Win32 (MS Windows)",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License v3 "
                   "(GPLv3)",
                   "Natural Language :: English",
                   "Operating System :: Microsoft :: Windows :: Windows 10",
                   "Programming Language :: C",
                   "Programming Language :: C++",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: Implementation :: "
                   "CPython",
                   "Topic :: Artistic Software",
                   "Topic :: Education",
                   "Topic :: Multimedia",
                   "Topic :: Multimedia :: Graphics",
                   "Topic :: Multimedia :: Graphics :: 3D Modeling",
                   "Topic :: Multimedia :: Graphics :: 3D Rendering",
                   "Topic :: Games/Entertainment"],
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      python_requires=">=3.4.0,<3.7.0",
      url="https://github.com/TylerGubala/bpy-ensure",
      cmdclass={'install': EnsureBpy},
      entry_points={'console_scripts':['ensure_bpy=ensure_bpy:run']})
