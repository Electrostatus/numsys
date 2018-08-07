numsys
======
numeral system conversion module; converts values from one number base to another

Any real or complex number can be converted to/from a base of any real or imaginary value

standard
--------
representation in a positional numeral system (base ten, base sixty)

Number bases here are integers (2, 3, 10, ...), negatives, (-2, -10, -25, ...), reals (1.5, 3.14159, -2.71828, ...) or imaginary (2i, -4.5i, 6i, ...). Additionally, inverted values (0.5, -0.36788, 0.001, ...) are allowed in use as a base. Invalid values as a base are 0, 1 and any value whose absolute value is 1.

non-standard
------------
representation in a non-positional numeral system (roman, factorial)

A non-positional numeral system is one where values do not conform to the positional system. These can be alphabetic, like Roman numerals, or a mixed base system, like factorial. Also included are positional-like bases that have limited representation; not all values can be shown. Examples of these are base one and minus one.

digits
------
The first one hundred digits used (in order) are 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ \t\n\r\x0b\x0c. After this, which digits are used will be dependent on your system encoding. However, general order will be from the lowest Unicode plane to the highest (skipping already seen digits).


references
----------
positive real base converison: (link_) A. Rényi, "Representations for real numbers and their ergodic properties", *Acta Mathematica Academic Sci. Hungar.*, **1957**, vol. 8, pp. 433-493
.. _link: https://doi.org/10.1007/BF02020331
negative real base conversion: (link_)  S. Ito, T. Sadahiro, "Beta-expansions with negative bases", *Integers*, **2009**, vol. 9, pp. 239-259
.. _link: https://doi.org/10.1515/INTEG.2009.023
imaginary base conversion: (link_) P. Herd, "Imaginary Number Bases"
.. _link: https://arxiv.org/abs/1701.04506







