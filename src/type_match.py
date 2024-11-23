"""match 文で型分岐"""

from dataclasses import dataclass


@dataclass
class Card:
    """トランプクラス"""

    suit: str
    number: int


def main(arg):
    """分岐"""
    match arg:
        case {"suit":x,"number":y} :
            print("x,y:",x,y)
            return f"Card dict! Suit:{x} Number:{y}"
        case str():
            print("String!")
            return "String!"
        case int():
            print("Int!")
            return ""
        case float():
            print("Float!")
            return ""
        case list():
            print("List!")
            return ""
        case dict():
            print("Dict!")
            return ""
        # dataclass の分岐
        case Card(suit, number):
            print("Card class!")
            return (suit, number)
        case _:
            return "UNKNOWN"
    raise KeyError("error!")

# """ポーランド記法の計算"""
type Pn = tuple[str, Pn|int|float, Pn|int|float]
def pn_calculator(expression: Pn|int|float) -> int | float:
    """ポーランド記法の式を計算する"""
    match expression:
        case ("+", left, right):
            return pn_calculator(left) + pn_calculator(right)
        case ("-", left, right):
            return pn_calculator(left) - pn_calculator(right)
        case ("*", left, right):
            return pn_calculator(left) * pn_calculator(right)
        case ("/", left, right):
            return pn_calculator(left) / pn_calculator(right)
        case int() | float():
            return expression
    raise ValueError("無効な式です")


if __name__ == "__main__":
    D5 = Card("ダイヤ", 5)
    print(main(D5))
    DDD = {
        "suit":"ダイヤ",
        "number": 5
    }
    print(main(DDD))
    print(type(D5))
    print(pn_calculator(("+", 2, 3)))
    print(pn_calculator(("+", ("+",1,1), 3)))
    print(pn_calculator(("+", ("/",5.0,2), 3)))
