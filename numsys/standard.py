"standard base conversion functions"
import support as _sup

log, floor, ceil = _sup.log, _sup.floor, _sup.ceil
cmplx, decml = _sup.cmplx, _sup.decml


def to_zb(num, base, sgn='-'):  # to integer base (Z)
    """
    converts an integer from base ten to base (integer and abs(base) > 1)
    returns a list
    """
    if not num: return [0]
    E = ValueError('invalid base')
    if abs(base) < 2:
        raise E
    
    num, lst, base = int(num), [], int(base)
    if num < 0 and base > 0: num *= -1; lst = [sgn]  # negatives in +bases
    
    while num:
        num, d = divmod(num, base)
        if d < 0: num += 1; d -= base   # values in -bases
        lst.append(d)
    lst.reverse()  
    return lst

def to_pb(num, base, sgn='-', sep='.'):  # to Positive base
    """
    converts a real in base 10 to base (real and > 1)
    returns a list
    """
    # use integer conversion when both are integers (faster)
    if int(num) == num and int(base) == base: return to_zb(num, base, sgn)
    
    if not num: return [0]
    E = ValueError('invalid base')
    if base <= 1:
        raise E

    num, base = decml(num), decml(base) # to insure precision
    if num < 0: lst = [sgn]; num = -num  # handle negative values
    else: lst = []
    
    P = ceil(log(abs(num), base)); X = num / base ** P  # setup stuff
    #while not 0 <= X < 1: P += 1; X = num / base ** P  # log should cover this
    def T(x): return base * x - floor(base * x)  # transformation function

    if P <= 0:  # if starting with a fractional value
        lst.extend([0, sep])
        lst.extend(([0] * -int(P)))

    prc = _sup.prec
    prc = int(prc * log(2, base))  # insure precision is in new base
    prc = P - prc  # go only as far as precision is good
    if prc >= 0: prc = -1  # but in this event, go as far as B^-1

    while P > prc:  # conversion step
        d = int(floor(X * base))  # get digit
        X = T(X)
        if P == 0 and sep not in lst:  # don't add it if its already there!
            lst.append(sep)
        lst.append(d)  # store digit
        P -= 1
    return lst

def to_nb(num, base, sgn='-', sep='.'):  # to Negative base
    """
    converts a real from base 10 to base (real and < -1)
    returns a list
    """
    # use integer conversion when both are integers (faster)
    if int(num) == num and int(base) == base: return to_zb(num, base, sgn)
    
    if num == 0: return [0]
    E = ValueError('invalid base')
    if base >= -1:
        raise E

    num, base, one = decml(num), abs(decml(base)), decml(1)
    # ref. defines method for -base where base > 0

    prc = _sup.prec
    P, lst = int(floor(log(abs(num), base))), []
    l, r, X = -base / (base + one), 1 / (base + one), num
    while not l <= X < r:  # P is better determined here
        P += 1             # the log taken above just speeds it up
        X = num / (-base) ** P
    def T(x): return -base * x - floor(-base * x - l)
    
    if P <= 0:  # starting with a fractional value
        lst.extend([0, sep])
        lst.extend(([0] * -int(P)))

    #this appears to work for negative bases so I'm going with it
    prc = int(prc * log(2, abs(base)))
    prc = -1 if (P - prc) >= 0 else (P - prc)

    while P >= prc:  # conversion step
        d = int(floor(-base * X - l))
        X = T(X)
        if P == 0 and sep not in lst: lst.append(sep)  # add sep only once
        if d == base: lst.extend([d - 1, 0])  # if this happens, you do this
        else: lst.append(d)
        P -= 1
    return lst

def to_vb(num, base, sgn='-', sep='.'):  # to inVerted base
    """
    converts a real from base ten to base (abs(base) < 1 and base != 0)
    returns a list
    """
    if not abs(base) < 1 or base == 0:
        E = ValueError('invalid base')
        raise E

    # for a base 0<b<1: convert to base 1/b,
    #  shift radix to the left one column and swap all the digits
    inv = decml(1) / decml(base)  # invert the base, convert to base 1/B
    if int(num) == num and int(inv) == inv: ans = to_zb(num, inv, sgn)
    elif base < 0: ans = to_nb(num, inv, sgn, sep)
    else: ans = to_pb(num, inv, sgn, sep)

    add_sgn = False  # handle negative values cleanly
    if sgn in ans: ans.remove(sgn); add_sgn = True

    try: shift = ans.index(sep) - 1; ans.remove(sep)
    except ValueError: shift = -1  # handle radix point
    ans.insert(shift, sep); ans.reverse()
    if add_sgn: ans.insert(0, sgn)
    return ans

