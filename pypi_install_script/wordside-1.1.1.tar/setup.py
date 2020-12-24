from setuptools import setup, find_packages

setup(
    name='wordside',
    version='1.1.1',
    packages=find_packages(),
    include_package_data=True,
    author='Evgeni Pochchuev',
    author_email='jackio@tuta.io',
    url='https://github.com/jacki0/wordside',
)
install_requires=[
    'pymorphy2==0.8'
]
