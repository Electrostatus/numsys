try:  # Python 2
    import support as _sup
    import standard as _std
    import nonstandard as _nsd
except ImportError:  # Python 3
    from numsys import support as _sup
    from numsys import standard as _std
    from numsys import nonstandard as _nsd


__doc__ = """A number base conversion system, version {}

    can convert any real or complex number
    to a base of any real or imaginary value

    invalid bases are abs(base) == 1 or abs(base) == 0

    The number of available characters are {:,}.
    If a base requires more characters, then the system will return a list
    containing the positional values in base ten.

    If not using gmpy2 or mpmath, conversion to imaginary bases or of complex
    values may fall to custom complex class based on Python's decimal module.
    The decimal module will also be used if converting to a float base or
    conversion of a float-like value should mpmath or gmpy2 is not found.

    sgn - what character the negative sign is (default '-')
    sep - what character the radix point (fractional separator) is (default '.')
    """.format(_sup.version, _sup.maxchr)

__all__ = ['rebase', 'guess', 'in_decimal', 'num_digits', # this file
           'to_base', 'to_ten',
           'mpf', 'mpc', 'set_precision', 'set_digitset', # support file
           'version', 'backend', 'max_base', 'numStor',
           'roman', 'roman_to', 'named_bases',            # nonstandard file
           'factorial', 'factorial_to',
           ]

# from support file
mpf, mpc = _sup.mpf, _sup.mpc
backend = _sup.backend
set_precision = _sup.set_prec
set_digitset = _sup.set_digitset
max_base = _sup.maxchr
numStor = _sup.numStor
version = _sup.version

# from nonstandard file
roman = _nsd.to_ro
roman_to = _nsd.ro_to
factorial = _nsd.to_fc
factorial_to = _nsd.fc_to
named_bases = list(_nsd.nstd_bases.keys())
prime_gen = _nsd._pgen


def rebase(num, b1, b2, **kwargs):
    """
    Convert a number from base b1 to base b2

    Base inputs can be numeric strings (i.e. "-13.93486") to insure precision
    and can contain 'i' or 'j' to signify that they are imaginary values. Bases
    may additionally be names ('roman') to access nonstandard or mixed radix
    bases - see 'named_bases' for full list

    number input can be a numeric type (int, float, complex, mpc, mpf),
    strings, or two length tuples (for real, imag values)

    output - string if no imaginary value
           - namedtuple if imaginary value (see numStor)
           - int, long, float, complex, mpc or mpf type
             if as_numeric is True and b2 is 10 (regardless of digitset order)
    keywords:
        sgn - what character the negative sign is
              default '-'
        sep - what character the radix point (fractional separator) is
              default '.'
        as_numeric - return will be a python numeric type if b2 is 10
              default False
        joke_bases - True/False - allow bases 1, 0, -1 to be valid
              default False
    """
    jokes = kwargs.get('joke_bases')
    # if the number is zero, why do any math? return a zero
    if not jokes and not num: return _sup.digitset[0]

    # parse input
    real, imag = _sup.parse_input(num)
    b1, b2 = _sup.parse_base(b1), _sup.parse_base(b2)

    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')

    E1 = ValueError('invalid input base')
    E2 = ValueError('invalid output base')

    # convert input from base b1 to base ten (outputs here are numerical)
    if jokes and b1 in _nsd.joke_bases:             # joke bases
        jb = _nsd.joke_bases.get(b1)[1]
        res = jb(real, **kwargs)
        ult = '' if not imag else jb(imag, **kwargs)
        val10 = res if not ult else (res + ult * mpc(0, 1))
    elif b1 in (1, 0, -1):                          # invalid bases
        raise E1
    elif _sup.str_(b1).lower() in _nsd.nstd_bases:  # custom bases
        nsd_to = _nsd.nstd_bases.get(_sup.str_(b1).lower())[1]
        res = nsd_to(real, **kwargs)
        try: ult = nsd_to(imag, **kwargs)
        except AttributeError: ult = ''
        val10 = res if not ult else (res + ult * mpc(0, 1))
    elif ((b1.real and not b1.imag) or              # real, imag bases
          (not b1.real and b1.imag)):
        val10 = to_ten(num, b1, **kwargs)
    else:  # complex base, base 0
        raise E1

    # return as a numeric type
    if kwargs.get('as_numeric') and b2 == 10: return val10

    # convert base ten value to base b2 (outputs here will be lists)
    if jokes and b2 in _nsd.joke_bases:             # joke bases
            jb = _nsd.joke_bases.get(b2)[0]
            res = jb(val10.real, **kwargs)
            ult = jb(val10.imag, **kwargs)
    elif _sup.str_(b2).lower() in _nsd.nstd_bases:# custom bases
        to_nsd = _nsd.nstd_bases.get(_sup.str_(b2).lower())[0]
        res = to_nsd(val10.real, **kwargs)
        ult = to_nsd(val10.imag, **kwargs)
    elif ((b2.real and not b2.imag) or            # real, imag bases
          (not b2.real and b2.imag)):
        res = to_base(val10, b2, **kwargs)
        ult = 0
    else:                                         # complex base, base 0
        raise E2

    result = res if ult in _sup.zero_types else numStor(res, ult)
    return result