def to_rb(num, base, sgn='-', sep='.'):  # to Real base
    """
    converts a real number in base ten to a real base
    num may be a int, float, mpc or string (digits 0-9 only)
    returns a list
    ties to_zb, to_pb, to_nb, to_vb into one function
    """
    E = ValueError('invalid base')
    num, base = decml(num), decml(base)
    if base < -1: ans = to_nb(num, base, sgn, sep)
    elif 0 < abs(base) < 1: ans = to_vb(num, base, sgn, sep)
    elif base > 1: ans = to_pb(num, base, sgn, sep)
    else: raise E
    return ans

def to_ib(num, base, sgn='-', sep='.'):  # to Imaginary base
    """
    converts a complex number from base ten to imaginary base
    where base.real == 0 and base.imag != 1 or 0
    returns a list
    """
    E = ValueError('invalid base')
    if base.real != 0:
        raise E
    
    # split input into real and imag parts
    try: real, imag = num.real, num.imag  # numeric types, named tuple
    except AttributeError:
        if len(num) == 2:  # normal tuple, list of lists
            real, imag = num 
        else:  # possibly a string
            real, imag = num, 0
    
    # convert real and imag parts to effective base
    eb = -(abs(base) ** 2)
    if abs(base.imag) > 1:
        real = to_nb(real, eb, sgn, sep)
        imag = to_nb(decml(imag) / decml(base.imag), eb, sgn, sep)
    elif 0 < abs(base.imag) < 1:
        real = to_vb(real, eb, sgn, sep)
        imag = to_vb(decml(imag) / decml(base.imag), eb, sgn, sep)
    else: raise E

    # split into whole and fractional parts
    if sep in real:
        i = real.index(sep)
        wr, fr = real[:i], real[i + 1:]
    else: wr, fr = real, [0]
    if sep in imag:
        i = imag.index(sep)
        wi, fi = imag[:i], imag[i + 1:]
    else: wi, fi = imag, [0]

    # interweave the parts (http://stackoverflow.com/q/24583017)
    wr, wi = list(wr), list(wi)  # whole part
    r, i = len(wr), len(wi)  
    l = 2 * max(r, i); ans = [0] * l
    ans[l - 2 * r + 1:: 2] = wr
    ans[l - 2 * i:: 2]  = wi
    ans.append(sep)

    fr, fi = list(fr), list(fi)  # fractional part
    r, i = len(fr), len(fi)
    frc = [0] * (2 * max(i, r))
    frc[1: 2 * r: 2] = fr
    frc[0: 2 * i: 2] = fi
    ans.extend(frc)
    return ans

def to_10(num, base, sgn='-', sep='.'):
    """
    converts a number from given base to base ten
    not valid for nonstandard bases
    """
    # verifiy input
    if type(num).__name__ in _sup.str_types:
        num = _sup.str_to_lst(num, sgn, sep)
    elif type(num) == list: pass
    else: return num
    
    if base.imag:  # imag/complex bases
        s, ans, base = 1, cmplx(0), cmplx(base)
    elif int(base) == base and sep not in num:  # integer bases
        s, ans, base = 1, 0, int(base)
    else:  # real bases
        s, ans, base = 1, decml(0), decml(base)
    if sgn in num: num.remove(sgn); s = -1  # handle negatives

    # determine order of magnitude
    try: P = num.index(sep) - 1; num.remove(sep)  # floats
    except: P = len(num) - 1  # ints, longs

    # find max allowed character for base
    if base.imag: chk = abs(base * cmplx(base.real, -base.imag))  # can't use .conjugate(), gmpy2 2.0.8 crashes
    else: chk = abs(base)

    # error checking
    E = ValueError('invalid base')  # invalid bases 0 or 1
    if 0 < chk < 1: chk = int(ceil(decml(1) / chk))
    elif chk > 1: chk = int(ceil(chk))
    else: raise E
    if max(num) >= chk:  # invalid characters
        mes = _sup.str_('invalid character for base {}').format(base)
        try:  # unprintable SyntaxError object?
            errant = _sup.digitSet[max(num)]
            E = SyntaxError((mes + ': {}').format(errant))
        except IndexError:  # if it gets here, digit is greater than base
            E = SyntaxError(mes)  # and digitSet does not have that character
        raise E

    for d in num:  # conversion step (this is the definition of a base)
        ans += (d * base ** P); P -= 1
    return s * ans
