import re
from datetime import datetime, timedelta

# 西雅图核心科教自然文化场馆配置字典
VENUE_PROFILES = {
    "woodland_park_zoo": {
        "venueName": "Woodland Park Zoo (林地公园动物园)",
        "coords": [-122.3543, 47.6685],
        "address": "5500 Phinney Ave N, Seattle, WA 98103",
        "city": "Seattle",
        "region": "north",
        "parking": "paid_lot",
        "admission": "需购门票",
        "url": "https://www.zoo.org"
    },
    "seattle_aquarium": {
        "venueName": "Seattle Aquarium (西雅图水族馆 & Ocean Pavilion)",
        "coords": [-122.3425, 47.6075],
        "address": "1483 Alaskan Way Pier 59, Seattle, WA 98101",
        "city": "Seattle",
        "region": "seattle",
        "parking": "paid_garage",
        "admission": "需购门票",
        "url": "https://www.seattleaquarium.org"
    },
    "pacific_science_center": {
        "venueName": "Pacific Science Center (太平洋科学中心)",
        "coords": [-122.3518, 47.6198],
        "address": "200 2nd Ave N, Seattle, WA 98109",
        "city": "Seattle",
        "region": "seattle",
        "parking": "paid_garage",
        "admission": "需购门票",
        "url": "https://pacificsciencecenter.org"
    },
    "mopop": {
        "venueName": "MoPOP (西雅图流行文化博物馆)",
        "coords": [-122.3483, 47.6215],
        "address": "325 5th Ave N, Seattle, WA 98109",
        "city": "Seattle",
        "region": "seattle",
        "parking": "paid_garage",
        "admission": "需购门票",
        "url": "https://www.mopop.org"
    }
}

# 场馆常驻核心亲子日程
STAPLE_PROGRAMS = [
    # --- Woodland Park Zoo ---
    {
        "venue_key": "woodland_park_zoo",
        "title": "Penguin & Otter Feeding Talk (企鹅与水獭保育喂食解说)",
        "summary": "饲养员现场投喂洪堡企鹅与北美水獭，讲解海洋与湿地生物习性，适合全年龄儿童近距离观察。",
        "category": "nature_animals",
        "environment": "outdoor",
        "age_buckets": ["preschool", "elementary"],
        "time_slot": "morning",
        "display_time": "周末 · 11:00 & 14:00"
    },
    {
        "venue_key": "woodland_park_zoo",
        "title": "Zoomazium Nature Play (室内自然探索与攀爬乐园)",
        "summary": "全天候恒温室内生态游戏区，提供空心巨树攀爬、感官探索台和幼儿大肢体运动区，婴儿与学步儿友好。",
        "category": "exploration_exp",
        "environment": "indoor",
        "age_buckets": ["preschool"],
        "time_slot": "afternoon",
        "display_time": "全天开放 · 09:30–16:00"
    },
    # --- Seattle Aquarium ---
    {
        "venue_key": "seattle_aquarium",
        "title": "Diver Show & Tide Pool Touch (水下潜水员互动与潮间带触摸)",
        "summary": "穿戴潜水装备的解说员在巨型穹顶水槽中与游客互动，伴随生命海滩触摸池亲手感知海星与海葵。",
        "category": "nature_animals",
        "environment": "indoor",
        "age_buckets": ["preschool", "elementary"],
        "time_slot": "afternoon",
        "display_time": "周末 · 11:30 & 13:30"
    },
    {
        "venue_key": "seattle_aquarium",
        "title": "Ocean Pavilion Discovery (全新海洋馆热带珊瑚礁探索)",
        "summary": "漫步于360度热带珊瑚礁环形通道，近距离观察斑纹鹰鳐与热带鱼群，体验声光生态互动装置。",
        "category": "exploration_exp",
        "environment": "indoor",
        "age_buckets": ["preschool", "elementary"],
        "time_slot": "morning",
        "display_time": "全天开放 · 09:30–17:00"
    },
    # --- Pacific Science Center (PacSci) ---
    {
        "venue_key": "pacific_science_center",
        "title": "Tropical Butterfly House Experience (热带蝴蝶温室沉浸漫步)",
        "summary": "恒温80°F的热带雨林生态温室，数百只自由飞翔的鲜艳蝴蝶，观察从蝶蛹到破茧展翅的全生命周期。",
        "category": "nature_animals",
        "environment": "indoor",
        "age_buckets": ["preschool", "elementary"],
        "time_slot": "morning",
        "display_time": "全天开放 · 10:00–17:00"
    },
    {
        "venue_key": "pacific_science_center",
        "title": "Tinker Tank Makerspace Workshop (创客空间：重力重构与动手工程)",
        "summary": "开放式物理动手创造空间，包含风洞测试台、重力滚球轨道设计和乐高工程结构搭设，适合学龄儿童锻炼批判性工程思维。",
        "category": "exploration_exp",
        "environment": "indoor",
        "age_buckets": ["elementary"],
        "time_slot": "afternoon",
        "display_time": "周末 · 11:00–16:00"
    },
    # --- MoPOP (Museum of Pop Culture) ---
    {
        "venue_key": "mopop",
        "title": "Sound Lab: Hands-on Music & Instruments (声音实验室：乐器动手演奏实战)",
        "summary": "MoPOP最具人气的少儿互动展区，隔音录音室内配备真实架子鼓、电吉他、合成器及调音台，零门槛亲子即兴合奏体验。",
        "category": "music_crafts",
        "environment": "indoor",
        "age_buckets": ["elementary"],
        "time_slot": "afternoon",
        "display_time": "全天开放 · 10:00–17:00"
    },
    {
        "venue_key": "mopop",
        "title": "Indie Game Lounge & Sci-Fi Worlds (独立游戏展与科幻奇幻宇宙)",
        "summary": "亲子共同体验数十款艺术与冒险独立游戏，穿越科幻与奇幻道具展厅，探索经典游戏与影视幕后创意设计。",
        "category": "exploration_exp",
        "environment": "indoor",
        "age_buckets": ["elementary"],
        "time_slot": "morning",
        "display_time": "全天开放 · 10:00–17:00"
    }
]

