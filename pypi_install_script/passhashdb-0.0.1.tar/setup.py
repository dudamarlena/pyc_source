import os
from setuptools import setup
from passhashdb.version import __version__ as version

def read_project_file(path):
    proj_dir = os.path.dirname(__file__)
    path = os.path.join(proj_dir, path)
    with open(path, 'r') as f:
        return f.read()

setup(
    name = 'passhashdb',
    version = version,
    description = 'Build and search a password hash database',
    long_description = read_project_file('README.md'),
    long_description_content_type = 'text/markdown',
    python_requires = '>=3.5',
    author = 'Jonathon Reinhart',
    author_email = 'jonathon.reinhart@gmail.com',
    url = 'https://gitlab.com/JonathonReinhart/passhashdb',
    license = 'MIT',
    packages = ['passhashdb'],
    scripts = [
        'scripts/hibp-to-passhashdb',
        'scripts/samba-check-passhashdb',
    ],
)
