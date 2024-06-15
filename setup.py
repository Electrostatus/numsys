from numsys.support import version
from setuptools import setup

setup(name = 'numsys',
      version = version,
      description = 'numeral systems - number base conversion module',
      long_description = open('README.rst', encoding='utf-8').read(),
      license = 'GPLv3',
      author = 'Electrostatus',
      url = 'http://github.com/Electrostatus/numsys',
      packages = ['numsys'],
      package_data = {'': ['*.rst']},
      extra_requires = ['gmpy2'],  # optional, for fast float pt precision
      keywords = 'number base numeral system mixed radix roman',
      classifiers = [
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        ],
      )
