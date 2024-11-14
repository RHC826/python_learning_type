import unittest
import calc_parser


class TestUnionMethod(unittest.TestCase):
    """calc_parser.py unittest"""

    def test_tokenize(self):
        tokenized = r"[('NUMBER', 3), ('PLUS', '+'), ('NUMBER', 5), ('TIMES', '*'), ('LPAREN', '('), ('NUMBER', 2), ('MINUS', '-'), ('NUMBER', 8), ('RPAREN', ')')]"
        self.assertEqual(
            msg="Warning!",
            first=str(calc_parser.tokenize("3 + 5 * (2 - 8)")),
            second=tokenized,
        )

    def test_parser(self):
        # テスト
        TOKENS = calc_parser.tokenize("3 + 5 * (2 - 8)")
        parser = calc_parser.Parser(TOKENS)
        tree = parser.parse()

        # テスト
        result = calc_parser.evaluate(tree)
        self.assertEqual(
                first=result,
                second=-27
                )


if __name__ == "__main__":
    unittest.main()
