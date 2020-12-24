from setuptools import setup, find_packages

install_requires = [
    'broccoli-interface==1.0',
    'oauthlib==3.1.0',
    'requests==2.22.0',
    'python-twitter==3.5'
]

setup(
    name='broccoli_twitter',
    version='1.4',
    url='http://github.com/broccoli-platform/twitter',
    author='KTachibanaM',
    author_email='whj19931115@gmail.com',
    license='WTFPL',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
)
