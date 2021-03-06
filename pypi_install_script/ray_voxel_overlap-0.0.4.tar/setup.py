import setuptools
import numpy
import os

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='ray_voxel_overlap',
    version="0.0.4",
    author='Sebastian Achim Mueller',
    author_email='sebastian-achim.mueller@mpi-hd.mpg.de',
    description='Estimate the tomographic system-matrix for rays in voxels.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cherenkov-plenoscope/ray_voxel_overlap',
    packages=[
        'ray_voxel_overlap'
    ],
    install_requires=[
        'setuptools>=18.0',
        'cython',
        'scipy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires='>=3',
    ext_modules=[
        setuptools.Extension(
            "ray_voxel_overlap._cython_overlap",
            sources=[
                os.path.join(
                    'ray_voxel_overlap', '_cython_overlap_implementation.pyx'),
                os.path.join(
                    'ray_voxel_overlap', '_c_overlap_implementation.c'),
            ],
            include_dirs=[numpy.get_include(), "ray_voxel_overlap"],
            language="c",
        ),
    ],
)
