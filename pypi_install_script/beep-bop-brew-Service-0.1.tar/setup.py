from setuptools import find_packages, setup

setup(
    name='beep-bop-brew-Service',
    version='0.1',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/FA-noway/beep-bop-brew-Service',
    author='Michael Ardron',
    author_email='beep.bop.brew@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Hardware',
    ],
    keywords='brewing brewpi brewblox embedded plugin service',
    packages=find_packages(exclude=['test', 'docker']),
    install_requires=[
        'brewblox-service'
    ],
    python_requires='>=3.7',
    extras_require={'dev': ['pipenv']}
)
