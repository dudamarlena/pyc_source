from setuptools import setup, find_packages
setup(name='keras-yolo3-core',
      version='1.0.3',
      description=(
          'darknet + yolo3'
      ),
      long_description='For detail please step to https://github.com/yfyvan/keras-yolo3-core',
      long_description_content_type="text/markdown",
      author='ldhsights',
      author_email='yfyvan@gmail.com',
      maintainer='Yvan L',
      maintainer_email='yfyvan@gmail.com',
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      url='https://github.com/yfyvan/keras-yolo3-core',
      classifiers=[
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Topic :: Text Processing :: Indexing",
          "Topic :: Utilities",
          "Topic :: Internet",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python",
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      install_requires=[
            'tensorflow-gpu==1.12',
            'keras<=2.2.4',
            'pillow',
            'sklearn',
            'matplotlib',
            'numpy'
      ])

