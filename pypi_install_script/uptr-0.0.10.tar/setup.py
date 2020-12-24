from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='uptr',
    version='0.0.10',
    description='Command line interface for update tracker.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://gitlab.com/teonite/update-tracker-backend',
    author='TEONITE',
    author_email='support@teonite.com',
    packages=['update_tracker_client'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'confire==0.2.0',
        'click==6.7',
        'requests==2.18.4',
    ],
    entry_points={
        'console_scripts': [
            'uptr=update_tracker_client:entry_point'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
    ],
)
