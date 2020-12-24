from distutils.core import setup

setup(
    name='getlink_fshare',
    packages=['getlink_fshare'],
    version='0.3',
    license='MIT',
    description='Get download link from Fshare.vn',
    author='trandatdt',
    author_email='trandat021197@gmail.com',  # Type in your E-Mail
    url='https://github.com/TranDatDT/getlink_fshare',  # Provide either the link to your github or to your website
    keywords=['getlink', 'fshare',],
    install_requires=[  # I get to this in a second
        'requests-html'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)
