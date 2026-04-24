# -*- coding: utf-8 -*-
"""각 제품의 officialLink / affiliateLink 에서 og:image 를 수집해 products.json 에 imageUrl 로 저장."""
import json
import re
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "products.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "ko,en;q=0.9",
}

OG_PATTERNS = [
    re.compile(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']', re.I),
    re.compile(r'<meta[^>]*name=["\']twitter:image["\'][^>]*content=["\']([^"\']+)["\']', re.I),
]


def fetch_og(url: str, timeout: int = 8) -> str:
    if not url:
        return ""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(500_000)
        html = raw.decode("utf-8", errors="ignore")
        for pat in OG_PATTERNS:
            m = pat.search(html)
            if m:
                img = m.group(1).strip()
                if img.startswith("//"):
                    img = "https:" + img
                return img
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception):
        pass
    return ""


def resolve_image(product: dict) -> str:
    for key in ("officialLink", "affiliateLink"):
        url = product.get(key, "")
        if not url:
            continue
        img = fetch_og(url)
        if img:
            return img
    return ""


def main():
    with SRC.open("r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    print(f"[*] {total} products. fetching og:image ...", flush=True)

    done = 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = {ex.submit(resolve_image, p): i for i, p in enumerate(data)}
        for fut in as_completed(futures):
            i = futures[fut]
            try:
                data[i]["imageUrl"] = fut.result() or ""
            except Exception:
                data[i]["imageUrl"] = ""
            done += 1
            if done % 20 == 0 or done == total:
                print(f"  {done}/{total}", flush=True)

    with SRC.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    found = sum(1 for p in data if p.get("imageUrl"))
    print(f"[+] done. imageUrl filled: {found}/{total}")


if __name__ == "__main__":
    main()
