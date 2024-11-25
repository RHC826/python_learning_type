"""メトロポリタン美術館 API を Match 文で解析"""

import json
import time
import requests


def main(query: str = "sunflowers") -> None:
    """1. キーワード検索 2. 該当する作品の情報を得る
    Document URL:https://metmuseum.github.io/
    """
    res = []
    total = 0
    domain = "https://collectionapi.metmuseum.org"

    request = requests.get(
        f"{domain}/public/collection/v1/search?q={query}&=hasImages=true", timeout=10
    )

    match request.status_code:
        case 200:
            match json.loads(request.text):
                case {"total": total, "objectIDs": ids}:
                    if total == 0:
                        return

                    for cnt, _id in enumerate(ids):
                        request_work_query = f"/public/collection/v1/objects/{_id}"

                        work = requests.get(
                            f"{domain}/{request_work_query}", timeout=10
                        )

                        match work.status_code:
                            case 200:
                                _dump = json.dumps(
                                    _load := json.loads(work.text),
                                    ensure_ascii=False,
                                    indent=4,
                                )

                                match _load:
                                    case {"title": title, "primaryImage": url} if len(
                                        url
                                    ) > 0 and str(url):
                                        res.append(work)
                                        print(
                                            f"https://www.metmuseum.org/art/collection/search/{_id}"
                                        )
                                        print(
                                            f"""
    {title}
    {_load['artistDisplayName']}
    {_load['primaryImageSmall']}
    {_load['primaryImage']}
"""
                                        )
                        # リクエスト制限
                        time.sleep(0.1)
                        if cnt > 100:
                            break
    print(res)
    print(f"total:{total}")

def sain(query: str = "sunflowers") -> None:
    """1. キーワード検索 2. 該当する作品の情報を得る
    Document URL:https://metmuseum.github.io/
    """
    domain = "https://collectionapi.metmuseum.org"

    request = requests.get(
        f"{domain}/public/collection/v1/search?q={query}&=hasImages=true", timeout=10
    )

    match request.status_code:
        case 200:
            match json.loads(request.text):
                case {"total": total, "objectIDs": ids} if total > 0:
                    for id in ids:
                        print(f"https://www.metmuseum.org/art/collection/search/{id}")

main()
