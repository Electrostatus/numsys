from numsys.support import version
from setuptools import setup

setup(name = 'numsys',
      version = version,
      description = 'numeral systems - conversion module of number bases',
	  long_description = open('README.rst').read(),
      author = 'Electrostatus',
      url = 'http://github.com/Electrostatus/numsys',
      packages = ['numsys'],
	  package_data = {'': ['*.rst']},
      keywords = 'number base numeral system',
      classifiers = [
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        ],
      )
