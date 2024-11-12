"""union 型などの複数の型にまたがる型"""

from typing import Optional

type Vector = list[int | float]


def main() -> Optional[bool]:
    """type, Optional, ほか色々"""
    return True


def katahiki[T](x: T) -> T:
    return x


if __name__ == "__main__":
    print("main:", main())
    print("katahiki:", katahiki(True))
