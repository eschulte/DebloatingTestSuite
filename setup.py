from setuptools import setup

import os

# build an rpm with the command:
#  python setup.py bdist_rpm


# read the version number out of the version.py file
# --> then the __version__ variable exists
exec(open('pytestbed/version.py').read())


setup(name='pytestbed',
      version=__version__,
      packages=['pytestbed'],
      include_package_data=True,
      install_requires=[
      ],
      description='TPCP Test Bed',
      entry_points={
          'console_scripts': [
              'pytestbed = pytestbed.cmdline:run_testbed'
          ]
      },
      url='https://github.com/tpcp-project/DebloatingTestSuite',
      author='Garret Wassermann',
      author_email='gwassermann@cert.org',
      license='MIT',
      classifiers=['Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3 :: Only'],
      zip_safe=False)
