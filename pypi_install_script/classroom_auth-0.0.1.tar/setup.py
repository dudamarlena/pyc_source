from setuptools import setup, find_packages


setup(
    name='classroom_auth',
    author="Mirko Mälicke",
    author_email="mirko.maelicke@kit.edu",
    version='0.0.1',
    description="Custom jupyterhub.Authorizors for classroom usage",
    packages=find_packages(),
    entry_points={
        'jupyterhub.authenticators': [
            'classroom = classroom_auth:ClassroomFileAuthenticator'
        ]
    }
)