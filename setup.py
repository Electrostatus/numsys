from numsys.support import version
from setuptools import setup

setup(name = 'numsys',
      version = version,
      description = 'numeral systems - number base conversion module',
	  long_description = open('README.rst').read(),
      author = 'Electrostatus',
      url = 'http://github.com/Electrostatus/numsys',
      packages = ['numsys'],
	  package_data = {'': ['*.rst']},
      keywords = 'number base numeral system mixed radix roman',
      classifiers = [
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        ],
      )
