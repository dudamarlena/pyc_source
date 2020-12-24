from distutils.core import setup
from glob import glob

setup(
    name="mldas",
    version="0.6.5",
    author="Vincent Dumont",
    author_email="vincentdumont11@gmail.com",
    packages=["mldas"],
    url="https://ml4science.gitlab.io/mldas",
    description="Machine learning analysis tools for Distributed Acoustic Sensing data.",
    install_requires=["h5py","numpy","torch"]
)
