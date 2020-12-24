from distutils.core import setup
import os

dependencies = []
classifiers  = [
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
    "Operating System :: POSIX"
]

setup(
    name="mathdocpy",
    version="0.0.1",
    description="A markdown extension for mathematical documents.",
    long_description="A markdown extension for mathematical documents.",
    author="Hara Yuki",
    author_email="youhui.dev@gmail.com",
    install_requires=dependencies,
    packages=["mathdocpy"]
)