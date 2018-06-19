import support as _sup
import standard as _std
import nonstandard as _nsd


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

    sgn - what character the negative sign is (default '-')
    sep - what character the radix point (fractional seperator) is (default '.')
    """.format(_sup.version, _sup.maxchr)

__all__ = ['rebase', 'guess', 'inDecimal', 'numDigits', # this file
           'decml', 'cmplx', 'setPrec', 'setDigitSet',  # support file
           'roman', 'factorial',                        # nonstandard file
           ]

# from support file
decml = _sup.decml
cmplx = _sup.cmplx
setPrec = _sup.setPrec
setDigitSet = _sup.setDigitSet
numStor = _sup.numStor

# from nonstandard file
roman = _nsd.to_ro
romanTo = _nsd.ro_to
factorial = _nsd.to_fc
factorialTo = _nsd.fc_to


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

    # parse input
    real, imag = _sup.parseInput(num)
    b1, b2 = _sup.parseBase(b1), _sup.parseBase(b2)

    # convert input from base b1 to base ten (outputs here are numerical)
    if _sup.str_(b1).lower() in _nsd.nstd_bases:  # custom base
        nsd_to = _nsd.nstd_bases.get(_sup.str_(b1).lower())[1]
        res = nsd_to(real, sgn, sep)
        try: ult = nsd_to(imag, sgn, sep)
        except AttributeError: ult = ''
        val10 = res if not ult else (res + ult * cmplx(0, 1))
    elif b1.real and not b1.imag:  # real base
        valr = _std.to_10(real, b1, sgn, sep)
        vali = _std.to_10(imag, b1, sgn, sep)
        val10 = valr if not vali else (valr + vali * cmplx(0, 1))
    elif not b1.real and b1.imag:  # imaginary base
        val10 = _std.to_10(real, b1, sgn, sep)  # imag base values have no imag part
    else:  # complex base, base 0
        E = ValueError('invalid input base')
        raise E

    # return as a numeric type
    if as_numeric and b2 == 10: return val10

    # convert base ten value to base b2 (outputs here will be lists)
    if _sup.str_(b2).lower() in _nsd.nstd_bases:  # custom base
        to_nsd = _nsd.nstd_bases.get(_sup.str_(b2).lower())[0]
        ansr = to_nsd(val10.real, sgn, sep)
        ansi = to_nsd(val10.imag, sgn, sep)
    elif b2.real and not b2.imag:  # real base
        ansr = _std.to_rb(val10.real, b2, sgn, sep)
        ansi = _std.to_rb(val10.imag, b2, sgn, sep)
    elif not b2.real and b2.imag:  # imaginary base
        ansr = _std.to_ib(cmplx(val10.real, val10.imag), b2, sgn, sep)
        ansi = [0]
    else:  # complex base, base 0
        E = ValueError('invalid output base')
        raise E

    # convert to string
    try:
        res = _sup.lst_to_str(ansr, sgn, sep)
        ult = _sup.lst_to_str(ansi, sgn, sep)
    except TypeError:  # custom base return is a string?
        res, ult = ansr, ansi
    result = res if ult in _sup.zero_types else numStor(res, ult)
    return result

def toBase(x, b, sgn='-', sep='.'):
    "convert a base ten numeric value x to base b"
    # same as the second half of rebase
    x, b = _sup.parseBase(x), _sup.parseBase(b)
    
    lts, tr, ti = _sup.lst_to_str, _std.to_rb, _std.to_ib
    E = ValueError('invalid base')
    if b in (1, 0):
        raise E
    elif _sup.str_(b).lower() in _nsd.nstd_bases:  # custom base
        to_nsd = _nsd.nstd_bases.get(_sup.str_(b).lower())[0]
        res = to_nsd(x.real, sgn, sep)
        ult = to_nsd(x.imag, sgn, sep)
    elif b.real and not b.imag:  # real base
        res = lts(tr(x.real, b, sgn, sep), sgn, sep)
        ult = lts(tr(x.imag, b, sgn, sep), sgn, sep)
    elif not b.real and b.imag:  # imaginary base
        res = lts(ti(cmplx(x.real, x.imag), b, sgn, sep), sgn, sep)
        ult = lts([0], sgn, sep)
    else: raise E

    return res if ult in _sup.zero_types else numStor(res, ult)

def toTen(x, b, sgn='-', sep='.'):
    "convert a string x in base b to base ten"
    # same as the first half of rebase
    real, imag = _sup.parseInput(x)
    b = _sup.parseBase(b)

    E = ValueError('invalid base')
    if b in (1, 0):  # invalid bases
        raise E
    elif _sup.str_(b).lower() in _nsd.nstd_bases:  # custom base
        nsd_to = _nsd.nstd_bases.get(_sup.str_(b).lower())[1]
        res = nsd_to(real, sgn, sep)
        try: ult = nsd_to(imag, sgn, sep)
        except AttributeError: ult = ''
        result = res if not ult else (res + ult * cmplx(0, 1))
    elif b.real and not b.imag:  # real base
        res = _std.to_10(real, b, sgn, sep)
        ult = _std.to_10(imag, b, sgn, sep)
        result = res if not ult else (res + ult * cmplx(0, 1))
    elif not b.real and b.imag:  # imaginary base
        result = _std.to_10(real, b, sgn, sep)
    else: raise E
    return result

def inDecimal(num, sgn='-', sep='.', as_str=False):
    """
    Leaves num as is, but converts each symbol to its value in base 10
    will return a list unless as_str is True
    """
    sgn, sep = _sup.str_(sgn), _sup.str_(sep)
    lst = _sup.str_to_lst(num, sgn, sep)

    if as_str:
        split = ':;|'  # just in case the sgn or sep takes these symbols
        split = split.replace(sgn, ''); split = split.replace(sep, '')
        
        # if the number has both whole and fractional parts
        if sep in lst:  # should be one block; 5.6, not 5:.:6
            loc = lst.index(sep); lst.pop(loc)
            whol = lst.pop(loc - 1); frac = lst.pop(loc - 1)
            lst.insert(loc - 1, sep.join([_sup.str_(whol), _sup.str_(frac)]))

        # if the number is negative, should be one block; -num, not -:num
        if sgn in lst:
            lst.pop(0); num = lst.pop(0)
            lst.insert(0, _sup.str_().join([sgn, _sup.str_(num)]))
            
        in_deci = [_sup.str_(j) for j in lst]
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
    "returns the number of characters a base uses"
    if base.imag: base = base * cmplx(base.real, -base.imag); base = base.real
    base = abs(base)  # can't use .conjugate(), gmpy2 2.0.8 will crash

    E, one = ValueError('invalid base'), decml(1)
    if base == 0: return 0  # not actually a base
    elif 0 < base < 1: return int(_sup.ceil(one / base))
    elif base == 1: return 1  # same with this one
    elif base > 1: return int(_sup.ceil(base))
    else: raise E

def availableBases():  # does this make any sense to have?
    "print out avaiable bases"
    maxchr = _sup.maxchr
    line = 'available bases:'
    line += '\nreal bases -{} < -1 and 1 < {}'.format(maxchr, maxchr)
    line += '\nreal bases -1 < -1/{} and 1/{} < 1'.format(maxchr, maxchr)

    sqmxc = int(maxchr ** 0.5)
    line += '\nimag bases -{}j < 1j and 1j < {}j'.format(sqmxc, sqmxc)
    line += '\nimag bases -1j < -1/{}j and 1/{}j < 1j'.format(sqmxc, sqmxc)

    line += '\ncustom bases:'
    for i in _nsd.nstd_bases: line += '\n\t{}'.format(_sup.str_(i).lower())
    print(line)

def basePrec(prec, newbase, oldbase=2):
    "gives precision in new base"
    if newbase.imag: newbase *= cmplx(newbase.real, -newbase.imag)
    if oldbase.imag: oldbase *= cmplx(oldbase.real, -oldbase.imag)
    return int(prec * abs(_sup.log(abs(oldbase), abs(newbase))))
