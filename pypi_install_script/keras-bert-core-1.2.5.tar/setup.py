from setuptools import setup, find_packages
setup(name='keras-bert-core',
      version='1.2.5',
      description=(
          '基于谷歌中文预训练模型的keras版bert框架'
      ),
      long_description='For detail please step to https://github.com/yfyvan/keras-bert',
      long_description_content_type="text/markdown",
      author='yfyvan',
      author_email='yfyvan@gmail.com',
      maintainer='Yvan L',
      maintainer_email='yfyvan@gmail.com',
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      url='https://github.com/yfyvan/keras-bert',
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
          'Programming Language :: Python :: 3.7'
      ],
      install_requires=[
          'wget',
          'tensorflow',
          'keras',
          'numpy'
      ])

