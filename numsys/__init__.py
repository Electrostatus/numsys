import support as _sup
import standard as _std


__doc__ = """A number rebasing system, version {}

    can convert any real or complex number
    to a base of any real or imaginary value

    invalid bases are abs(base) == 1 or == 0
    complex bases are not implemented
	
    The number of available characters are {:,}.
    If a base requires more characters, then the system will return a list
    containing the positional values in base ten.

    If not using gmpy2 or mpmath, conversion to imaginary bases or of compelx
    values may fall to custom complex class based on Python's decimal module.
    The decimal module will also be used if converting to a float base or
    conversion of a float-like value should mpmath or gmpy2 is not found.
    """.format(_sup.version, _sup.maxchr)

__all__ = ['rebase', 'guess', 'inDecimal', 'numDigits', # this file
           'decml', 'cmplx', 'setPrec', 'setDigitSet',  # support file
           ]

# from support file
decml = _sup.decml
cmplx = _sup.cmplx
setPrec = _sup.setPrec
setDigitSet = _sup.setDigitSet
numStor = _sup.numStor


def rebase(num, b1, b2, sgn='-', sep='.', as_numeric=False):
    """
    Convert a number from base b1 to base b2

    base inputs can be numeric strings (i.e. "-13.93486") to insure precision
    and can contain 'i' or 'j' to signify that they are imaginary values.

    number input can be a numeric type (int, float, complex, cmplx, decml),
    strings, or two length tuples (for real, imag values)

    output - string if no imaginary value
           - namedtuple if imaginary value (see numStor)
           - int, long, float, complex, cmplx or decml type
             if as_numeric is True and b2 is 10 (regardless of digitSet order)
    """
    # if the number is zero, why do any math? return a zero
    if not num: return _sup.digitSet[0]

    # checking/error values
    zero_types = [[], [0], _sup.digitSet[0], _sup.str_()]
    str_types = ('str', 'unicode')
    
    # parse input
    if type(num).__name__ in str_types:
        real, imag = num, 0  # string types
    elif type(num) == tuple:
        real, imag = num[0], num[1]  # tuple
    else:
        try: real, imag = num.real, num.imag  # numeric types, named tuple
        except AttributeError: real, imag = num, 0  # anything else

    # parse base inputs
    bases = []
    for b in (b1, b2):
        if type(b).__name__ in str_types:  # string input
            if 'i' in b or 'j' in b: b = cmplx(b.replace('i', 'j'))
            else: b = decml(b)
        bases.append(b)
    b1, b2 = bases

    # convert input from base b1 to base ten (outputs here are numerical)
    if b1.real and not b1.imag:  # real base
        valr = _std.to_10(real, b1, sgn, sep)
        vali = _std.to_10(imag, b1, sgn, sep)
        val10 = valr if not vali else (valr + vali * 1j)
    elif not b1.real and b1.imag:  # imaginary base
        val10 = _std.to_10(real, b1, sgn, sep)  # imag base values have no imag part
    else:  # complex base, base 0
        E = ValueError('invalid input base')
        raise E

    # return as a numeric type
    if as_numeric and b2 == 10: return val10

    # convert base ten value to base b2 (outputs here will be lists)
    if b2.real and not b2.imag:  # real base
        ansr = _std.to_rb(val10.real, b2, sgn, sep)
        ansi = _std.to_rb(val10.imag, b2, sgn, sep)
    elif not b2.real and b2.imag:  # imaginary base
        ansr = _std.to_ib(cmplx(val10.real, val10.imag), b2, sgn, sep)
        ansi = [0]
    else:  # complex base, base 0
        E = ValueError('invalid output base')
        raise E

    # convert to string
    res = _sup.lst_to_str(ansr, sgn, sep)
    ult = _sup.lst_to_str(ansi, sgn, sep)
    result = res if ult in zero_types else numStor(res, ult)
    return result
    
def inDecimal(num, sgn='-', sep='.', as_str=False):
    """
    Leaves num as is, but converts each symbol to its value in base 10
    will return a list unless as_str is True
    """
    lst = _sup.str_to_lst(num, sgn, sep)

    if as_str:
        split = ':;|'  # just in case the sgn or sep takes these symbols
        split = split.replace(sgn, ''); split = split.replace(sep, '')
        
        # if the number has both whole and fractional parts
        if sep in lst:  # should be one block; 5.6, not 5:.:6
            loc = lst.index(sep); lst.pop(loc)
            whol = lst.pop(loc - 1); frac = lst.pop(loc - 1)
            lst.insert(loc - 1, sep.join([sup.str_(whol), sup.str_(frac)]))

        # if the number is negative, should be one block; -num, not -:num
        if sgn in lst:
            lst.pop(0); num = lst.pop(0)
            lst.insert(0, sup.str_().join([sgn, sup.str_(num)]))
            
        in_deci = [sup.str_(j) for j in lst]
        output = split[0].join(in_deci)
    else: output = lst
    return output

def guess(n, sgn='-', sep='.'):
    "returns possible base of n\nactual may be >=abs() of return"
    lst = _sup.str_to_lst(n, sgn, sep)
    if sgn in lst: lst.remove(sgn)
    if sep in lst: lst.remove(sep)
    return max(lst) + 1

def numDigits(base):
    "returns the number of digits a base uses"
    if base.imag: base = base * (base.real - base.imag); base = base.real
    base = abs(base)  # can't use .conjugate(), gmpy2 2.0.8 will crash

    E, one = ValueError('invalid base'), decml(1)
    if base == 0: return 0  # not actually a base
    elif 0 < base < 1: return int(_sup.ceil(one / base))
    elif base == 1: return 1  # same with this one
    elif base > 1: return int(_sup.ceil(base))
    else: raise E 

def base_prec(prec, newbase, oldbase=2):
    "gives precision in new base"
    # work on this
    return int(prec * abs(_sup.log(oldbase, newbase)))
