from distutils.core import setup
import os,gdas.__init__
from glob import glob

#del os.link
setup(
    name="gdas",
    version=gdas.__version__,
    author="Vincent Dumont",
    author_email="vincentdumont11@gmail.com",
    packages=["gdas"],
    requires=["numpy","matplotlib","scipy","astropy","gwpy","pycbc"],
    scripts = glob('bin/*'),
    url="https://gnome.pages.gitlab.rlp.net/gdas/",
    description="GNOME Data Analysis Software"
)
