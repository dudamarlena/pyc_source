#!/usr/bin/python -u
"""
Setup script for PLIB.GUI package
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information
"""

from plib.gui import __version__ as version

name = "plib.gui"
description = "A simple Python GUI framework."

author = "Peter A. Donis"
author_email = "peterdonis@alum.mit.edu"

startline = 5
endspec = "The Zen of PLIB"

dev_status = "Beta"

license = "GPLv2"

data_dirs = ["examples"]

classifiers = """
Environment :: Console
Environment :: MacOS X
Environment :: Win32 (MS Windows)
Environment :: X11 Applications :: GTK
Environment :: X11 Applications :: KDE
Environment :: X11 Applications :: Qt
Intended Audience :: Developers
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: POSIX :: Linux
Programming Language :: Python :: 2.7
Topic :: Software Development :: Libraries :: Python Modules
"""

install_requires = """
plib.stdlib (>=0.9.24)
"""

post_install = ["plib-setup-{}".format(s) for s in ("gui-examples", "gui")]

rst_header_template = """**{basename}** for {name} {version}

:Author:        {author}
:Release Date:  {releasedate}
"""


if __name__ == '__main__':
    import sys
    import os
    from subprocess import call
    from distutils.core import setup
    from setuputils import convert_rst, current_date, setup_vars, long_description as make_long_description
    
    if "sdist" in sys.argv:
        convert_rst(rst_header_template,
            startline=2,
            name=name.upper(),
            version=version,
            author=author,
            releasedate=current_date("%d %b %Y")
        )
        call(['sed', '-i', 's/gitlab.com\/pdonis\/plib-/pypi.python.org\/pypi\/plib./', 'README'])
        call(['sed', '-i', 's/gitlab.com\/pdonis\/plib3-/pypi.python.org\/pypi\/plib3./', 'README'])
        call(['sed', '-i', 's/gitlab.com\/pdonis/pypi.python.org\/pypi/', 'README'])
    elif os.path.isfile("README.rst"):
        startline = 3
        long_description = make_long_description(globals(), filename="README.rst")
    setup(**setup_vars(globals()))
    if "install" in sys.argv:
        for scriptname in post_install:
            os.system(scriptname)
