from setuptools import setup

setup(name='opentarock-server-users',
      description="OpenTarock user managment and authentication service",
      author='The OpenTarock Project',
      author_email='opentarockofficial@gmail.com',
      license='AGPLv3',
      version='0.1',
      packages=[
          'opentarock',
          'opentarock.server',
          'opentarock.users'
      ],
      entry_points={
          'console_scripts': ['server-users = opentarock.server:main']
      }
      )
