from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gpgeternal',
      version='0.9',
      description='A package that is able to constantly write encrypted bytes to disk',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/yirzhou/gpgeternal',
      author='Yiren Zhou',
      author_email='yiren.chow@gmail.com',
      scripts=['bash_scripts/gpg.sh'],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security :: Cryptography',
      ],
      keywords='gnu linux encrypt decrypt multiprocess',
      license='MIT',
      packages=['gpgeternal'],
      include_package_data=True,
      zip_safe=False)