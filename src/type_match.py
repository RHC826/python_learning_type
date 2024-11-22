"""match 文で型分岐"""


def main(arg):
    """分岐"""
    match arg:
        case str():
            print("Strin!")
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
        case _:
            return ""
    raise LookupError("error!")


if __name__ == "__main__":
    pass
