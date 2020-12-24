from distutils.core import setup

setup(
    name='universal-vim-config-generator',
    version='0.1',
    license='MIT',
    description='Package that I use to convert yaml files to multiple separate configs (In my case nvim and intellij)',
    author='Gytis Ivaskevicius',
    author_email='gytis02.21@gmail.com',
    url='https://github.com/WithoutCaps/vim-config-parser',
    download_url='https://github.com/WithoutCaps/vim-config-parser/archive/0.1.tar.gz',
    keywords=['vim', 'config', 'parser'],
    install_requires=['PyYAML'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
