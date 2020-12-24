"""Setup file for package."""
import setuptools

with open("README.md", 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
      name='chthonic',
      packages=['chthonic'],
      description='A boilerplate environment for Python package development.',
      install_requires=[],
      url='https://github.com/crainiac/chthonic',
      author='Alex Crain',
      author_email='alex@crain.xyz',
      platforms=['any'],
      license='MIT',
      classifiers=[
          'Programming Language :: Python :: 3',
	  'License :: OSI Approved :: MIT License',
	  'Operating System :: OS Independent',
      ],
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      version='1.0.0',
)
