import re
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

KCLS_API_URL = "https://gateway.bibliocommons.com/v2/libraries/kcls/events"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

CATEGORY_RULES = {
    "nature_animals": ["nature", "animal", "wildlife", "garden", "outdoor", "zoo", "bird", "park"],
    "music_crafts": ["music", "concert", "sing", "craft", "art", "maker", "paint", "origami", "clay", "rhyme"],
    "festivals_markets": ["festival", "celebrate", "fair", "market", "holiday", "storytelling", "puppet"],
    "exploration_exp": ["lego", "stem", "steam", "robot", "science", "code", "coding", "chess", "game", "tinker"]
}

BRANCH_COORDS = {
    "bellevue": [-122.1932, 47.6185],
    "redmond": [-122.1215, 47.6740],
    "kirkland": [-122.2030, 47.6765],
    "mercer island": [-122.2285, 47.5750],
    "renton": [-122.2035, 47.4795],
    "issaquah": [-122.0405, 47.5301],
    "sammamish": [-122.0305, 47.6165],
    "bothell": [-122.2065, 47.7600],
    "kenmore": [-122.2450, 47.7570],
    "shoreline": [-122.3450, 47.7560],
    "federal way": [-122.3125, 47.3150],
    "woodinville": [-122.1550, 47.7540],
    "auburn": [-122.2285, 47.3075],
    "newcastle": [-122.1700, 47.5390],
    "kingsgate": [-122.1950, 47.7050],
    "lake hills": [-122.1450, 47.6080],
    "newport way": [-122.1750, 47.5750],
    "maple valley": [-122.0450, 47.3850],
    "kent": [-122.2300, 47.3800]
}

def infer_category(title, summary):
    text = f"{title} {summary}".lower()
    for cat, kws in CATEGORY_RULES.items():
        if any(kw in text for kw in kws):
            return cat
    return "exploration_exp"

def infer_region(city_or_branch):
    text = city_or_branch.lower()
    if any(k in text for k in ["bellevue", "redmond", "kirkland", "mercer", "issaquah", "sammamish", "newcastle", "newport"]):
        return "eastside"
    if any(k in text for k in ["bothell", "kenmore", "shoreline", "woodinville", "kingsgate"]):
        return "north"
    if any(k in text for k in ["renton", "kent", "auburn", "federal way", "maple valley"]):
        return "south"
    return "eastside"

def fetch_kcls_events():
    print("[KCLS] 正在连接金县官方 Gateway API...")
    
    # 明确西雅图本地时区 (Pacific Time)
    seattle_tz = ZoneInfo("America/Los_Angeles")
    now = datetime.now(seattle_tz)
    start_str = now.strftime("%Y-%m-%d")
    end_str = (now + timedelta(days=30)).strftime("%Y-%m-%d")

    # 查询未来 30 天，已在 API 层面直接限定为 Kids & Families 分类
    params = {
        "startDate": start_str,
        "endDate": end_str,
        "audiences": "605a5a1f6a01492400511874,605a5a226a01492400511875",
        "limit": 100
    }

    try:
        res = requests.get(KCLS_API_URL, headers=HEADERS, params=params, timeout=15)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print(f"[KCLS] ⚠️ 请求官方 API 异常: {e}")
        return []

    entities = data.get("entities", {})
    events_map = entities.get("events", {})
    locations_map = entities.get("locations", {})

    print(f"[KCLS] 成功获取 {len(events_map)} 条儿童/家庭活动，按西雅图本地时区严格提取周末场次...")

    features = []

    for event_id, item in events_map.items():
        title = item.get("title", "")
        desc = item.get("description", "") or item.get("briefDescription", "")
        full_text = f"{title} {desc}".lower()

        # 1. 严格使用 ISO 解析并转换为西雅图当地时间
        start_iso = item.get("start")
        if not start_iso:
            continue

        try:
            # 标准化 UTC 字符串并转为西雅图时区
            if start_iso.endswith("Z"):
                start_iso = start_iso.replace("Z", "+00:00")
            utc_dt = datetime.fromisoformat(start_iso)
            event_dt = utc_dt.astimezone(seattle_tz)
        except Exception:
            continue

        # 2. 严格按西雅图本地时间判断是否为周末 (周六=5, 周日=6)
        if event_dt.weekday() not in (5, 6):
            continue

        day_name = "周六" if event_dt.weekday() == 5 else "周日"
        date_str = event_dt.strftime("%Y-%m-%d")
        display_time = f"{event_dt.strftime('%m月%d日')} ({day_name}) · {event_dt.strftime('%H:%M')}"
        time_slot = "morning" if event_dt.hour < 12 else "afternoon"

        # 3. 提取分馆
        loc_id = item.get("locationId")
        loc_data = locations_map.get(loc_id, {})
        venue_name = loc_data.get("name") or "KCLS Library"
        clean_branch = venue_name.replace("Library", "").strip()

        # 匹配经纬度与区域
        coords = [-122.1932, 47.6185]
        for key, c in BRANCH_COORDS.items():
            if key in clean_branch.lower():
                coords = c
                break

        region = infer_region(clean_branch)
        category = infer_category(title, desc)

        clean_summary = re.sub(r"<[^>]+>", "", desc).strip()
        if len(clean_summary) > 160:
            clean_summary = clean_summary[:160] + "..."

        event_link = f"https://kcls.bibliocommons.com/events/{event_id}"

        features.append({
            "type": "Feature",
            "id": f"evt_kcls_{event_id}",
            "geometry": {
                "type": "Point",
                "coordinates": coords
            },
            "properties": {
                "title": title,
                "summary": clean_summary or "金县公共图书馆周末精选亲子活动。",
                "organizer": f"KCLS ({clean_branch})",
                "category": category,
                "location": {
                    "venueName": venue_name,
                    "address": loc_data.get("address", f"{clean_branch}, WA"),
                    "city": clean_branch,
                    "region": region,
                    "googleMapsUrl": f"https://maps.google.com/?q={venue_name.replace(' ', '+')}"
                },
                "schedule": {
                    "startDate": date_str,
                    "endDate": date_str,
                    "timeSlot": time_slot,
                    "displayTime": display_time
                },
                "familyAttributes": {
                    "ageBuckets": ["preschool"] if any(b in full_text for b in ["toddler", "baby", "play & learn", "infant"]) else ["preschool", "elementary"],
                    "environment": "indoor",
                    "isFree": True,
                    "priceLabel": "免费入场",
                    "requiresRsvp": bool(item.get("isRegistrationRequired", False)),
                    "strollerFriendly": True,
                    "hasChangingTable": True,
                    "parking": "free_lot"
                },
                "source": {
                    "originalUrl": event_link,
                    "sourceName": "金县图书馆 (KCLS)"
                }
            }
        })

    print(f"[KCLS] 筛选完成：成功提取出 {len(features)} 条符合条件的周末儿童活动！")
    return features

if __name__ == "__main__":
    res = fetch_kcls_events()