def to_base(x, b, **kwargs):
    """convert a base ten numeric value x to positional base b
    only handles positional bases - use rebase for nonpositional bases
    return a string
    (unless given base and converted digit is larger than available characters,
    then returns a list)
    """
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    x, b = _sup.parse_base(x), _sup.parse_base(b)

    if kwargs.get('as_numeric') and b == 10:
        return to_ten(x, 10, **kwargs)

    lts, tr, ti = _sup.lst_to_str, _std.to_rb, _std.to_ib
    E = ValueError('invalid base')
    if b in (1, 0, -1):                            # invalid bases
        raise E
    elif b.real and not b.imag:                    # real bases
        if not x.imag:
            res, ult = lts(tr(x, b, **kwargs), sgn, sep), 0
        else:
            res = lts(tr(x.real, b, **kwargs), sgn, sep)
            ult = lts(tr(x.imag, b, **kwargs), sgn, sep)
    elif not b.real and b.imag:                    # imaginary bases
        res = lts(ti(mpc(x.real, x.imag), b, **kwargs), sgn, sep)
        ult = lts([0], sgn, sep)  # i base values have no i part
    else: raise E

    return res if ult in _sup.zero_types else numStor(res, ult)

def to_ten(x, b, **kwargs):
    """convert a string x in positional base b to base ten
    only handles positional bases - use rebase for nonpositional bases
    always returns a python numeric type
    """
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    real, imag = _sup.parse_input(x)
    b = _sup.parse_base(b)

    E = ValueError('invalid base')
    if b in (1, 0, -1):                            # invalid bases
        raise E
    elif b.real and not b.imag:                    # real bases
        res = _std.to_10(real, b, **kwargs)
        ult = _std.to_10(imag, b, **kwargs)
        result = res if not ult else (res + ult * mpc(0, 1))
    elif not b.real and b.imag:                    # imaginary bases
        result = _std.to_10(real, b, **kwargs)
    else: raise E
    return result

def in_decimal(num, sgn='-', sep='.', as_str=False):
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

def num_digits(base):
    "returns the number of characters a base uses"
    if base.imag: base = base * mpc(base.real, -base.imag); base = base.real
    base = abs(base)  # can't use .conjugate(), gmpy2 2.0.8 will crash

    E, one = ValueError('invalid base'), mpf(1)
    if base == 0: return 0  # not actually a base
    elif 0 < base < 1: return int(_sup.ceil(one / base))
    elif base == 1: return 1  # same with this one
    elif base > 1: return int(_sup.ceil(base))
    else: raise E

def available_bases():  # does this make any sense to have?
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

def base_prec(prec, newbase, oldbase=2):
    "gives precision in new base"
    if newbase.imag: newbase *= mpc(newbase.real, -newbase.imag)
    if oldbase.imag: oldbase *= mpc(oldbase.real, -oldbase.imag)
    return int(prec * abs(_sup.log(abs(oldbase), abs(newbase))))
