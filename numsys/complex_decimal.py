import decimal

class ComplexDecimal(object):
    "A class for handling complex values with Python's decimal module."

    def __init__(self, real=0, imag=0):
        if type(real) in (str, ):
            real = real.replace('(', '').replace(')', '')
            # 9 ways:
            #       imag
            #      +imag
            #      -imag
            #  real+imag
            #  real-imag
            # +real+imag
            # +real-imag
            # -real+imag
            # -real-imag
            if 'j' in real:  # imag value
                plus, minus = real.count('+'), real.count('-')
                if plus == 1 and minus == 1:
                    if not real.index('+'):               # +real-imag
                        real, imag = real.rsplit('-', 1); imag = '-' + imag
                    else:                                 # -real+imag
                        real, imag = real.rsplit('+', 1)
                elif plus == 1 and not real.index('+'):   # +imag
                    real, imag = 0, real
                elif minus == 1 and not real.index('-'):  # -imag
                    real, imag = 0, real
                elif plus == 1 and real.index('+'):       #  real+imag
                    real, imag = real.rsplit('+', 1)
                elif minus == 1 and real.index('-'):      #  real-imag
                    real, imag = real.rsplit('-', 1); imag = '-' + imag
                elif plus == 2:                           # +real+imag
                    real, imag = real.rsplit('+', 1)
                elif minus == 2:                          # -real-imag
                    real, imag = real.rsplit('-', 1)
                else:                                     #       imag
                    real, imag = 0, real
                self.real = decimal.Decimal(real)
                self.imag = decimal.Decimal(imag.replace('j', ''))
            else:  # real value
                self.real = decimal.Decimal(real)
                self.imag = decimal.Decimal(0)

        elif type(real) in (complex, type(self)):
            self.real = decimal.Decimal(real.real)
            self.imag = decimal.Decimal(real.imag)
        else:
            self.real = decimal.Decimal(real)
            self.imag = decimal.Decimal(imag)

    # arithmetic methods
    def __add__(self, other):
        "x.__add__(y) <==> x+y"
        other = ComplexDecimal(other)
        real = self.real + other.real
        imag = self.imag + other.imag
        return +ComplexDecimal(real, imag)

    def __sub__(self, other):
        "x.__sub__(y) <==> x-y"
        other = ComplexDecimal(other)
        real = self.real - other.real
        imag = self.imag - other.imag
        return +ComplexDecimal(real, imag)

    def __mul__(self, other):
        "x.__mul__(y) <==> x*y"
        other = ComplexDecimal(other)
        real = self.real * other.real - self.imag * other.imag
        imag = self.imag * other.real + self.real * other.imag
        return +ComplexDecimal(real, imag)

    def __div__(self, other):
        "x.__div__(y) <==> x/y"
        other = ComplexDecimal(other)
        denom = other.real * other.real + other.imag * other.imag
        real = (self.real * other.real + self.imag * other.imag) / denom
        imag = (self.imag * other.real - self.real * other.imag) / denom
        return +ComplexDecimal(real, imag)

    def __truediv__(self, other):
        "x.__truediv__(y) <==> x/y"
        return self.__div__(other)

    def __floordiv__(self, other):
        "x.__floordiv__(y) <==> x//y"
        other = ComplexDecimal(other)
        denom = other.real * other.real + other.imag * other.imag
        real = (self.real * other.real + self.imag * other.imag) // denom
        imag = (self.imag * other.real - self.real * other.imag) // denom
        return +ComplexDecimal(real, imag)

    def __mod__(self, other):
        "x.__mod__(y) <==> x%y"
        raise TypeError("can't take floor or mod of complex number.")

    def __divmod__(self, other):
        "x.__divmod__(y) <==> divmod(x, y)"
        raise TypeError("can't take floor or mod of complex number.")

    def __pow__(self, other, modulo=None):
        "x.__pow__(y[, z]) <==> pow(x, y[, z])"
        if modulo is not None:
            raise ValueError("complex modulo")

        # a shortcut for integer powers of purely real or purely imag
        if not other.imag and other.real == int(other.real):
            if self.real and not self.imag:  # purely real
                return ComplexDecimal(self.real ** int(other))
            elif self.imag and not self.real:  # purely imag
                sgn, val = 1j ** int(other), self.imag ** int(other)
                if sgn.real: return ComplexDecimal(int(sgn.real) * val)
                else: return ComplexDecimal(0, int(sgn.imag) * val)
            else: pass  # complex

        decimal.getcontext().prec += 3
        ex = (ComplexDecimal(other) * self.ln()).exp()
        decimal.getcontext().prec -= 3

        return +ComplexDecimal(ex)

    # reverse arithmetic methods
    def __radd__(self, other):
        "x.__radd__(y) <==> y+x"
        other = ComplexDecimal(other)
        real = self.real + other.real
        imag = self.imag + other.imag
        return ComplexDecimal(real, imag)

    def __rsub__(self, other):
        "x.__rsub__(y) <==> y-x"
        other = ComplexDecimal(other)
        real = other.real - self.real
        imag = other.imag - self.imag
        return +ComplexDecimal(real, imag)

    def __rmul__(self, other):
        "x.__rmul__(y) <==> y*x"
        other = ComplexDecimal(other)
        real = self.real * other.real - self.imag * other.imag
        imag = self.imag * other.real + self.real * other.imag
        return +ComplexDecimal(real, imag)

    def __rdiv__(self, other):
        "x.__rdiv__(y) <==> y/x"
        other = ComplexDecimal(other)
        denom = self.real ** 2 + self.imag ** 2
        real = (other.real * self.real + other.imag * self.imag) / denom
        imag = (other.imag * self.real - other.real * self.imag) / denom
        return +ComplexDecimal(real, imag)

    def __rtruediv__(self, other):
        "x.__rtruediv__(y) <==> y/x"
        return self.__rdiv__(other)

    def __rfloordiv__(self, other):
        "x.__rfloordiv__(y) <==> y//x"
        other = ComplexDecimal(other)
        denom = self.real ** 2 + self.imag ** 2
        real = (other.real * self.real + other.imag * self.imag) // denom
        imag = (other.imag * self.real - other.real * self.imag) // denom
        return +ComplexDecimal(real, imag)

    def __rmod__(self, other):
        "x.__rmod__(y) <==> y%x"
        raise TypeError("can't take floor or mod of complex number.")

    def __rdivmod__(self, other):
        "x.__rdivmod__(y) <==> divmod(y, x)"
        raise TypeError("can't take floor or mod of complex number.")

    def __rpow__(self, other, modulo=None):
        "y.__rpow__(x[, z]) <==> pow(y, x[, z])"
        return +(ComplexDecimal(other) ** self)

    # conversions
    def __int__(self):
        "x.__int__() <==> int(x)"
        if not self.imag: return int(self.real)
        else: raise TypeError("can't convert complex to int")

    def __long__(self):
        "x.__long__() <==> long(x)"
        if not self.imag:
            try: return long(self.real)
            except NameError: return int(self.real)
        else: raise TypeError("can't convert complex to long")

    def __float__(self):
        "x.__float__() <==> float(x)"
        if not self.imag: return float(self.real)
        else: raise TypeError("can't convert complex to float")

    def __complex__(self):
        "x.__complex__() <==> complex(x)"
        return complex(float(self.real), float(self.imag))

    def __round__(self, ndigits=0):
        "x.__round__() <==> round(x)"
        try: return round(float(self), ndigits)
        except TypeError:
            raise TypeError("can't convert complex to float")

    def __hex__(self):
        "x.__hex__() <==> hex(x)"
        try: return hex(int(self))
        except TypeError:
            raise TypeError("hex() argument can't be converted to hex")

    def __oct__(self):
        "x.__oct__() <==> oct(x)"
        try: return oct(int(self))
        except TypeError:
            raise TypeError("oct() argument can't be converted to hex")

    def __bin__(self):
        "x.__bin__() <==> bin(x)"
        try: return bin(int(self))
        except TypeError:
            raise TypeError("bin() argument can't be converted to bin")

    def __coerce__(self, other):
        "x.__coerce__(y) <==> coerce(x, y)"
        return self, ComplexDecimal(other)

    def __str__(self):
        "x.__str__() <==> str(x)"
        if not self.imag: val = str(self.real)
        elif not self.real: val = str(self.imag) + 'j'
        else: val = str(self.real) + ('+' + str(self.imag) + 'j')
        return val.replace('+-', '-')

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        sgn = '+' if self.imag >= 0 else '-'
        return "ComplexDecimal({}{}{}j)".format(self.real, sgn, abs(self.imag))

    # functions
    def __inverse__(self):
        "x.__inverse__() <==> 1/x"
        denom = self.real ** 2 + self.imag ** 2
        real = self.real / denom
        imag = self.imag / denom
        return ComplexDecimal(real, imag)

    def __pos__(self):
        "x.__pos__() <==> +x"
        return ComplexDecimal(+self.real, +self.imag)

    def __neg__(self):
        "x.__neg__() <==> -x"
        return ComplexDecimal(-self.real, -self.imag)

    def __abs__(self):
        "x.__abs__() <==> abs(x)"
        return decimal.Decimal(self.real ** 2 + self.imag ** 2).sqrt()

    def conjugate(self):
        "Return the complex conjugate of self."
        return ComplexDecimal(self.real, -self.imag)

    def sqrt(self):
        "Return the square root of self."
        inner = (self.real ** 2 + self.imag ** 2).sqrt()
        gamma = (( self.real + inner) / 2).sqrt()
        delta = ((-self.real + inner) / 2).sqrt()
        return ComplexDecimal(gamma, delta * (-1 if self.imag < 0 else 1))

    def phase(self):
        "Return the phase of self as measured in radians."
        if self.real > 0:
            arg = ComplexDecimal(self.imag / self.real).atan()
        elif self.real < 0 and self.imag >= 0:
            arg = ComplexDecimal(self.imag / self.real).atan() + self.pi()
        elif self.real < 0 and self.imag < 0:
            arg = ComplexDecimal(self.imag / self.real).atan() - self.pi()
        elif self.real == 0 and self.imag > 0:
            arg = self.pi() / 2
        elif self.real == 0 and self.imag < 0:
            arg = -self.pi() / 2
        else: # real = imag = 0, indeterminate
            arg = 0
        return arg.real

    def exp(self):
        "Return e ** self."
        decimal.getcontext().prec += 3
        k, f, x = 0, 1, 1
        psum, last = 0, 1
        while last != psum:
            last = psum
            psum += x / f
            k += 1
            x *= self
            f *= k
        decimal.getcontext().prec -= 3
        return +ComplexDecimal(psum)

    def ln(self):
        "Return the natural logarithm of self."
        decimal.getcontext().prec += 3
        z, ph = abs(self), self.phase()
        k, x = 1, (z - 1) / (z + 1)
        y, psum, last = x * x, 0, 1
        while last != psum:
            last = psum
            psum += x / k
            k += 2; x *= y
        decimal.getcontext().prec -= 3
        return +ComplexDecimal(2 * psum, ph)

    def log(self, base=None):
        "Return the logarithm of self to the given base."
        if base is None: return self.ln()
        elif base == 10: return self.log10()
        else: return self.ln() / ComplexDecimal(base).ln()

    def log10(self):
        "Return the base ten logarithm of self."
        return self.ln() / decimal.Decimal('10').ln()

    # trigonometric functions
    def cos(self):
        "Return the cosine of self as measured in radians."
        decimal.getcontext().prec += 3
        k, f, x, x2, s = 0, 1, 1, self * self, 1
        psum, last = 0, 1
        while last != psum:
            last = psum
            psum += x / f * s
            k += 2; x *= x2
            f *= k * (k - 1); s *= -1
        decimal.getcontext().prec -= 3
        return +ComplexDecimal(psum)

    def cosh(self):
        "Return the hyperbolic cosine of self as measured in radians."
        decimal.getcontext().prec += 3
        k, f, x, x2 = 0, 1, 1, self * self
        psum, last = 0, 1
        while last != psum:
            last = psum
            psum += x / f
            k += 2; x *= x2
            f *= k * (k - 1)
        decimal.getcontext().prec -= 3
        return +ComplexDecimal(psum)

    def sin(self):
        "Return the sine of self as measured in radians."
        decimal.getcontext().prec += 3
        k, f, x, x2, s = 1, 1, self, self * self, 1
        psum, last = 0, 1
        while last != psum:
            last = psum
            psum += x / f * s
            k += 2; x *= x2
            f *= k * (k - 1); s *= -1
        decimal.getcontext().prec -= 3
        return +ComplexDecimal(psum)

    def sinh(self):
        "Return the hyperbolic sine of self as measured in radians."
        decimal.getcontext().prec += 3
        k, f, x, x2 = 1, 1, self, self * self
        psum, last = 0, 1
        while last != psum:
            last = psum
            psum += x / f
            k += 2; x *= x2
            f *= k * (k - 1)
        decimal.getcontext().prec -= 3
        return +ComplexDecimal(psum)

    def tan(self):
        "Return the tangent of self as measured in radians."
        return +ComplexDecimal(self.sin() / self.cos())

    def tanh(self):
        "Return the hyperbolic tangent of self as measured in radians."
        return +ComplexDecimal(self.sinh() / self.cosh())

    # inverse trigonometric functions
    def acos(self):
        "Return the inverse cosine of self as measured in radians."
        return self.pi() / 2 - self.asin()

    def acosh(self):
        "Return the inverse hyperbolic cosine of self as measured in radians."
        return (self + (self - 1).sqrt() * (self + 1).sqrt()).ln()

    def asin(self):
        "Return the inverse sine of self as measured in radians."
        i = ComplexDecimal(0, 1)
        return -i * (i * self + (1 - self * self).sqrt()).ln()

    def asinh(self):
        "Return the inverse hyperbolic sine of self as measured in radians."
        return (self + (self * self + 1).sqrt()).ln()

    def atan(self):
        "Return the inverse tangent of self as measured in radians."
        if abs(self) > 1:
            s = 1 if self.real >= 0 else -1
            return s * self.pi() / 2 - (1 / self).atan()

        decimal.getcontext().prec += 3
        tn = f1 = j = f2 = k = 1
        x, x1 = self, self * self
        y = y1 = (1 + x1)
        psum, last = 0, 1
        while last != psum:
            last = psum
            psum += (tn * f1  * x / (f2 * y))
            tn *= 4; f1 *= j * j
            j += 1; k += 2
            f2 *= k * (k - 1)
            x *= x1; y *= y1
        decimal.getcontext().prec -= 3
        return +ComplexDecimal(psum.real, psum.imag)

    def atanh(self):
        "Return the inverse hyperbolic tangent of self as measured in radians."
        return ((1 + self).ln() - (1 - self).ln()) / 2

    def pi(self):
        "Return the constant pi."
        txt = (  # keep a large precomputed value on hand (1020 digits)
            "3.1415926535897932384626433832795028841971693993751058209749"
            "445923078164062862089986280348253421170679821480865132823066"
            "470938446095505822317253594081284811174502841027019385211055"
            "596446229489549303819644288109756659334461284756482337867831"
            "652712019091456485669234603486104543266482133936072602491412"
            "737245870066063155881748815209209628292540917153643678925903"
            "600113305305488204665213841469519415116094330572703657595919"
            "530921861173819326117931051185480744623799627495673518857527"
            "248912279381830119491298336733624406566430860213949463952247"
            "371907021798609437027705392171762931767523846748184676694051"
            "320005681271452635608277857713427577896091736371787214684409"
            "012249534301465495853710507922796892589235420199561121290219"
            "608640344181598136297747713099605187072113499999983729780499"
            "510597317328160963185950244594553469083026425223082533446850"
            "352619311881710100031378387528865875332083814206171776691473"
            "035982534904287554687311595628638823537875937519577818577805"
            "321712268066130019278766111959092164201989380952572010654858")
        if decimal.getcontext().prec <= len(txt):
            return decimal.Decimal(txt)

        else:  # calculate pi for required precision (Chudnovsky algorithm)
            decimal.getcontext().prec += 3
            l, x, k, m, i = 13591409, 1, 6, 1, 1
            psum, last = 0, 1
            while last != psum:
                last = psum
                psum += decimal.Decimal(m * l) / x
                m  = m * (k ** 3 - 16 * k) // i ** 3
                l += 545140134
                x *= -262537412640768000
                k += 12; i += 1
            apple = 426880 * decimal.Decimal(10005).sqrt() / psum
            decimal.getcontext().prec -= 3
            return +apple

    # comparisons
    def __lt__(self, other):
        "x.__lt__(y) <==> x<y"
        raise TypeError("no ordering relation is defined for complex numbers")

    def __le__(self, other):
        "x.__le__(y) <==> x<=y"
        raise TypeError("no ordering relation is defined for complex numbers")

    def __eq__(self, other):
        "x.__eq__(y) <==> x==y"
        if self.real == other.real and self.imag == other.imag: return True
        else: return False

    def __ne__(self, other):
        "x.__eq__(y) <==> x!=y"
        return not self.__eq__(other)

    def __gt__(self, other):
        "x.__gt__(y) <==> x>y"
        raise TypeError("no ordering relation is defined for complex numbers")

    def __ge__(self, other):
        "x.__ge__(y) <==> x>=y"
        raise TypeError("no ordering relation is defined for complex numbers")

    def __nonzero__(self):
        "x.__bool__() <==> bool(x)"
        if self.real or self.imag: return True
        else: return False

    def __bool__(self):
        "x.__bool__() <==> bool(x)"
        return self.__nonzero__()