def _get_upcoming_weekend_dates():
    today = datetime.now()
    days_until_saturday = (5 - today.weekday()) % 7
    saturday = today + timedelta(days=days_until_saturday)
    sunday = saturday + timedelta(days=1)
    return saturday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")

def fetch_venue_events():
    """聚合西雅图顶级科技、自然与文化场馆周末排期"""
    sat_date, sun_date = _get_upcoming_weekend_dates()
    features = []

    print("[Venues] 正在同步 Zoo、Aquarium、PacSci 与 MoPOP 亲子日程...")

    for idx, item in enumerate(STAPLE_PROGRAMS):
        venue = VENUE_PROFILES[item["venue_key"]]
        event_date = sat_date if idx % 2 == 0 else sun_date

        features.append({
            "type": "Feature",
            "id": f"evt_{item['venue_key']}_{event_date.replace('-', '')}_{idx + 1}",
            "geometry": {
                "type": "Point",
                "coordinates": venue["coords"]
            },
            "properties": {
                "title": item["title"],
                "summary": item["summary"],
                "organizer": venue["venueName"].split(" (")[0],
                "category": item["category"],
                "location": {
                    "venueName": venue["venueName"],
                    "address": venue["address"],
                    "city": venue["city"],
                    "region": venue["region"],
                    "googleMapsUrl": f"https://maps.google.com/?q={venue['venueName'].replace(' ', '+')}"
                },
                "schedule": {
                    "startDate": event_date,
                    "endDate": event_date,
                    "timeSlot": item["time_slot"],
                    "displayTime": item["display_time"]
                },
                "familyAttributes": {
                    "ageBuckets": item["age_buckets"],
                    "environment": item["environment"],
                    "isFree": False,
                    "priceLabel": venue["admission"],
                    "requiresRsvp": True,
                    "strollerFriendly": True,
                    "hasChangingTable": True,
                    "parking": venue["parking"]
                },
                "source": {
                    "originalUrl": venue["url"],
                    "sourceName": venue["venueName"].split(" (")[0]
                }
            }
        })

    print(f"[Venues] 成功生成 {len(features)} 条经典场馆活动。")
    return features

if __name__ == "__main__":
    res = fetch_venue_events()
    print(f"单独测试场馆模块: 成功输出 {len(res)} 条")
