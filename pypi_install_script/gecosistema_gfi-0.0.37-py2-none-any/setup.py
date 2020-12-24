# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2016 Luzzi Valerio for Gecosistema S.r.l.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Name:         setup.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     22/08/2016
#-------------------------------------------------------------------------------

from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("gfi_core.pyx"),
    include_dirs=[numpy.get_include()]
)