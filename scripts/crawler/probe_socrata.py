# scripts/crawler/probe_socrata.py
import json
import requests

def probe_seattle_catalog():
    print("=== 开始探测 data.seattle.gov 上的公开数据集 ===")
    
    # 检索 SPL / Library / Events 相关的所有数据集
    catalog_url = "https://api.us.socrata.com/api/catalog/v1"
    params = {
        "domains": "data.seattle.gov",
        "search_context": "data.seattle.gov",
        "q": "Seattle Public Library events calendar",
        "limit": 10
    }
    
    headers = {"User-Agent": "SeattleKidsWeekendApp/1.0"}
    
    try:
        res = requests.get(catalog_url, params=params, headers=headers, timeout=12)
        res.raise_for_status()
        data = res.json()
        
        results = data.get("results", [])
        print(f"共发现 {len(results)} 个候选数据集：\n")
        
        for idx, item in enumerate(results):
            resource = item.get("resource", {})
            dataset_id = resource.get("id")
            name = resource.get("name")
            description = resource.get("description", "无描述")[:100]
            updated_at = resource.get("updatedAt")
            columns_field_names = resource.get("columns_field_name", [])
            
            print(f"[{idx + 1}] ID: {dataset_id}")
            print(f"    名称: {name}")
            print(f"    更新时间: {updated_at}")
            print(f"    字段列表: {columns_field_names[:8]}")
            print(f"    描述摘要: {description}...")
            
            # 对前 3 个数据集尝试拉取 1 条真实样本数据
            if idx < 3 and dataset_id:
                sample_url = f"https://data.seattle.gov/resource/{dataset_id}.json?$limit=1"
                try:
                    s_res = requests.get(sample_url, headers=headers, timeout=5)
                    if s_res.status_code == 200 and s_res.json():
                        print(f"    数据样本键值: {list(s_res.json()[0].keys())}")
                    else:
                        print(f"    样本拉取结果: 状态码 {s_res.status_code} (数据为空或无权限)")
                except Exception as e:
                    print(f"    样本拉取异常: {e}")
            print("-" * 60)
            
    except Exception as e:
        print(f"探测失败: {e}")

if __name__ == "__main__":
    probe_seattle_catalog()