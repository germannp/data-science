import unittest
import random
import string

from hypothesis import given
from hypothesis.strategies import text, floats

from cluster import zipstance


class TestZipstance(unittest.TestCase):

    @given(text(), text())
    def test_positivity(self, a, b):
        self.assertTrue(zipstance(a, b) >= 0)

    @given(text(min_size=10), text(min_size=10), text(min_size=10))
    def test_triangle_inequality(self, a, b, c):
        self.assertTrue(zipstance(a, c) <= zipstance(a, b) + zipstance(b, c))

    @given(floats(0, 1))
    def test_precision(self, ratio):
        """zipstance(a, x*a + (1 - x)*b) ~ 1 - x, if zipstance(a, b) ~ 1"""
        eps = 0.02
        n = 10000
        a = ''.join([random.choice(string.ascii_letters + '. ') for _ in range(n)])
        b = ''.join([random.choice(string.ascii_letters + '. ') for _ in range(n)])
        dist = zipstance(a, a[0:int(ratio*n)] + b[int(ratio*n):])
        self.assertTrue(dist >= 1 - ratio - eps)
        self.assertTrue(dist <= 1 - ratio + eps)


if __name__ == '__main__':
    unittest.main()
