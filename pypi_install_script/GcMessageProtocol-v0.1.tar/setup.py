from distutils.core import setup
setup(
    name = 'GcMessageProtocol',
    packages = ['GcMessageProtocol', 'GcMessageProtocol.protocols'],
    version = '0.1',
    license='MIT',
    description = 'A protocol to standardize the conversation between all GameCompany bots with logs',
    author = 'HidekiHrk',
    author_email = 'hidekihiroki123@gmail.com', 
    url = 'https://github.com/GameCompanyGC/Python-GCDiscordMessageProtocol',
    download_url = 'https://github.com/GameCompanyGC/Python-GCDiscordMessageProtocol/archive/v_01.tar.gz',
    keywords = ['GameCompany', 'GC', 'Protocol'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

    ],
)