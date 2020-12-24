from distutils.core import setup
setup(
    name = 'aws-mailman',
    packages = ['aws-mailman'],
    version = '0.1.1',
    license='MIT',
    description = 'A utility for updating domain registrant information in Amazon Route 53',
    author = 'Fernando Medina Corey',
    author_email = 'fernandomc.sea@gmail.com',
    url = 'https://github.com/fernando-mc/',
    download_url = 'https://github.com/fernando-mc/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['AWS', 'Route53', 'Domains'],
    entry_points={
        'console_scripts': [
            'aws-mailman = aws-mailman.mailman:main',
        ],
    },
    install_requires=[
        'boto3',
        'bullet',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
  ],
)