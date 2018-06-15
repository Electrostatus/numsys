"supporting functions and variables for numsys"


# imports -----------------------------------------------------------------
from sys import maxunicode as maxchr
from collections import namedtuple
import string

try:  # to look for better installed modules
    try:  # look for gmpy2 
        import gmpy2 as gm
        def log(x, b=None):
            if not b: return gm.log(x)
            else: return gm.log(x) / gm.log(b)
        ceil, floor = gm.ceil, gm.floor
        #decml, cmplx = gm.mpfr, gm.mpc
        def decml(x):
            "converts input into multiprecision float - type gmpy2.mpfr"
            return gm.mpfr(x)
        def cmplx(a, b=None):
            "converts input into multiprecision complex - type gmpy2.mpc"
            if not b: return gm.mpc(a)
            else: return gm.mpc(a, b)
        backend = 'gmpy2'
    
    except ImportError:  # use mpmath instead
        from mpmath import mp as mp
        log, ceil, floor = mp.log, mp.ceil, mp.floor
        #decml, cmplx = mp.mpf, mp.mpc
        def decml(x):
            "converts input into multiprecision float - type mpmath.mp.mpf"
            return mp.mpf(x)
        def cmplx(a, b=None):
            "converts input into multiprecision complex - type mpmath.mp.mpc"
            if not b: return mp.mpc(a)
            else: return mp.mpc(a, b)
        backend = 'mpmath' 
    
except ImportError:  # failing those, use the built-in modules
    from math import ceil, floor
    import decimal as dm, complex_decimal as cd
    def log(x, b=None):
        if not b: return decml(x).ln()
        else: return decml(x).ln() / decml(b).ln()
    #decml, cmplx = dm.Decimal, cd.ComplexDecimal
    def decml(x):
        "converts input into multiprecision float - type decimal.Decimal"
        return dm.Decimal(x)
    def cmplx(a, b=None):
        "converts input into multiprecision complex - type ComplexDecimal"
        if not b: return cd.ComplexDecimal(a)
        else: return cd.ComplexDecimal(a, b)
    backend = 'decimal'

##except ImportError:  # don't use the decimal module (not recommended)
##    from math import log, ceil, floor
##    decml, cmplx = float, complex
##    backend = None

# functions ---------------------------------------------------------------

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

def defaultDigitSet(full=True):
    "returns the default digit set as a list"
    digits = list(string.printable.swapcase())
    if full: digits += list(map(chr_, range(maxchr)))
    return unique(digits)

def setDigitSet(seq):
    "sets digitSet to given digits in seq"
    global digitSet
    digitSet = unique(seq)

def setPrec(prc=None):
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
    global digitSet

    # handle negative sign
    if sgn and sgn in num:
        try: num = num.replace(sgn, '')  # str
        except: num = list(filter(lambda x: x != sgn, num))  # list
        neg = True
    else: neg = False

    for zero in (digitSet[0], 0):  # remove zeros
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
        try: num = digitSet[0] + num  # str
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
            try: val = digitSet.index(char)  # digit value
            except ValueError:  # char not in digitSet
                E = ValueError('unknown character/character not in digitSet')
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
        digit_get = digitSet.__getitem__
        num_str = ((sgn if has_sgn else emp) +
                   emp.join(map(digit_get, whl)) +
                   (sep + emp.join(map(digit_get, frc)) if frc else emp))
    except IndexError:  # value larger than available digits, put as list
        num_str = ([sgn] if has_sgn else []) + lst

    # check if radix or negative sign shows up when it shouldn't
    catch = False  # or more times than it should
    if num_str.count(sgn) > 1 or (not has_sgn and num_str.count(sgn)):
        W = "output contains negative sign in use as a value"
        catch = True
    if num_str.count(sep) > 1 or (not has_sep and num_str.count(sep)):
        W = "output contains a radix sign in use as a value"
        catch = True
    #if catch:
    #    # put a warning here instead?
    #    return ([sgn] if has_sgn else []) + lst  # return as a list if so

    gn = sgn if has_sgn else has_sgn
    ep = sep if has_sep else has_sep
    return clean(num_str, gn, ep)


# constants ---------------------------------------------------------------
version = '0.9.8'
maxchr += 1  # base 0 uses no characters, so all of unicode is valid
prec = setPrec(100)   # precision (in base two)
digitSet = defaultDigitSet()
zero_types = [0, [], [0], digitSet[0], str_(), '']
str_types = ('str', 'unicode')

