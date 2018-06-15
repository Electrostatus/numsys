"non-standard base conversion functions"
import support as _sup
from os import urandom  # used in ze_to

nstd_bases = {}  # {'name': [func from 10 to base, func from base to 10]}

## --------------- base one --------------------------------
def to_p1(num, sgn='-'):
    "converts an integer in base ten to base one"
    if num < 0: return sgn + (_sup.digitSet[1] * int(-num))
    elif num > 0: return _sup.digitSet[1] * int(num)
    else: return ''

def p1_to(num, sgn='-'):
    "converts a base one value to base ten"
    if sgn in num: return -(len(num) - 1)
    else: return len(num)


## --------------- base negative one -----------------------
def to_n1(num):
    "converts an integer in base ten to base negative one"
    if num > 0: return _sup.digitSet[1] * (int(num) * 2 - 1)
    elif num < 0: return _sup.digitSet[1] * (-int(num) * 2)
    else: return ''

def n1_to(num):
    "converts a base negative one value to base ten"
    l = len(num)
    if not l % 2: return -l // 2
    else: return l // 2 + 1


## --------------- base zero -------------------------------
def to_ze(num):
    "converts any number in base ten to base zero"
    return ''

def ze_to(num):
    "converts a base zero value to base ten"
    E1 = SyntaxError('base zero does not use any characters')
    class BaseZero(ZeroDivisionError): pass  # ice cream koan
    
    E2_errs = ['Makes you think, doesn\'t it?', 'Wait, what?', 'Crazy, huh?', 
               'It\'s somewhat Zen, but not really', 'It\'s utter nonsense',
               'You thought this would actually return something?', 'error!',
               '...Clever girl *killed by raptors*', 'Confused? Try again.',
               ]
    try:
        n = hash(urandom(9))
        E2 = BaseZero(E2_errs[int(abs(n)) % len(E2_errs)])
    except Exception:
        E2 = BaseZero(E2_errs[5])
        
    if num == '' or num is None:
        raise E2
    else: raise E1
    return  # if it got here (and it shouldn't) return nothin'


## --------------- roman numerals --------------------------
_rmap = (#('Q', 500000), ('MQ', 499000),  # roman numeral extension
         ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
         ('C', 100),  ('XC', 90),  ('L', 50),  ('XL', 40),
         ('X', 10),   ('IX', 9),   ('V', 5),   ('IV', 4), ('I', 1))

def to_ro(n, *args):  # args is just to generalize input, none are used
    "coverts a base ten integer to roman numerals"
    #if not n: return 'nulla'  # zero extension
    romu, i = [], abs(n)
    for r, j in _rmap:
        k = i // j; i -= j * k
        romu.append(r * k)
    return ''.join(romu)

def ro_to(n, *args):
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

    sgn = sgn if x < 0 else ''
    n, one = abs(x), _sup.decml(1)
    whl, frc = int(n), _sup.decml(n) - int(n)

    ans, f = [], 1
    while whl:  # whole part
        whl, d = divmod(whl, f)
        ans.append(d); f += 1
    ans.reverse()

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
    ans = 0 if is_int else _sup.decml(0)
    one = _sup.decml(1)

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
            try: E = SyntaxError(_sup.str_(err1a).format(digitSet[j], i))
            except IndexError: E = SyntaxError(err1b.format(i))
            raise E
        if k > i:  # fractional value error checking
            try: E = SyntaxError(_sup.str_(err2a).format(digitSet[k], i))
            except IndexError: E = SyntaxError(err2b.format(i))
            raise E

        ans += j * f
        if not is_int: ans += k * (one / f)
        i += 1; f *= i
    return ans * neg

nstd_bases['factorial'] = [to_fc, fc_to]
nstd_bases['f'] = [to_fc, fc_to]

    
