import unittest, random

import support as _sup
import standard as _std
import nonstandard as _nsd
#import __init__ as _nys


class testNumsys(unittest.TestCase):
    longMessage = True

    def test_int_int_identity(self):
        "integer base conversion with integers from base 10 to base B to 10"
        mesg = ('base 10 to base {} to base 10 conversion failed'
                ' with input {} (output: {})')

        # select multiple random integers
        ints = list(range(-10, 11))
        for i in range(100): ints.append(random.randint(-5000, 5000))
        for i in range(25): ints.append(random.randint(-2 ** 257, 2 ** 257))

        # select random valid integer bases
        mb = _sup.maxchr
        bases = filter(lambda x: abs(x) > 1, range(-mb, mb + 1))

        for b in random.sample(list(bases), max(250, mb // 4000)):
            for i in ints:
                j = _std.to_10(_std.to_zb(i, b), b)
                self.assertEqual(i, j, msg=mesg.format(b, i, j))


    def test_real_int_identity(self):
        "integer base conversion with reals from base 10 to base B to 10"
        mesg = ('base 10 to base {} to base 10 conversion failed'
                ' with input {} (output: {})')

        # select multiple random reals
        reals = [-0.1, 0.2, -0.3, 0.4, 0, 75, -18985410]
        for i in range(10):
            reals.append(random.random() * random.choice([-1, 1]))
        for i in range(10):
            r = random.random() * 10 ** random.randint(-300, 300)
            reals.append(r * random.choice([-1, 1]))

        # select random valid integer bases
        mb = _sup.maxchr
        bases = filter(lambda x: abs(x) > 1, range(-mb, mb + 1))
        _sup.set_prec(1000)  # will need more precision for this test

        for b in random.sample(list(bases), max(125, mb // 8000)):
            for i in reals:
                j = _std.to_10(_std.to_rb(i, b), b)

                rnd_i = _sup.rround(i)  # within reason
                rnd_j = _sup.rround(j)  # floats are not always exact
                self.assertEqual(rnd_i, rnd_j, msg=mesg.format(b, i, float(j)))


    def test_real_real_identity(self):
        "real base conversion with reals from base 10 to base B to 10"
        mesg = ('base 10 to base {} to base 10 conversion failed'
                ' with input {} (output: {})')

        # select multiple random reals
        reals = [-0.1, 0.2, -0.3, 0.4, 0, -123, 9610772]
        for i in range(10): reals.append(random.randint(-5000, 5000))
        for i in range(10):
            reals.append(random.random() * random.choice([-1, 1]))
        for i in range(10):
            r = random.random() * 10 ** random.randint(-300, 300)
            reals.append(r * random.choice([-1, 1]))

        # select random valid real bases
        mb = _sup.maxchr
        mx = max(125, mb // 8000)
        rnd_bases = [round(random.uniform(-mb, mb), 3) for i in range(mx)]

        bases = filter(lambda x: abs(x) not in [1, 0], rnd_bases)
        _sup.set_prec(1000)  # will need more precision for this test

        for b in bases:
            for i in reals:
                j = _std.to_10(_std.to_rb(i, b), b)

                rnd_i = _sup.rround(i)
                rnd_j = _sup.rround(j)
                self.assertEqual(rnd_i, rnd_j, msg=mesg.format(b, i, float(j)))


    def test_imag_cmpx_identity(self):
        "imag base conversion with complex from base 10 to base B to 10"
        # this tests complex values moreso than conversion
        # as the three tests above deal with the conversion functions
        mesg = ('base 10 to base {} to base 10 conversion failed'
                ' with input {} (output: {})')

        # random complexes
        cmpx = [1j]
        for i in range(25):
            r = random.random() * 10 ** random.randint(-12, 12)
            j = random.random() * 10 ** random.randint(-12, 12)
            cpx = complex(r * random.choice([-1, 1]),
                          j * random.choice([-1, 1]))
            cmpx.append(cpx)

        # random bases
        mb = int(_sup.maxchr ** .5)
        mx = max(70, mb // 16000)
        rnd_bases = [round(random.uniform(-mb, mb), 3) for i in range(mx)]
        bases = filter(lambda x: abs(x) not in [1, 0], rnd_bases)

        _sup.set_prec(250)
        for b in bases:
            b = complex(0, b)
            for i in cmpx:
                j = complex(_std.to_10(_std.to_ib(i, b), b))

                ir = _sup.rround(i.real, 3); ij = _sup.rround(i.imag, 3)
                jr = _sup.rround(j.real, 3); jj = _sup.rround(j.imag, 3)
                rnd_i = complex(ir, ij)
                rnd_j = complex(jr, jj)
                self.assertEqual(rnd_i, rnd_j, msg=mesg.format(b, i, j))


    def test_nstd_int_identity(self):
        "base conversion of nonstandard bases"
        mesg = ('10 to {} to 10 conversion failed'
                ' with input {} (output: {})')
        # could test reals with the nonstandard bases, but not all of them
        # can handle real values (like the roman base)

        # select multiple random values
        nums = [random.randint(1, 50000) for i in range(1009)]

        for b in _nsd.nstd_bases:
            tb, tt = _nsd.nstd_bases[b]
            for i in nums:
                j = tt(tb(i))
                self.assertEqual(i, j, msg=mesg.format(b, i, j))


if __name__ == '__main__':
    print('version: ' + _sup.version)
    print('backend: ' + _sup.backend)
    # python 3.8.5:
    # testing just test_imag_cmpx_identity (all others commented out):
    # gmpy2 (v2.0.8):                        Ran 1 test in 22.653s (22 - 36s)
    # mpmath (v1.1.0):                       Ran 1 test in  2.905s (2.7 - 3.3s)
    # decimal + own complex_decimal.py file: Ran 1 test in 4.430s (4.4 - 4.6s)
    # python 2.7.10:
    # gmpy2 (v2.0.8):                        Ran 1 test in 15.423s (15 - 26s)
    # mpmath (v1.1.0):                       Ran 1 test in 5.623s  (4.6 - 5.6s)
    # decimal + own complex_decimal.py file: Ran 1 test in 58.266s (52 - 58s)
    #
    # each was run at least three times, sometimes more
    # all tried 70 random bases at a precision of 250
    # and here I thought gmpy2 would be the fastest for complex
    # perhaps drop the optional use of gmpy2 or mpmath?
    # though, gmpy2 is far faster with just floats than decimal, and are people
    # going to be using complex values more often than reals?
    unittest.main(verbosity=2)
