from setuptools import setup, find_packages

import project_rename

	
setup(
    name='project_rename',
    packages=find_packages(),
    license='BSD',
    version=project_rename.__version__,
    description='ProjectRename is a Django app to renaming the project of boilerplate',
    author='Jitender Singh',
    author_email='jitender0514@gmail.com',
    include_package_data=True,
    download_url='https://github.com/jitender0514/djnago-rename/archive/{}.tar.gz'.format(project_rename.__version__),
    url='https://github.com/jitender0514/djnago-rename',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)