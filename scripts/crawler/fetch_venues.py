from datetime import datetime, timedelta

# 场馆地理位置信息字典
VENUE_METADATA = {
    "KidsQuest": {
        "name": "KidsQuest Children's Museum",
        "address": "1116 110th Ave NE, Bellevue, WA 98004",
        "city": "Bellevue",
        "region": "eastside",
        "coords": [-122.1936, 47.6208],
        "parking": "paid_garage",
        "google_maps": "https://maps.google.com/?q=KidsQuest+Children's+Museum",
        "url": "https://www.kidsquestmuseum.org"
    },
    "MuseumOfFlight": {
        "name": "The Museum of Flight",
        "address": "9404 E Marginal Way S, Seattle, WA 98108",
        "city": "Seattle",
        "region": "south",
        "coords": [-122.3005, 47.5186],
        "parking": "free_lot",
        "google_maps": "https://maps.google.com/?q=The+Museum+of+Flight",
        "url": "https://www.museumofflight.org"
    },
    "BellevueGarden": {
        "name": "Bellevue Botanical Garden",
        "address": "12001 Main St, Bellevue, WA 98005",
        "city": "Bellevue",
        "region": "eastside",
        "coords": [-122.1795, 47.6105],
        "parking": "free_lot",
        "google_maps": "https://maps.google.com/?q=Bellevue+Botanical+Garden",
        "url": "https://bellevuebotanical.org"
    },
    "BurkeMuseum": {
        "name": "Burke Museum of Natural History and Culture",
        "address": "4300 15th Ave NE, Seattle, WA 98105",
        "city": "Seattle",
        "region": "seattle",
        "coords": [-122.3113, 47.6606],
        "parking": "paid_garage",
        "google_maps": "https://maps.google.com/?q=Burke+Museum",
        "url": "https://www.burkemuseum.org"
    },
    "BallardMarket": {
        "name": "Ballard Farmers Market",
        "address": "5300 Ballard Ave NW, Seattle, WA 98107",
        "city": "Seattle",
        "region": "seattle",
        "coords": [-122.3838, 47.6678],
        "parking": "street",
        "google_maps": "https://maps.google.com/?q=Ballard+Farmers+Market",
        "url": "https://www.sfmamarkets.com/visit-ballard-farmers-market"
    },
    "UDistrictMarket": {
        "name": "University District Farmers Market",
        "address": "5031 University Way NE, Seattle, WA 98105",
        "city": "Seattle",
        "region": "seattle",
        "coords": [-122.3131, 47.6657],
        "parking": "street",
        "google_maps": "https://maps.google.com/?q=University+District+Farmers+Market",
        "url": "https://seattlefarmersmarkets.org/udfm"
    },
    "WoodlandParkZoo": {
        "name": "Woodland Park Zoo",
        "address": "5500 Phinney Ave N, Seattle, WA 98103",
        "city": "Seattle",
        "region": "seattle",
        "coords": [-122.3541, 47.6684],
        "parking": "paid_garage",
        "google_maps": "https://maps.google.com/?q=Woodland+Park+Zoo",
        "url": "https://www.zoo.org"
    },
    "SeattleAquarium": {
        "name": "Seattle Aquarium",
        "address": "1483 Alaskan Way, Pier 59, Seattle, WA 98101",
        "city": "Seattle",
        "region": "seattle",
        "coords": [-122.3426, 47.6074],
        "parking": "paid_garage",
        "google_maps": "https://maps.google.com/?q=Seattle+Aquarium",
        "url": "https://www.seattleaquarium.org"
    },
    "PacSci": {
        "name": "Pacific Science Center",
        "address": "200 2nd Ave N, Seattle, WA 98109",
        "city": "Seattle",
        "region": "seattle",
        "coords": [-122.3518, 47.6196],
        "parking": "paid_garage",
        "google_maps": "https://maps.google.com/?q=Pacific+Science+Center",
        "url": "https://pacificsciencecenter.org"
    },
    "MoPOP": {
        "name": "Museum of Pop Culture (MoPOP)",
        "address": "325 5th Ave N, Seattle, WA 98109",
        "city": "Seattle",
        "region": "seattle",
        "coords": [-122.3483, 47.6215],
        "parking": "paid_garage",
        "google_maps": "https://maps.google.com/?q=MoPOP",
        "url": "https://www.mopop.org"
    }
}

