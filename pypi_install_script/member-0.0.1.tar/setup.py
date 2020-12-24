import setuptools

import member_data as member

setuptools.setup(
    name='member',
    version=member.__version__,
    url=member.__url__,
    author=member.__author__,
    packages=['member', 'member_data'],
    python_requires='>=3.7.0',
    include_package_data=True,
    data_files=[
        ('', ['README.md', 'CHANGELOG.md']),
    ],
    install_requires=[]
)
