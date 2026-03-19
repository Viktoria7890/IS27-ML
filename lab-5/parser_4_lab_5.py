import os
import time
import requests

BASE_URL = "https://commons.wikimedia.org/w/api.php"
OUT_DIR = "data_wikimedia"
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "bigcats-ml-lab/1.0 (student project; contact:my_pochta_swwwwwwwaaaaag@gmail.com)"
}

def fetch_from_category(category, n_images=200):
    urls = []
    params = {
        "action": "query",
        "format": "json",
        "generator": "categorymembers",
        "gcmtitle": category,
        "gcmnamespace": 6,
        "gcmlimit": 50,
        "prop": "imageinfo",
        "iiprop": "url",
    }

    cont = {}

    while len(urls) < n_images:
        actual = params.copy()
        actual.update(cont)

        resp = requests.get(BASE_URL, params=actual, headers=HEADERS, timeout=15)

        if resp.status_code != 200:
            print(f"[WARN] HTTP {resp.status_code}: {resp.text[:200]}")
            break

        data = resp.json()

        pages = data.get("query", {}).get("pages", {})
        if not pages:
            print("[INFO] Больше результатов нет")
            break

        for p in pages.values():
            info = p.get("imageinfo")
            if info:
                url = info[0].get("url")
                if url and url.lower().endswith((".jpg", ".jpeg", ".png")):
                    urls.append(url)
                    if len(urls) >= n_images:
                        break

        if "continue" in data and len(urls) < n_images:
            cont = data["continue"]
        else:
            break

        time.sleep(0.3)

    print(f"[INFO] {len(urls)} images from {category}")
    return urls

def download_images(urls, save_dir, prefix="img"):
    os.makedirs(save_dir, exist_ok=True)
    for i, url in enumerate(urls, start=1):
        clean = url.split("?")[0]
        ext = os.path.splitext(clean)[1]
        if ext == "":
            ext = ".jpg"
        filename = f"{prefix}_{i:04d}{ext}"
        path = os.path.join(save_dir, filename)

        if os.path.exists(path):
            continue

        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    f.write(r.content)
                print(f"[OK] {path}")
            else:
                print(f"[ERR] {r.status_code} {url}")
        except Exception as e:
            print(f"[ERR] {url} -> {e}")

        time.sleep(0.2)


def build_bigcats_dataset(
    n_lions=200,
    n_tigers=200,
):
    lion_urls = fetch_from_category("Category:Panthera leo", n_images=n_lions)
    download_images(lion_urls, os.path.join(OUT_DIR, "lion"), prefix="lion")

    tiger_urls = fetch_from_category("Category:Panthera tigers", n_images=n_tigers)
    download_images(tiger_urls, os.path.join(OUT_DIR, "tiger"), prefix="tiger")

if __name__ == "__main__":
    build_bigcats_dataset(
        n_lions=600,
        n_tigers=600,
    )