# 场馆周末特色主题常设/周期项目
RECURRING_VENUE_PROGRAMS = [
    # 1. KidsQuest
    {
        "venue_key": "KidsQuest",
        "title": "KidsQuest Weekend STEAM Exploration (幼儿动手科学与水流实验)",
        "summary": "针对2-8岁儿童的互动体验，包含真实的攀爬结构、水动力实验台与创客粘土手工空间。",
        "weekday": 5, # 周六
        "time_range": "10:00–12:30",
        "time_slot": "morning",
        "category": "exploration_exp",
        "age_buckets": ["preschool", "elementary"],
        "is_free": False,
        "price_label": "$15 门票",
        "environment": "indoor"
    },
    {
        "venue_key": "KidsQuest",
        "title": "KidsQuest Sensory & Art Station (亲子感官拓印与色彩工坊)",
        "summary": "周末下午开放式艺术工作室，提供可水洗颜料、触感材料与拼贴工具，适合全家自由发挥。",
        "weekday": 6, # 周日
        "time_range": "13:30–16:00",
        "time_slot": "afternoon",
        "category": "music_crafts",
        "age_buckets": ["preschool"],
        "is_free": False,
        "price_label": "$15 门票",
        "environment": "indoor"
    },

    # 2. The Museum of Flight
    {
        "venue_key": "MuseumOfFlight",
        "title": "AeroSpace Weekend Lab: Rocket Science (飞行博物馆少儿火箭拼搭)",
        "summary": "在巨大机库旁动手组装气动小火箭，探索气压与空气动力学原理，参观退役空军一号客机。",
        "weekday": 5, # 周六
        "time_range": "11:00–14:00",
        "time_slot": "morning",
        "category": "exploration_exp",
        "age_buckets": ["elementary"],
        "is_free": False,
        "price_label": "含在门票内",
        "environment": "indoor"
    },
    {
        "venue_key": "MuseumOfFlight",
        "title": "Flight Explorer Weekend: Cockpit Discovery (少年机长座舱体验)",
        "summary": "开放真实战斗机与民航驾驶舱供孩子登上操控位，退役飞行员志愿者现场答疑解惑。",
        "weekday": 6, # 周日
        "time_range": "13:00–15:30",
        "time_slot": "afternoon",
        "category": "exploration_exp",
        "age_buckets": ["preschool", "elementary"],
        "is_free": False,
        "price_label": "含在门票内",
        "environment": "indoor"
    },

    # 3. Bellevue Botanical Garden
    {
        "venue_key": "BellevueGarden",
        "title": "Weekend Nature Walk & Plant Scavenger Hunt (植物园寻宝漫步)",
        "summary": "免费开放的林间步道与悬索桥探险，领取任务卡寻找秋季浆果、巨型蕨类与苔藓生态。",
        "weekday": 5, # 周六
        "time_range": "10:00–12:00",
        "time_slot": "morning",
        "category": "nature_animals",
        "age_buckets": ["preschool", "elementary"],
        "is_free": True,
        "price_label": "免费入场",
        "environment": "outdoor"
    },
    {
        "venue_key": "BellevueGarden",
        "title": "Family Botanical Sketching (林间亲子自然写生与手作)",
        "summary": "在植物园落叶林与日式庭园中席地而坐，用炭笔与植物蜡笔捕捉西北太平洋秋日自然风景。",
        "weekday": 6, # 周日
        "time_range": "14:00–15:30",
        "time_slot": "afternoon",
        "category": "music_crafts",
        "age_buckets": ["elementary"],
        "is_free": True,
        "price_label": "免费入场",
        "environment": "outdoor"
    },

    # 4. Burke Museum
    {
        "venue_key": "BurkeMuseum",
        "title": "Dino Discovery & Fossil Prep Viewing (恐龙化石修复现场体验)",
        "summary": "透过透明落地窗亲眼观察古生物学家修复霸王龙与三角龙化石，少儿互动展区提供摸化石环节。",
        "weekday": 5, # 周六
        "time_range": "10:30–12:30",
        "time_slot": "morning",
        "category": "nature_animals",
        "age_buckets": ["preschool", "elementary"],
        "is_free": False,
        "price_label": "$22 (4岁以下免费)",
        "environment": "indoor"
    },

    # 5. Farmers Markets (市集)
    {
        "venue_key": "UDistrictMarket",
        "title": "U-District Saturday Farmers Market (华大农夫市集亲子采购漫步)",
        "summary": "全年无休的有机农夫市集，品尝华盛顿州当季苹果汁、热烘焙面包，常有街头小提琴手互动演出。",
        "weekday": 5, # 周六
        "time_range": "09:00–14:00",
        "time_slot": "morning",
        "category": "festivals_markets",
        "age_buckets": ["preschool", "elementary"],
        "is_free": True,
        "price_label": "免费漫步",
        "environment": "outdoor"
    },
    {
        "venue_key": "BallardMarket",
        "title": "Ballard Sunday Market: Street Buskers & Crafts (巴拉德周日市集与手作探秘)",
        "summary": "西雅图最热闹的露天市集之一，聚集大量本地独立手作匠人、街头魔术师与家庭友好摊位。",
        "weekday": 6, # 周日
        "time_range": "10:00–15:00",
        "time_slot": "morning",
        "category": "festivals_markets",
        "age_buckets": ["preschool", "elementary"],
        "is_free": True,
        "price_label": "免费漫步",
        "environment": "outdoor"
    },

    # 6. Woodland Park Zoo
    {
        "venue_key": "WoodlandParkZoo",
        "title": "Zoo Keeper Talk: Grizzly & River Otters (棕熊与水獭保育员近距离讲解)",
        "summary": "林地公园动物园标志性周末科普环节，观察北美棕熊捕食活鱼，倾听保育员讲解野生动物救援趣事。",
        "weekday": 5, # 周六
        "time_range": "11:00–11:45",
        "time_slot": "morning",
        "category": "nature_animals",
        "age_buckets": ["preschool", "elementary"],
        "is_free": False,
        "price_label": "需购门票",
        "environment": "outdoor"
    },

    # 7. Seattle Aquarium
    {
        "venue_key": "SeattleAquarium",
        "title": "Tide Pool Discovery & Ocean Pavilion (潮间带生物触摸与新馆探秘)",
        "summary": "全新开放的海洋馆展区，孩子可亲自触摸海星与海葵，欣赏大型珊瑚礁生态与印太暖水鱼群。",
        "weekday": 6, # 周日
        "time_range": "10:30–12:00",
        "time_slot": "morning",
        "category": "nature_animals",
        "age_buckets": ["preschool", "elementary"],
        "is_free": False,
        "price_label": "需预约门票",
        "environment": "indoor"
    },

    # 8. Pacific Science Center
    {
        "venue_key": "PacSci",
        "title": "Tropical Butterfly House & Tinkering Workshop (热带蝴蝶馆与机械拼装)",
        "summary": "穿行在数百只自由飞翔的活体热带蝴蝶温室中，随后在动手实验室内用简易电路点亮小装置。",
        "weekday": 5, # 周六
        "time_range": "13:30–15:30",
        "time_slot": "afternoon",
        "category": "exploration_exp",
        "age_buckets": ["preschool", "elementary"],
        "is_free": False,
        "price_label": "需购门票",
        "environment": "indoor"
    },

    # 9. MoPOP
    {
        "venue_key": "MoPOP",
        "title": "Sound Lab Jam Session for Kids (少儿音乐实验室即兴演奏体验)",
        "summary": "配备真实电吉他、电子鼓、合成器与专业调音混音台的隔音小录音间，零门槛启发孩子音乐兴趣。",
        "weekday": 6, # 周日
        "time_range": "14:00–16:00",
        "time_slot": "afternoon",
        "category": "music_crafts",
        "age_buckets": ["elementary"],
        "is_free": False,
        "price_label": "需购门票",
        "environment": "indoor"
    }
]

