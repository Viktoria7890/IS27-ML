import csv
import time
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.banki.ru/services/responses/bank/alfabank/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0 Safari/537.36"
    )
}


def get_soup(page: int) -> BeautifulSoup:
    params = {
        "page": page,
        "isMobile": "0",
    }
    resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_list_page(page: int) -> List[Dict]:
    soup = get_soup(page)
    reviews = []

    for block in soup.select("div.la8a5ef73"):


        title_tag = block.select_one("h3 a")
        title = title_tag.get_text(strip=True) if title_tag else ""

        rating_tag = block.select_one("div.l8887a9d8 div.lb3db10af")
        if rating_tag:
            try:
                rating = int(rating_tag.get_text(strip=True))
            except ValueError:
                rating = None
        else:
            rating = None


        if rating is None:
            target = ""
        elif rating >= 4:
            target = "positive"
        elif rating <= 2:
            target = "negative"
        else:
            target = "neutral"

        text_tag = block.select_one("div.l22dd3882")
        text = text_tag.get_text(" ", strip=True) if text_tag else ""

        dt_tag = block.select_one("span.l0caf3d5f")
        date_str = ""
        time_str = ""

        if dt_tag:
            dt_raw = dt_tag.get_text(strip=True)
            parts = dt_raw.split()
            if len(parts) >= 2:
                date_str, time_str = parts[0], parts[1]
            elif len(parts) == 1:
                date_str = parts[0]

        reviews.append(
            {
                "title": title,
                "rating": rating,
                "text": text,
                "date": date_str,
                "time": time_str,
                "target": target,
            }
        )

    return reviews


def scrape_alfabank_reviews(
    min_reviews: int = 1000,
    max_pages: int = 500,
    out_csv: str = "alfabank_reviews.csv",
    delay_sec: float = 1.0,
) -> None:

    all_reviews: List[Dict] = []
    page = 1

    while len(all_reviews) < min_reviews and page <= max_pages:
        print(f"[INFO] Парсим страницу {page} (сейчас собрано {len(all_reviews)} отзывов)")

        page_reviews = parse_list_page(page)

        if not page_reviews:
            print("[INFO] Отзывы закончились — выходим.")
            break

        all_reviews.extend(page_reviews)
        print(f"[INFO] После страницы {page} всего отзывов: {len(all_reviews)}")

        page += 1
        if delay_sec > 0:
            time.sleep(delay_sec)

    if len(all_reviews) > 200000:
        print(f"[INFO] Собрано {len(all_reviews)} отзывов. Обрезаем до 200000.")
        all_reviews = all_reviews[:200000]

    fieldnames = ["title", "rating", "text", "date", "time", "target"]

    print(f"[INFO] Сохраняем {len(all_reviews)} отзывов в {out_csv}")

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_reviews:
            writer.writerow(r)

    print("[INFO] Готово")


if __name__ == "__main__":
    scrape_alfabank_reviews(
        min_reviews=200000,
        max_pages=500,
        out_csv="alfabank_reviews.csv",
        delay_sec=1.0,
    )
