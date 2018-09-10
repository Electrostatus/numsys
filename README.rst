numsys
======
numeral system conversion module; converts values from one number base to another

Any real or complex number can be converted to/from a base of any real or imaginary value

Standard
--------
representation in a positional numeral system (base ten, base sixty)

Number bases here are integers (2, 3, 10, ...), negatives, (-2, -10, -25, ...), reals (1.5, 3.14159, -2.71828, ...) or imaginary (2i, -4.5i, 6i, ...). Additionally, inverted values (0.5, -0.36788, 0.001, ...) are allowed in use as a base. Invalid values as a base are 0, 1 and any value whose absolute value is 1.

Non-standard
------------
representation in a non-positional numeral system (roman, factorial)

A non-positional numeral system is one where values do not conform to the positional system. These can be alphabetic, like Roman numerals, or a mixed base system, like factorial. Also included are positional-like bases that have limited representation; not all values can be shown. Examples of these are base one and minus one.

Digits
------
The first one hundred digits used (in order) are ``0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ \t\n\r\x0b\x0c``. After this, which digits are used will be dependent on your system encoding. However, general order will be from the lowest Unicode plane to the highest (skipping already seen digits).


References
----------
positive real base conversion: (`Ref. A`_) A. Rényi, "Representations for real numbers and their ergodic properties", *Acta Mathematica Academic Sci. Hungar.*, **1957**, vol. 8, pp. 433-493
negative real base conversion: (`Ref. B`_)  S. Ito, T. Sadahiro, "Beta-expansions with negative bases", *Integers*, **2009**, vol. 9, pp. 239-259
base 2i: (`Ref. C`_) D. Knuth, "An Imaginary Number System", *Communications of the ACM*, **1960**, vol. 3, pp. 245-247
base -10: (Ref. D) V. Grünwald, "Intorno all'aritmetica dei sistemi numerici a base negativa con particolare riguardo al sistema numerico a base negativo-decimale per lo studio delle sue analogie coll'aritmetica ordinaria (decimale)", *Giornale di matematiche di Battaglini*, **1885**, vol. 23, pp. 203-221
imaginary base conversion/summary: (`Ref. E`_) P. Herd, "Imaginary Number Bases"


.. _`Ref. A`: https://doi.org/10.1007/BF02020331
.. _`Ref. B`: https://doi.org/10.1515/INTEG.2009.023
.. _`Ref. C`: https://doi.org/10.1145/367177.367233
.. _`Ref. E`: https://arxiv.org/abs/1701.04506
