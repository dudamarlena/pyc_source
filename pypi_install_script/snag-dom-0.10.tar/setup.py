import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
        name='snag-dom',
        version='0.10',
        author='Cassandra Gentry',
        author_email='cassiegentlekitty@gmail.com',
        description='An HTML utility package',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(),
        install_requires= [
            'requests',
            'bs4'
        ],
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: OS Independent'
        ]
)
