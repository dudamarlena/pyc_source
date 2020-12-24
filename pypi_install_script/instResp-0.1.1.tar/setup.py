from setuptools import setup

version = "0.1.1"

requirements=[
    'numpy',
    'matplotlib',
]

setup(
    name='instResp',
    version=version,
    description=('MTH: seismic/acoustic instrument response lib'),
    long_description=open('README.txt').read(),
    author='MTH',
    author_email='m.hagerty@isti.com',
    packages=[
        'instResp',
    ],
    #package_dir={'mth_lib': 'lib'},
    #entry_points=ENTRY_POINTS,
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    data_files = [("", ["LICENSE.txt", "README.md"] )],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=(
        'microquake, seismology, acoustics, signal processing, '
        'instrument response, polezeros'
    ),
    entry_points={
        'console_scripts': [
            'snek = instResp.libInst:main',
        ],
    }
)
