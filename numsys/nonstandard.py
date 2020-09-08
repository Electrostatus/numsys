"non-standard base conversion functions"
try: import support as _sup
except ImportError: from numsys import support as _sup
from os import urandom  # used in ze_to

nstd_bases = {}  # {'name': [func from 10 to base, func from base to 10]}

# functions all take a number, sgn and sep - but not all are used
# this is to generalize the input and make it easy to call from
# nstd_bases; i.e. value = nstd_bases[name][0](number, sgn, sep)

def addBase(name, func_to_base, func_from_base):
    """
    adds a base to list of nonstandard or custom number bases
    name - lowercase string of base name
    func_to_base - function that converts a numeric input to base
                   must accept one input and keywords:
                   x (the numeric input), **kwargs
    func_from_base - function that converts a string input to base
                     must accept one inputs and keywords:
                     x (the string input), **kwargs
    """
    global nstd_bases
    nstd_bases[name] = [func_to_base, func_from_base]

joke_bases = {}

## --------------- base one --------------------------------
def to_p1(n, **kwargs):
    "converts an integer in base ten to base one"
    sgn = kwargs.get('sgn', '-')
    if n < 0: return sgn + (_sup.digitSet[1] * int(-n))
    elif n > 0: return _sup.digitSet[1] * int(n)
    else: return ''

def p1_to(n, **kwargs):
    "converts a base one value to base ten"
    sgn = kwargs.get('sgn', '-')
    print(n, len(n))
    if sgn in n: return -(len(n) - 1)
    else: return len(n)

joke_bases[1] = [to_p1, p1_to]

## --------------- base negative one -----------------------
def to_n1(n, **kwargs):
    "converts an integer in base ten to base negative one"
    if n > 0: return _sup.digitSet[1] * (int(n) * 2 - 1)
    elif n < 0: return _sup.digitSet[1] * (-int(n) * 2)
    else: return ''

def n1_to(n, **kwargs):
    "converts a base negative one value to base ten"
    l = len(n)
    if not l % 2: return -l // 2
    else: return l // 2 + 1

joke_bases[-1] = [to_n1, n1_to]

## --------------- base zero -------------------------------
def to_ze(x, **kwargs):
    "converts any number in base ten to base zero"
    return ''

_zn = [0]
class BaseZero(ZeroDivisionError): pass  # ice cream koan

def ze_to(x, **kwargs):
    "converts a base zero value to base ten"
    E1 = SyntaxError('base zero does not use any characters')
    global _zn

    E2_errs = ['Makes you think, doesn\'t it?', 'Wait, what?', 'Crazy, huh?',
               'It\'s somewhat Zen, but not really', 'It\'s utter nonsense',
               'You thought this would actually return something?', 'error!',
               '...Clever girl *killed by raptors*', 'Confused? Try again.',
               'You spent your nickle, we\'re done!', ('Well summer\'s over,'
               ' the bonfires are dying down, the explosives are packed '#mst3k
               'away and the last rabid dog has been shot.'), 'Huh?!??1?one',
               'Try our sister base, base negative zero!', 'error? err-ror?',
               'What? Were you thinking this was an actual operating base?',
               'Exactly squat, sir.', ('Perhaps you\'re wondering who I am,'
               ' what I\'m doing here, why I have a picture of a burger '
               'on the wall.'), 'Is confusing. It! It! \'It\' is confusing!',
               ]
    try:
        n = int(abs(hash(urandom(9)))) % len(E2_errs)
        while n in _zn: n = int(abs(hash(urandom(9)))) % len(E2_errs)
        _zn.append(n)  # random, but no immediate repeats
        if len(_zn) > 4: _zn = _zn[-4:]
        E2 = BaseZero(E2_errs[n])
    except Exception:
        E2 = BaseZero(E2_errs[5])

    if x == '' or x is None:
        raise E2
    else: raise E1
    return  # if it got here (and it shouldn't) return nothin'

joke_bases[0] = [to_ze, ze_to]

## --------------- roman numerals --------------------------
_rmap = (#('Q', 500000), ('MQ', 499000),  # roman numeral extension
         ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
         ('C', 100),  ('XC', 90),  ('L', 50),  ('XL', 40),
         ('X', 10),   ('IX', 9),   ('V', 5),   ('IV', 4), ('I', 1))

