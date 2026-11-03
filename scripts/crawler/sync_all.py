import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# 导入各数据源提取模块
sys.path.append(os.path.dirname(__file__))
from fetch_kcls import fetch_kcls_events
from fetch_spl import fetch_spl_events
from fetch_venues import fetch_venue_events

OUTPUT_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../public/data/events.geojson")
)

def sync_all():
    print("=== 开始执行大西雅图亲子活动多源同步 ===\n")
    all_features = []

    tasks = {
        "金县公共图书馆 (KCLS)": fetch_kcls_events,
        "西雅图公共图书馆 (SPL)": fetch_spl_events,
        "自然科教场馆 (Zoo & Aquarium)": fetch_venue_events
    }

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_source = {executor.submit(func): name for name, func in tasks.items()}
        for future in as_completed(future_to_source):
            source_name = future_to_source[future]
            try:
                data = future.result()
                print(f"✅ [{source_name}] 执行完毕，成功获取 {len(data)} 条。")
                all_features.extend(data)
            except Exception as e:
                print(f"❌ [{source_name}] 执行失败: {e}")

    # 去重与清洗（根据标题与地点的指纹组合去重）
    unique_features = []
    seen_fingerprints = set()

    for feat in all_features:
        props = feat.get("properties", {})
        title = props.get("title", "").strip().lower()
        venue = props.get("location", {}).get("venueName", "").strip().lower()
        fingerprint = f"{title}_{venue}"
        
        if fingerprint not in seen_fingerprints and title:
            seen_fingerprints.add(fingerprint)
            unique_features.append(feat)

    geojson_output = {
        "type": "FeatureCollection",
        "metadata": {
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "totalCount": len(unique_features),
            "sources": ["KCLS", "SPL", "Woodland Park Zoo", "Seattle Aquarium"]
        },
        "features": unique_features
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(geojson_output, f, ensure_ascii=False, indent=2)

    print(f"\n数据清洗：原始 {len(all_features)} 条，去重后保留 {len(unique_features)} 条。")
    print(f"🎉 成功同步并导出至: {OUTPUT_FILE}")

if __name__ == "__main__":
    sync_all()
