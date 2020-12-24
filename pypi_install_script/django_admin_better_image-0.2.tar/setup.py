from setuptools import setup, find_packages

setup(
    name='django_admin_better_image',
    packages=find_packages(),
    version='0.2',
    license='MIT',
    description='Django package that provides widget to display images.',
    author='Serhii Beznisko',
    author_email='beznisko.ss@gmail.com',
    url='https://github.com/serhiibeznisko/django-admin-better-image',
    keywords=['django', 'admin', 'widget', 'image', 'imagefield'],
    install_requires=[
        'django',
    ],
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
