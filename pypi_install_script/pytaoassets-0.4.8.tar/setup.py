from setuptools import setup

setup(name='pytaoassets',
      version='0.4.8',
      description='Python implementation of the PeerAssets protocol for the Tao blockchain.',
      keywords=["blockchain", "digital assets", "protocol"],
      url='https://github.com/taoblockchain/pytaoassets',
      author='Bryce Weiner',
      author_email='bryce@tao.network',
      license='BSD',
      packages=['pytaoassets', 'pytaoassets.provider'],
      install_requires=['protobuf', 'taoassets-taopy'],
      extras_require={
        'rcp_provider': ['python-taorpc>=1.0']
                        }
      )
