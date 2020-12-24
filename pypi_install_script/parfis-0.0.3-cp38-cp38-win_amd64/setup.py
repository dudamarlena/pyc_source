import setuptools
from distutils.core import Extension

setuptools.setup(
    name="parfis",
    version="0.0.7",
    author="Ginko Balboa",
    author_email="ginkobalboa3@gmail.com",
    description="Dummy package for testing",
    packages=['parfis', 'parfis.helloworld'],
    ext_modules=[Extension(name='parfis.helloworld.cmodule',
                           sources=['./helloworld/cmodule/src/cmodule.cpp'],
                           include_dirs=['./helloworld/cmodule/src'],
                           define_macros=[('HELLOWORLD_LIBRARY', None)])],
    long_description_content_type="text/markdown",
    url="https://github.com/GinkoBalboa/parfis",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: C++"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires='>=3.7',
    zip_safe=False,
)