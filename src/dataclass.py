from dataclasses import dataclass
from typing import Generator


@dataclass
class ChangeLog:
    version: float
    content: str
    pep: int

    def __iter__(self) -> Generator[float | str | int]:
        yield from self.__dict__.values()

@dataclass
class ChangeLogs:
    ChangeLogs: list[ChangeLog]

    def __iter__(self) -> Generator[ChangeLog, None, None]:
        yield from self.ChangeLogs


ChangeLog_1 = ChangeLog(
    3.5, "Type hinting introduced as an optional feature with the `typing` module", 484
)
ChangeLog_2 = ChangeLog(
    3.6,
    "Addition of variable annotations, allowing inline type annotations for variables",
    526,
)
ChangeLog_3 = ChangeLog(
    3.7,
    "Data Classes added to simplify the creation of classes with default behaviors for methods like __init__ and __repr__",
    557,
)
ChangeLog_4 = ChangeLog(3.8, "Positional-only parameters with typing support", 570)
ChangeLog_5 = ChangeLog(
    3.9, "Introduction of new union operator `|` for type annotations", 604
)
ChangeLog_6 = ChangeLog(
    3.9, "Introduction of `Annotated` for attaching metadata to types", 593
)
ChangeLog_7 = ChangeLog(
    3.10, "Pattern Matching with type support for structured data", 634
)
ChangeLog_8 = ChangeLog(
    3.10,
    "Parameter Specification Variables to better support higher-order functions",
    612,
)
ChangeLog_9 = ChangeLog(3.10, "Precise type aliasing with `TypeAlias`", 613)
ChangeLog_10 = ChangeLog(
    3.11,
    "`Self` type introduced for methods that return an instance of the containing class",
    673,
)
ChangeLog_11 = ChangeLog(
    3.11,
    "`TypedDict` becomes a built-in class for type-safe dictionary-like objects",
    655,
)
ChangeLog_12 = ChangeLog(
    3.11,
    "Variadic Generics support with `TypeVarTuple` for defining variadic generic types",
    646,
)
ChangeLog_13 = ChangeLog(3.11, "Enhanced error messages for typing-related errors", 657)
ChangeLog_14 = ChangeLog(
    3.12,
    "Improvements to `TypedDict` syntax with a new concise syntax for defining TypedDicts",
    692,
)
ChangeLog_15 = ChangeLog(
    3.12, "Improvements to structural pattern matching with type guards", 681
)

for i in ChangeLog_1:
    print(i)


_ChangeLogs = ChangeLogs([ChangeLog_1, ChangeLog_2])
for j in _ChangeLogs:
    print(j)
