import json
import os
import sys

# 导入各数据源采集模块
from fetch_spl import fetch_spl_events
from fetch_venues import fetch_venue_events
from fetch_kcls import fetch_kcls_events

OUTPUT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../public/data/events.geojson")
)

def deduplicate_events(features):
    """
    按 (venueName, title, startDate) 联合去重
    保证同一个场馆不同周末的排期都能完整保留
    """
    seen_keys = set()
    cleaned = []

    for feat in features:
        p = feat.get("properties", {})
        venue = p.get("location", {}).get("venueName", "").strip().lower()
        title = p.get("title", "").strip().lower()
        date = p.get("schedule", {}).get("startDate", "").strip()

        # 联合键：地点 + 标题 + 具体排期日期
        dedup_key = f"{venue}|{title}|{date}"

        if dedup_key not in seen_keys:
            seen_keys.add(dedup_key)
            cleaned.append(feat)

    return cleaned

def sync_all():
    print("=== 开始执行大西雅图亲子活动多源同步 ===\n")
    all_features = []

    # 1. 西雅图公共图书馆 (SPL)
    try:
        spl_events = fetch_spl_events()
        all_features.extend(spl_events)
        print(f"✅ [西雅图公共图书馆 (SPL)] 成功采集 {len(spl_events)} 条。\n")
    except Exception as e:
        print(f"❌ [SPL] 抓取失败: {e}\n")

    # 2. 地标场馆与市集 (KidsQuest, 飞行博物馆, 植物园, 动物园, 水族馆, 农夫市集等)
    try:
        venue_events = fetch_venue_events()
        all_features.extend(venue_events)
        print(f"✅ [地标场馆与特色市集] 成功采集 {len(venue_events)} 条。\n")
    except Exception as e:
        print(f"❌ [Venues] 抓取失败: {e}\n")

    # 3. 金县图书馆 (KCLS)
    try:
        kcls_events = fetch_kcls_events()
        all_features.extend(kcls_events)
        print(f"✅ [金县公共图书馆 (KCLS)] 成功采集 {len(kcls_events)} 条。\n")
    except Exception as e:
        print(f"❌ [KCLS] 抓取失败: {e}\n")

    # 严格去重与输出
    total_raw = len(all_features)
    final_features = deduplicate_events(all_features)

    # 按照开始日期升序排序
    final_features.sort(
        key=lambda x: (
            x.get("properties", {}).get("schedule", {}).get("startDate", "9999-99-99"),
            x.get("properties", {}).get("location", {}).get("city", "")
        )
    )

    geojson_data = {
        "type": "FeatureCollection",
        "metadata": {
            "generatedAt": json.dumps(os.environ.get("GITHUB_RUN_ID", "local")),
            "totalCount": len(final_features)
        },
        "features": final_features
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)

    print(f"数据清洗：原始 {total_raw} 条，保留未来 30 天各周末排期共 {len(final_features)} 条。")
    print(f"🎉 成功同步并导出至: {OUTPUT_PATH}")

if __name__ == "__main__":
    sync_all()
