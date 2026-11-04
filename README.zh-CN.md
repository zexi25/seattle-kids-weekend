<p align="right">
  <a href="./README.md">English</a> | <strong>简体中文</strong>
</p>

# Seattle Kids Weekend (西雅图亲子活动指南)

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

## 🙏 致谢与灵感

- 产品形态与界面交互设计灵感来源于优秀的「湾区亲子活动」网站。
- 地图底图服务由 [OpenStreetMap](https://www.openstreetmap.org/) 提供。
- 活动数据均通过自动化流水线采集自大西雅图各公共图书馆及地标场馆公开信息。