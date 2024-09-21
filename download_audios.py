import json
import math
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests as rq
from tqdm import tqdm


def download_file(url, save_path):
    if os.path.exists(save_path) and os.fstat(save_path).st_size > 10:
        return

    resp = rq.get(url)
    resp.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(resp.content)


def download_audios(collection_dir):
    save_dir = collection_dir + "/audios/"

    pool = ThreadPoolExecutor(max_workers=25)
    tasks = []
    os.makedirs(save_dir, exist_ok=True)
    with open(collection_dir + "/all.json") as f:
        data = json.load(f)
        for e in data["sents"]:
            url = e["ttsAudioUrl"]
            save_path = save_dir + "/" + e["ttsAudioUrl"].rsplit("/")[-1]
            task = pool.submit(download_file, url, save_path)
            tasks.append(task)

    for _ in tqdm(as_completed(tasks), total=len(tasks)):
        pass


if __name__ == "__main__":
    # download_audios("english-chinese")
    # download_audios("eng-ind-fluent-fast")
    for n in [100,500,1000,2000,3000,4000]:
        download_audios(f"Cm-Ind-MC{n}")
