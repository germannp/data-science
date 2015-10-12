import unittest

from hypothesis import given
from hypothesis.strategies import text

from cluster import zipstance


class TestZipstance(unittest.TestCase):

    @given(text(), text())
    def test_positivity(self, a, b):
        self.assertTrue(zipstance(a, b) >= 0)

    @given(text(min_size=10), text(min_size=10), text(min_size=10))
    def test_triangle_inequality(self, a, b, c):
        self.assertTrue(zipstance(a, c) <= zipstance(a, b) + zipstance(b, c))


if __name__ == '__main__':
    unittest.main()
