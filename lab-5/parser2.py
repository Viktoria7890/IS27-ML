import os
import time
import requests

BASE_URL = "https://api.inaturalist.org/v1/observations"

TAXON_LION = 41964
TAXON_TIGER = 41967

N_LIONS = 500
N_TIGERS = 500

BASE_DIR = "data_wikimedia"
LION_DIR = os.path.join(BASE_DIR, "lion")
TIGER_DIR = os.path.join(BASE_DIR, "tiger")
os.makedirs(LION_DIR, exist_ok=True)
os.makedirs(TIGER_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "bigcats-ml-lab/1.0"
}


def fetch_urls(taxon_id, n_images):
    urls = []
    page = 1

    while len(urls) < n_images:
        resp = requests.get(
            BASE_URL,
            params={
                "taxon_id": taxon_id,
                "per_page": 200,
                "page": page,
                "order_by": "id",
                "order": "desc",
                "quality_grade": "research",
                "photos": True
            },
            headers=HEADERS
        )

        results = resp.json().get("results", [])
        if not results:
            break

        for obs in results:
            for p in obs.get("photos", []):
                url = p.get("url")
                if url:
                    urls.append(url.replace("square", "medium").split("?")[0])
                    if len(urls) >= n_images:
                        break
            if len(urls) >= n_images:
                break

        page += 1

    return urls


def download(urls, save_dir, prefix):
    for i, url in enumerate(urls, 1):
        ext = os.path.splitext(url)[1] or ".jpg"
        path = os.path.join(save_dir, f"{prefix}_{i:04d}{ext}")
        if not os.path.exists(path):
            img = requests.get(url).content
            with open(path, "wb") as f:
                f.write(img)
        time.sleep(0.1)


def main():
    lion_urls = fetch_urls(TAXON_LION, N_LIONS)
    download(lion_urls, LION_DIR, "lion")

    tiger_urls = fetch_urls(TAXON_TIGER, N_TIGERS)
    download(tiger_urls, TIGER_DIR, "tiger")


if __name__ == "__main__":
    main()
