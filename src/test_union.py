import unittest
import union


class TestUnionMethod(unittest.TestCase):
    """union.py unittest"""

    def test_union(self):
        self.assertTrue(True, "test")

    def test_main(self):
        self.assertEqual(union.main(), True)


if __name__ == "__main__":
    unittest.main()
