import unittest

from hypothesis import given
from hypothesis.strategies import text

from cluster import zipstance


class TestZipstance(unittest.TestCase):
    @given(text(min_size=1), text(min_size=1), text(min_size=1))
    def test_triangle_inequality(self, a, b, c):
        self.assertTrue(zipstance(a, c) <= zipstance(a, b) + zipstance(b, c))


if __name__ == '__main__':
    unittest.main()
