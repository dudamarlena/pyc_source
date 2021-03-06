# Copyright 2015 Alex Orange
# 
# This file is part of PyLua.
# 
# PyLua is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyLua is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with PyLua.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup

setup(name="PyLua",
      version="0.1.1",
      description="A cffi based lua package.",
      packages=['lua'],
      author="Alex Orange",
      author_email="crazycasta@gmail.com",
      url="http://hg.crazycasta.net/PyLua/",
      license="AGPLv3",
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU Affero General Public License v3",
          "Programming Language :: Other Scripting Engines",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Software Development :: Interpreters",
      ],
      setup_requires=["cffi>=1.0.0", "setuptools_hg"],
      cffi_modules=["cffi/build_lua.py:ffi"],
      install_requires=["cffi>=1.0.0"],
      tests_require=["cffi>=1.0.0"],
      test_suite='test',
     )
