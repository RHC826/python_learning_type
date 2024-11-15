"""parser :簡単な数式"""
import re
from typing import Literal, cast

# 型エイリアスを使用してトークンと構文木の型を定義
type Terms = Literal['PLUS','MINUS','TIMES','DIVIDE']
type Token = tuple[str, int | float | str]
type Expression = Token | tuple[Terms, Expression, Expression]

class Parser:
    """Parser
    数式文字列をトークン化し、抽象構文木 (AST) にパースして評価します。
    """

    tokens: list[Token]
    pos: int

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        # MEMO:current_position -> pos
        self.pos = 0

    @staticmethod
    def tokenize(expression: str) -> list[Token]:
        """数式をトークン化してリストとして返します。

        Args:
            expression (str): 数式の文字列。中置記法

        Returns:
            list[Token]: トークンのリスト

        Raises:
            SyntaxError: 数式以外の不正な入力があった場合
        """
        # 数字、演算子、括弧に対応する正規表現パターンを定義
        token_specification = [
            ("NUMBER", r"\d+(\.\d*)?"),  # 数字
            ("PLUS", r"\+"),  # 足し算
            ("MINUS", r"-"),  # 引き算
            ("TIMES", r"\*"),  # 掛け算
            ("DIVIDE", r"/"),  # 割り算
            ("LPAREN", r"\("),  # 左括弧
            ("RPAREN", r"\)"),  # 右括弧
            ("SKIP", r"[ \t]+"),  # 空白とタブ（無視）
        ]

        # 正規表現パターンを結合
        tok_regex = "|".join(
            f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification
        )
        tokens:list[Token] = []

        for match in re.finditer(tok_regex, expression):
            kind = match.lastgroup
            value = match.group()
            if kind is None:
                raise SyntaxError(
                    "Unexpected token: 設定されたパターンに属さない入力があります"
                )

            if kind == "NUMBER":
                value = float(value) if "." in value else int(value)
            elif kind == "SKIP":
                continue  # 空白とタブはスキップ

            tokens.append((kind, value))

        return tokens

    def parse(self) -> Expression:
        """トークンリストをパースして抽象構文木 (AST) を生成します。

        Returns:
            Expression: AST（抽象構文木）
        """
        return self.expr()

    def consume(self, expected_type: str) -> Token:
        """現在のトークンが期待される型なら取得し、次のトークンに進む。

        Args:
            expected_type (str): 期待するトークンの型

        Returns:
            Token: 現在のトークン

        Raises:
            SyntaxError: 期待される型でないトークンが出現した場合
        """
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")

    def expr(self) -> Expression:
        """expr : term (('+' | '-') term)*"""
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in (
            "PLUS",
            "MINUS",
        ):
            op = self.tokens[self.pos][0]

            if op not in ['PLUS','MINUS','TIMES','DIVIDE']:
                raise ValueError("Unexpected operator")
            # op を Literal['PLUS', 'MINUS', 'TIMES', 'DIVIDE'] にキャスト
            op = cast(Terms, op)

            self.consume(op)
            right = self.term()
            node = (op, node, right)
        return node

    def term(self) -> Expression:
        """term : factor (('*' | '/') factor)*"""
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in (
            "TIMES",
            "DIVIDE",
        ):
            op = self.tokens[self.pos][0]
            self.consume(op)
            right = self.factor()

            if op not in ['PLUS','MINUS','TIMES','DIVIDE']:
                raise ValueError("Unexpected operator")
            # op を Literal['PLUS', 'MINUS', 'TIMES', 'DIVIDE'] にキャスト
            op = cast(Terms, op)

            node = (op, node, right)
        return node

    def factor(self) -> Expression:
        """factor : NUMBER | '(' expr ')'"""
        token = self.tokens[self.pos]
        if token[0] == "NUMBER":
            self.consume("NUMBER")
            return token
        if token[0] == "LPAREN":
            self.consume("LPAREN")
            node = self.expr()
            self.consume("RPAREN")
            return node
        raise SyntaxError(f"Unexpected token: {token}")

    @staticmethod
    def evaluate(node: Expression) -> int | float:
        """再帰的にASTを評価し、計算結果を返します。

        Args:
            node (Expression): ASTのノード

        Returns:
            int | float: 計算結果
        """
        match node:
            case ("PLUS", left, right):
                return Parser.evaluate(left) + Parser.evaluate(right)
            case ("MINUS", left, right):
                return Parser.evaluate(left) - Parser.evaluate(right)
            case ("TIMES", left, right):
                return Parser.evaluate(left) * Parser.evaluate(right)
            case ("DIVIDE", left, right):
                return Parser.evaluate(left) / Parser.evaluate(right)
            case ("NUMBER", value) if isinstance(value, (int, float)):
                return value
            case _:
                raise SyntaxError("無効なノード")



if __name__ == "__main__":
    pass
