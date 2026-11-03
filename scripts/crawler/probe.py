# scripts/crawler/probe.py
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# 1. 探测 SPL 的公开 RSS 日历源
url_spl_rss = "https://seattle.bibliocommons.com/events/rss/all"
res_spl = requests.get(url_spl_rss, headers=headers, timeout=10)
print(f"[SPL RSS] 状态码: {res_spl.status_code}, 内容长度: {len(res_spl.text)}")
if res_spl.status_code == 200:
    print(f"[SPL RSS] 前 200 字预览:\n{res_spl.text[:200]}\n")

# 2. 探测 KCLS 的公开 RSS 日历源
url_kcls_rss = "https://kcls.bibliocommons.com/events/rss/all"
res_kcls = requests.get(url_kcls_rss, headers=headers, timeout=10)
print(f"[KCLS RSS] 状态码: {res_kcls.status_code}, 内容长度: {len(res_kcls.text)}")
if res_kcls.status_code == 200:
    print(f"[KCLS RSS] 前 200 字预览:\n{res_kcls.text[:200]}\n")