from setuptools import setup

setup(
    name='foster_lab',
    version='1.1',
    packages=['foster_lab'],
    author="Evan Widloski",
    author_email="evan@evanw.org",
    description="Foster Lab Python scripts for cluster sorting",
    license="GPLv3",
    keywords="mountainsort foster lab",
    url="https://github.com/evidlo/foster_lab",
    entry_points={
        'console_scripts': ['get_offsets.py = foster_lab.get_offsets:main']
    },
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
