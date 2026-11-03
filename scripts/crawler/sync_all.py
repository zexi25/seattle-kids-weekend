import json
import os
import sys
from datetime import datetime

# 保证能正确引用当前目录下的子模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetch_spl import fetch_spl_events
from fetch_kcls import fetch_kcls_events

# 核心场馆精选兜底数据（确保博物馆与科技馆常驻）
MUSEUM_STAPLES = [
    {
        "type": "Feature",
        "id": "evt_staple_kidsquest",
        "geometry": {
            "type": "Point",
            "coordinates": [-122.1963, 47.6205]
        },
        "properties": {
            "title": "STEAM Exploration & Water Play (儿童科技与水动力工坊)",
            "summary": "Bellevue 核心亲子馆，室内双层攀爬架与流体实验平台，学龄前与小学生的雨天首选。",
            "organizer": "KidsQuest Children's Museum",
            "category": "exploration_exp",
            "location": {
                "venueName": "KidsQuest Children's Museum",
                "address": "1116 108th Ave NE, Bellevue, WA 98004",
                "city": "Bellevue",
                "region": "eastside",
                "googleMapsUrl": "https://maps.google.com/?q=KidsQuest+Children's+Museum"
            },
            "schedule": {
                "startDate": datetime.now().strftime("%Y-%m-%d"),
                "endDate": datetime.now().strftime("%Y-%m-%d"),
                "timeSlot": "afternoon",
                "displayTime": "周末 · 13:00–16:30"
            },
            "familyAttributes": {
                "ageBuckets": ["preschool", "elementary"],
                "environment": "indoor",
                "isFree": False,
                "priceLabel": "门票 $15 / 会员免费",
                "requiresRsvp": False,
                "strollerFriendly": True,
                "hasChangingTable": True,
                "parking": "free_lot"
            },
            "source": {
                "originalUrl": "https://www.kidsquestmuseum.org",
                "sourceName": "KidsQuest 官网"
            }
        }
    },
    {
        "type": "Feature",
        "id": "evt_staple_burke",
        "geometry": {
            "type": "Point",
            "coordinates": [-122.3116, 47.6605]
        },
        "properties": {
            "title": "Fossil Prep & Dino Discovery (古生物化石研学工坊)",
            "summary": "近距离隔着透明玻璃观察古生物修复师修整恐龙骨骼，设有小学生动手动脑探索专区。",
            "organizer": "Burke Museum",
            "category": "nature_animals",
            "location": {
                "venueName": "Burke Museum",
                "address": "4300 15th Ave NE, Seattle, WA 98105",
                "city": "Seattle",
                "region": "seattle",
                "googleMapsUrl": "https://maps.google.com/?q=Burke+Museum"
            },
            "schedule": {
                "startDate": datetime.now().strftime("%Y-%m-%d"),
                "endDate": datetime.now().strftime("%Y-%m-%d"),
                "timeSlot": "morning",
                "displayTime": "周末 · 10:00–12:30"
            },
            "familyAttributes": {
                "ageBuckets": ["elementary"],
                "environment": "indoor",
                "isFree": False,
                "priceLabel": "门票 $14–$22",
                "requiresRsvp": False,
                "strollerFriendly": True,
                "hasChangingTable": True,
                "parking": "paid_garage"
            },
            "source": {
                "originalUrl": "https://www.burkemuseum.org",
                "sourceName": "Burke Museum"
            }
        }
    }
]

def deduplicate_features(features):
    """根据活动标题和场馆名称进行简单去重"""
    seen_keys = set()
    unique_list = []
    for f in features:
        p = f.get("properties", {})
        key = f"{p.get('title')}_{p.get('location', {}).get('venueName')}"
        if key not in seen_keys:
            seen_keys.add(key)
            unique_list.append(f)
    return unique_list

def main():
    print("=== 开始执行大西雅图亲子活动多源同步 ===\n")
    all_features = []

    # 1. 抓取 SPL
    try:
        spl_events = fetch_spl_events()
        all_features.extend(spl_events)
    except Exception as e:
        print(f"⚠️ SPL 流程异常: {e}")

    # 2. 抓取 KCLS
    try:
        kcls_events = fetch_kcls_events()
        all_features.extend(kcls_events)
    except Exception as e:
        print(f"⚠️ KCLS 流程异常: {e}")

    # 3. 追加常驻精选场馆
    all_features.extend(MUSEUM_STAPLES)

    # 4. 去重
    unique_features = deduplicate_features(all_features)
    print(f"\n数据清洗：原始 {len(all_features)} 条，去重后保留 {len(unique_features)} 条。")

    # 5. 输出写入 public/data/events.geojson
    output_path = os.path.join(os.path.dirname(__file__), "../../public/data/events.geojson")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    result_geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "region": "Greater Seattle Area",
            "totalCount": len(unique_features)
        },
        "features": unique_features
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result_geojson, f, ensure_ascii=False, indent=2)

    print(f"🎉 成功同步并导出至: {output_path}")

if __name__ == "__main__":
    main()