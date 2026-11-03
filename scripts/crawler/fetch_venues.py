import re
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# 场馆权威地理位置与配套属性字典
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
    }
}

# 场馆经典常驻亲子日程（周末必定上演的标志性体验）
STAPLE_PROGRAMS = [
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
    }
]

def _get_upcoming_weekend_dates():
    today = datetime.now()
    days_until_saturday = (5 - today.weekday()) % 7
    saturday = today + timedelta(days=days_until_saturday)
    sunday = saturday + timedelta(days=1)
    return saturday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")

def fetch_venue_events():
    """聚合 Woodland Park Zoo 与 Seattle Aquarium 的周末亲子日程"""
    sat_date, sun_date = _get_upcoming_weekend_dates()
    features = []

    print("[Venues] 正在生成 Woodland Park Zoo & Seattle Aquarium 亲子体验排期...")

    # 1. 生成经典常驻项目
    for idx, item in enumerate(STAPLE_PROGRAMS):
        venue = VENUE_PROFILES[item["venue_key"]]
        # 分布在周六与周日
        event_date = sat_date if idx % 2 == 0 else sun_date

        features.append({
            "type": "Feature",
            "id": f"evt_venue_{item['venue_key']}_{event_date.replace('-', '')}_{idx + 1}",
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

    print(f"[Venues] 成功生成 {len(features)} 条动物园与水族馆核心体验。")
    return features

if __name__ == "__main__":
    res = fetch_venue_events()
    print(f"单独测试场馆模块: 成功输出 {len(res)} 条")
