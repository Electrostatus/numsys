# -*- coding: utf-8 -*-
"supporting functions and variables for numsys"


# imports -----------------------------------------------------------------
from sys import maxunicode as maxchr
from collections import namedtuple
import warnings
import string

try:  # to look for better installed modules
    #import this_is_not_a_module_name_this_is_just_for_testing
    try:  # look for gmpy2
        #import this_is_also_not_a_module_but_for_testing
        import gmpy2 as gm
        ceil, floor = gm.ceil, gm.floor
        #mpf, mpc = gm.mpfr, gm.mpc
        def log(x, b=None):
            if not b: return gm.log(x)
            else: return gm.log(x) / gm.log(b)

        def mpf(x):
            "converts input into multiprecision float - type gmpy2.mpfr"
            return gm.mpfr(x)

        def mpc(a, b=None):
            "converts input into multiprecision complex - type gmpy2.mpc"
            if not b: return gm.mpc(a)
            else: return gm.mpc(a, b)
        backend = 'gmpy2'

    except ImportError:  # use mpmath instead
        from mpmath import mp as mp
        ceil, floor = mp.ceil, mp.floor
        #mpf, mpc = mp.mpf, mp.mpc
        log = mp.log

        def mpf(x):
            "converts input into multiprecision float - type mpmath.mp.mpf"
            return mp.mpf(x)

        def mpc(a, b=None):
            "converts input into multiprecision complex - type mpmath.mp.mpc"
            if not b: return mp.mpc(a)
            else: return mp.mpc(a, b)
        backend = 'mpmath'

except ImportError:  # failing those, use the built-in modules
    from math import ceil as _cil, floor as _flr
    floor, ceil = lambda x: int(_flr(x)), lambda x: int(_cil(x))

    import decimal as dm
    try: import complex_decimal as cd
    except ImportError: from numsys import complex_decimal as cd
    #mpf, mpc = dm.Decimal, cd.ComplexDecimal

    def log(x, b=None):
        if not b: return mpf(x).ln()
        else: return mpf(x).ln() / mpf(b).ln()

    def mpf(x):
        "converts input into multiprecision float - type decimal.Decimal"
        return dm.Decimal(x)

    def mpc(a, b=None):
        "converts input into multiprecision complex - type ComplexDecimal"
        if not b: return cd.ComplexDecimal(a)
        else: return cd.ComplexDecimal(a, b)
    backend = 'decimal'

##except ImportError:  # don't use the decimal module (not recommended)
##    from math import log, ceil, floor
##    mpf, mpc = float, complex
##    backend = None

try: import nonstandard as nstd  # used in parse_base
except ImportError: from numsys import nonstandard as nstd

# functions ---------------------------------------------------------------
warnings.simplefilter('always')  # warnings in this should be rare (hopefully!)

# unicode/str for Python 2/3
try:          str_ = unicode
except NameError: str_ = str

# unichr/chr for Python 2/3
try:           chr_ = unichr
except NameError: chr_ = chr

numStor = namedtuple('numStor', 'real imag')
#class numStor(namedtuple('numStor', 'real imag')):
#    "numerical storage of arbitrary base"
#    pass

