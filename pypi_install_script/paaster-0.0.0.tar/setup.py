'''

'''

from setuptools import setup, find_packages
import versioneer

setup(
    name='paaster',
    # version=versioneer.get_version(),
    version='0.0.0',
    # cmdclass=versioneer.get_cmdclass(),
    author='Sean Ross-Ross',
    author_email='srossross@gmail.com',
    url='http://github.com/srossross/paaster',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'plaaster.frontend': [
            "notebook = plaaster.notebook:use_notebook"
        ]
    },
)