def to_ro(n, **kwargs):
    "coverts a base ten integer to roman numerals"
    #if not n: return 'nulla'  # zero extension
    romu, i = [], abs(n)
    for r, j in _rmap:
        k = int(i // j); i -= j * k
        romu.append(r * k)
    return ''.join(romu)

def ro_to(n, **kwargs):
    "converts roman numerals to a base ten integer"
    #if n == 'nulla': return 0  # zero extension
    ans = i = 0; n = n.upper()
    for r, j in _rmap:
        while n[i: i + len(r)] == r: ans += j; i += len(r)
    return ans

nstd_bases['roman'] = [to_ro, ro_to]


## --------------- general mixed base ---------------------
# these are not general enough for negative mixed radixes or floats
# which, as far as I can tell, have not been attempted or thought of yet
# it skips any starting zeros (may crash if there's zeros in the middle)
# ones also don't really work (it'll be okay if theres not many of them)
#
# because it skips starting zeros, factorial base won't have 0! or 1/0!
# positions - likewise for the fibonacci bases
# possibly spin these out into a seperate file later - mixed.py
def _to_mixed(x, generator, **kwargs):
    """converts any number in base ten to a mixed base
    this is a generalized form, do not call directly
    gen_args are a dictionary of input flags fed to the generator
    generator is a function that gives the mixed base digits via next()
    """
    if not x: return [0]

    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    gen_args = kwargs.get('gen_args', {})

    n, one = abs(x), _sup.mpf(1)
    whl = int(n)
    if whl != n: frc = _sup.mpf(n) - int(n)
    else: frc = 0  # if not enough precision, a "fraction" might appear

    gw = generator(**gen_args); b = next(gw)
    while not b: b = next(gw)  # base can't start at zero

    ans = [sgn] if x < 0 else []
    while whl:  # whole part
        whl, d = divmod(whl, b)
        ans.append(d); b = next(gw)
    ans.reverse()

    if not frc: return ans  # is an integer
    prc = -int(_sup.log(frc, 10)) + 1 + _sup.prec // 7 # this is a total guess
    ans.append(sep)

    gf = generator(**gen_args); b = next(gf)
    while not b: b = next(gf)

    while prc > 0:  # fractional part
        d, frc = divmod(frc, one / b)
        ans.append(int(d))
        b *= next(gf); prc -= 1
    return ans

def _mixed_to(n, generator, **kwargs):
    """converts a mixed radix number to base ten
    this is a generalized form, do not call directly
    flags: sgn='-', sep='.', gen_args={}, sym='', name=''
    gen_args are a dictionary of input flags fed to the generator
    generator is a function that gives the mixed base digits via next()
    """
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    gen_args = kwargs.get('gen_args', {})
    lst = _sup.str_to_lst(n, sgn, sep)

    try:  # split into whole, fractional parts
        pt = lst.index(sep)
        whl, frc = lst[:pt], lst[pt + 1:]
    except ValueError: whl, frc = lst, []

    try: whl.remove(sgn); neg = -1
    except ValueError: neg = 1

    is_int = True if not frc else False # answer will be an integer
    ans = 0 if is_int else _sup.mpf(0)
    one = _sup.mpf(1)

    mx = len(max(whl, frc, key=len))
    whl = [0] * (mx - len(whl)) + whl
    frc.extend([0] * (mx - len(frc)))

    gen = generator(**gen_args); i = next(gen); b = 1
    while not i: i = next(gen)  # base can't start at zero

    # error messages
    err1a = 'invalid character \'{{}}\' at position {{}}{} for {}base'
    err1b = 'invalid character at position {{}}{} for {}base'
    err2a = 'invalid character \'{{}}\' at position 1/{{}}{} for {}base'
    err2b = 'invalid character at position 1/{{}}{} for {}base'

    sym = kwargs.get('sym', '')  # symbol, if any, for base (! for factorial)
    name = kwargs.get('name', '')  # name of base
    err1a = err1a.format(sym, name + (' ' if name else ''))
    err1b = err1b.format(sym, name + (' ' if name else ''))
    err2a = err2a.format(sym, name + (' ' if name else ''))
    err2b = err2b.format(sym, name + (' ' if name else ''))

    for idx, (j, k) in enumerate(zip(whl[::-1], frc)):
        if j >= i:  # whole value error checking
            try: E = SyntaxError(_sup.str_(err1a).format(_sup.digitSet[j], idx))
            except IndexError: E = SyntaxError(err1b.format(i))
            raise E
        if k >= i:  # fractional value error checking
            try: E = SyntaxError(_sup.str_(err2a).format(_sup.digitSet[k], idx))
            except IndexError: E = SyntaxError(err2b.format(i))
            raise E

        # the actual conversion process
        ans += j * b
        if not is_int: ans += k * (one / (b * i))
        b *= i; i = next(gen)
    return ans * neg


## --------------- generators ------------------------------
def _const(n=10):
    "constant generator"
    while 1: yield n

def _count(start=0, step=1):
    "counting generator"
    while 1: yield start; start += step

def _gfib(n=0):
    "generalized fibonacci sequence generator"
    n = abs(n) + 1
    fseq = [0] * n + [1]
    while 1:
        f = sum(fseq[-(n + 1):])
        fseq.append(f); yield fseq.pop(0)

def _wpps():
    """2-7 wheel postponed prime sieve, yields prime and wheel index
    do not call this directly, instead call pgen
    modified from https://stackoverflow.com/a/32803201"""
    c = 11; gps = (2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6,
    8, 4, 2, 4, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2,
    4, 2, 10, 2, 10)

    yield c, 0; m = {}; o = m.pop
    s = _wpps(); p, x = next(s)
    q = p * p; g = len(gps) - 1
    i = j = k = 0
    def y(x): return 0 if x > g else x

    while 1:
        c += gps[i]; i = y(i + 1)
        b, j = o(c, (0, 0))
        if not b:
            if c < q: yield c, i; continue
            else: j = k; b = p; p, k = next(s); q = p * p
        d = c + b * gps[j]; j = y(j + 1)
        while d in m: t = b * gps[j]; j = y(j + 1); d += t
        m[d] = (b, j)

def _pgen(amt=None):
    """prime generator
    for an indefinite amount of primes, leave amt as None"""
    init = (2, 3, 5, 7)  # dependent on what wheel is used
    if not amt:
        for p in init: yield p
        for p, i in _wpps(): yield p
    else:  # not using yield from as that won't work in python 2
        a = abs(int(amt))  # even though it's depreciated as of this writing
        if a <= len(init):  # (sept-2020) # note, make v1.0 work in both 2 and 3
             for p in init[:a]: yield p  # then move to just making it work in 3
        else:
            for p in init: yield p
            c = len(init); w = _wpps()
            while c < a: p, i = next(w); yield p; c += 1

def _catalan():
    "catalan number generator"
    ni, i = 1, 0; nj, j = 1, 1; nk, k = 1, 0
    while 1:
        yield ni // (nj * nk)
        i += 1; ni *= i; i += 1; ni *= i
        j += 1; nj *= j; k += 1; nk *= k

def _lucas():
    "lucas number generator"
    l = [2, 1]
    while 1:
        l.append(sum(l))
        yield l.pop(0)

def _noble():
    "yields full nucleon shell levels (\"Magic\")"
    i = 0  # https://en.wikipedia.org/wiki/Magic_number_(physics)
    mgc = lambda n: (2*n**3 + 12*n**2 + 25*n - 6 + (-1)**n*(3*n + 6))//12
    while 1:
        yield mgc(i); i += 1

def _whatever(n=13):  # prime damped (but is is critically damped?)
    "I'm making up this sequence"  # made up Sat. evening, Sep 5th, 2020
    n = abs(n); n = 1 if not n else n  # only allow a finite amount of primes!
    init = list(_pgen(n))[::-1]  # backwards 'cause I can! so there!
    while 1:  # how many steps to stable for n? and what's the stable point?
        init.append(sum(init) // n)  # if this line before yield, stable
        yield init.pop(0)            # if after, then decay to 0
              # how many steps to 0 for n?

def _bell():
    "yields bell numbers"
    l = [1]
    while 1:
        yield l[-1]
        for i in range(len(l) - 1):
            l[i + 1] = l[i] + l[i + 1]
        l.insert(0, l[-1])

def _simp(n=0):
    "n-simplex number generator"
    ni = 1; i = 1  # or are these figurate numbers of triangular type?
    while i < n: ni *= i; i += 1
    f = ni; nk = 1; k = 1
    while 1:
        yield ni // (f * nk)
        ni *= i; i += 1
        nk *= k; k += 1

def _caterer():
    "yields lazy caterer's sequence (lazily!)"
    n = 0  # you're the worst caterer we've ever had!
    while 1: yield (n * n + n + 2) // 2; n += 1

def _syl():
    "sylvester's sequence generator"
    s = 1; yield 2
    while 1: s *= (s + 1); yield s + 1

def _ooze():  # ooze base requested by brother
    "the ooze base generator"
    n = 10  # starting value
    mx, stch = 10, 1  # max value and stretch
    mn, d, c = 2, 1, 1  # min value (must be > 1), decay amount, decay count
    stp, sgn = 1, -1  # step and sign
    while 1:
        for i in range(stch): yield n
        n += (stp * sgn)
        if n < 1: n = 1; sgn = -sgn; stch += stch
        if n > mx: n = mx; sgn = -sgn; c += 1
        if c >= d: mx -= 1; c = 0
        if mx < mn: mx = mn

## --------------- test base -------------------------------
def to_tn(x, **kwargs):
    "base ten to \"mixed\" base ten - only for testing"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _const, sgn=sgn, sep=sep)
    return _sup.lst_to_str(lst, sgn, sep)

def tn_to(x, **kwargs):
    "\"mixed\" base ten to base ten - only for testing"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _const, sgn=sgn, sep=sep, name='ten')
    return num

