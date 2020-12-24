#!/usr/bin/env python


import sys
import os
import glob
from distutils import version

try:
  import DistUtilsExtra.auto
except ImportError:
  print >>sys.stderr, \
        "To build Boarded you need " \
        "https://launchpad.net/python-distutils-extra"
  sys.exit(1)


current_ver = version.StrictVersion(DistUtilsExtra.auto.__version__)
required_ver = version.StrictVersion("2.12")
assert current_ver >= required_ver, "needs DistUtilsExtra.auto >= 2.12"


def search_files(pattern):
  return [fn for fn in glob.iglob(pattern) if os.path.isfile(fn)]


DistUtilsExtra.auto.setup(
    name = "boarded",
    version = "0.1",
    author = "Robert Schindler",
    author_email = "r-schindler@users.sourceforge.net",
    url = "http://boarded.sourceforge.net",
    license = "GPL-3",
    description = "On-screen keyboard for X",

    packages = ["Boarded"],

    data_files = [
                  ("share/doc/boarded", search_files("docs/*")),
                  ("share/doc/boarded/examples", search_files("docs/examples/*")),
                  ("share/icons/hicolor/scalable/apps", search_files("icons/*")),
                 ],

    #scripts = ["bin/boarded"],
)