def mod(a, b):
    "mod(a, b) <==> a % b"
    return a - (b * (a // b))

def unique(seq):
    "removes duplicates in seq, maintaining order"
    seen = set(); sead = seen.add  # http://stackoverflow.com/a/480227
    return [x for x in seq if not (x in seen or sead(x))]
    # return list(dict.fromkeys(seq))  # valid for python 3.7 and higher

def rround(n, d=5):
    "relative float rounding: 9.0123456789e-307 -> 9.01235e-307"
    ln = log(abs(n), 10) if n != 0 else 0
    return round(float(n), -int(floor(ln)) + d)

def default_digitset(full=True):
    "returns the default digitset as a list"
    digits = list(string.printable.swapcase())
    if full: digits += list(map(chr_, range(maxchr)))
    return unique(digits)

def set_digitset(seq):
    "sets digitset to given digits in seq"
    global digitset, zero_types
    digitset = unique(seq)  # be a tuple? but tuple has slower access time
    zero_types = [0, [], [0], digitset[0], str_(), '']  # than a list - curious

def set_prec(prc=None):
    """
    set the precision
    pass None to get current precision
    prc is the number of digits that should be accurate in base two
    """
    #note:
    #  precision is defined in base 2. It needs to be redefined in the base
    #  that is being used so as the number in the new base so it doesn't lose
    #  precision. That is, the number shouldn't return with trailing garbage
    #  (45.0000000000000000052...). The conversions are automatically done in
    #  the functions that need the precision - it is not done here.

    global prec
    if prc is None: return prec
    prc = int(abs(prc))

    if backend == 'mpmath':  # base ten precision
        mp.prec = int(prc * log(2, 10))
    elif backend == 'gmpy2':  # base two precision
        gm.set_context(gm.context(precision = prc))
    elif  backend == 'decimal':  # base ten precision
        dm.getcontext().prec = int(prc * log(2, 10))
    else: pass

    prec = prc
    return prc

def clean(num, sgn='-', sep='.'):
    """removes leading and trailing zeros from a list
    pass False to sgn and sep if known to NOT to be in num"""
    global digitset

    # handle negative sign
    if sgn and sgn in num:
        try: num = num.replace(sgn, '')  # str
        except: num = list(filter(lambda x: x != sgn, num))  # list
        neg = True
    else: neg = False

    for zero in (digitset[0], 0):  # remove zeros
        while num[0] == zero and len(num) > 1 and num[1] != sep:  # leading
            num = num[1:]
        if sep and sep in num:  # trailing
            while num[-1] == zero and len(num) > 1 and num[-1] != sep:
                num = num[:-1]

    # remove radix if last digit
    if num[-1] == sep and num.count(sep) == 1:
        num = num[:-1]

    # add zero if first digit is radix
    if num[0] == sep:
        try: num = digitset[0] + num  # str
        except: num = [0, ] + num  # list

    # restore negative sign
    if neg:
        try: num = sgn + num  # str
        except: num = [sgn, ] + num  # list
    return num

def str_to_lst(s, sgn='-', sep='.'):
    "converts a string to a list of base ten digit values"
    # check if already a list of digits
    if type(s) == list: return s
    else: s = str_(s)

    # error checking
    if sgn in s and s[0] != sgn:
        E = SyntaxError('negative sign is not leading the number')
        raise E
    if s.count(sgn) > 1:
        E = SyntaxError('negative sign appears more than once')
        raise E
    if s.count(sep) > 1:
        E = SyntaxError('fractional separator (radix) appears more than once')
        raise E

    # convert to list of base ten digits
    lst = []
    for char in s:
        if char == sgn: val = sgn  # minus sign
        elif char == sep: val = sep  # radix
        else:
            try: val = digitset.index(char)  # digit value
            except ValueError:  # char not in digitset
                E = ValueError('unknown character/character not in digitset')
                raise E
        lst.append(val)
    return lst

def lst_to_str(lst, sgn='-', sep='.'):
    "converts a list of base ten digit values to a string"
    emp = str_()

    # handle negative sign
    if sgn in lst: lst.remove(sgn); has_sgn = True
    else: has_sgn = False

    # handle radix
    if sep in lst:
        pt = lst.index(sep)
        whl, frc = lst[:pt], lst[pt + 1:]  # whole, fractional parts
        has_sep = True
    else:
        whl, frc = lst, []
        has_sep = False

    try:  # map values in list to corresponding characters
        digit_get = digitset.__getitem__
        num_str = ((sgn if has_sgn else emp) +
                   emp.join(map(digit_get, whl)) +
                   (sep + emp.join(map(digit_get, frc)) if frc else emp))
    except IndexError:  # value larger than available digits, put as list
        num_str = ([sgn] if has_sgn else []) + lst

    # check if radix or negative sign shows up when it shouldn't
    catch = False  # or more times than it should
    if num_str.count(sgn) > 1 or (not has_sgn and num_str.count(sgn)):
        msg = "output contains negative sign in use as a value"
        catch = True
    if num_str.count(sep) > 1 or (not has_sep and num_str.count(sep)):
        msg = "output contains a radix sign in use as a value"
        catch = True
    if catch:
        warnings.warn(msg, stacklevel=3)  # ex: rebase(1114112*75, 10, 1114112)
    #    return ([sgn] if has_sgn else []) + lst  # return as a list if so

    gn = sgn if has_sgn else has_sgn
    ep = sep if has_sep else has_sep
    return clean(num_str, gn, ep)

def parse_input(x):
    "parse a generic input to real, imag parts"
    name = type(x).__name__
    if name in str_types:
        real, imag = x, 0  # string types
    elif name == 'tuple':
        real, imag = x[0], x[1]  # tuple
    else:
        try: real, imag = x.real, x.imag  # numeric types, named tuple
        except AttributeError: real, imag = x, 0  # anything else
    return real, imag

def parse_base(b):
    "parse a numeric input"
    name = type(b).__name__
    if name in str_types:
        b = str_(b).lower()
        if b in nstd.nstd_bases: pass
        elif 'i' in b or 'j' in b: b = mpc(b.replace('i', 'j'))
        else:
            try: b = int(b)
            except ValueError: b = mpf(b)
    elif name == 'tuple':
        b = mpc(b[0], b[1])
    else: pass
    return b

# refs --------------------------------------------------------------------
references = {'A': {'ref': u'A. Rényi, "Representations for real numbers '
                    'and their ergodic properties", Acta Mathematica Acad'
                    'emic Sci. Hungar., 1957, vol. 8, pp. 433-493',
                    'link': 'https://doi.org/10.1007/BF02020331'},
              'B': {'ref': u'S. Ito, T. Sadahiro, "Beta-expansions with n'
                    'egative bases", Integers, 2009, vol. 9, pp. 239-259',
                    'link': 'https://doi.org/10.1515/INTEG.2009.023'},
              'C': {'ref': u'D. Knuth, "An Imaginary Number System", Comm'
                    'unications of the ACM, 1960, vol. 3, pp. 245-247',
                    'link': 'https://doi.org/10.1145/367177.367233'},
              'D': {'ref': u'V. Grünwald, "Intorno all\'aritmetica dei si'
                    'stemi numerici a base negativa con particolare rigua'
                    'rdo al sistema numerico a base negativo-decimale per'
                    ' lo studio delle sue analogie coll\'aritmetica ordin'
                    'aria (decimale)", Giornale di matematiche di Battagl'
                    'ini, 1885, vol. 23, pp. 203-221', 'link': ''},
              'E': {'ref': u'P. Herd, "Imaginary Number Bases"',
                    'link': 'https://arxiv.org/abs/1701.04506'},
              }

# constants ---------------------------------------------------------------
version = '1.0.01'
maxchr += 1  # base 0 uses no characters, so all of unicode is valid
prec = set_prec(100)   # precision (in base two)
digitset = default_digitset()
zero_types = [0, [], [0], digitset[0], str_(), '']  # this is reset with set_digitset
str_types = ('str', 'unicode')