## --------------- factorial base --------------------------
def to_fc(x, **kwargs):
    "converts any number in base ten to factorial base\nreturns a string"
    # largest value that can be made using N digits is (N*N!)-1
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _count, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def fc_to(x, **kwargs):
    "converts a factorial base number to base ten"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _count, sgn=sgn, sep=sep, name='factorial', sym='!')
    return num

nstd_bases['factorial'] = [to_fc, fc_to]

## --------------- primorial base --------------------------
def to_pm(x, **kwargs):
    "converts any number in base ten to primorial base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _pgen, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def pm_to(x, **kwargs):
    "converts a primorial base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _pgen, sgn=sgn, sep=sep, name='primorial', sym='#')
    return num

nstd_bases['primorial'] = [to_pm, pm_to]

## --------------- fibonacci base --------------------------
def to_fb(x, **kwargs):
    "converts any number in base ten to fibonacci base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _gfib, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def fb_to(x, **kwargs):
    "converts a fibonacci base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _gfib, sgn=sgn, sep=sep, name='fibonacci', sym='F')
    return num

nstd_bases['fibonacci'] = [to_fb, fb_to]

## --------------- tribonacci base -------------------------
def to_fb3(x, **kwargs):
    "converts any number in base ten to tribonacci base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _gfib, sgn=sgn, sep=sep, gen_args={'n':1})
    return _sup.lst_to_str(lst, sgn, sep)