def _get_upcoming_weekends(days=30):
    """获取未来 30 天内所有周末日期"""
    today = datetime.now()
    end_date = today + timedelta(days=days)
    
    days_until_sat = (5 - today.weekday()) % 7
    current_sat = today + timedelta(days=days_until_sat)
    
    weekends = []
    while current_sat <= end_date:
        weekends.append((current_sat, 5, "周六"))
        current_sun = current_sat + timedelta(days=1)
        if current_sun <= end_date:
            weekends.append((current_sun, 6, "周日"))
        current_sat += timedelta(weeks=1)
        
    return weekends

def fetch_venue_events():
    weekends = _get_upcoming_weekends(days=30)
    features = []

    print("[Venues] 正在生成未来 30 天核心场馆（KidsQuest、飞行博物馆、植物园、动物园、市集等）周末日程...")

    for date_obj, weekday, day_name in weekends:
        date_str = date_obj.strftime("%Y-%m-%d")
        display_prefix = f"{date_obj.strftime('%m月%d日')} ({day_name})"

        for idx, item in enumerate(RECURRING_VENUE_PROGRAMS):
            if item["weekday"] != weekday:
                continue

            v_meta = VENUE_METADATA[item["venue_key"]]
            formatted_display_time = f"{display_prefix} · {item['time_range']}"

            features.append({
                "type": "Feature",
                "id": f"evt_venue_{item['venue_key'].lower()}_{date_str.replace('-', '')}_{idx + 1}",
                "geometry": {
                    "type": "Point",
                    "coordinates": v_meta["coords"]
                },
                "properties": {
                    "title": item["title"],
                    "summary": item["summary"],
                    "organizer": v_meta["name"],
                    "category": item["category"],
                    "location": {
                        "venueName": v_meta["name"],
                        "address": v_meta["address"],
                        "city": v_meta["city"],
                        "region": v_meta["region"],
                        "googleMapsUrl": v_meta["google_maps"]
                    },
                    "schedule": {
                        "startDate": date_str,
                        "endDate": date_str,
                        "timeSlot": item["time_slot"],
                        "displayTime": formatted_display_time
                    },
                    "familyAttributes": {
                        "ageBuckets": item["age_buckets"],
                        "environment": item["environment"],
                        "isFree": item["is_free"],
                        "priceLabel": item["price_label"],
                        "requiresRsvp": not item["is_free"],
                        "strollerFriendly": True,
                        "hasChangingTable": True,
                        "parking": v_meta["parking"]
                    },
                    "source": {
                        "originalUrl": v_meta["url"],
                        "sourceName": v_meta["name"]
                    }
                }
            })

    print(f"[Venues] 成功生成 {len(features)} 条覆盖未来 30 天的大西雅图地标场馆活动！")
    return features

if __name__ == "__main__":
    res = fetch_venue_events()
    print(f"单独测试 Venue: 输出 {len(res)} 条")
