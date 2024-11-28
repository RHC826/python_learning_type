"""メトロポリタン美術館 API を例に Match 文を活用する"""

import json
import time
from typing import Never, TypedDict
import requests


def assert_never(arg:Never) -> Never:
    """網羅性チェック"""
    raise AssertionError("Expected code to be unreachable")


def get_info(query: str = "sunflowers") -> None:
    """1. キーワード検索 2. 該当する作品の情報を得る
    Document URL:https://metmuseum.github.io/
    """
    allow_list = []
    total = 0
    domain = "https://collectionapi.metmuseum.org"

    request = requests.get(
        f"{domain}/public/collection/v1/search?q={query}&=hasImages=true",
        # f"{domain}/public/collection/v1/search?q={query}&=hasImages=true&=tags=true",
        timeout=10,
    )

    match request.status_code:
        case 200:
            match json.loads(request.text):
                case {"total": total, "objectIDs": ids}:
                    if total == 0:
                        return

                    for cnt, _id in enumerate(ids):
                        request_work_query = f"/public/collection/v1/objects/{_id}"

                        try:
                            work = requests.get(
                                f"{domain}/{request_work_query}", timeout=10
                            )

                        except TimeoutError:
                            continue

                        match work.status_code:
                            case 200:
                                _dump = json.dumps(
                                    _load := json.loads(work.text),
                                    ensure_ascii=False,
                                    indent=4,
                                )

                                match _load:
                                    # 画像が存在するケース
                                    case {"title": title, "primaryImage": url} if len(
                                        url
                                    ) > 0 and str(url):
                                        assert str(title)
                                        allow_list.append(work)

                        # リクエスト制限
                        time.sleep(0.1)
                        if cnt > 10:
                            break
    print(allow_list)
    filter_tag = "Portraits"
    assert len(allow_list) > 0, "len(res) == 0"
    mini_data = [
        (
            data["title"],
            f"https://www.metmuseum.org/art/collection/search/{data['objectID']}",
            data["tags"],
        )
        for request in allow_list
        if (data := json.loads(request.text))  # `data`を解析
        and (tags := data.get("tags")) is not None  # `tags`がNoneでないことを確認
        for tag in tags
        if tag.get("term") == filter_tag  # タグの中で`term`が tag であるものを抽出
    ]
    for i, j in enumerate(mini_data):
        print(i, j)

    print(f"total:{total}")
    with open("./test3.json", "w+", encoding="utf-8") as w:
        json.dump([json.loads(request.text) for request in allow_list], w)


class ApiResponse(TypedDict):
    """match に型付けるため"""

    total: int
    objectIDs: list[int]


def get_address(query: str = "sunflowers") -> None:
    """1. キーワード検索 2. 該当する作品のページのアドレスを得るi
    Document URL:https://metmuseum.github.io/
    """
    domain = "https://collectionapi.metmuseum.org"

    request = requests.get(
        f"{domain}/public/collection/v1/search?q={query}&=hasImages=true", timeout=10
    )

    match request.status_code:
        case 200:
            data: ApiResponse = json.loads(request.text)
            match data:
                case {"total": total, "objectIDs": ids} if total > 0 and isinstance(
                    ids, list
                ) and all(map(lambda x: isinstance(x, int), ids)):

                    for _id in ids:
                        assert isinstance(_id, int)
                        print(f"https://www.metmuseum.org/art/collection/search/{_id}")


if __name__ == "__main__":
    USAGE = """
Usage:
    address <query>  - Get addresses of artworks matching the query.
    info <query>     - Get detailed information of artworks matching the query.
Example:
    address sunflowers
    info van gogh

Please input your command:
"""

    Query = input(USAGE)

    match Tokens := Query.split(" ", maxsplit=1):
        # リテラルパターン
        case ["address", _]:
            get_address(Tokens[1])
        case ["info", _]:
            get_info(Tokens[1])
        # AS パターン
        case _ as Word if len(Word) > 0:
            print(len(Word), f"{Word=}")
            raise ValueError("クエリが不定形です")
        case capt:
            print(f"{capt=}")
