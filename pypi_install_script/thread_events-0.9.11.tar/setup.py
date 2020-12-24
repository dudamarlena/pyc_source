from setuptools import setup

setup(
    name='thread_events',
    version='0.9.11',
    description='Compiled protobuf files to send Thread events',
    url='https://github.com/thread/thread-events',
    author='Thread',
    packages=['thread_events', 'thread_events.styleme'],
    install_requires=['protobuf==3.4.0'],
    zip_safe=False,
)