def fb3_to(x, **kwargs):
    "converts a tribonacci base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _gfib, sgn=sgn, sep=sep, name='tribonacci',
                    sym='F', gen_args={'n':1})
    return num

nstd_bases['tribonacci'] = [to_fb3, fb3_to]

## --------------- tetranacci base -------------------------
def to_fb4(x, **kwargs):
    "converts any number in base ten to tetranacci base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _gfib, sgn=sgn, sep=sep, gen_args={'n':2})
    return _sup.lst_to_str(lst, sgn, sep)

def fb4_to(x, **kwargs):
    "converts a tetranacci base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _gfib, sgn=sgn, sep=sep, name='tetranacci',
                    sym='F', gen_args={'n':2})
    return num

nstd_bases['tetranacci'] = [to_fb4, fb4_to]

## --------------- n-nacci base ----------------------------
def to_fbn(x, **kwargs):
    "converts any number in base ten to the nth-nacci base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    n = kwargs.get('n', 5)
    lst = _to_mixed(x, _gfib, sgn=sgn, sep=sep, gen_args={'n':n-2})
    return _sup.lst_to_str(lst, sgn, sep)

def fbn_to(x, **kwargs):
    "converts a tetranacci base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    n = kwargs.get('n', 5)
    num = _mixed_to(x, _gfib, sgn=sgn, sep=sep, name='n-nacci',
                    sym='F', gen_args={'n':n-2})
    return num

#nstd_bases['nnacci'] = [to_fbn, fbn_to]

## --------------- catalan base ----------------------------
def to_ct(x, **kwargs):
    "converts any number in base ten to catalan base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _catalan, sgn=sgn, sep=sep)
    return _sup.lst_to_str(lst, sgn, sep)

def ct_to(x, **kwargs):
    "converts a catalan base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _catalan, sgn=sgn, sep=sep, name='catalan', sym='C')
    return num

