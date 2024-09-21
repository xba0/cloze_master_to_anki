import json
import math
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests as rq
from tqdm import tqdm

# TODO: replace the following with yours (copy from the browser console)
HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,id;q=0.6",
    "baggage": "sentry-environment=production,sentry-public_key=270247323506691a6039203bf8f3b0bf,sentry-trace_id=c77a06458dcc40b8bd17f3770ab492f2,sentry-sample_rate=1,sentry-sampled=true",
    "cookie": "_hjSessionUser_213069=eyJpZCI6IjNiOGZiYjcwLTU5YmEtNWY0MC04YTZlLWI4YzY3ZTJlNjVlMiIsImNyZWF0ZWQiOjE3MTA4NTkyODg0MjIsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.1049099302.1708397689; _ga_4CWWQZXE57=GS1.1.1719816909.17.0.1719816921.48.0.769698588; timezone=Asia/Hong_Kong; _clozemaster_session=fTmylPn%2BdMsHArs0RzchbcJi1whm5G9Pc4GhzMW8mlusQIaT%2FpT5SVUz%2FpXmBoN%2BonVz1xj%2FwGypG6pfIsR%2Bn294EdNgLllxtMJCAmew%2BG8%2F153UEn63YzxtyIy5i08Chh0Rh7u4Q3TgYUdgpZBHQLqI7LcyTzU1TaHhyAWMl8aGRQFFKmjT04XpBcfo375xaz4%2BEHsfgXLaQa%2F5Dj3VLxFEuiCawhsLvTtrrAZ4L%2BzjGeR%2BIH2AOGLbm0q7eRI0GdqYHv%2FmGDMrfuU%2BNj3mLdj%2FtQ5zMDcKdQLKvOESbJiCsz7qldIUbwytemmOb%2Fc74Q4Bao4muSiogoP3wrcVjmvutpDJK17IbMAPK9cvbN3sXhziMc89Mbba9iAE9ZUtsBYICQxU5hb%2FariA%2BxTc6UPH80U%3D--8Ax3eBCu%2FQX4HS0V--%2FZgivTkRqMWoCRK23WXN0w%3D%3D",
    "dnt": "1",
    "if-none-match": 'W/"15eda3345864d2c87307f8e77348cfd9"',
    "priority": "u=1, i",
    "referer": "https://www.clozemaster.com/l/eng-cmn/collections/random-4959f770-9ddc-480f-88e3-26335e930372/play?scope=&skill=vocabulary&count=10&mode=multiple_choice",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sentry-trace": "c77a06458dcc40b8bd17f3770ab492f2-ad39836c1e6ea308-1",
    "time-zone-offset-hours": "8",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    "x-csrf-token": "navGs77P-4391qef0zzXVOech-dDDSlN-96PMtZqYREqcdOmsswvuVBM0lJJ80FtmPGkcCk0wMqYJJZLKPWWPQ",
    "x-requested-with": "XMLHttpRequest",
}


def download_page(collection, page, save_dir, use_cache=True):
    page_file = f"{save_dir}/{page}.json"
    if use_cache and os.path.exists(page_file):
        with open(page_file, "r") as f:
            data = json.load(f)
    else:
        url = f"https://www.clozemaster.com/api/v1/lp/{collection}/ccs?context=sentences&page={page}&perPage=20&query=&scope=all"
        resp = rq.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        with open(page_file, "w") as f:
            json.dump(data, f, ensure_ascii=False)
    assert data["page"] == page
    return (
        data["collection"]["name"],
        data["page"],
        data["total"],
        data["collectionClozeSentences"],
    )


def download_collection(collection, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    name, _, total, sents = download_page(collection, 1, save_dir)
    data = {"name": name, "total": total, "sents": sents}

    PAGE_SIZE = 20

    pool = ThreadPoolExecutor(max_workers=5)
    tasks = []
    for page in range(2, math.ceil(total / PAGE_SIZE)):
        task = pool.submit(download_page, collection, page, save_dir)
        tasks.append(task)
        # download_page(collection, page, save_dir)

    for _ in tqdm(as_completed(tasks), total=len(tasks)):
        pass

    for page in range(2, math.ceil(total / PAGE_SIZE)):
        _, _, _, sents = download_page(collection, page, save_dir)
        data["sents"].extend(sents)

    with open(f"{save_dir}/all.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # download_collection("11/c/30", "english-chinese")
    # download_collection("203/c/1948", "eng-ind-fluent-fast")
    download_collection("203/c/1949", "Cm-Ind-MC100")
    download_collection("203/c/1950", "Cm-Ind-MC500")
    download_collection("203/c/1951", "Cm-Ind-MC1000")
    download_collection("203/c/1952", "Cm-Ind-MC2000")
    download_collection("203/c/1953", "Cm-Ind-MC3000")
    download_collection("203/c/1954", "Cm-Ind-MC4000")

