from distutils.core import setup
import os
from glob import glob

#del os.link
setup(
    name="gdas",
    version="1.0.2",
    author="Vincent Dumont",
    author_email="vincentdumont11@gmail.com",
    packages=["gdas"],
    scripts = glob('bin/*'),
    url="https://gnome.pages.gitlab.rlp.net/gdas/",
    description="GNOME Data Analysis Software",
    install_requires=["astropy","gwpy","numpy","matplotlib","pycbc","scipy"],
)
