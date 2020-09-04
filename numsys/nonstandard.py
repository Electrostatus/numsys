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
                   must accept three inputs in this order:
                   x (the numeric input), sgn='-', sep='.'
    func_from_base - function that converts a string input to base
                     must accept three inputs in this order:
                     x (the string input), sgn='-', sep='.'
    """
    global nstd_bases
    nstd_bases[name] = [func_to_base, func_from_base]

## --------------- base one --------------------------------
def to_p1(n, sgn='-', sep='.'):
    "converts an integer in base ten to base one"
    if n < 0: return sgn + (_sup.digitSet[1] * int(-n))
    elif n > 0: return _sup.digitSet[1] * int(n)
    else: return ''

def p1_to(n, sgn='-', sep='.'):
    "converts a base one value to base ten"
    if sgn in n: return -(len(n) - 1)
    else: return len(n)


## --------------- base negative one -----------------------
def to_n1(n, sgn='-', sep='.'):
    "converts an integer in base ten to base negative one"
    if n > 0: return _sup.digitSet[1] * (int(n) * 2 - 1)
    elif n < 0: return _sup.digitSet[1] * (-int(n) * 2)
    else: return ''

def n1_to(n, sgn='-', sep='.'):
    "converts a base negative one value to base ten"
    l = len(n)
    if not l % 2: return -l // 2
    else: return l // 2 + 1


## --------------- base zero -------------------------------
def to_ze(x, sgn='-', sep='.'):
    "converts any number in base ten to base zero"
    return ''

_zn = [0]
class BaseZero(ZeroDivisionError): pass  # ice cream koan

def ze_to(x, sgn='-', sep='.'):
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
               'Am I an ice cream koan? or am I not an ice cream koan?',
               ]
    try:
        n = int(abs(hash(urandom(9)))) % len(E2_errs)
        while n in _zn: n = int(abs(hash(urandom(9)))) % len(E2_errs)
        _zn.append(n)  # random, but no immediate repeats
        if len(_zn) > 3: _zn = _zn[-3:]
        E2 = BaseZero(E2_errs[n])
    except Exception:
        E2 = BaseZero(E2_errs[5])
        
    if x == '' or x is None:
        raise E2
    else: raise E1
    return  # if it got here (and it shouldn't) return nothin'


## --------------- roman numerals --------------------------
_rmap = (#('Q', 500000), ('MQ', 499000),  # roman numeral extension
         ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
         ('C', 100),  ('XC', 90),  ('L', 50),  ('XL', 40),
         ('X', 10),   ('IX', 9),   ('V', 5),   ('IV', 4), ('I', 1))

def to_ro(n, sgn='-', sep='.'):
    "coverts a base ten integer to roman numerals"
    #if not n: return 'nulla'  # zero extension
    romu, i = [], abs(n)
    for r, j in _rmap:
        k = int(i // j); i -= j * k
        romu.append(r * k)
    return ''.join(romu)

def ro_to(n, sgn='-', sep='.'):
    "converts roman numerals to a base ten integer"
    #if n == 'nulla': return 0  # zero extension
    ans = i = 0; n = n.upper()
    for r, j in _rmap:
        while n[i: i + len(r)] == r: ans += j; i += len(r)
    return ans

nstd_bases['roman'] = [to_ro, ro_to]
nstd_bases['r'] = [to_ro, ro_to]


## --------------- factorial base --------------------------
def to_fc(x, sgn='-', sep='.'):
    "converts any number in base ten to factorial base\nreturns a string"
    # largest value that can be made using N digits is (N*N!)-1
    if not x: return _sup.digitSet[0]

    n, one = abs(x), _sup.mpf(1)
    whl, frc = int(n), _sup.mpf(n) - int(n)

    ans, f = [], 1
    while whl:  # whole part
        whl, d = divmod(whl, f)
        ans.append(d); f += 1
    ans.reverse()
    if x < 0: ans.append(sgn)

    if not frc: return _sup.lst_to_str(ans, sgn, sep)  # is an integer

    # fractional part
    prc = -int(_sup.log(frc, 10)) + 20  # this is a total guess
    ans.append(sep); f = i = 1
    while prc > 0:
        d, frc = divmod(frc, one / f)
        ans.append(int(d))
        f *= i; i += 1; prc -= 1
    return _sup.lst_to_str(ans, sgn, sep)

def fc_to(n, sgn='-', sep='.'):
    "converts a factorial base number to base ten"
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

    # error messages
    err1a = 'invalid character \'{}\' at position {}! for factorial base'
    err1b = 'invalid character at position {}! for factorial base'
    err2a = 'invalid character \'{}\' at position 1/{}! for factorial base'
    err2b = 'invalid character at position 1/{}! for factorial base'

    f, i = 1, 0
    for j, k in zip(whl[::-1], frc):
        if j > i:  # whole value error checking
            try: E = SyntaxError(_sup.str_(err1a).format(_sup.digitSet[j], i))
            except IndexError: E = SyntaxError(err1b.format(i))
            raise E
        if k > i:  # fractional value error checking
            try: E = SyntaxError(_sup.str_(err2a).format(_sup.digitSet[k], i))
            except IndexError: E = SyntaxError(err2b.format(i))
            raise E

        ans += j * f
        if not is_int: ans += k * (one / f)
        i += 1; f *= i
    return ans * neg

nstd_bases['factorial'] = [to_fc, fc_to]
nstd_bases['f'] = [to_fc, fc_to]

# add primorial and fibonacci bases?



## --------------- general mixed base ---------------------
def _to_mixed(x, generator, sgn='-', sep='.', gen_inputs={}):
    """converts any number in base ten to a mixed base
    this is a generalized form, do not call directly
    gen_inputs are a dictionary of input flags fed to the generator
    generator is a function that gives the mixed base digits via next()
    """
    if not x: return [0]

    n, one = abs(x), _sup.mpf(1)
    whl, frc = int(n), _sup.mpf(n) - int(n)
    
    gw = generator(**gen_inputs); b = next(gw) 
    while not b: b = next(gw)  # base can't start at zero

    ans = [sgn] if x < 0 else []
    while whl:  # whole part
        whl, d = divmod(whl, b)
        ans.append(d); b = next(gw)
    ans.reverse()

    if not frc: return ans  # is an integer
    prc = -int(_sup.log(frc, 10)) + 20  # this is a total guess
    ans.append(sep)
    
    gf = generator(**gen_inputs); b = next(gf)
    while not b: b = next(gf)

    while prc > 0:  # fractional part
        d, frc = divmod(frc, one / b)
        ans.append(int(d))
        b *= next(gf); prc -= 1
    return ans


def count(start=0, step=1):
    "counting generator"
    while 1: yield start; start += step

def fib():
    "fibonacci sequence generator"
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b

def gfib(n=0):
    "generalized fibonacci sequence generator"
    n = abs(n) + 1
    fseq = [0] * n + [1]
    while 1:
        f = sum(fseq[-(n + 1):])
        fseq.append(f); yield fseq.pop(0)
