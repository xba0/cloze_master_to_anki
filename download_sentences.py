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
    "cookie": "******",
    "dnt": "1",
    "priority": "u=1, i",
    "referer": "https://www.clozemaster.com/l/cmn-eng",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "time-zone-offset-hours": "8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "x-csrf-token": "**********",
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
    # download_collection("203/c/1949", "Cm-Ind-MC100")
    # download_collection("203/c/1950", "Cm-Ind-MC500")
    # download_collection("203/c/1951", "Cm-Ind-MC1000")
    # download_collection("203/c/1952", "Cm-Ind-MC2000")
    # download_collection("203/c/1953", "Cm-Ind-MC3000")
    # download_collection("203/c/1954", "Cm-Ind-MC4000")
    for level in range(1, 11):
        download_collection(
            "88/c/" + str(26847 + level), "cm-en-zh/FastTrackLevel" + str(level)
        )
    download_collection("88/c/363", "cm-en-zh/MostCommon100")
    download_collection("88/c/364", "cm-en-zh/MostCommon200")
    download_collection("88/c/365", "cm-en-zh/MostCommon500")
    download_collection("88/c/366", "cm-en-zh/MostCommon1000")
    download_collection("88/c/367", "cm-en-zh/MostCommon2000")
    download_collection("88/c/368", "cm-en-zh/MostCommon5000")
    download_collection("88/c/369", "cm-en-zh/MostCommonGT5000")
