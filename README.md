# iThome Ironman Scraper

一個簡單的 Python + Selenium 爬蟲工具，用來批次抓取 iThome 鐵人賽系列文章的：

- 文章標題
- Like 數
- 留言數
- 瀏覽數

並自動輸出成一份 CSV 檔，方便後續統計或視覺化分析。

## 📂 專案結構

```
.
├── main.py              # 主程式
├── requirements.txt     # 依賴套件
└── ithome_all_series.csv (程式執行後產生)
```

## 功能特色

- 支援多系列一次爬取（可在 TARGETS 列表中設定多個 user_id / series_id）
- 自動判斷頁數，逐頁抓取
- 容錯處理：不同年份 iThome 網頁 class 名稱有差異，程式會自動兼容
- 結果統一輸出到單一 CSV，便於整理分析

## 安裝與執行

### 1. 下載專案

```bash
git clone https://github.com/<你的帳號>/<repo 名稱>.git
cd <repo 名稱>
```

### 2. 建立虛擬環境並安裝套件

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### 3. 編輯目標系列

打開 `main.py`，修改最上方的 TARGETS 列表，例如：

```python
TARGETS = [
    {"user_id": "20140998", "series_id": "4362"},  # 2021 影片教學
    {"user_id": "20140998", "series_id": "5461"},  # 2023 python爬蟲
]
```

### 4. 執行程式

```bash
python main.py
```

執行後，結果會輸出到：

```
out/ithome_all_series.csv
```

## 輸出格式 (CSV)

範例：

| user_id | series_id | page | title | like | comment | view |
|---------|-----------|------|-------|------|---------|------|
| 20140998 | 4362 | 1 | 每個人都該學的30個Python技巧｜技巧 1：快樂學Python ... | 12 | 3 | 20366 |
| 20140998 | 4362 | 1 | 每個人都該學的30個Python技巧｜技巧 2：Python語法基礎 ... | 2 | 0 | 4318 |

## 環境需求

- Python 3.9+
- Google Chrome（最新版）
- Selenium 4+
