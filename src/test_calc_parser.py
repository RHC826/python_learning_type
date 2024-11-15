""" 電卓プログラム テスト"""
import unittest
import calc_parser


class TestUnionMethod(unittest.TestCase):
    """calc_parser.py unittest"""

    def test_tokenize(self):
        """ トークナイズテスト: 3 + 5 * (2 - 8) """
        # pylint: disable=line-too-long
        tokenized = r"[('NUMBER', 3), ('PLUS', '+'), ('NUMBER', 5), ('TIMES', '*'), ('LPAREN', '('), ('NUMBER', 2), ('MINUS', '-'), ('NUMBER', 8), ('RPAREN', ')')]"
        # pylint: enable=line-too-long
        self.assertEqual(
            msg="Warning!",
            first=str(calc_parser.Parser.tokenize("3 + 5 * (2 - 8)")),
            second=tokenized,
        )

    def test_parser(self):
        """ 計算テスト: 3 + 5 * (2 - 8) """
        # テスト
        tokens = calc_parser.Parser.tokenize("3 + 5 * (2 - 8)")
        parser = calc_parser.Parser(tokens)
        tree = parser.parse()

        # テスト
        # result = calc_parser.Parser.evaluate_expression(tree)
        result = calc_parser.Parser.evaluate(tree)
        self.assertEqual(first=result, second=-27)


if __name__ == "__main__":
    unittest.main()
