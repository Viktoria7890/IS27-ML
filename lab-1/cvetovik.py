import csv, json, os, random, time, string
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from config import BASE, OUT, COLS, UA, FLOWERS, NON_FLOWER_TOKENS, CATEGORIES

S = requests.Session()

def GET(u, timeout=(6,20)):
    try:
        return S.get(u, headers={"User-Agent": random.choice(UA)}, timeout=timeout)
    except requests.RequestException:
        return None

def text(soup, css):
    el = soup.select_one(css)
    return el.get_text(" ", strip=True) if el else ""

def tokens(txt):
    if not txt: return []
    tbl = str.maketrans({c:" " for c in (string.punctuation+"«»„”…—–\t\r\n")})
    return [t for t in (txt or "").lower().translate(tbl).split() if t]

def to_float_any(txt):
    if not txt: return None
    s = txt.replace(" ","").replace(",",".")
    buf, got, dot = "", False, False
    for ch in s:
        if ch.isdigit(): buf+=ch; got=True
        elif ch=="." and got and not dot: buf+=ch; dot=True
        elif got: break
    try: return float(buf) if buf else None
    except: return None

def product_links(list_url, soup):
    out, seen = [], set()
    for a in soup.select(".product-item .product-item-name a[href^='/catalog/'], a.product-item__title[href^='/catalog/']"):
        href = (a.get("href") or "").split("#")[0].strip()
        if not href: continue
        u = urljoin(list_url, href)
        if u in seen: continue
        seen.add(u); out.append(u)
    return out

def price_from_soup(soup):
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            obj = json.loads((tag.string or tag.text or "").strip())
        except:
            continue
        for o in (obj if isinstance(obj, list) else [obj]):
            if not isinstance(o, dict): continue
            tp, off = o.get("@type"), o.get("offers")
            if tp=="Product" or (isinstance(tp,list) and "Product" in tp):
                off = off[0] if isinstance(off, list) and off else off
                if isinstance(off, dict):
                    for k in ("price","lowPrice","highPrice"):
                        v = to_float_any(str(off.get(k)));
                        if v is not None: return v
    for css in ("#price_container [data-price]","#price_container [itemprop='price']",".product-card-price",".price","[itemprop='price']"):
        for el in soup.select(css):
            v = to_float_any(el.get("content") or el.get("value") or el.get_text(" ", strip=True))
            if v is not None: return v
    return to_float_any(soup.get_text(" ", strip=True))

def rating_and_count(soup):
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            obj = json.loads((tag.string or tag.text or "").strip())
        except:
            continue
        for o in (obj if isinstance(obj, list) else [obj]):
            ag = o.get("aggregateRating") if isinstance(o, dict) else None
            if isinstance(ag, dict):
                r = to_float_any(str(ag.get("ratingValue") or ag.get("rating")))
                rc = ag.get("ratingCount") or ag.get("reviewCount")
                if isinstance(rc, str) and rc.isdigit(): rc = int(rc)
                if isinstance(rc, (float,int)) and r is not None: return float(r), int(rc)
    r = to_float_any(text(soup, ".star-enabled small")) or 0.0
    rc_txt = text(soup, ".star-enabled .star-disabled.small")
    return float(r), (int(rc_txt) if rc_txt.isdigit() else 0)

def composition_from(name, desc):
    bag = tokens((name or "")+" "+(desc or "")); res, seen = [], set()
    has_santini = any(w.startswith("сантини") for w in bag)
    for w in bag:
        if w in NON_FLOWER_TOKENS: continue
        if has_santini and w.startswith("ромашк"): continue
        base = FLOWERS.get(w)
        if base and base not in seen:
            seen.add(base); res.append(base)
        if len(res) >= 2: break
    return ", ".join(res)

def num_flowers_from(name, desc):
    bag = tokens((name or "")+" "+(desc or ""))
    units = ("шт","штук","цвет","цвета","цветов","роз","тюльпан","тюльпана","тюльпанов",
             "хризантем","лилий","пионов","ирисов","гладиолус","гладиолусов")
    for i in range(len(bag)-1):
        if bag[i].isdigit() and any(bag[i+1].startswith(u) for u in units): return int(bag[i])
    for i,w in enumerate(bag):
        if w.isdigit() and any(u in "".join(bag[i+1:i+3]) for u in units): return int(w)
    return None

def aroma_from(soup):
    for span in soup.select("div.aroma-container ul.list-aromas li span"):
        v = (span.get_text(" ", strip=True) or "").lower()
        if v: return v
    return ""

def bonus_from(soup, desc):
    for t in (text(soup, ".product-card-info-bonuses")+" "+(desc or "")).split():
        if t.isdigit(): return int(t)
    return None

def city_from(soup):
    el = soup.select_one('[href="#chooseRegionModal"]')
    return el.get_text(" ", strip=True) if el else ""

def parse_pdp(url):
    r = GET(url);
    if not (r and r.ok): return None
    s = BeautifulSoup(r.text, "lxml")
    pid = (s.select_one("input#loaded_product[value]") or {}).get("value","").strip()
    if not pid:
        can = s.select_one('link[rel="canonical"]'); href = can.get("href") if can and can.get("href") else url
        pid = href.strip("/").split("/")[-1]
    name = text(s, "h1#product_title_desktop") or text(s, "h1")
    price = price_from_soup(s)
    if not (pid and name and price): return None
    rating, rc = rating_and_count(s)
    if rating <= 0 or rc <= 0: return None
    desc = text(s, "#product_tab_description_content") or text(s, ".product-card-info-description")
    return {
        "product_id": pid, "name": name,
        "rating": float(rating), "rating_count": int(rc),
        "num_flowers": num_flowers_from(name, desc),
        "aroma": aroma_from(s),
        "composition_flowers": composition_from(name, desc),
        "target_price": float(price),
        "bonus": bonus_from(s, desc),
        "city": city_from(s),
    }

def ensure_csv():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if not os.path.exists(OUT):
        with open(OUT, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=COLS).writeheader()

def run(categories=CATEGORIES, rate=0.3):
    ensure_csv(); saved = 0
    for base, pages in categories:
        print(f"\nКатегория: {base} (1..{pages})")
        for p in range(1, pages+1):
            url = base if p == 1 else f"{base}?page={p}"
            r = GET(url);
            if not (r and r.ok): break
            soup = BeautifulSoup(r.text, "lxml")
            links = product_links(url, soup)
            print(f"  {url} -> {len(links)} карточек")
            if not links: break
            for u in links:
                time.sleep(rate + random.random()*0.15)
                row = parse_pdp(u)
                if not row: continue
                with open(OUT, "a", newline="", encoding="utf-8") as f:
                    csv.DictWriter(f, fieldnames=COLS).writerow(row); saved += 1
    print(f"\nSaved {saved} rows -> {OUT}")

if __name__ == "__main__":
    run()
