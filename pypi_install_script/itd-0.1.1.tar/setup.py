
import os
import sys
from setuptools import setup, find_packages


__version_info__ = (0, 1, 1) 


readme = os.path.normpath(os.path.join(__file__, '..', 'README.md'))
with open(readme, 'r') as fh:
    long_description = fh.read()

def get_version():
    global __version_info__
    return (
        '.'.join(str(x) for x in __version_info__)
    )

setup(
    name='itd',
    version=get_version(),
    description='In The Dark - An Adventure / Escape Game for python programers.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/dee909/itd',
    author='Damien "dee" Coureau',
    author_email='dee909@gmail.com',
    license='LGPLv3+',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',

        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    ],
    keywords='game escape adventure codegame',
    install_requires=[
        'pyreadline',
    ],
    extras_require={
    },
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',
    #packages=find_packages('src'),
    packages=['itd'],
    package_dir={'': 'src'},
    package_data={
        #'': ['*.css', '*.png', '*.svg', '*.gif'],
    },
    entry_points = {}
)
