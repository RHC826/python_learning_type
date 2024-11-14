"""parser :簡単な数式"""

import re

# トークンは、型と値のタプルで定義します。例: ("NUMBER", 3)
type Token = tuple[str, float | int | str]

# Expression型は再帰的な構造で、数値ノードまたは演算ノードを表現します
type Expression = (
    Token | tuple[str, Expression, Expression]  # ('PLUS', 左, 右) のような演算ノード
)


def tokenize(expression):
    # 数字、演算子、括弧に対応する正規表現パターンを定義します
    token_specification: list[tuple[str, str]] = [
        ("NUMBER", r"\d+(\.\d*)?"),  # 数字
        ("PLUS", r"\+"),  # 足し算
        ("MINUS", r"-"),  # 引き算
        ("TIMES", r"\*"),  # 掛け算
        ("DIVIDE", r"/"),  # 割り算
        ("LPAREN", r"\("),  # 左括弧
        ("RPAREN", r"\)"),  # 右括弧
        ("SKIP", r"[ \t]+"),  # 空白とタブ（無視）
    ]
    tokens: list[Token] = []
    # 正規表現のパターンをまとめます
    tok_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
    for match in re.finditer(tok_regex, expression):
        kind = match.lastgroup
        value = match.group()
        if kind is None:
            raise SyntaxError(
                "Unexpected token: Unexpected type.設定された正規表現のパターンに属さない入力があった可能性があります"
            )

        if kind == "NUMBER":
            value = float(value) if "." in value else int(value)
        elif kind == "SKIP":
            continue

        tokens.append((kind, value))
    return tokens


class Parser:
    tokens: list[Token]
    pos: int

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Expression:
        return self.expr()

    def consume(self, expected_type: str) -> Token:
        """現在のトークンが期待される型かを確認し、次のトークンへ進む"""
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
            node = (op, node, right)
        return node

    def factor(self) -> Expression:
        """factor : NUMBER | '(' expr ')'"""
        token = self.tokens[self.pos]
        if token[0] == "NUMBER":
            self.consume("NUMBER")
            return token
        elif token[0] == "LPAREN":
            self.consume("LPAREN")
            node = self.expr()
            self.consume("RPAREN")
            return node
        raise SyntaxError(f"Unexpected token: {token}")


# 出力例: ('+', ('NUMBER', 3), ('*', ('NUMBER', 5), ('-', ('NUMBER', 2), ('NUMBER', 8))))
def evaluate(node: Expression) -> int | float:
    if isinstance(node, tuple) and len(node) == 3:
        op, left, right = node[0], node[1], node[2]
        if op == "PLUS":
            return evaluate(left) + evaluate(right)
        if op == "MINUS":
            return evaluate(left) - evaluate(right)
        if op == "TIMES":
            return evaluate(left) * evaluate(right)
        if op == "DIVIDE":
            return evaluate(left) / evaluate(right)
    # ('NUMBER', value) の形式なので、値部分を返す
    ans = node[1]
    if isinstance(ans, str) or ans is None:
        raise SyntaxError("文字列またはNoneを答えにしようとしている")
    # 確実に int/float の場合だけ返す
    return ans if isinstance(ans, (int, float)) else 0


if __name__ == "__main__":
    # テスト
    TOKENS = tokenize("3 + 5 * (2 - 8)")
    parser = Parser(TOKENS)
    tree = parser.parse()
    # print("tree:", tree)

    # テスト
    result = evaluate(tree)
    # print("3:", result)  # 出力例: -22.0
