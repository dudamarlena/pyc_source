from distutils.core import setup
setup(
  name='s3_sync',
  packages=['s3_sync'],
  version='0.1.1',
  license='MIT',
  description='TYPE YOUR DESCRIPTION HERE',
  author='Julius Krahn',
  author_email='juliuskrahn@outlook.de',
  url='https://github.com/juliuskrahn/s3_sync',
  download_url='https://github.com/juliuskrahn/s3_sync/archive/v0.1.1.tar.gz',
  keywords=['sync', 'AWS', 'S3', 'bucket'],
  install_requires=['boto3'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    "Operating System :: OS Independent",
    'Programming Language :: Python :: 3'
  ],
)