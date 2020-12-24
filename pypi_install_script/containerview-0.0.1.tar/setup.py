import setuptools

import containerview_data as containerview

setuptools.setup(
    name='containerview',
    version=containerview.__version__,
    url=containerview.__url__,
    author=containerview.__author__,
    packages=['containerview', 'containerview_data'],
    python_requires='>=3.7.0',
    include_package_data=True,
    data_files=[
        ('', ['README.md', 'CHANGELOG.md']),
    ],
    install_requires=[]
)
