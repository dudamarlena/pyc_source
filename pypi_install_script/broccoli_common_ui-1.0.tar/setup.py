from setuptools import setup, find_packages

install_requires = [
    'broccoli-interface==1.0',
    'broccoli-ui-interface==1.0'
]

setup(
    name='broccoli_common_ui',
    version='1.0',
    url='http://github.com/KTachibanaM/common-ui',
    author='KTachibanaM',
    author_email='whj19931115@gmail.com',
    license='WTFPL',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires
)
