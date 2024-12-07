""" 再帰的ディレクトリ探索 """

import os


def main(current_dir="."):
    """Recursively list files and directories using match-case"""
    print("----------")
    print(f"current_dir: {current_dir}")
    for file_or_dir in os.listdir(current_dir):
        full_path = os.path.join(current_dir, file_or_dir)  # フルパスを生成

        match full_path:
            case file_path if os.path.isfile(file_path):
                print(f"FILE: {file_path}")
            case dir_path if os.path.isdir(dir_path):
                print(f"DIRECTORY: {dir_path}")
                main(dir_path)  # 再帰的にディレクトリを探索
            case other:
                print(f"UNKNOWN: {other}")
                assert False, "This code path should never be reached."


if __name__ == "__name__":
    main()
