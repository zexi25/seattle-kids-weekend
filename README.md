# Seattle Kids Weekend (西雅图亲子活动指南)

> 🌐 **在线访问 / Live Demo**: [https://seattle-kids-weekend.vercel.app](https://seattle-kids-weekend.vercel.app)

A modern, responsive weekend activity aggregator tailored for families across Greater Seattle (Seattle, Eastside, North, and South Sound). The platform automates data collection from regional library networks and premier cultural landmarks, presenting curated events through an intuitive floating-card interface and interactive geospatial mapping.

---

## ✨ Features

- **Multi-Source Automated Ingestion Pipeline**: Consolidates schedules from the Seattle Public Library (SPL), King County Library System (KCLS Bibliocommons Gateway API), and 10+ core regional cultural landmarks (The Museum of Flight, KidsQuest Children's Museum, Burke Museum, Pacific Science Center, Seattle Aquarium, and historic farmers markets).
- **Multi-Dimensional Instant Filtering**: Supports dynamic presets (`Next 30 Days`, `This Weekend`, `Next Weekend`, `Custom Range`) alongside composite filters for sub-regions, age groups (0–5 Preschool / 6–12 Elementary), time of day (Morning/Afternoon), free admission, and indoor/rain-safe spaces.
- **Refined Floating-Card Visual Design**: Built with a calm `#f8f9fa` backdrop and isolated white floating cards with subtle shadows, pairing `Inter` and `PingFang SC` typography with optimized kerning and font weights for clean reading comfort.
- **Interactive Dual-Pane Map Sync**: Features Leaflet-powered mapping with resizable split-pane widths. Clicking an activity card smoothly pans to its map coordinate, and marker clicks isolate corresponding event details.
- **Zero-Maintenance Serverless CI/CD**: 100% static page prerendering (SSG) with scheduled data scraping via GitHub Actions and instant edge deployment via Vercel.

---

## 🛠️ Tech Stack

- **Frontend**: Next.js 16 (App Router, Turbopack), React 19, TypeScript
- **Styling**: Tailwind CSS, Lucide React
- **Mapping**: Leaflet, React-Leaflet
- **Data Engineering**: Python 3.11+ (Requests, ZoneInfo)
- **Deployment & CI/CD**: Vercel, GitHub Actions

---

## 📂 Project Structure

```text
seattle-kids-weekend/
├── .github/workflows/      # Automated weekly scraper workflow
├── public/
│   └── data/
│       └── events.geojson  # Standardized event GeoJSON dataset
├── scripts/
│   └── crawler/            # Python extraction and cleaning pipeline
│       ├── fetch_spl.py    # Seattle Public Library extractor
│       ├── fetch_kcls.py   # King County Library System API extractor
│       ├── fetch_venues.py # Landmark venue and farmers market aggregator
│       └── sync_all.py     # Aggregation, deduplication, and GeoJSON export
├── src/
│   ├── app/
│   │   ├── globals.css     # Global styles and antialiasing rules
│   │   ├── layout.tsx      # Root layout, font optimization, and metadata
│   │   └── page.tsx        # Main view, split-pane resizer, filter state
│   ├── components/
│   │   ├── DataSourceFooter.tsx # Attribution and data disclaimer footer
│   │   ├── EventList.tsx        # Scrollable event cards and detail drill-down
│   │   ├── FilterBar.tsx        # Floating multi-criteria control bar
│   │   └── LeafletMap.tsx       # Dynamic geospatial visualization
│   └── types/
│       └── event.ts        # GeoJSON schema and domain type definitions
└── package.json
```

---

## 🚀 Quick Start

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/<your-username>/seattle-kids-weekend.git
cd seattle-kids-weekend
npm install
```

### 2. Run the Data Pipeline

Generate the latest `events.geojson` dataset locally:

```bash
# Setup Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install requests

# Execute multi-source crawler and deduplication pipeline
python scripts/crawler/sync_all.py
```

### 3. Launch Development Server

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build for Production

```bash
npm run build
npm run start
```

---

## 🔄 Automated Data Pipeline (CI/CD)

The project runs unattended through `.github/workflows/sync-events.yml`:
1. GitHub Actions triggers automatically on Thursdays and Saturdays (08:00 UTC / 00:00 PST).
2. The pipeline executes `scripts/crawler/sync_all.py` to pull, parse, and validate weekend schedules.
3. If new events are detected, the updated `public/data/events.geojson` is committed and pushed back to `main`.
4. The push triggers a fast, incremental static build on Vercel Edge Network, keeping live data up to date across the upcoming 30-day window.

---

## 📄 Disclaimer

All event schedules and details are gathered automatically from public domain sources and are intended solely for personal weekend trip planning. Please verify admission costs, registration requirements, and weather-related cancellations directly through official venue websites before traveling.



面向大西雅图地区（西雅图市区、东区、北区、南区）家庭的现代化周末亲子活动聚合平台。通过多源自动化采集管线持续跟踪公共图书馆与核心文化地标排期，配合轻量级悬浮卡片美学与交互地图可视化，帮助本地家长快速筛选并规划周末家庭出行。

---

## ✨ 核心特性

- **多源自动化数据流**：聚合西雅图公共图书馆 (SPL)、金县公共图书馆 (KCLS Gateway API) 以及 10+ 本地核心场馆（飞行博物馆、KidsQuest 儿童博物馆、伯克自然博物馆、太平洋科学中心、西雅图水族馆、各大农夫市集等）。
- **多维度即时复合筛选**：支持「未来 30 天 / 本周末 / 下周末 / 自选日期」时间预设，结合地区分区、适龄段（0–5 岁学龄前 / 6–12 岁小学）、上午/下午时段、免费入场及室内避雨等多维度实时联动。
- **现代悬浮卡片美学**：采用 `#f8f9fa` 浅灰底色搭配独立圆角浮动卡片（Floating Cards），结合 Inter / PingFang SC 字体栈与定制字重排版，带来清爽现代的阅读质感。
- **交互式地图联动**：集成 Leaflet 地图，支持工作台双栏宽度自由拖拽（Split-pane Resizing），点击活动卡片与地图标记点（Marker）实现平滑双向联动聚焦。
- **免运维 Serverless 架构**：全站静态预渲染（Static Prerender），结合 GitHub Actions 定时调度与 Vercel 静态托管，实现零服务器成本的自动持续交付。

---

## 🛠️ 技术栈

- **前端框架**：Next.js 16 (App Router, Turbopack)
- **UI & 样式**：React 19, Tailwind CSS, Lucide React
- **地图渲染**：Leaflet, React-Leaflet
- **数据采集与清洗**：Python 3.11+ (Requests, ZoneInfo)
- **CI/CD 与托管**：GitHub Actions, Vercel

---

## 📂 项目结构

```text
seattle-kids-weekend/
├── .github/workflows/      # GitHub Actions 定时采集工作流
├── public/
│   └── data/
│       └── events.geojson  # 规范化活动 GeoJSON 数据集
├── scripts/
│   └── crawler/            # Python 数据抓取与清洗管线
│       ├── fetch_spl.py    # 西雅图公共图书馆采集
│       ├── fetch_kcls.py   # 金县图书馆 API 采集
│       ├── fetch_venues.py # 核心地标场馆与市集排期
│       └── sync_all.py     # 多源聚合、去重与 GeoJSON 导出
├── src/
│   ├── app/
│   │   ├── globals.css     # 全局样式与字体平滑规则
│   │   ├── layout.tsx      # 根布局与元数据配置
│   │   └── page.tsx        # 主界面与复合筛选状态调度
│   ├── components/
│   │   ├── DataSourceFooter.tsx # 数据源版权说明
│   │   ├── EventList.tsx        # 滚动活动卡片流与详情视图
│   │   ├── FilterBar.tsx        # 悬浮复合筛选控制栏
│   │   └── LeafletMap.tsx       # 交互式地图组件
│   └── types/
│       └── event.ts        # GeoJSON 与活动业务类型定义
└── package.json
```

---

## 🚀 本地开发指南

### 1. 克隆项目与安装前端依赖

```bash
git clone https://github.com/<your-username>/seattle-kids-weekend.git
cd seattle-kids-weekend
npm install
```

### 2. 运行数据采集脚本（生成最新数据）

```bash
# 创建并激活 Python 虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装数据抓取依赖
pip install requests

# 执行全量多源同步
python scripts/crawler/sync_all.py
```

### 3. 启动本地开发服务

```bash
npm run dev
```

在浏览器打开 [http://localhost:3000](http://localhost:3000) 即可预览。

### 4. 生产构建打包测试

```bash
npm run build
npm run start
```

---

## 🔄 自动化更新机制 (CI/CD)

项目通过 `.github/workflows/sync-events.yml` 维持自动化运作：
1. 每周四与周六定时启动 GitHub Actions 运行环境。
2. 自动运行 `scripts/crawler/sync_all.py` 执行多源数据聚合与清洗。
3. 若检测到数据变动，自动将最新的 `public/data/events.geojson` 提交并推送到仓库主分支。
4. 仓库更新自动触发 Vercel 进行增量静态生成（SSG），保持线上数据始终为最新 30 天状态。

---

## 📄 免责声明

本网站活动信息由公开数据管道自动汇总，仅供大西雅图本地家庭周末出行参考。具体活动安排、实时门票价格、预约要求以及暴雨恶劣天气变更请以各场馆/图书馆官方最新公告为准。