"""type_match test"""

import unittest
from src.type_match import main


class TestUnionMethod(unittest.TestCase):
    """ src/type_match.py unittest"""

    def test_str(self):
        """str"""
        res = main("test")
        print(str(res))
        self.assertEqual(isinstance(res, str), True)


if __name__ == "__main__":
    unittest.main()
