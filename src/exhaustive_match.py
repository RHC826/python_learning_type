""" match case で網羅性検査 """

import enum
from typing import Never


def assert_never(arg: Never) -> Never:
    """網羅性チェック"""
    raise AssertionError("Expected code to be unreachable")


class SHIKOKU(enum.Enum):
    """四国の特産品を列挙したクラス"""

    KAGAWA = "うどん"
    TOKUSHIMA = "すだち"
    EHIME = "みかん"
    KOUCHI = "かつお"


def main(shikoku: SHIKOKU):
    """Never 型による網羅性検査"""
    match shikoku:
        case shikoku.KAGAWA:
            return shikoku.KAGAWA.value
        case shikoku.TOKUSHIMA:
            return shikoku.TOKUSHIMA.value
        case shikoku.EHIME:
            return shikoku.EHIME.value
        case shikoku.KOUCHI:
            return shikoku.KOUCHI.value
        case _:
            assert_never(shikoku)


if __name__ == "__main__":
    for cnt, i in enumerate(SHIKOKU):
        print(cnt, main(i))
        match cnt:
            case 0:
                print("ズルル〜")
            case _ if cnt > 0:
                print("パクパク")
