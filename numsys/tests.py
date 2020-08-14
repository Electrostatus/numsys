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
        _sup.setPrec(1500)  # will need more precision for this test

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
        _sup.setPrec(1500)  # will need more precision for this test

        for b in bases:
            for i in reals:
                j = _std.to_10(_std.to_rb(i, b), b)

                rnd_i = _sup.rround(i)
                rnd_j = _sup.rround(j)
                self.assertEqual(rnd_i, rnd_j, msg=mesg.format(b, i, float(j)))

if __name__ == '__main__':
    unittest.main(verbosity=2)
