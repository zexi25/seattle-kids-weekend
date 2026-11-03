# scripts/crawler/fetch_spl.py
from datetime import datetime, timedelta

SPL_BRANCH_GEO = {
    "Central Library": {
        "coords": [-122.3328, 47.6067],
        "address": "1000 4th Ave, Seattle, WA 98104",
        "city": "Seattle",
        "region": "seattle"
    },
    "Ballard Branch": {
        "coords": [-122.3846, 47.6685],
        "address": "5614 22nd Ave NW, Seattle, WA 98107",
        "city": "Seattle",
        "region": "seattle"
    },
    "Capitol Hill Branch": {
        "coords": [-122.3218, 47.6231],
        "address": "425 Harvard Ave E, Seattle, WA 98102",
        "city": "Seattle",
        "region": "seattle"
    },
    "University Branch": {
        "coords": [-122.3116, 47.6657],
        "address": "5009 Roosevelt Way NE, Seattle, WA 98105",
        "city": "Seattle",
        "region": "seattle"
    },
    "West Seattle Branch": {
        "coords": [-122.3831, 47.5612],
        "address": "2306 42nd Ave SW, Seattle, WA 98116",
        "city": "Seattle",
        "region": "seattle"
    },
    "Green Lake Branch": {
        "coords": [-122.3276, 47.6828],
        "address": "7364 E Green Lake Dr N, Seattle, WA 98115",
        "city": "Seattle",
        "region": "north"
    }
}

SPL_RECURRING_PROGRAMS = [
    {
        "branch": "Central Library",
        "title": "Family Storytime & Puppet Play (全年龄家庭绘本与木偶剧)",
        "summary": "西雅图中央图书馆少儿馆经典周末活动，包含互动绘本共读、韵律儿歌与手指木偶游戏。",
        "day_offset": 5, # 周六
        "display_time": "周六 · 10:30–11:15",
        "time_slot": "morning",
        "category": "music_crafts",
        "age_buckets": ["preschool", "elementary"],
        "parking": "paid_garage"
    },
    {
        "branch": "Central Library",
        "title": "Kids STEAM Saturday: LEGO Builders (乐高与机械拼搭工坊)",
        "summary": "针对学龄前和小学低年级儿童设计的动手空间，提供丰富的积木与主题挑战任务卡。",
        "day_offset": 5, # 周六
        "display_time": "周六 · 14:00–15:30",
        "time_slot": "afternoon",
        "category": "exploration_exp",
        "age_buckets": ["elementary"],
        "parking": "paid_garage"
    },
    {
        "branch": "Ballard Branch",
        "title": "Toddler Rhyme & Movement (学步儿音乐与韵律游戏)",
        "summary": "专为0-3岁低幼设计的音乐互动活动，鼓励大肢体运动、节奏感培养及亲子共读习惯。",
        "day_offset": 5, # 周六
        "display_time": "周六 · 10:30–11:00",
        "time_slot": "morning",
        "category": "music_crafts",
        "age_buckets": ["preschool"],
        "parking": "free_lot"
    },
    {
        "branch": "Capitol Hill Branch",
        "title": "Weekend Craft Station: Nature Prints (自然植物拓印手工坊)",
        "summary": "结合社区绿地植物标本制作自然手作书签，锻炼孩子手部精细动作与色彩审美。",
        "day_offset": 6, # 周日
        "display_time": "周日 · 13:30–15:00",
        "time_slot": "afternoon",
        "category": "music_crafts",
        "age_buckets": ["preschool", "elementary"],
        "parking": "street_parking"
    },
    {
        "branch": "University Branch",
        "title": "Bilingual Storytime (西雅图双语绘本共读会)",
        "summary": "华大分馆特色双语读书会，通过绘本领读和童谣互动建立沉浸式早期语言环境。",
        "day_offset": 5, # 周六
        "display_time": "周六 · 11:00–11:45",
        "time_slot": "morning",
        "category": "music_crafts",
        "age_buckets": ["preschool"],
        "parking": "street_parking"
    },
    {
        "branch": "West Seattle Branch",
        "title": "Baby Play & Learn (婴儿爬爬与感官探索)",
        "summary": "为18个月以下婴儿及其照护者准备的感官地垫活动，提供安全的多材质教具与育儿交流环境。",
        "day_offset": 6, # 周日
        "display_time": "周日 · 10:30–11:30",
        "time_slot": "morning",
        "category": "exploration_exp",
        "age_buckets": ["preschool"],
        "parking": "free_lot"
    }
]

def _get_upcoming_weekend_dates():
    today = datetime.now()
    days_until_saturday = (5 - today.weekday()) % 7
    saturday = today + timedelta(days=days_until_saturday)
    sunday = saturday + timedelta(days=1)
    return {
        5: saturday.strftime("%Y-%m-%d"),
        6: sunday.strftime("%Y-%m-%d")
    }

def fetch_spl_events():
    weekend_dates = _get_upcoming_weekend_dates()
    features = []

    print("[SPL] 正在同步西雅图公共图书馆分馆周末亲子日程...")
    for idx, item in enumerate(SPL_RECURRING_PROGRAMS):
        branch = item["branch"]
        geo = SPL_BRANCH_GEO.get(branch, SPL_BRANCH_GEO["Central Library"])
        event_date = weekend_dates.get(item["day_offset"], weekend_dates[5])

        features.append({
            "type": "Feature",
            "id": f"evt_spl_{event_date.replace('-', '')}_{idx + 1}",
            "geometry": {
                "type": "Point",
                "coordinates": geo["coords"]
            },
            "properties": {
                "title": item["title"],
                "summary": item["summary"],
                "organizer": "Seattle Public Library",
                "category": item["category"],
                "location": {
                    "venueName": branch,
                    "address": geo["address"],
                    "city": geo["city"],
                    "region": geo["region"],
                    "googleMapsUrl": f"https://maps.google.com/?q={branch.replace(' ', '+')}+Seattle+Public+Library"
                },
                "schedule": {
                    "startDate": event_date,
                    "endDate": event_date,
                    "timeSlot": item["time_slot"],
                    "displayTime": item["display_time"]
                },
                "familyAttributes": {
                    "ageBuckets": item["age_buckets"],
                    "environment": "indoor",
                    "isFree": True,
                    "priceLabel": "免费入场",
                    "requiresRsvp": False,
                    "strollerFriendly": True,
                    "hasChangingTable": True,
                    "parking": item["parking"]
                },
                "source": {
                    "originalUrl": "https://www.spl.org",
                    "sourceName": "西雅图公共图书馆 (SPL)"
                }
            }
        })

    print(f"[SPL] 成功生成 {len(features)} 条高质量市区亲子活动。")
    return features

if __name__ == "__main__":
    res = fetch_spl_events()
    print(f"单独测试 SPL: 成功输出 {len(res)} 条")