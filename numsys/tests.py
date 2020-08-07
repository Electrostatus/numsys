import unittest, random

import support as _sup
import standard as _std
import nonstandard as _nsd

class testNumsys(unittest.TestCase):
    longMessage = True

    def test_integer_identity(self):
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
