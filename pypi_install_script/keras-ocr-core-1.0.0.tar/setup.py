from setuptools import setup, find_packages
setup(name='keras-ocr-core',
      version='1.0.0',
      description=(
          'darknet + crnn'
      ),
      long_description='For detail please step to https://github.com/yfyvan/keras-ocr-core',
      long_description_content_type="text/markdown",
      author='ldhsights',
      author_email='yfyvan@gmail.com',
      maintainer='Yvan L',
      maintainer_email='yfyvan@gmail.com',
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      url='https://github.com/yfyvan/keras-ocr-core',
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
            'tensorflow',
            'keras',
            'pillow',
            'numpy',
            'opencv-python'
      ])