nstd_bases['catalan'] = [to_ct, ct_to]

## --------------- lucas base ------------------------------
def to_lc(x, **kwargs):
    "converts any number in base ten to lucas base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _lucas, sgn=sgn, sep=sep)
    return _sup.lst_to_str(lst, sgn, sep)

def lc_to(x, **kwargs):
    "converts a lucas base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _lucas, sgn=sgn, sep=sep, name='lucas', sym='L')
    return num

nstd_bases['lucas'] = [to_lc, lc_to]

## --------------- magic base ------------------------------
def to_nb(x, **kwargs):
    "converts any number in base ten to noble base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _noble, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def nb_to(x, **kwargs):
    "converts a noble base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _noble, sgn=sgn, sep=sep, name='noble', sym='N')
    return num

nstd_bases['noble'] = [to_nb, nb_to]

## --------------- ??? base --------------------------------
def to_wh(x, **kwargs):
    "converts any number in base ten to ???"  # evenually base 10
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _whatever, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def wh_to(x, **kwargs):
    "converts a ??? base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _whatever, sgn=sgn, sep=sep, name='???', sym='?')
    return num

## --------------- bell base -------------------------------
def to_bl(x, **kwargs):
    "converts any number in base ten to bell base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _bell, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def bl_to(x, **kwargs):
    "converts a bell base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _bell, sgn=sgn, sep=sep, name='bell', sym='B')
    return num

nstd_bases['bell'] = [to_bl, bl_to]

## --------------- triangular base -------------------------
def to_tr(x, **kwargs):
    "converts any number in base ten to triangular base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _simp, sgn=sgn, sep=sep, gen_args={'n':3})
    return _sup.lst_to_str(lst, sgn, sep)

def tr_to(x, **kwargs):
    "converts a bell triangular number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _simp, sgn=sgn, sep=sep, name='triangular', sym='t',
                    gen_args={'n':3})
    return num

nstd_bases['triangular'] = [to_tr, tr_to]

## --------------- tetrahedral base ------------------------
def to_tt(x, **kwargs):
    "converts any number in base ten to tetrahedral base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _simp, sgn=sgn, sep=sep, gen_args={'n':4})
    return _sup.lst_to_str(lst, sgn, sep)

def tt_to(x, **kwargs):
    "converts a tetrahedral base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _simp, sgn=sgn, sep=sep, name='tetrahedral', sym='t',
                    gen_args={'n':4})
    return num

nstd_bases['tetrahedral'] = [to_tt, tt_to]

## --------------- pentatope base --------------------------
def to_pt(x, **kwargs):
    "converts any number in base ten to pentatope base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _simp, sgn=sgn, sep=sep, gen_args={'n':5})
    return _sup.lst_to_str(lst, sgn, sep)

def pt_to(x, **kwargs):
    "converts a pentatope base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _simp, sgn=sgn, sep=sep, name='pentatope', sym='p',
                    gen_args={'n':5})
    return num

nstd_bases['pentatope'] = [to_pt, pt_to]

## --------------- lazy caterer's base ---------------------
def to_yc(x, **kwargs):
    "converts any number in base ten to the lazy caterer's base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _caterer, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def yc_to(x, **kwargs):
    "converts a lazy caterer's base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _caterer, sgn=sgn, sep=sep, name='caterer', sym='c')
    return num

nstd_bases['caterer'] = [to_yc, yc_to]

## --------------- sylvester base --------------------------
def to_sy(x, **kwargs):
    "converts any number in base ten to sylvester base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _syl, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def sy_to(x, **kwargs):
    "converts a sylvester base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _syl, sgn=sgn, sep=sep, name='sylvester', sym='s')
    return num

nstd_bases['sylvester'] = [to_sy, sy_to]

## --------------- ooze base -------------------------------
# brother wanted an "ooze" base - so here's a base that slowly smears out
def to_oz(x, **kwargs):
    "converts any number in base ten to the ooze base\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    lst = _to_mixed(x, _ooze, **kwargs)
    return _sup.lst_to_str(lst, sgn, sep)

def oz_to(x, **kwargs):
    "converts an ooze base number to base ten\nreturns a string"
    sgn, sep = kwargs.get('sgn', '-'), kwargs.get('sep', '.')
    num = _mixed_to(x, _ooze, sgn=sgn, sep=sep, name='ooze', sym='o')
    return num

nstd_bases['ooze'] = [to_oz, oz_to]
