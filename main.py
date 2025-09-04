from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import csv, time, re

TARGETS = [
    {"user_id": "20140998", "series_id": "4362"},   # 2021 影片教學
    {"user_id": "20140998", "series_id": "5461"},   # 2023 python爬蟲
    {"user_id": "20140998", "series_id": "5718"},   # 2023 java
    {"user_id": "20140998", "series_id": "7373"},   # 2024 network
    {"user_id": "20140998", "series_id": "8438"}    # 2025 vibe coding
]

OUT_FILE = Path("ithome_all_series.csv")

def digits(s: str) -> str:
    m = re.search(r"\d[\d,]*", s or "")
    return m.group(0).replace(",", "") if m else "0"

def text(el) -> str:
    return (el.get_attribute("innerText") or "").strip()

def setup_driver(headless=False):
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--lang=zh-TW")
    opts.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36")
    opts.add_argument("--window-size=1400,1000")
    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 45)
    return driver, wait

def wait_list_loaded(driver, wait):
    selectors = [
        "a.qa-list__title-link",
        "div.qa-list",
        "div.profile-list__item",
        "li.profile-list__item",
        "div.profile-list",
        ".ir-profile-list",
        ".profile-list__content",
    ]
    return wait.until(lambda d: any(d.find_elements(By.CSS_SELECTOR, sel) for sel in selectors))

def get_rows(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "div.qa-list")
    if not rows:
        rows = driver.find_elements(By.CSS_SELECTOR, "div.profile-list__item, li.profile-list__item")
    return rows

def find_title_el(row):
    for sel in ["a.qa-list__title-link", "a.profile-list__title-link", "a[href*='/articles/']"]:
        found = row.find_elements(By.CSS_SELECTOR, sel)
        if found:
            return found[0]
    return None

def read_counts_from_row(driver, row):
    like = comment = view = "0"
    for b in row.find_elements(By.CSS_SELECTOR, "div.profile-list__condition a.qa-condition"):
        label_el = b.find_elements(By.CSS_SELECTOR, ".qa-condition__text")
        count_el = b.find_elements(By.CSS_SELECTOR, ".qa-condition__count")
        label = text(label_el[0]) if label_el else ""
        count = digits(text(count_el[0]) if count_el else "")
        if "Like" in label:   like = count
        elif "留言" in label: comment = count
        elif "瀏覽" in label: view = count
    return like, comment, view

def scrape_one_series(driver, wait, user_id, series_id):
    base = f"https://ithelp.ithome.com.tw/users/{user_id}/ironman/{series_id}"
    page = 1
    rows_out = []

    while True:
        driver.get(f"{base}?page={page}")
        try:
            wait_list_loaded(driver, wait)
        except:
            break

        rows = get_rows(driver)
        if not rows:
            break

        page_has_any = False
        for row in rows:
            title_el = find_title_el(row)
            if not title_el:
                continue
            page_has_any = True
            title = text(title_el)
            like, comment, view = read_counts_from_row(driver, row)
            rows_out.append({
                "user_id": user_id,
                "series_id": series_id,
                "page": page,
                "title": title,
                "like": like,
                "comment": comment,
                "view": view,
            })

        if not page_has_any:
            break

        page += 1
        time.sleep(0.15)
    return rows_out

def write_single_csv(path: Path, rows):
    header = ["user_id", "series_id", "page", "title", "like", "comment", "view"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in header})

def main():
    driver, wait = setup_driver(headless=False)
    all_rows = []
    try:
        for t in TARGETS:
            all_rows.extend(scrape_one_series(driver, wait, t["user_id"], t["series_id"]))
    finally:
        driver.quit()

    all_rows.sort(key=lambda r: (r["user_id"], r["series_id"], r["page"]))
    write_single_csv(OUT_FILE, all_rows)
    print(f"→ 已輸出：{OUT_FILE.resolve()}")

if __name__ == "__main__":
    main()
