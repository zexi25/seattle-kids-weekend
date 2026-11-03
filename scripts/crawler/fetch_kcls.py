import html
import re
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

KCLS_BRANCH_GEO = {
    "Bellevue": {
        "coords": [-122.1931, 47.6186],
        "address": "1111 110th Ave NE, Bellevue, WA 98004",
        "city": "Bellevue",
        "region": "eastside"
    },
    "Redmond": {
        "coords": [-122.1264, 47.6784],
        "address": "15990 NE 85th St, Redmond, WA 98052",
        "city": "Redmond",
        "region": "eastside"
    },
    "Kirkland": {
        "coords": [-122.2045, 47.6765],
        "address": "308 Kirkland Ave, Kirkland, WA 98033",
        "city": "Kirkland",
        "region": "eastside"
    },
    "Issaquah": {
        "coords": [-122.0366, 47.5301],
        "address": "10 W Sunset Way, Issaquah, WA 98027",
        "city": "Issaquah",
        "region": "eastside"
    },
    "Renton": {
        "coords": [-122.2081, 47.4816],
        "address": "100 Mill Ave S, Renton, WA 98057",
        "city": "Renton",
        "region": "south"
    },
    "Sammamish": {
        "coords": [-122.0315, 47.6174],
        "address": "825 228th Ave SE, Sammamish, WA 98075",
        "city": "Sammamish",
        "region": "eastside"
    },
    "Mercer Island": {
        "coords": [-122.2285, 47.5796],
        "address": "4400 88th Ave SE, Mercer Island, WA 98040",
        "city": "Mercer Island",
        "region": "eastside"
    }
}

DEFAULT_KCLS_GEO = KCLS_BRANCH_GEO["Bellevue"]

def _infer_attributes(title: str, desc: str):
    text = f"{title} {desc}".lower()
    
    age_buckets = []
    if any(k in text for k in ['baby', 'toddler', 'preschool', 'storytime', 'infant', '0-5', 'early learning', 'play & learn']):
        age_buckets.append('preschool')
    if any(k in text for k in ['kids', 'elementary', 'school-age', 'steam', 'lego', 'math', '6-12', 'robot', 'fossil', 'science']):
        age_buckets.append('elementary')
    if not age_buckets:
        age_buckets = ['preschool', 'elementary']

    if any(k in text for k in ['story', 'craft', 'music', 'sing', 'book', 'rhyme', 'art', 'reading']):
        category = 'music_crafts'
    elif any(k in text for k in ['nature', 'animal', 'farm', 'garden', 'dino', 'fossil', 'outdoor', 'zoo']):
        category = 'nature_animals'
    elif any(k in text for k in ['festival', 'market', 'fair', 'celebration', 'parade']):
        category = 'festivals_markets'
    else:
        category = 'exploration_exp'

    environment = 'outdoor' if any(k in text for k in ['outdoor', 'park', 'garden', 'trail', 'farm']) else 'indoor'
    return age_buckets, category, environment

def _is_kids_relevant(title: str, desc: str):
    """过滤出适合儿童和家庭的活动"""
    text = f"{title} {desc}".lower()
    kids_keywords = [
        'storytime', 'children', 'kids', 'baby', 'toddler', 'preschool',
        'family', 'steam', 'lego', 'play & learn', 'craft', 'puppet', 'teen'
    ]
    # 排除纯成人主题
    exclude_keywords = ['tax help', 'medicare', 'esl', 'job search', 'citizenship class', 'adult book club']
    if any(e in text for e in exclude_keywords):
        return False
    return any(k in text for k in kids_keywords)

def fetch_kcls_events():
    url = "https://kcls.bibliocommons.com/events/rss/all"
    headers = {"User-Agent": "Mozilla/5.0"}
    features = []

    print("[KCLS] 正在拉取金县官方 RSS 订阅源...")
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        
        # 解析 XML
        root = ET.fromstring(res.content)
        items = root.findall('./channel/item')
        print(f"[KCLS] RSS 共包含 {len(items)} 条全系统活动，开始筛选儿童家庭活动...")

        for idx, item in enumerate(items):
            title = item.findtext('title', default='').strip()
            link = item.findtext('link', default='')
            raw_desc = item.findtext('description', default='')
            pub_date = item.findtext('pubDate', default='')

            # 清理 HTML 实体与标签
            clean_desc = re.sub(r'<[^>]+>', ' ', html.unescape(raw_desc))
            clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()

            if not _is_kids_relevant(title, clean_desc):
                continue

            # 匹配分馆地点与地理坐标
            branch_name = "Bellevue Library"
            geo = DEFAULT_KCLS_GEO
            for name, data in KCLS_BRANCH_GEO.items():
                if name.lower() in f"{title} {clean_desc}".lower():
                    branch_name = f"{name} Library"
                    geo = data
                    break

            age_buckets, category, environment = _infer_attributes(title, clean_desc)

            features.append({
                "type": "Feature",
                "id": f"evt_kcls_{datetime.now().strftime('%Y%m%d')}_{len(features) + 1}",
                "geometry": {
                    "type": "Point",
                    "coordinates": geo["coords"]
                },
                "properties": {
                    "title": title,
                    "summary": clean_desc[:140] + ("..." if len(clean_desc) > 140 else ""),
                    "organizer": "King County Library System",
                    "category": category,
                    "location": {
                        "venueName": branch_name,
                        "address": geo["address"],
                        "city": geo["city"],
                        "region": geo["region"],
                        "googleMapsUrl": f"https://maps.google.com/?q={branch_name.replace(' ', '+')}+Library"
                    },
                    "schedule": {
                        "startDate": datetime.now().strftime("%Y-%m-%d"),
                        "endDate": datetime.now().strftime("%Y-%m-%d"),
                        "timeSlot": "morning" if any(k in clean_desc.lower() for k in ['10:', '11:', 'am']) else "afternoon",
                        "displayTime": pub_date[:16] if pub_date else "周末 · 10:30–11:30"
                    },
                    "familyAttributes": {
                        "ageBuckets": age_buckets,
                        "environment": environment,
                        "isFree": True,
                        "priceLabel": "免费入场",
                        "requiresRsvp": False,
                        "strollerFriendly": True,
                        "hasChangingTable": True,
                        "parking": "free_lot"
                    },
                    "source": {
                        "originalUrl": link,
                        "sourceName": "金县公共图书馆 (KCLS)"
                    }
                }
            })

            # 控制单次写入精选数量（前 30 条高质量亲子活动）
            if len(features) >= 30:
                break

    except Exception as e:
        print(f"[KCLS] 解析异常: {e}")

    print(f"[KCLS] 筛选完成，提取到 {len(features)} 条儿童亲子活动！")
    return features

if __name__ == "__main__":
    results = fetch_kcls_events()
    print(f"单独测试 KCLS: 成功输出 {len(results)} 条")