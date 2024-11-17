""" cast: 型キャスト
* cast() で型をキャストできる
"""
from typing import cast,Literal


def g(arg:str):
    """ TEST """
    if arg == "T":
        return "T"
    return "F"

HOGE = g("T")
PIYO = "T" if HOGE != "F" else "T"
FUGA = cast(Literal["T"],g("T"))
assert isinstance(FUGA,str) and FUGA == "T"
assert FUGA == "T"
# (constant) FUGA: Literal['T']
print(FUGA)
