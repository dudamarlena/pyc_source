from pathlib import Path
from setuptools import setup

current_dir = Path(__file__).parent.resolve()

with open(current_dir / 'README.md', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name = 'restrict',
    version = '0.1.3',
    author = 'BTaskaya',
    author_email = 'batuhanosmantaskaya@gmail.com',
    packages = ['restrict'],
    description = "Restrict python methods",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/btaskaya/restrict'
)
