from setuptools import setup, find_packages

setup(name='django-softdelete-forked',
      version='0.7.1',
      description='Soft delete support for Django ORM, with undelete.',
      author='Steve Coursen, Glyn Jackson',
      author_email='smcoursen@gmail.com',
      maintainer='Glyn Jackson',
      maintainer_email='me@glynjackson.org',
      license="BSD",
      url="https://github.com/glynjackson/django-softdelete",
      packages=find_packages(),
      install_requires=['setuptools',],
      include_package_data=True,
      setup_requires=['setuptools_hg',],
      classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        ]
)
